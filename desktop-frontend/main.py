import sys
import base64
import requests
import webbrowser
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QStackedWidget, QFileDialog, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QDialog, QFrame, QGraphicsDropShadowEffect,
                             QScrollArea, QGridLayout)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Styling Constants
COLORS = {
    "bg": "#0f172a",
    "sidebar": "#1e293b",
    "primary": "#0ea5e9",
    "secondary": "#8b5cf6",
    "emerald": "#10b981",
    "orange": "#f59e0b",
    "text": "#f8fafc",
    "text_dark": "#94a3b8",
    "card": "#1e293b",
    "border": "#334155"
}

QSS = f"""
QMainWindow {{
    background-color: {COLORS['bg']};
}}

QWidget#MainContent {{
    background-color: {COLORS['bg']};
}}

QFrame#Sidebar {{
    background-color: {COLORS['sidebar']};
    border-right: 1px solid {COLORS['border']};
}}

QLabel {{
    color: {COLORS['text']};
    font-family: 'Segoe UI', sans-serif;
}}

QPushButton#SidebarBtn {{
    background-color: transparent;
    color: {COLORS['text_dark']};
    text-align: left;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}}

QPushButton#SidebarBtn:hover {{
    background-color: rgba(255, 255, 255, 0.05);
    color: {COLORS['text']};
}}

QPushButton#SidebarBtn[active="true"] {{
    background-color: rgba(14, 165, 233, 0.15);
    color: {COLORS['primary']};
    font-weight: bold;
}}

QPushButton#PrimaryBtn {{
    background-color: {COLORS['primary']};
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
}}

QPushButton#PrimaryBtn:hover {{
    background-color: #0284c7;
}}

QLineEdit {{
    background-color: #0f172a;
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    color: white;
    padding: 10px;
}}

QLineEdit:focus {{
    border: 1px solid {COLORS['primary']};
}}

QTableWidget {{
    background-color: {COLORS['card']};
    border: 1px solid {COLORS['border']};
    color: {COLORS['text']};
    gridline-color: {COLORS['border']};
    border-radius: 12px;
}}

QHeaderView::section {{
    background-color: #334155;
    color: white;
    padding: 8px;
    border: none;
}}

QMessageBox {{
    background-color: #1e293b;
    color: #f8fafc;
}}

QMessageBox QLabel {{
    color: #f8fafc;
}}

QMessageBox QPushButton {{
    background-color: #0ea5e9;
    color: white;
    border-radius: 4px;
    padding: 5px 15px;
    min-width: 60px;
}}

QScrollArea {{
    border: none;
    background-color: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: #334155;
    min-height: 20px;
    border-radius: 4px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
"""

API_BASE = "http://localhost:8000/api/"

class APIManager:
    def __init__(self):
        self.auth_header = None

    def login(self, username, password):
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.auth_header = {"Authorization": f"Basic {token}"}
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
            with open(filepath, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{API_BASE}{endpoint}", files=files, headers=self.auth_header)
                
                # Try to parse JSON, regardless of status code
                try:
                    res_data = response.json()
                except:
                    res_data = {"error": f"Server Error ({response.status_code})"}

                if response.status_code >= 400:
                    err = res_data.get("error") if isinstance(res_data, dict) else str(res_data)
                    return {"error": err or "Unknown server error"}
                
                return res_data
        except Exception as e:
            print(f"Upload Error: {e}")
            return {"error": f"Connection Error: {str(e)}"}

api = APIManager()

class StatCard(QFrame):
    def __init__(self, title, value, color="#0ea5e9"):
        super().__init__()
        self.setObjectName("StatCard")
        self.setFixedWidth(240)
        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 500; border:none;")
        
        self.value_lbl = QLabel(value)
        self.value_lbl.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold; border:none;")
        
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.value_lbl)

