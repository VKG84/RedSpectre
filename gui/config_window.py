from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton, QFormLayout

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration des modules")
        self.setGeometry(200, 200, 500, 400)
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.scan_tab = QWidget()
        self.nuclei_tab = QWidget()
        self.general_tab = QWidget()

        self.tabs.addTab(self.scan_tab, "Scan Réseau")
        self.tabs.addTab(self.nuclei_tab, "Nuclei")
        self.tabs.addTab(self.general_tab, "Général")

        self.init_scan_tab()
        self.init_nuclei_tab()
        self.init_general_tab()

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_scan_tab(self):
        layout = QFormLayout()
        self.port_range = QLineEdit()
        self.port_range.setPlaceholderText("Ex: 1-1000 ou 22,80,443")
        layout.addRow("Ports personnalisés :", self.port_range)

        self.scan_mode = QComboBox()
        self.scan_mode.addItems(["Complet (-sV -O)", "Rapide (-F)", "TCP connect (-sT)"])
        layout.addRow("Mode de scan :", self.scan_mode)

        self.scan_tab.setLayout(layout)

    def init_nuclei_tab(self):
        layout = QFormLayout()
        self.thread_count = QLineEdit("10")
        self.timeout = QLineEdit("5")
        self.verbose = QCheckBox("Activer le mode verbose")
        self.custom_path = QLineEdit()
        self.custom_path.setPlaceholderText("Ex: /chemin/vers/templates")

        layout.addRow("Threads :", self.thread_count)
        layout.addRow("Timeout (s) :", self.timeout)
        layout.addRow("Path templates perso :", self.custom_path)
        layout.addRow("", self.verbose)

        self.nuclei_tab.setLayout(layout)

    def init_general_tab(self):
        layout = QFormLayout()
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText("Ex: ./rapports")
        self.auto_export = QCheckBox("Exporter automatiquement le rapport HTML")
        layout.addRow("Répertoire de sortie :", self.output_dir)
        layout.addRow("", self.auto_export)

        self.general_tab.setLayout(layout)
