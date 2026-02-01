# Chemical Equipment Parameter Visualizer

A professional hybrid application designed to visualize and analyze chemical equipment parameters (Flowrate, Pressure, Temperature) through both Web and Desktop interfaces.

![Project Banner](placeholder-for-banner-image.png)

## 📖 Project Description

The **Chemical Equipment Parameter Visualizer** is a full-stack solution that enables engineers to upload CSV datasets containing equipment operational data. The system processes this data to generate real-time analytics, statistical summaries, and visual charts. It features a robust Django backend that serves a modern React web dashboard and a native PyQt5 desktop application, ensuring accessibility across different environments.

## ✨ Features

- **Dual-Platform Access**: Seamlessly switch between Web (React) and Desktop (PyQt5) interfaces.
- **Data Processing**: Upload generic CSV files with automatic parsing and validation using Pandas.
- **Interactive Dashboard**:
    - **Key Metrics**: Real-time calculation of Total Count, Average Flowrate, Pressure, and Temperature.
    - **Visualizations**: Dynamic bar charts showing equipment type distribution.
- **Report Generation**: One-click PDF report download for any uploaded dataset.
- **History Management**: Tracks the last 5 uploads with detailed historical logs.
- **Secure Authentication**: Basic authentication system for both platforms.

## 🛠️ Tech Stack

### Backend
- **Framework**: Django & Django REST Framework (DRF)
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite (Development)
- **PDF Generation**: ReportLab
- **Authentication**: Session & Basic Auth

### Web Frontend
- **Framework**: React.js (Vite)
- **Styling**: TailwindCSS
- **Charts**: Chart.js / React-Chartjs-2
- **Networking**: Axios

### Desktop Frontend
- **Framework**: PyQt5
- **Charts**: Matplotlib Integration
- **GUI Engine**: Qt Widgets

## 🚀 Installation & Setup

Follow these steps to set up the project locally.

### Prerequisites
- Python 3.9 or higher
- Node.js & npm

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ChemicalEquipmentVisualizer.git
cd ChemicalEquipmentVisualizer
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv

# Activate Virtual Environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python create_test_user.py # Creates admin/password123
python manage.py runserver
```
*Backend runs on: `http://localhost:8000`*

### 3. Web Frontend Setup
Open a new terminal:
```bash
cd web-frontend
npm install
npm run dev
```
*Web App runs on: `http://localhost:5173`*

### 4. Desktop Frontend Setup
Open a new terminal:
```bash
cd desktop-frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 🔌 API Endpoints

The backend exposes the following RESTful endpoints:

| Method | Endpoint | Description |
|bbox | | |
| `GET` | `/api/` | API Root / Welcome |
| `POST` | `/api/upload/` | Upload CSV File |
| `GET` | `/api/summary/` | Get Dashboard Stats |
| `GET` | `/api/history/` | List Upload History |
| `GET` | `/api/report/<id>/` | Download PDF Report |

## 📸 Screenshots

*(Placeholder: Add screenshots of Dashboard, Upload Page, and PDF Report here)*

---
**Developed for [Project/Course Name]**