class ChartContainer(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px; border:none;")
        layout.addWidget(self.title_lbl)
        
        self.figure = Figure(facecolor='#1e293b')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header with Subtext
        top_layout = QHBoxLayout()
        header_vbox = QVBoxLayout()
        header = QLabel("Advanced Analytics Dashboard")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        sub_header = QLabel("Real-time equipment monitoring & cross-parameter analysis")
        sub_header.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px;")
        header_vbox.addWidget(header)
        header_vbox.addWidget(sub_header)
        top_layout.addLayout(header_vbox)
        
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.setObjectName("PrimaryBtn")
        self.refresh_btn.setFixedWidth(150)
        self.refresh_btn.clicked.connect(self.load_data)
        top_layout.addWidget(self.refresh_btn, alignment=Qt.AlignRight | Qt.AlignVCenter)
        main_layout.addLayout(top_layout)
        
        # Scroll area for dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(25)
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # 1. Stats Row
        self.stats_layout = QHBoxLayout()
        self.total_card = StatCard("Total Equipment", "0")
        self.flow_card = StatCard("Avg Flowrate", "0", COLORS['secondary'])
        self.press_card = StatCard("Avg Pressure", "0", COLORS['emerald'])
        self.temp_card = StatCard("Avg Temp", "0", COLORS['orange'])
        
        self.stats_layout.addWidget(self.total_card)
        self.stats_layout.addWidget(self.flow_card)
        self.stats_layout.addWidget(self.press_card)
        self.stats_layout.addWidget(self.temp_card)
        self.content_layout.addLayout(self.stats_layout)

        # 2. Charts Grid
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)
        
        self.scatter_chart = ChartContainer("Pressure vs Temp (Correlation)")
        self.metrics_chart = ChartContainer("Avg Metrics by Type")
        self.dist_chart = ChartContainer("Equipment Distribution")
        
        # Statistical Table Area (Mocking the stats breakdown in web)
        self.stats_table_container = QFrame()
        self.stats_table_container.setStyleSheet(f"background-color: {COLORS['card']}; border: 1px solid {COLORS['border']}; border-radius: 12px;")
        self.stats_table_layout = QVBoxLayout(self.stats_table_container)
        self.stats_table_layout.setContentsMargins(15, 15, 15, 15)
        st_title = QLabel("Statistical Breakdown")
        st_title.setStyleSheet("font-size: 16px; font-weight: bold; border:none;")
        self.stats_table_layout.addWidget(st_title)
        
        self.stats_scroll = QScrollArea()
        self.stats_scroll.setWidgetResizable(True)
        self.stats_scroll_content = QWidget()
        self.stats_scroll_layout = QVBoxLayout(self.stats_scroll_content)
        self.stats_scroll.setWidget(self.stats_scroll_content)
        self.stats_table_layout.addWidget(self.stats_scroll)

        charts_grid.addWidget(self.scatter_chart, 0, 0)
        charts_grid.addWidget(self.metrics_chart, 0, 1)
        charts_grid.addWidget(self.dist_chart, 1, 0)
        charts_grid.addWidget(self.stats_table_container, 1, 1)
        
        self.content_layout.addLayout(charts_grid)

    def style_axes(self, ax, title):
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='#94a3b8', labelsize=8)
        ax.spines['bottom'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title(title, color='white', fontsize=10, pad=10)
        ax.grid(True, color='#ffffff', alpha=0.05, linestyle='--')

    def load_data(self):
        data = api.get("summary/")
        if not data: return

        self.total_card.value_lbl.setText(str(data['total_count']))
        self.flow_card.value_lbl.setText(f"{data['avg_flowrate']:.1f} L/m")
        self.press_card.value_lbl.setText(f"{data['avg_pressure']:.1f} PSI")
        self.temp_card.value_lbl.setText(f"{data['avg_temperature']:.1f} °C")

        # Update Distribution Chart
        self.dist_chart.figure.clear()
        ax1 = self.dist_chart.figure.add_subplot(111)
        self.style_axes(ax1, "Units by Equipment Type")
        types = [d['equipment_type'] for d in data['type_distribution']]
        counts = [d['count'] for d in data['type_distribution']]
        ax1.bar(types, counts, color=COLORS['primary'], alpha=0.7)
        self.dist_chart.canvas.draw()

        # Update Scatter Chart
        self.scatter_chart.figure.clear()
        ax2 = self.scatter_chart.figure.add_subplot(111)
        self.style_axes(ax2, "Pressure vs Temperature Scatter")
        temps = [p['temperature'] for p in data['raw_data_points']]
        pressures = [p['pressure'] for p in data['raw_data_points']]
        ax2.scatter(temps, pressures, color=COLORS['secondary'], alpha=0.6, s=30)
        ax2.set_xlabel("Temp (°C)", color='#64748b', fontsize=8)
        ax2.set_ylabel("Pressure (PSI)", color='#64748b', fontsize=8)
        self.scatter_chart.canvas.draw()

        # Update Metrics Line Chart
        self.metrics_chart.figure.clear()
        ax3 = self.metrics_chart.figure.add_subplot(111)
        self.style_axes(ax3, "Average Metrics Comparison")
        avg_flows = [d['avg_flow'] for d in data['type_distribution']]
        avg_presss = [d['avg_press'] for d in data['type_distribution']]
        ax3.plot(types, avg_flows, marker='o', label='Flow', color=COLORS['primary'], linewidth=2)
        ax3.plot(types, avg_presss, marker='s', label='Press', color=COLORS['secondary'], linewidth=2)
        ax3.legend(facecolor='#1e293b', edgecolor='#334155', fontsize=8, labelcolor='white')
        self.metrics_chart.canvas.draw()

        # Update Statistical Breakdown List
        while self.stats_scroll_layout.count():
            item = self.stats_scroll_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            
        for type_data in data['type_distribution']:
            item_frame = QFrame()
            item_frame.setStyleSheet(f"background-color: #0f172a; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 5px;")
            if_layout = QVBoxLayout(item_frame)
            
            top_h = QHBoxLayout()
            t_lbl = QLabel(type_data['equipment_type'].upper())
            t_lbl.setStyleSheet(f"color: {COLORS['primary']}; font-weight: bold; font-size: 10px; border:none;")
            c_lbl = QLabel(f"{type_data['count']} units")
            c_lbl.setStyleSheet("color: #64748b; font-size: 10px; border:none;")
            top_h.addWidget(t_lbl)
            top_h.addWidget(c_lbl, alignment=Qt.AlignRight)
            if_layout.addLayout(top_h)
            
            metrics_h = QHBoxLayout()
            m_text = f"Flow: {type_data['avg_flow']:.1f} | Press: {type_data['avg_press']:.1f} | Temp: {type_data['avg_temp']:.1f}"
            m_lbl = QLabel(m_text)
            m_lbl.setStyleSheet("color: white; font-size: 11px; border:none;")
            metrics_h.addWidget(m_lbl)
            if_layout.addLayout(metrics_h)
            
            self.stats_scroll_layout.addWidget(item_frame)
        self.stats_scroll_layout.addStretch()

class UploadPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        container = QFrame()
        container.setStyleSheet(f"background-color: {COLORS['sidebar']}; border-radius: 20px; border: 2px dashed #475569;")
        container.setFixedSize(500, 300)
        
        c_layout = QVBoxLayout(container)
        c_layout.setAlignment(Qt.AlignCenter)
        
        self.icon_lbl = QLabel("📂")
        self.icon_lbl.setStyleSheet("font-size: 50px; border:none;")
        c_layout.addWidget(self.icon_lbl, alignment=Qt.AlignCenter)
        
        self.status_lbl = QLabel("Drag & Drop CSV or Click to Select")
        self.status_lbl.setStyleSheet("font-size: 16px; color: #94a3b8; border:none;")
        c_layout.addWidget(self.status_lbl, alignment=Qt.AlignCenter)
        
        self.btn = QPushButton("Choose File")
        self.btn.setObjectName("PrimaryBtn")
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.clicked.connect(self.select_file)
        c_layout.addWidget(self.btn, alignment=Qt.AlignCenter)
        
        layout.addWidget(container)
    
    def select_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open CSV', '.', "CSV Files (*.csv)")
        if fname:
            self.status_lbl.setText(f"Processing: {fname.split('/')[-1]}")
            res = api.post_file("upload/", fname)
            if res and "error" not in res:
                QMessageBox.information(self, "Success", "Data processed successfully.")
                self.status_lbl.setText("Upload Complete!")
            else:
                err_msg = res.get("error") if res else "Failed to connect to server."
                QMessageBox.warning(self, "Upload Failed", f"Error: {err_msg}")
                self.status_lbl.setText("Upload Failed")

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("Dataset History & Reports")
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(header)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Filename", "Upload Date", "Records", "Avg Flow", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.setObjectName("PrimaryBtn")
        self.refresh_btn.setFixedWidth(150)
        self.refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(self.refresh_btn, alignment=Qt.AlignRight)
    
    def load_history(self):
        data = api.get("history/")
        if not data: return
            
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(row['filename']))
            self.table.setItem(i, 1, QTableWidgetItem(row['upload_date'][:16].replace('T', ' ')))
            self.table.setItem(i, 2, QTableWidgetItem(str(row['total_records'])))
            self.table.setItem(i, 3, QTableWidgetItem(f"{row['avg_flowrate']:.2f}"))
            
            btn = QPushButton("Download Report")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"background-color: transparent; color: {COLORS['primary']}; font-weight: bold; border: 1px solid {COLORS['primary']}; border-radius: 4px; padding: 4px;")
            btn.clicked.connect(lambda checked, r=row['id']: webbrowser.open(f"{API_BASE}report/{r}/"))
            self.table.setCellWidget(i, 4, btn)

