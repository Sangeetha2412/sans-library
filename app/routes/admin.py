from flask import (Blueprint, render_template, redirect, url_for,
                   request, flash, abort, current_app)
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import check_password_hash
from app import db, login_manager
from app.models import (Book, Announcement, Subscriber,
                        ContactMessage, Review, DownloadLog, SiteSettings)
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


class AdminUser(UserMixin):
    def __init__(self, username, email):
        self.id = 'admin'
        self.username = username
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    if user_id == 'admin':
        return AdminUser(
            current_app.config['ADMIN_USERNAME'],
            current_app.config['ADMIN_EMAIL']
        )
    return None


# ── AUTH ─────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    secret = request.args.get('key', '')
    if secret != current_app.config['ADMIN_SECRET_KEY']:
        abort(404)
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        stored_hash = current_app.config['ADMIN_PASSWORD_HASH']
        admin_username = current_app.config['ADMIN_USERNAME']
        admin_email = current_app.config['ADMIN_EMAIL']

        print("DEBUG username entered:", repr(username))
        print("DEBUG configured username:", repr(admin_username))
        print("DEBUG username match:", username == admin_username)
        print("DEBUG password match:", check_password_hash(stored_hash, password))
        
        if username == admin_username and check_password_hash(stored_hash, password):
            user = AdminUser(admin_username, admin_email)
            login_user(user, remember=True)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))


# ── DASHBOARD ────────────────────────────────────────────────────

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_books': Book.query.count(),
        'total_downloads': db.session.query(db.func.sum(Book.downloads_count)).scalar() or 0,
        'total_subscribers': Subscriber.query.count(),
        'total_messages': ContactMessage.query.count(),
        'unread_messages': ContactMessage.query.filter_by(is_read=False).count(),
        'most_downloaded': Book.query.order_by(Book.downloads_count.desc()).first(),
        'most_viewed': Book.query.order_by(Book.views_count.desc()).first(),
        'recent_messages': ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all(),
        'recent_subscribers': Subscriber.query.order_by(Subscriber.subscribed_at.desc()).limit(5).all(),
    }
    return render_template('admin/dashboard.html', stats=stats)


# ── BOOKS ─────────────────────────────────────────────────────────

@admin_bp.route('/books')
@login_required
def books():
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('admin/books.html', books=books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        image_links = []
        for i in range(1, 6):
            link = request.form.get(f'image_link_{i}', '').strip()
            if link:
                image_links.append(link)
        release_date = None
        rds = request.form.get('release_date')
        if rds:
            try:
                release_date = datetime.strptime(rds, '%Y-%m-%d').date()
            except ValueError:
                pass
        new_featured = bool(request.form.get('featured'))
        if new_featured:
            Book.query.filter_by(featured=True).update({'featured': False})
        book = Book(
            title=request.form.get('title', '').strip(),
            author=request.form.get('author', 'Sangeetha M').strip(),
            genre=request.form.get('genre', '').strip(),
            description=request.form.get('description', '').strip(),
            short_description=request.form.get('short_description', '').strip(),
            image_links=','.join(image_links),
            pdf_link=request.form.get('pdf_link', '').strip(),
            amazon_link=request.form.get('amazon_link', '').strip(),
            table_of_contents=request.form.get('table_of_contents', '').strip(),
            pages=request.form.get('pages', type=int),
            release_date=release_date,
            featured=new_featured,
        )
        db.session.add(book)
        db.session.commit()
        flash(f'Book "{book.title}" added!', 'success')
        return redirect(url_for('admin.books'))
    return render_template('admin/add_book.html')


@admin_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        image_links = []
        for i in range(1, 6):
            link = request.form.get(f'image_link_{i}', '').strip()
            if link:
                image_links.append(link)
        rds = request.form.get('release_date')
        if rds:
            try:
                book.release_date = datetime.strptime(rds, '%Y-%m-%d').date()
            except ValueError:
                pass
        new_featured = bool(request.form.get('featured'))
        if new_featured and not book.featured:
            Book.query.filter_by(featured=True).update({'featured': False})
        book.title = request.form.get('title', '').strip()
        book.author = request.form.get('author', 'Sangeetha M').strip()
        book.genre = request.form.get('genre', '').strip()
        book.description = request.form.get('description', '').strip()
        book.short_description = request.form.get('short_description', '').strip()
        book.image_links = ','.join(image_links)
        book.pdf_link = request.form.get('pdf_link', '').strip()
        book.amazon_link = request.form.get('amazon_link', '').strip()
        book.table_of_contents = request.form.get('table_of_contents', '').strip()
        book.pages = request.form.get('pages', type=int)
        book.featured = new_featured
        db.session.commit()
        flash('Book updated!', 'success')
        return redirect(url_for('admin.books'))
    image_links = book.get_image_list()
    while len(image_links) < 5:
        image_links.append('')
    return render_template('admin/edit_book.html', book=book, image_links=image_links)


@admin_bp.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.', 'success')
    return redirect(url_for('admin.books'))


# ── ANNOUNCEMENTS ─────────────────────────────────────────────────

@admin_bp.route('/announcements')
@login_required
def announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=announcements)


