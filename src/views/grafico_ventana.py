import calendar
from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QDialog, QMainWindow
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from src.utils import ruta_recurso
from src.views.crear_gasto_dialog import CrearGastoDialog

class GraficoVentana(QMainWindow):
    def __init__(self, servicio, filtro_mes):
        super().__init__()
        self.servicio = servicio
        self.filtro_mes = filtro_mes
        self.setWindowTitle("Gráfico de gastos por categoría")
        self.setGeometry(200, 200, 280, 260)  # Ventana más chica

        # --- Widget central y layout principal ---
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        central_widget.setStyleSheet("background: white;")

        # --- Botones principales ---
        botones_layout = QHBoxLayout()
        self.boton = QPushButton("Crear gasto", self)
        self.boton.setIcon(QIcon(ruta_recurso("resources/img/add.png")))
        self.boton.setFixedSize(140, 36)
        self.boton.clicked.connect(self.crear_gasto)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
                border: none;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)

        botones_layout.addStretch()
        botones_layout.addWidget(self.boton)
        botones_layout.addStretch()
        self.layout.addLayout(botones_layout)

        self.canvas = None
        self.mostrar_grafico_categoria()
        self.filtro_mes.currentIndexChanged.connect(self.mostrar_grafico_categoria)

    def mostrar_grafico_categoria(self):
        # Elimina el gráfico anterior si existe
        if self.canvas is not None:
            self.layout.removeWidget(self.canvas)
            self.canvas.setParent(None)
            self.canvas.deleteLater()
            self.canvas = None

        gastos = self.servicio.listar_gastos()
        mes_nombre = self.filtro_mes.currentText()
        if mes_nombre != "Todos":
            mes_num = str(list(calendar.month_name).index(mes_nombre)).zfill(2)
            gastos = [g for g in gastos if g.fecha[5:7] == mes_num]
        categorias = {}
        for gasto in gastos:
            cat = gasto.categoria
            monto = float(gasto.monto)
            categorias[cat] = categorias.get(cat, 0) + monto

        if not categorias:
            QMessageBox.information(self, "Sin datos", "No hay gastos para graficar.")
            return

        fig, ax = plt.subplots()
        ax.pie(categorias.values(), labels=categorias.keys(), autopct='%1.1f%%')
        ax.set_title("Gastos por categoría")
        fig.patch.set_facecolor('white')
        self.canvas = FigureCanvas(fig)
        self.layout.addWidget(self.canvas)

    def crear_gasto(self):
        dialog = CrearGastoDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            fecha, descripcion, monto, categoria = dialog.get_datos()
            from src.utils import validar_descripcion, validar_monto
            if not validar_descripcion(descripcion):
                QMessageBox.warning(self, "Validación", "La descripción no puede estar vacía.")
                return
            if not validar_monto(monto):
                QMessageBox.warning(self, "Validación", "El monto debe ser un número válido y mayor a cero.")
                return
            try:
                self.servicio.crear_gasto(fecha, descripcion, monto, categoria)
                QMessageBox.information(self, "Éxito", "¡Gasto creado correctamente!")
                # Si quieres actualizar el gráfico automáticamente:
                self.mostrar_grafico_categoria()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))