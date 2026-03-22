# HRMS Lite – Human Resource Management System

## 📌 Project Overview

HRMS Lite is a lightweight, web-based Human Resource Management System designed to handle HR operations for a single admin user. The application focuses on simplicity, usability, and clean UI while providing core functionalities such as employee management and attendance tracking.

This project simulates a basic internal HR tool commonly used in organizations, with a professional dashboard-style interface and RESTful backend services.

---

## 🚀 Live Demo

* 🌐 **Frontend URL:** https://hrms-frontend-rust-five.vercel.app/
* 🔗 **Backend API:** https://myhrms.zapto.org/api/ (AWS)
* 📂 **Frontend GitHub Repository:** https://github.com/reyjaisal/hrms-frontend/

> ⚠️ Backend is deployed on AWS EC2 free server, site might be take time to load, check the backend [API link](https://myhrms.zapto.org/api/) to ensure the backend server status!!

---

## 🛠️ Tech Stack

### Frontend ([Link](https://github.com/reyjaisal/hrms-frontend/))

* HTML5, SCSS, CSS3, JavaScript
* Bootstrap / Custom CSS (for UI styling)
* jQuery / Vanilla JS (for DOM manipulation & AJAX)

### Backend

* Django / Django REST Framework
* RESTful API architecture

### Database

* PostgreSQL

### Deployment

* Frontend: [Vercel](https://vercel.com/)
* Backend: [AWS](http://aws.amazon.com/)
* Database: Postgres - [AWS](http://aws.amazon.com/)
* Website Walkthrough Video: https://www.awesomescreenshot.com/video/50686343?key=6f1ccf01c58fc8831d057fb9bb3d0111

---

## ✨ Features

### 👨‍💼 Employee Management

* Add new employees with:
  * Employee ID (unique)
  * Full Name
  * Email Address (unique)
  * Department
* View all employees in a structured table
* Delete employees and restore employees
* Validation for:
  * Required fields
  * Email format
  * Password
  * Duplicate employee IDs
* Filter attendance

---

### 📅 Attendance Management

* Mark attendance with:

  * Employee
  * Status (Present / Absent)
* View attendance records
* Filter attendance

---

### 📊 Dashboard

* Total number of active and archived employees
* Daily attendance summary

---

### 🎯 UI/UX Highlights

* Clean and professional dashboard layout
* Sidebar navigation for easy access
* Reusable UI components
* Proper spacing and typography

> ⚠️ UI design is not responsive, (Responsive designe will be updated soon)

---

### ⚠️ UI States Implemented

* Loading states (spinners)
* Empty states (no data available)
* Error handling (API failures and frontend handling with different options)

---

## 🔌 API Endpoints

### Employee APIs

```
GET - /api/employees/get_employees/
GET - /api/employees/employee_id/get_employee/
POST - /api/employees/add_employee/
PUT - /api/employees/employee_id/update_employee
DELETE - /api/employees/employee_id/archive_employee/
PATCH - /api/employees/employee_id/restore_employee/
```
---

### Attendance APIs

```
GET - api/attendances/get_calendar_attendance/
GET - api/attendances/get_listview_attendance/
PATCH - api/attendances/employee_id/mark_attendance/
```
---

## 🧠 Backend Featuers

* Unique employee ID enforcement
* Graceful error handling
* Proper HTTP status codes:

  * `200 OK`
  * `201 Created`
  * `400 Bad Request`
  * `404 Not Found`

---

## 📂 Project Structure

```
hrms-lite/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── images/
│
├── backend/
│   └── employees/
│   │   ├── api/
│   │   ├── models/
│   │   └── urls/
|   ├── manage.py
│   └── hrms/

└── README.md
```

---

## ⚙️ Setup Instructions (Local Development)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/reyjaisal/hrms-backend.git
```

---

### 2️⃣ Backend Setup

```bash
cd (main dir)
python3 -m venv venv (create python virtual environment)
pip install -r requirements.txt
python manage.py runserver
```

---

### 3️⃣ Frontend Setup

```bash
git clone https://github.com/reyjaisal/hrms-frontend.git
```

Use index.html OR use Live Server.
> ⚠️ Don't forget to change API domain to localhost.

---

## 📌 Assumptions & Limitations

* Single admin user (no authentication system)
* No role-based access control
* No payroll, leave management, or advanced HR features
* Attendance is marked manually (no automation)
* Basic UI without complex charts
* UI is not responsives 

---

## 🎁 Bonus Features

* Filter attendance by date
* Filter employees by name
* Display total present per days on calendar view
* Dashboard summary cards

---

## 👨‍💻 Author

**Vishal Jaiswal**
Fullstack Software Developer

---

## 📄 License

This project is for assessment/demo purposes only.