@admin_bp.route('/announcements/add', methods=['GET', 'POST'])
@login_required
def add_announcement():
    if request.method == 'POST':
        ann = Announcement(
            title=request.form.get('title', '').strip(),
            description=request.form.get('description', '').strip(),
            banner_image=request.form.get('banner_image', '').strip(),
            category=request.form.get('category', 'General').strip(),
        )
        db.session.add(ann)
        db.session.commit()
        flash('Announcement created!', 'success')
        return redirect(url_for('admin.announcements'))
    return render_template('admin/add_announcement.html')


@admin_bp.route('/announcements/edit/<int:ann_id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(ann_id):
    ann = Announcement.query.get_or_404(ann_id)
    if request.method == 'POST':
        ann.title = request.form.get('title', '').strip()
        ann.description = request.form.get('description', '').strip()
        ann.banner_image = request.form.get('banner_image', '').strip()
        ann.category = request.form.get('category', 'General').strip()
        db.session.commit()
        flash('Announcement updated!', 'success')
        return redirect(url_for('admin.announcements'))
    return render_template('admin/edit_announcement.html', ann=ann)


@admin_bp.route('/announcements/delete/<int:ann_id>', methods=['POST'])
@login_required
def delete_announcement(ann_id):
    ann = Announcement.query.get_or_404(ann_id)
    db.session.delete(ann)
    db.session.commit()
    flash('Announcement deleted.', 'success')
    return redirect(url_for('admin.announcements'))


# ── MESSAGES ──────────────────────────────────────────────────────

@admin_bp.route('/messages')
@login_required
def messages():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    ContactMessage.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('admin/messages.html', messages=msgs)


@admin_bp.route('/messages/delete/<int:msg_id>', methods=['POST'])
@login_required
def delete_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.messages'))


# ── SUBSCRIBERS ───────────────────────────────────────────────────

@admin_bp.route('/subscribers')
@login_required
def subscribers():
    subs = Subscriber.query.order_by(Subscriber.subscribed_at.desc()).all()
    return render_template('admin/subscribers.html', subscribers=subs)


@admin_bp.route('/subscribers/delete/<int:sub_id>', methods=['POST'])
@login_required
def delete_subscriber(sub_id):
    sub = Subscriber.query.get_or_404(sub_id)
    db.session.delete(sub)
    db.session.commit()
    flash('Subscriber removed.', 'success')
    return redirect(url_for('admin.subscribers'))

# ── REVIEWS ───────────────────────────────────────────────────────

@admin_bp.route('/reviews')
@login_required
def reviews():
    all_reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin/reviews.html', reviews=all_reviews)


@admin_bp.route('/reviews/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    db.session.delete(review)
    db.session.commit()

    flash('Review deleted successfully.', 'success')
    return redirect(url_for('admin.reviews'))


# ── SETTINGS ──────────────────────────────────────────────────────

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        logo_url = request.form.get('logo_url', '').strip()
        SiteSettings.set('logo_url', logo_url)
        for key in ['stat_readers', 'stat_countries']:
            val = request.form.get(key, '').strip()
            if val:
                SiteSettings.set(key, val)
        flash('Settings updated!', 'success')
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html',
                           current_logo=SiteSettings.get('logo_url', ''),
                           stat_readers=SiteSettings.get('stat_readers', '10,000+'),
                           stat_countries=SiteSettings.get('stat_countries', '25+'))
