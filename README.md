# 📰 Django News Application

A **Django-based news application** that allows users to **view, like, and manage news articles**. 
It supports **infinite scrolling**, **tag-based filtering**, **user authentication**, and **admin management** for CRUD operations.

---

## 🚀 Features
✅ **User Authentication** – Register, login, and logout users.  
✅ **Admin Management** – Admins can create, delete news.  
✅ **News Articles** – Users can view news articles with images, tags, and view counts.  
✅ **Likes System** – Authenticated users can like/unlike news in real-time.  
✅ **Infinite Scroll** – Fetches additional news dynamically when scrolling.  
✅ **Tag Filtering** – Clickable tags to filter news.  
✅ **News Statistics** – View the most popular articles by views and likes.  

---

## 🛠️ Setup Guide

### 1️⃣ Clone the Repository
```sh
git https://github.com/Leanstix/ZavodInterview.git
cd ZavodInterview
cd news_project
```

### 2️⃣ Create & Activate a Virtual Environment
#### On Windows (CMD)
```sh
python -m venv venv
venv\Scripts\activate
```
#### On Mac/Linux
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up the Database
Run migrations to create the necessary database tables.
```sh
python manage.py migrate
```

### 5️⃣ Create a Superuser (Admin)
```sh
python manage.py createsuperuser
```
Enter a **username, email, and password** when prompted.

### 6️⃣ Run the Development Server
```sh
python manage.py runserver
```
The application will be available at:  
🌐 **http://127.0.0.1:8000/**

---

## 📝 API Endpoints
### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register/` | `POST` | Register a new user |
| `/api/login/` | `POST` | Login user |
| `/api/logout/` | `POST` | Logout user |

### News
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/news/` | `GET` | Get latest news articles |
| `/api/news/<id>/` | `GET` | Get a single news article |
| `/api/news/<id>/like/` | `POST` | Like/Unlike a news article |
| `/api/news/<id>/delete/` | `DELETE` | Delete a news (Admin only) |

### Tags & Stats
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/news/tag/<id>/` | `GET` | View news by tag |
| `/news/stats/` | `GET` | View news stats (likes & views) |

---

## 🛠️ Admin Panel
To manage news and users, visit:  
🌐 **http://127.0.0.1:8000/admin/**  

Use the **superuser** credentials created earlier to log in.

---

## 📌 Notes
- **Media files (images) are stored in `media/news_images/`**  
- **Ensure `DEBUG=True` in `settings.py` during development**  
- **For production, configure a database and a proper web server (e.g., Gunicorn, Nginx)**  

---

## 🛠️ Troubleshooting
- **Database Issues?** Run migrations again:  
  ```sh
  python manage.py migrate --run-syncdb
  ```
- **Static files not loading?** Run:
  ```sh
  python manage.py collectstatic
  ```

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 💡 Contributors
🚀 Developed by Aleshinloye Olamilekan  
🔗 GitHub: [Aleshinloy Olamilekan](https://github.com/Leanstix)  
