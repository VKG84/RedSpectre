from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer
from modules.exploit.metasploit_client import MetasploitClient

class MeterpreterTerminal(QWidget):
    def __init__(self, session_id):
        super().__init__()
        self.setWindowTitle(f"Session Meterpreter #{session_id}")
        self.setGeometry(200, 200, 800, 500)
        self.session_id = str(session_id)
        self.client = MetasploitClient()

        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Commande Meterpreter...")
        layout.addWidget(self.command_input)

        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_command)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        # Timer de lecture automatique
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_response)
        self.timer.start(2000)  # toutes les 2s

    def send_command(self):
        cmd = self.command_input.text().strip()
        if cmd:
            self.output.append(f"> {cmd}")
            self.client.send_command(self.session_id, cmd)
            self.command_input.clear()

    def read_response(self):
        response = self.client.read_response(self.session_id)
        if isinstance(response, dict) and "data" in response:
            self.output.append(response["data"])