class SettingsPage(QWidget):
    settingsSaved = pyqtSignal(str, str) # name, role

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        header = QLabel("System Settings")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(header)
        sub = QLabel("Manage your profile and dashboard preferences")
        sub.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px; margin-bottom: 20px;")
        layout.addWidget(sub)

        # Profile Card
        card = QFrame()
        card.setStyleSheet(f"background-color: {COLORS['card']}; border-radius: 12px; border: 1px solid {COLORS['border']};")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        
        profile_h = QHBoxLayout()
        self.avatar_lbl = QLabel("JD")
        self.avatar_lbl.setFixedSize(60, 60)
        self.avatar_lbl.setAlignment(Qt.AlignCenter)
        self.avatar_lbl.setStyleSheet(f"background-color: {COLORS['primary']}; color: white; border-radius: 30px; font-size: 20px; font-weight: bold;")
        profile_h.addWidget(self.avatar_lbl)
        
        p_info = QVBoxLayout()
        self.p_name_display = QLabel("John Doe")
        self.p_name_display.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.p_role_display = QLabel("Senior Industrial Engineer")
        self.p_role_display.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 12px;")
        p_info.addWidget(self.p_name_display)
        p_info.addWidget(self.p_role_display)
        profile_h.addLayout(p_info)
        profile_h.addStretch()
        card_layout.addLayout(profile_h)
        
        card_layout.addWidget(QLabel("<hr style='border: 0; border-top: 1px solid #334155;'>"))
        
        form_grid = QGridLayout()
        form_grid.setSpacing(15)
        
        self.inputs = {}
        fields = [
            ("name", "Full Name", "John Doe"),
            ("email", "Email Address", "j.doe@chemvisual.com"),
            ("dept", "Department", "Engineering"),
            ("role", "Role", "Senior Industrial Engineer")
        ]
        
        for i, (key, label, default) in enumerate(fields):
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 12px; font-weight: bold;")
            edit = QLineEdit(default)
            self.inputs[key] = edit
            form_grid.addWidget(lbl, i, 0)
            form_grid.addWidget(edit, i, 1)
        
        card_layout.addLayout(form_grid)
        layout.addWidget(card)
        
        # Appearance Card
        app_card = QFrame()
        app_card.setStyleSheet(f"background-color: {COLORS['card']}; border-radius: 12px; border: 1px solid {COLORS['border']};")
        app_layout = QHBoxLayout(app_card)
        app_layout.setContentsMargins(20, 20, 20, 20)
        
        app_text = QVBoxLayout()
        app_title = QLabel("Dark Theme")
        app_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        app_desc = QLabel("Currently active across the application")
        app_desc.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 11px;")
        app_text.addWidget(app_title)
        app_text.addWidget(app_desc)
        app_layout.addLayout(app_text)
        
        toggle = QPushButton("Active")
        toggle.setStyleSheet(f"background-color: {COLORS['primary']}; color: white; border-radius: 15px; padding: 5px 15px; font-size: 11px;")
        app_layout.addWidget(toggle, alignment=Qt.AlignRight)
        
        layout.addWidget(app_card)
        
        # Buttons
        btn_h = QHBoxLayout()
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setObjectName("PrimaryBtn")
        self.save_btn.setFixedWidth(150)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        btn_h.addStretch()
        btn_h.addWidget(self.save_btn)
        layout.addLayout(btn_h)
        
        layout.addStretch()

    def save_settings(self):
        name = self.inputs['name'].text()
        role = self.inputs['role'].text()
        
        # Update local displays
        self.p_name_display.setText(name)
        self.p_role_display.setText(role)
        
        # Generate initials
        initials = "".join([n[0] for n in name.split()[:2]]).upper()
        self.avatar_lbl.setText(initials)
        
        # Emit signal to update Sidebar
        self.settingsSaved.emit(name, role)
        
        QMessageBox.information(self, "Success", "Profile settings saved successfully!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChemVisualizer Desktop Pro")
        self.resize(1200, 850)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 40, 15, 30)
        sidebar_layout.setSpacing(12)
        
        logo = QLabel("ChemV.")
        logo.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {COLORS['primary']}; margin-bottom: 40px; padding-left: 10px;")
        sidebar_layout.addWidget(logo)
        
        self.nav_btns = []
        nav_info = [
            ("Dashboard", 0),
            ("Upload CSV", 1),
            ("History", 2),
            ("Settings", 3)
        ]
        
        for text, idx in nav_info:
            btn = QPushButton(text)
            btn.setObjectName("SidebarBtn")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("active", "false")
            btn.clicked.connect(lambda checked, i=idx: self.switch_page(i))
            sidebar_layout.addWidget(btn)
            self.nav_btns.append(btn)
        
        sidebar_layout.addStretch()
        
        # User Profile Mini
        user_mini = QFrame()
        user_mini.setStyleSheet("background-color: rgba(255,255,255,0.03); border-radius: 10px; padding: 5px;")
        user_layout = QHBoxLayout(user_mini)
        self.sidebar_avatar = QLabel("JD")
        self.sidebar_avatar.setFixedSize(30, 30)
        self.sidebar_avatar.setAlignment(Qt.AlignCenter)
        self.sidebar_avatar.setStyleSheet(f"background-color: {COLORS['primary']}; color: white; border-radius: 15px; font-weight: bold; font-size: 10px;")
        user_layout.addWidget(self.sidebar_avatar)
        self.sidebar_username = QLabel("John Doe")
        self.sidebar_username.setStyleSheet("font-size: 12px; color: white;")
        user_layout.addWidget(self.sidebar_username)
        sidebar_layout.addWidget(user_mini)
        
        main_layout.addWidget(self.sidebar)
        
        # Content Area
        self.content = QStackedWidget()
        self.content.setObjectName("MainContent")
        self.dashboard = DashboardPage()
        self.upload = UploadPage()
        self.history = HistoryPage()
        self.settings = SettingsPage()
        
        # Connect Settings Signal
        self.settings.settingsSaved.connect(self.update_profile)
        
        self.content.addWidget(self.dashboard)
        self.content.addWidget(self.upload)
        self.content.addWidget(self.history)
        self.content.addWidget(self.settings)
        
        main_layout.addWidget(self.content)
        
        self.switch_page(0) # Default to dashboard

    def update_profile(self, name, role):
        self.sidebar_username.setText(name)
        initials = "".join([n[0] for n in name.split()[:2]]).upper()
        self.sidebar_avatar.setText(initials)

    def switch_page(self, index):
        self.content.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_btns):
            btn.setProperty("active", "true" if i == index else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        
        # Auto-refresh logic
        if index == 0: self.dashboard.load_data()
        if index == 2: self.history.load_history()

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ChemVisualizer - Login")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(50, 50, 300, 400)
        self.main_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['sidebar']};
                border-radius: 20px;
                border: 1px solid {COLORS['border']};
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 5)
        self.main_frame.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self.main_frame)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(20)
        
        title = QLabel("Sign In")
        title.setStyleSheet("font-size: 24px; font-weight: bold; border:none;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setText("admin")
        layout.addWidget(self.username)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setText("password123")
        layout.addWidget(self.password)
        
        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("PrimaryBtn")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self.accept)
        layout.addWidget(self.login_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(f"color: {COLORS['text_dark']}; border: none;")
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)

    def get_credentials(self):
        return self.username.text(), self.password.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        user, pwd = login.get_credentials()
        api.login(user, pwd)
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
