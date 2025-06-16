from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLabel, QLineEdit, QComboBox, QFileDialog, QTabWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RedSpectre - Framework de Pentest")
        self.setGeometry(100, 100, 1000, 800)
        self.recon_data = ""
        self.scan_data = ""
        self.vuln_data = ""
        self.target_ip = ""
        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.exploit_tab = QWidget()
        self.tabs.addTab(self.main_tab, "Outils principaux")
        self.tabs.addTab(self.exploit_tab, "Exploitation")
        self.init_main_tab()
        self.setCentralWidget(self.tabs)

    def init_main_tab(self):
        layout = QVBoxLayout()

        self.label = QLabel("Entrez une cible (IP ou URL) :")
        layout.addWidget(self.label)

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Ex: 192.168.1.1 ou example.com")
        layout.addWidget(self.target_input)

        self.template_label = QLabel("Type de template Nuclei :")
        layout.addWidget(self.template_label)

        self.template_selector = QComboBox()
        self.template_selector.addItems([
            "cves", "misconfiguration", "exposures", "default-logins",
            "takeovers", "technologies", "dns", "files"
        ])
        layout.addWidget(self.template_selector)
        self.nmap_mode_label = QLabel("Niveau de scan Nmap :")
        layout.addWidget(self.nmap_mode_label)
        self.nmap_mode_selector = QComboBox()
        self.nmap_mode_selector.addItems(["rapide", "standard", "agressif"])
        layout.addWidget(self.nmap_mode_selector)

        self.scan_button = QPushButton("Scan réseau")
        self.scan_button.clicked.connect(self.run_scan)
        layout.addWidget(self.scan_button)

        self.recon_button = QPushButton("Reconnaissance passive")
        self.recon_button.clicked.connect(self.run_passive_recon)
        layout.addWidget(self.recon_button)

        self.map_button = QPushButton("Carte Réseau")
        self.map_button.clicked.connect(self.show_network_graph)
        layout.addWidget(self.map_button)

        self.vuln_button = QPushButton("Scan de vulnérabilités (Nuclei)")
        self.vuln_button.clicked.connect(self.run_vuln_scan)
        layout.addWidget(self.vuln_button)

        self.report_button = QPushButton("Exporter rapport HTML")
        self.report_button.clicked.connect(self.export_report)
        layout.addWidget(self.report_button)

        self.multi_button = QPushButton("Mode multi-cibles")
        self.multi_button.clicked.connect(self.run_multi_target)
        layout.addWidget(self.multi_button)

        self.cleanup_button = QPushButton("Effacer les traces")
        self.cleanup_button.clicked.connect(self.clean_traces)
        layout.addWidget(self.cleanup_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.main_tab.setLayout(layout)

    def run_scan(self):
        from modules.scan.nmap_scan import run_nmap_scan
        target = self.target_input.text().strip()
        if target:
            self.target_ip = target
            mode = self.nmap_mode_selector.currentText()
            result = run_nmap_scan(target, mode)
            self.scan_data = result
            self.output.append(f"\n[SCAN RÉSEAU] Résultats pour {target}:\n{result}")
        else:
            self.output.append("Veuillez entrer une cible valide.")

    def run_passive_recon(self):
        from modules.recon.passive import passive_recon
        target = self.target_input.text().strip()
        if target:
            result = passive_recon(target)
            self.recon_data = result
            self.output.append(f"\n[RECONNAISSANCE PASSIVE] Résultats pour {target}:\n{result}")
        else:
            self.output.append("Veuillez entrer une cible valide.")

    def show_network_graph(self):
        from gui.network_graph import NetworkGraphWindow
        from modules.scan.network_graph import extract_graph_from_nmap
        target = self.target_input.text().strip()
        if target:
            try:
                G = extract_graph_from_nmap(target)
                self.graph_window = NetworkGraphWindow(G)
                self.graph_window.show()
            except Exception as e:
                self.output.append(f"Erreur lors de la génération du graphe : {e}")
        else:
            self.output.append("Veuillez entrer une cible valide.")

    def run_vuln_scan(self):
        from modules.scan.vuln_scan import run_nuclei_scan
        from gui.exploitation_tab import ExploitationTab
        target = self.target_input.text().strip()
        template_type = self.template_selector.currentText()
        if target:
            self.target_ip = target
            result = run_nuclei_scan(target, template_type)
            self.vuln_data = result
            self.output.append(f"\n[NUCLEI - {template_type.upper()}] Résultats pour {target}:\n{result}")
            self.tabs.removeTab(1)
            self.exploit_tab = ExploitationTab(result, target)
            self.tabs.addTab(self.exploit_tab, "Exploitation")
        else:
            self.output.append("Veuillez entrer une cible valide.")

    def export_report(self):
        from modules.report.report_generator import generate_report
        target = self.target_input.text().strip()
        if target:
            output_file = f"rapport_{target.replace('.', '_')}.html"
            path = generate_report(target, self.recon_data, self.scan_data, self.vuln_data, output_file)
            self.output.append(f"\n[✔] Rapport HTML généré : {path}")
        else:
            self.output.append("Veuillez entrer une cible valide.")

    def run_multi_target(self):
        from utils.multi_target import load_targets_from_file
        from modules.recon.passive import passive_recon
        from modules.scan.nmap_scan import run_nmap_scan
        from modules.scan.vuln_scan import run_nuclei_scan
        from modules.report.report_generator_multi import generate_global_report

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Choisir un fichier de cibles", "", "Text Files (*.txt)")

        if file_path:
            targets = load_targets_from_file(file_path)
            if isinstance(targets, str):
                self.output.append(targets)
                return

            results = {}
            for target in targets:
                self.output.append(f"\n⏳ Traitement de la cible : {target}")
                recon = passive_recon(target)
                scan = run_nmap_scan(target)
                nuclei = run_nuclei_scan(target, self.template_selector.currentText())
                results[target] = {
                    "recon": recon,
                    "scan": scan,
                    "nuclei": nuclei
                }

            output_path = generate_global_report(results, "rapport_global.html")
            self.output.append(f"\n✅ Rapport global généré : {output_path}")

    def clean_traces(self):
        from utils.cleanup import clean_redspectre_traces
        self.output.append("\n🧹 Démarrage du nettoyage des traces...")
        result = clean_redspectre_traces()
        for line in result:
            self.output.append(line)
        self.output.append("✅ Nettoyage terminé.")

def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
