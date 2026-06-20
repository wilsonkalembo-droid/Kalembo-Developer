# SokoConnect - Local Business Connection Platform

A professional web platform designed to connect local traders and businesses, enabling them to collaborate, network, and grow together.

---

## 🚀 Features

* Professional Homepage with modern UI
* User Authentication (Login & Register)
* Business Directory by category and location
* Contact Page with inquiry form
* About Page with mission and vision
* Responsive Design (Mobile + Desktop)
* Clean and modern interface

---

## 📂 Project Structure

```
SokoConnect/
├── business/
├── SokoConnect/
├── static/
├── templates/
├── manage.py
└── db.sqlite3
```

---

## 🛠️ Installation & Setup

### Requirements

* Python 3.x
* pip
* Virtual Environment

### Setup

```bash
# Activate environment
env\Scripts\activate

# Run migrations
python manage.py migrate

# Create admin
python manage.py createsuperuser

# Run server
python manage.py runserver
```

👉 Open:
http://127.0.0.1:8000/

---

## 🌐 Pages

* Home
* Login
* Register
* Contact
* About
* Admin Panel

---

## 🎨 Customization

Edit styles in:

```
static/css/style.css
```

Add images/logo in:

```
static/images/
```

---

## 🔐 Security Notes

For production:

* Set DEBUG = False
* Use secure SECRET_KEY
* Configure ALLOWED_HOSTS
* Enable HTTPS

---

## 📧 Contact

Email: [pmkalembo77@gmail.com](mailto:pmkalembo77@gmail.com)
Phone: 0613850281

---

## 🚀 Future Improvements

* Business Reviews ⭐
* Map Integration 📍
* Chat System 💬
* Payment Integration 💳

---

## 📌 Author

Developed by: SokoConnect Team

---

## 📄 License

This project is for educational and development purposes.

---
