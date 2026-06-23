from app import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), default='Sangeetha M')
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300))
    image_links = db.Column(db.Text)
    pdf_link = db.Column(db.String(500))
    amazon_link = db.Column(db.String(500))
    table_of_contents = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    pages = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    featured = db.Column(db.Boolean, default=False)
    downloads_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='book', lazy=True, cascade='all, delete-orphan')
    download_logs = db.relationship('DownloadLog', backref='book', lazy=True, cascade='all, delete-orphan')

    def get_image_list(self):
        if self.image_links:
            return [u.strip() for u in self.image_links.split(',') if u.strip()]
        return []

    def get_first_image(self):
        imgs = self.get_image_list()
        return imgs[0] if imgs else None

    def __repr__(self):
        return f'<Book {self.title}>'
