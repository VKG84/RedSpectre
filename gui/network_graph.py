from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx

class NetworkGraphWindow(QWidget):
    def __init__(self, graph):
        super().__init__()
        self.setWindowTitle("Carte Réseau - Graphe Nmap")
        self.setGeometry(150, 150, 800, 600)
        layout = QVBoxLayout()
        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot(graph)

    def plot(self, graph):
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', ax=ax, node_size=2000, font_size=8)
        self.canvas.draw()
