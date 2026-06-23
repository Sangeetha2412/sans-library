# SANS LIBRARY — Production-Ready Author Platform

**Where Stories Find Their Readers.**

A premium Flask-based digital library and author portfolio platform featuring luxury dark mode design, Cloudinary image management, Supabase PostgreSQL database, and Render deployment.

## ✨ Features

- 📚 **Book Management**: Add, edit, delete books with image slideshows
- 📱 **Responsive Design**: Mobile-first luxury dark theme
- 🖼️ **Cloudinary Integration**: No file uploads needed—paste image URLs
- 🔐 **Admin Dashboard**: Secure single-admin authentication
- 📧 **Newsletter**: Email subscriber management
- 💬 **Contact System**: Message collection with admin review
- 📊 **Analytics**: Download tracking, view counts
- ⭐ **Reviews & Ratings**: Reader feedback system
- 🔍 **Search & Filters**: Dynamic genre filtering
- 🎯 **Rate Limiting**: DDoS protection on public endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Supabase account (free)
- Cloudinary account (free)
- Render account (free)
- GitHub account

### Local Setup

```bash
# 1. Clone and enter directory
git clone <your-repo-url>
cd sans-library

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (copy from .env.example)
cp .env.example .env

# 5. Edit .env with your credentials
# - DATABASE_URL (from Supabase)
# - ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD_HASH
# - ADMIN_SECRET_KEY
# - Cloudinary credentials

# 6. Run locally
python run.py
```

Visit `http://localhost:5000` and admin at `http://localhost:5000/admin/login?key=YOUR_SECRET_KEY`

## 📦 Deployment to Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial Sans Library"
git remote add origin https://github.com/yourname/sans-library.git
git push -u origin main
```

### Step 2: Connect Render
1. Go to render.com → New → Web Service
2. Connect GitHub repo
3. Use default settings, click "Create Web Service"

### Step 3: Set Environment Variables
In Render dashboard → Environment:
```
FLASK_ENV=production
SECRET_KEY=<long-random-string>
DATABASE_URL=<supabase-connection-string>
ADMIN_USERNAME=admin
ADMIN_EMAIL=owner@sanslib.com
ADMIN_PASSWORD_HASH=<hashed-password>
ADMIN_SECRET_KEY=your-secret-key
CLOUDINARY_CLOUD_NAME=<your-cloud>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
```

### Step 4: Initialize Database
In Render Shell:
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

## 🗝️ Admin Access

Your secret URL (never share!):
```
https://your-app.onrender.com/admin/login?key=YOUR_ADMIN_SECRET_KEY
```

Change the key anytime in Render environment variables.

## 📚 Project Structure

```
sans-library/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── routes/          # Blueprints (public, admin)
│   ├── templates/       # Jinja2 templates
│   └── static/          # CSS, JS, images
├── config.py            # Configuration
├── run.py               # Entry point
├── requirements.txt     # Dependencies
├── Procfile             # Render deployment
└── .env                 # Environment variables
```

## 🎨 Branding

Colors used throughout:
- **Primary**: `#ff4fd8` (Pink)
- **Secondary**: `#d633ff` (Purple)
- **Background**: `#090014` (Dark)
- **Card Background**: `#120020` (Darker)

## 🔐 Security

- ✅ CSRF protection on all forms
- ✅ Password hashing with Werkzeug
- ✅ Rate limiting on public endpoints
- ✅ Admin credentials via environment variables
- ✅ Session-based authentication
- ✅ No public registration allowed

## 📖 How to Use

### Add a Book
1. Login to admin dashboard
2. Go to **Books** → **Add Book**
3. Upload cover images to Cloudinary first
4. Copy image URLs and paste into form
5. Add PDF link (Google Drive shareable link)
6. Save

### Change Logo
1. Upload logo to Cloudinary
2. In Admin → Settings → paste URL
3. Saves automatically site-wide

### Change Admin Password
1. Generate new hash: `python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('NewPassword'))"`
2. Update `ADMIN_PASSWORD_HASH` in Render environment
3. Redeploy (automatic)

## 📝 License

Created by Sangeetha M. All rights reserved.

## 🤝 Support

For issues or questions, contact: contact@sanslib.com

---

**Built with:** Flask · PostgreSQL · Cloudinary · Render · Bootstrap 5  
**Last Updated:** 2025
