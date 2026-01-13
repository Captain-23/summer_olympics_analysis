# 🏅 Summer Olympics Web Application

This project is a **Summer Olympics data analysis and visualization web application**.  
It was originally built using **Streamlit** and later **migrated to Flask** for better flexibility, customization, and production-ready deployment.  
The application is **hosted on Render**.

---

## 🚀 Project Overview

The app allows users to explore **Summer Olympics data** and gain insights such as:
- Country-wise medal tally
- Athlete performance analysis
- Sport and event-based comparisons
- Overall Olympic trends

Migrating from Streamlit to Flask helped in achieving:
- Better control over backend logic
- Custom UI using HTML & CSS
- Easier deployment and scalability

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS (Jinja2)
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib / Seaborn
- **Deployment:** Render
- **Version Control:** Git & GitHub

---

## 🔁 Migration: Streamlit → Flask

- Converted Streamlit components into Flask routes
- Replaced Streamlit UI with HTML templates
- Separated backend logic and frontend presentation
- Prepared the app for production deployment

---

## 📁 Project Structure
- project/
- │
- ├── app.py
- ├── templates/
- │   ├── index.html
- │   └── results.html
- ├── static/
- │   └── style.css
- ├── data/
- │   └── olympics.csv
- ├── requirements.txt
- └── README.md

---

## ▶️ Run Locally

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-folder>
```
2. Install the dependencies:
```
pip install -r requirements.txt
```
3. Run the app:
```
python app.py
```
4. Open in browser:
http://127.0.0.1:5000

---

🌐 Deployment
	•	Deployed on Render
	•	Uses Gunicorn as the production server
	•	Environment variables configured via Render dashboard

---
📚 Learning Outcomes
	•	Migrated a project from Streamlit to Flask
	•	Learned Flask routing and templating
	•	Understood real-world deployment using Render
	•	Improved backend–frontend integration skills

---

