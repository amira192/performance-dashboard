# 📊 Performance Dashboard

A web-based **Performance Dashboard** built with **Django** to manage and visualize performance metrics for students, teachers, and tasks.  
It provides administrators and managers with real-time insights into academic and operational performance.

---

## 🚀 Features

- 👩‍🏫 **Role-based Access:** Separate dashboards for admins, teachers, and students.
- ✅ **Task Management:** Add, assign, and track tasks and submissions.
- 📈 **Analytics & Charts:** View visual summaries of student progress and task completion.
- 💬 **Feedback System:** Managers can provide feedback on student submissions.
- 🗓️ **Leave Requests:** Teachers can request and track leave approvals.
- 🔒 **Secure Authentication:** Login, registration, and permissions management.

---

## 🛠️ Tech Stack

- **Backend:** Django 5+
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (can be changed to PostgreSQL)
- **Charts:** Chart.js or Plotly
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

PerformanceDashboard/
│
├── accounts/ # User authentication & profiles
├── performance/ # Tasks, feedbacks, and analytics
├── dashboard/ # Unified dashboard views
├── notifications
├── static/ # CSS, JS, and images
├── manage.py
└── requirements.txt


---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/amira192/performance-dashboard.git
   cd performance-dashboard
2- Create a virtual environment

python -m venv venv
venv\Scripts\activate  # On Windows
3-Install dependencies
pip install -r requirements.txt
4--Run database migrations
python manage.py migrate
5-Create a superuser (admin)
python manage.py createsuperuser
6-Run the server
python manage.py runserver
7-Open in browser:
http://127.0.0.1:8000/

👩‍💻 Author

Amira Khattab
🔗 GitHub Profile

🪪 License

This project is licensed under the MIT License — feel free to use and modify it.

⭐ Support

If you find this project useful, please star ⭐ the repository to show your support!
