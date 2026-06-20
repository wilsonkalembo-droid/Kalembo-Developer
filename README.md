# SokoConnect - Local Business Connection Platform

A professional web platform designed to connect local traders and businesses, enabling them to collaborate, network, and grow together.

## 🚀 Features

- **Professional Homepage** - Modern, responsive design with Hero section
- **User Authentication** - Login and Registration pages
- **Business Directory** - Directory of local businesses by category
- **Contact Management** - Contact us page with inquiry form
- **About Section** - Company information, mission, values, and team
- **Responsive Design** - Mobile-friendly layout for all devices
- **Modern UI/UX** - Clean, professional interface with smooth animations

## 📋 Project Structure

```
SokoConnect/
├── business/                    # Main Django app
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py                 # App URL configuration
│   ├── views.py                # App views
│   └── tests.py
├── SokoConnect/                # Project settings
│   ├── settings.py             # Django settings (updated)
│   ├── urls.py                 # Main URL configuration (updated)
│   ├── asgi.py
│   └── wsgi.py
├── static/                      # Static files
│   ├── css/
│   │   └── style.css           # Professional styling
│   ├── js/
│   │   └── script.js           # JavaScript functionality
│   └── images/                 # Image directory (for logos, etc.)
├── templates/                   # Django templates
│   ├── base.html               # Base template with navigation & footer
│   ├── home.html               # Homepage
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── contact.html            # Contact page
│   └── about.html              # About page
├── manage.py                    # Django management script
└── db.sqlite3                  # SQLite database
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Install Dependencies

```bash
# Activate your virtual environment
# On Windows:
env\Scripts\activate

# On macOS/Linux:
source env/bin/activate
```

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

### Step 3: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account for accessing Django admin panel.

### Step 4: Collect Static Files (Optional, mainly for production)

```bash
python manage.py collectstatic
```

## 🚀 Running the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

### Pages Available:
- Home: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login/`
- Register: `http://127.0.0.1:8000/register/`
- Contact: `http://127.0.0.1:8000/contact/`
- About: `http://127.0.0.1:8000/about/`
- Admin: `http://127.0.0.1:8000/admin/`

## 🎨 Customization

### Colors
All colors can be customized in `static/css/style.css` by modifying the CSS variables:

```css
:root {
    --primary-color: #2563eb;      /* Blue */
    --secondary-color: #10b981;    /* Green */
    --dark-color: #1f2937;         /* Dark gray */
    --light-color: #f3f4f6;        /* Light gray */
    --gray-color: #6b7280;         /* Medium gray */
}
```

### Adding Custom Logo
1. Add your logo image to `static/images/`
2. Update the logo in `templates/base.html` navigation section

### Adding Contact Information
Update the contact details in `templates/contact.html` and `templates/base.html` footer

## 📱 Responsive Design

The design is fully responsive and works on:
- Desktop (1200px and above)
- Tablet (768px - 1199px)
- Mobile (below 768px)

## 🔐 Security Considerations

For production deployment:
1. Change `DEBUG = False` in settings.py
2. Update `SECRET_KEY` with a secure random key
3. Set proper `ALLOWED_HOSTS`
4. Use environment variables for sensitive settings
5. Enable CSRF protection
6. Use HTTPS

## 📧 Contact Form Implementation

The contact form is currently a template. To enable email functionality:

```python
# In settings.py, add email configuration:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-email-provider'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🗄️ Database Models (To Be Implemented)

The following models should be created for full functionality:
- User Profile
- Business Listing
- Contact Inquiry
- Partnership Request
- Review & Rating

## 📚 Additional Notes

- All pages use Django template inheritance with `base.html`
- Responsive mobile menu included
- Smooth animations and transitions throughout
- Font Awesome icons for visual elements
- Professional color scheme and typography

## 🤝 Contributing

To add new features:
1. Create new templates in `templates/`
2. Add corresponding views in `business/views.py`
3. Update URLs in `business/urls.py`
4. Add any new static files to `static/` directory

## 📄 License

This project is part of the SokoConnect platform.

## 📞 Support

For issues or questions, use the Contact page or email us at info@sokokonnect.com

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Developed by:** SokoConnect Team
