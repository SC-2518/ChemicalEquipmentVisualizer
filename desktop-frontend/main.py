import sys
import base64
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTabWidget, QFileDialog, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QDialog, QFormLayout)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import webbrowser

API_BASE = "http://localhost:8000/api/"

class APIManager:
    def __init__(self):
        self.auth_header = None

    def login(self, username, password):
        # Basic Auth
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.auth_header = {"Authorization": f"Basic {token}"}
        # In a real app, verify credential here
        return True

    def get(self, endpoint):
        try:
            response = requests.get(f"{API_BASE}{endpoint}", headers=self.auth_header)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}")
            return None

    def post_file(self, endpoint, filepath):
        try:
            files = {'file': open(filepath, 'rb')}
            response = requests.post(f"{API_BASE}{endpoint}", files=files, headers=self.auth_header)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Upload Error: {e}")
            return None

api = APIManager()

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)
        
        layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.accept)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)

    def get_credentials(self):
        return self.username.text(), self.password.text()

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Stats
        stats_layout = QHBoxLayout()
        self.total_lbl = QLabel("Total: -")
        self.flow_lbl = QLabel("Avg Flow: -")
        self.press_lbl = QLabel("Avg Press: -")
        self.temp_lbl = QLabel("Avg Temp: -")
        
        for lbl in [self.total_lbl, self.flow_lbl, self.press_lbl, self.temp_lbl]:
            lbl.setStyleSheet("font-size: 14px; font-weight: bold; border: 1px solid #ccc; padding: 10px;")
            stats_layout.addWidget(lbl)
        
        layout.addLayout(stats_layout)

        # Plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)

    def load_data(self):
        data = api.get("summary/")
        if not data:
            return

        # Update stats
        self.total_lbl.setText(f"Total: {data['total_count']}")
        self.flow_lbl.setText(f"Avg Flow: {data['avg_flowrate']:.2f}")
        self.press_lbl.setText(f"Avg Press: {data['avg_pressure']:.2f}")
        self.temp_lbl.setText(f"Avg Temp: {data['avg_temperature']:.2f}")

        # Update Plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Data for chart
        types = [d['equipment_type'] for d in data['type_distribution']]
        counts = [d['count'] for d in data['type_distribution']]
        
        ax.bar(types, counts, color='skyblue')
        ax.set_title("Equipment Type Distribution")
        ax.set_ylabel("Count")
        
        self.canvas.draw()

class UploadTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.status_lbl = QLabel("Select a CSV file to upload")
        layout.addWidget(self.status_lbl)
        
        btn = QPushButton("Select File")
        btn.clicked.connect(self.select_file)
        layout.addWidget(btn)
        
        self.setLayout(layout)
    
    def select_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '.', "CSV Files (*.csv)")
        if fname:
            self.status_lbl.setText(f"Uploading {fname}...")
            res = api.post_file("upload/", fname)
            if res:
                self.status_lbl.setText("Upload Successful!")
                QMessageBox.information(self, "Success", "File uploaded successfully.")
            else:
                self.status_lbl.setText("Upload Failed.")
                QMessageBox.warning(self, "Error", "Upload failed.")

class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Filename", "Date", "Records", "Avg Flow", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        refresh_btn = QPushButton("Refresh History")
        refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
    
    def load_history(self):
        data = api.get("history/")
        if not data:
            return
            
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(row['filename']))
            self.table.setItem(i, 1, QTableWidgetItem(row['upload_date'][:16])) # Simple truncate
            self.table.setItem(i, 2, QTableWidgetItem(str(row['total_records'])))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row['avg_flowrate']:.2f}"))
            
            btn = QPushButton("PDF Report")
            btn.clicked.connect(lambda checked, r=row['id']: self.download_pdf(r))
            self.table.setCellWidget(i, 4, btn)
            
    def download_pdf(self, pk):
        url = f"{API_BASE}report/{pk}/"
        webbrowser.open(url) # Simplest way to 'download' or view

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 800, 600)
        
        tabs = QTabWidget()
        self.dashboard = DashboardTab()
        self.upload = UploadTab()
        self.history = HistoryTab()
        
        tabs.addTab(self.dashboard, "Dashboard")
        tabs.addTab(self.upload, "Upload CSV")
        tabs.addTab(self.history, "History")
        
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        user, pwd = login.get_credentials()
        api.login(user, pwd)
        
        window = MainWindow()
        window.show()
        # Load initial data
        window.dashboard.load_data()
        window.history.load_history()
        
        sys.exit(app.exec_())
    else:
        sys.exit(0)
