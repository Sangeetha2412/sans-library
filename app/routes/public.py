from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db, limiter
from app.models import Book, Announcement, Subscriber, ContactMessage, Review, DownloadLog, SiteSettings

public_bp = Blueprint('public', __name__)
@public_bp.route("/health")
def health():
    return {"status": "ok", "message": "Sans Library is running"}, 200


def get_logo():
    return SiteSettings.get('logo_url', '')


@public_bp.route('/')
def index():
    featured_book = Book.query.filter_by(featured=True).first()
    latest_books = Book.query.order_by(Book.created_at.desc()).limit(6).all()
    total_books = Book.query.count()
    total_downloads = db.session.query(db.func.sum(Book.downloads_count)).scalar() or 0
    stat_readers = SiteSettings.get('stat_readers', '10,000+')
    stat_countries = SiteSettings.get('stat_countries', '25+')
    return render_template('index.html',
                           featured_book=featured_book,
                           latest_books=latest_books,
                           total_books=total_books,
                           total_downloads=total_downloads,
                           stat_readers=stat_readers,
                           stat_countries=stat_countries,
                           logo_url=get_logo())


@public_bp.route('/books')
def books():
    page = request.args.get('page', 1, type=int)
    genre = request.args.get('genre', '')
    search = request.args.get('q', '')

    query = Book.query
    if genre:
        query = query.filter_by(genre=genre)
    if search:
        query = query.filter(
            db.or_(
                Book.title.ilike(f'%{search}%'),
                Book.author.ilike(f'%{search}%'),
                Book.genre.ilike(f'%{search}%'),
                Book.description.ilike(f'%{search}%')
            )
        )

    books = query.order_by(Book.created_at.desc()).paginate(
        page=page, per_page=current_app.config['BOOKS_PER_PAGE'], error_out=False
    )
    genres = [g[0] for g in db.session.query(Book.genre).distinct().all()]
    return render_template('books.html', books=books, genres=genres,
                           current_genre=genre, search=search, logo_url=get_logo())


@public_bp.route('/books/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    book.views_count = (book.views_count or 0) + 1
    db.session.commit()
    related_books = Book.query.filter(
        Book.genre == book.genre, Book.id != book.id
    ).limit(4).all()
    reviews = Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc()).all()
    return render_template('book_detail.html', book=book,
                           related_books=related_books, reviews=reviews, logo_url=get_logo())


@public_bp.route('/books/<int:book_id>/download')
@limiter.limit("10 per hour")
def download_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.pdf_link:
        flash('No download available for this book.', 'warning')
        return redirect(url_for('public.book_detail', book_id=book_id))
    book.downloads_count = (book.downloads_count or 0) + 1
    log = DownloadLog(book_id=book_id, ip_address=request.remote_addr)
    db.session.add(log)
    db.session.commit()
    return redirect(book.pdf_link)


@public_bp.route('/announcements')
def announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('announcements.html', announcements=announcements, logo_url=get_logo())


@public_bp.route('/author')
def author():
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('author.html', books=books, logo_url=get_logo())


@public_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit("5 per hour", methods=["POST"])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        if not all([name, email, subject, message]):
            flash('All fields are required.', 'danger')
            return render_template('contact.html', logo_url=get_logo())
        msg = ContactMessage(name=name, email=email, subject=subject, message=message)
        db.session.add(msg)
        db.session.commit()
        flash('Message sent! We will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    return render_template('contact.html', logo_url=get_logo())


@public_bp.route('/subscribe', methods=['POST'])
@limiter.limit("3 per hour")
def subscribe():
    email = request.form.get('email', '').strip()
    if not email or '@' not in email:
        flash('Please enter a valid email address.', 'danger')
        return redirect(request.referrer or url_for('public.index'))
    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        flash('You are already subscribed!', 'info')
    else:
        subscriber = Subscriber(email=email)
        db.session.add(subscriber)
        db.session.commit()
        flash('Subscribed successfully! Thank you.', 'success')
    return redirect(request.referrer or url_for('public.index'))


@public_bp.route('/books/<int:book_id>/review', methods=['POST'])
@limiter.limit("2 per hour")
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    name = request.form.get('reviewer_name', '').strip()
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()
    if not name or not rating or not (1 <= rating <= 5):
        flash('Invalid review data.', 'danger')
        return redirect(url_for('public.book_detail', book_id=book_id))
    review = Review(book_id=book_id, reviewer_name=name, rating=rating, comment=comment)
    db.session.add(review)
    db.session.flush()
    avg = db.session.query(db.func.avg(Review.rating)).filter_by(book_id=book_id).scalar()
    book.rating = round(float(avg), 1) if avg else 0.0
    db.session.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('public.book_detail', book_id=book_id))
