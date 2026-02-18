# 📝 To-Do App v2

A simple and clean **To-Do application built with Django**, designed to manage daily tasks efficiently.  
This is **version 2** of my To-Do project, improved with better structure and logic.

---

## 🚀 Features

- Add new tasks
- Update existing tasks
- Delete tasks
- Mark tasks as completed
- Clean and minimal UI
- Follows Django best practices

---

## 🛠 Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (for development)
- **Frontend:** HTML, CSS, Django Templates
- **Version Control:** Git & GitHub

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally:

### 1️⃣ Clone the repository

git clone https://github.com/Diwakar-796/To-Do-v2.git

cd To-Do-v2

### 2️⃣ Create virtual environment

python -m venv venv

##### Activate it:

Windows: venv\Scripts\activate

Linux / Mac: source venv/bin/activate

### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Apply migrations
python manage.py makemigrations
python manage.py migrate

### 5️⃣ Run the server
python manage.py runserver

Open browser: http://127.0.0.1:8000/