import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QPushButton,
    QLabel, QLineEdit, QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox
)
from PyQt5.QtCore import QDate
from src.gastoservice import GastoService
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Gastos")
        #crea la ventana
        self.setGeometry(100, 100, 600, 600)
        #indica el tamaño de la ventana
        self.servicio = GastoService()

        self.label_fecha = QLabel("Fecha:", self)
        self.fecha_edit = QDateEdit(self)
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setDisplayFormat("yyyy-MM-dd")

        self.label_desc = QLabel("Descripción:", self)
        self.desc_edit = QLineEdit(self)

        self.label_monto = QLabel("Monto:", self)
        self.monto_edit = QLineEdit(self)

        self.label_categoria = QLabel("Categoría:", self)
        self.categoria_combo = QComboBox(self)
        self.categoria_combo.addItems(["Comida", "Transporte", "Ocio", "Salud", "Gustitos", "Otros"])

        # botones
        # Botón Crear
        self.boton = QPushButton("Crear gasto", self)
        self.boton.clicked.connect(self.crear_gasto)

        # Botón Actualizar
        self.boton_actualizar = QPushButton("Actualizar gasto", self)
        self.boton_actualizar.clicked.connect(self.actualizar_gasto)

        # Botón Eliminar
        self.boton_eliminar = QPushButton("Eliminar gasto", self)
        self.boton_eliminar.clicked.connect(self.eliminar_gasto)

        self.label_buscar = QLabel("Buscar:", self)
        self.buscar_edit = QLineEdit(self)
        self.buscar_edit.setPlaceholderText("Descripción...")
        self.boton_buscar = QPushButton("Filtrar", self)
        self.boton_buscar.clicked.connect(self.filtrar_gastos)
        self.boton_limpiar = QPushButton("Limpiar", self)
        self.boton_limpiar.clicked.connect(self.cargar_gastos_en_tabla)

        # ComboBox para filtrar por categoría
        self.filtro_categoria = QComboBox(self)
        self.filtro_categoria.addItem("Todas")
        self.filtro_categoria.addItems(["Comida", "Transporte", "Ocio", "Salud", "Gustitos", "Otros"])
        self.filtro_categoria.currentIndexChanged.connect(self.filtrar_gastos)

        # Mueve la tabla más abajo
        self.tabla = QTableWidget(self)
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Descripción", "Monto", "Categoría"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.cellClicked.connect(self.cargar_gasto_en_campos)

        # Mueve el total más abajo
        self.label_total = QLabel("Total gastado: $0", self)
        self.label_total.setFixedWidth(300)
        self.label_total.setStyleSheet("font-size: 18px; font-weight: bold; color: #2E8B57;")
        self.label_total.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.actualizar_total_gastado()

        # Aumenta la altura de la ventana
        self.setGeometry(100, 100, 650, 550)

        # Layouts
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        campos_layout = QVBoxLayout()
        botones_layout = QVBoxLayout()

        # Campos a la izquierda
        campos_layout.addWidget(self.label_fecha)
        campos_layout.addWidget(self.fecha_edit)
        campos_layout.addWidget(self.label_desc)
        campos_layout.addWidget(self.desc_edit)
        campos_layout.addWidget(self.label_monto)
        campos_layout.addWidget(self.monto_edit)
        campos_layout.addWidget(self.label_categoria)
        campos_layout.addWidget(self.categoria_combo)

        # Botones a la derecha
        botones_layout.addWidget(self.boton)
        botones_layout.addWidget(self.boton_actualizar)
        botones_layout.addWidget(self.boton_eliminar)

        form_layout.addLayout(campos_layout)
        form_layout.addLayout(botones_layout)

        main_layout.addLayout(form_layout)

        # Filtros y tabla
        filtros_layout = QHBoxLayout()
        filtros_layout.addWidget(self.label_buscar)
        filtros_layout.addWidget(self.buscar_edit)
        filtros_layout.addWidget(self.boton_buscar)
        filtros_layout.addWidget(self.boton_limpiar)
        filtros_layout.addWidget(self.filtro_categoria)
        main_layout.addLayout(filtros_layout)

        main_layout.addWidget(self.tabla)
        main_layout.addWidget(self.label_total)

        # Crea el botón antes de agregarlo al layout
        self.boton_grafico = QPushButton("Ver gráfico por categoría", self)
        self.boton_grafico.clicked.connect(self.mostrar_grafico_categoria)

        # ...luego agrégalo al layout
        main_layout.addWidget(self.boton_grafico)

        central_widget.setLayout(main_layout)

        self.cargar_gastos_en_tabla()

        import os
        ruta_estilos = os.path.join(os.path.dirname(__file__), "../resources/estilos.qss")
        with open(ruta_estilos, "r") as f:
            self.setStyleSheet(f.read())

    def crear_gasto(self):
        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")
        descripcion = self.desc_edit.text().strip()
        monto = self.monto_edit.text().strip()
        categoria = self.categoria_combo.currentText()

        # Validaciones GUI
        if not descripcion:
            QMessageBox.warning(self, "Validación", "La descripción no puede estar vacía.")
            return
        if not monto:
            QMessageBox.warning(self, "Validación", "El monto no puede estar vacío.")
            return
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                QMessageBox.warning(self, "Validación", "El monto debe ser mayor a cero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Validación", "El monto debe ser un número válido.")
            return

        try:
            self.servicio.crear_gasto(fecha, descripcion, monto, categoria)
            QMessageBox.information(self, "Éxito", "¡Gasto creado correctamente!")
            self.desc_edit.clear()
            self.monto_edit.clear()
            self.cargar_gastos_en_tabla()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def cargar_gastos_en_tabla(self):
        gastos = self.servicio.listar_gastos()
        self.tabla.setRowCount(len(gastos))
        for i, gasto in enumerate(gastos):
            self.tabla.setItem(i, 0, QTableWidgetItem(gasto.fecha))
            self.tabla.setItem(i, 1, QTableWidgetItem(gasto.descripcion))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(gasto.monto)))
            self.tabla.setItem(i, 3, QTableWidgetItem(gasto.categoria))
        self.actualizar_total_gastado()

    def eliminar_gasto(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un gasto para eliminar.")
            return
        try:
            self.servicio.eliminar_gasto(fila)
            QMessageBox.information(self, "Éxito", "Gasto eliminado correctamente.")
            self.cargar_gastos_en_tabla()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def actualizar_gasto(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Advertencia", "Seleccione un gasto para actualizar.")
            return

        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")
        descripcion = self.desc_edit.text().strip()
        monto = self.monto_edit.text().strip()
        categoria = self.categoria_combo.currentText()

        # Validaciones GUI
        if not descripcion:
            QMessageBox.warning(self, "Validación", "La descripción no puede estar vacía.")
            return
        if not monto:
            QMessageBox.warning(self, "Validación", "El monto no puede estar vacío.")
            return
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                QMessageBox.warning(self, "Validación", "El monto debe ser mayor a cero.")
                return
        except ValueError:
            QMessageBox.warning(self, "Validación", "El monto debe ser un número válido.")
            return

        try:
            self.servicio.actualizar_gasto(fila, fecha, descripcion, monto, categoria)
            QMessageBox.information(self, "Éxito", "Gasto actualizado correctamente.")
            self.cargar_gastos_en_tabla()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    def cargar_gasto_en_campos(self, row, column):
        self.fecha_edit.setDate(QDate.fromString(self.tabla.item(row, 0).text(), "yyyy-MM-dd"))
        self.desc_edit.setText(self.tabla.item(row, 1).text())
        self.monto_edit.setText(self.tabla.item(row, 2).text())
        # Cargar la categoría
        categoria = self.tabla.item(row, 3).text() if self.tabla.columnCount() > 3 else ""
        index = self.categoria_combo.findText(categoria)
        if index != -1:
            self.categoria_combo.setCurrentIndex(index)

    def actualizar_total_gastado(self):
        total = self.servicio.total_gastado()
        self.label_total.setText(f"Total gastado: ${total:.2f}")

    def filtrar_gastos(self):
        texto = self.buscar_edit.text().lower()
        categoria = self.filtro_categoria.currentText()
        gastos = self.servicio.listar_gastos()
        # Filtra por categoría si no es "Todas"
        if categoria != "Todas":
            gastos = [g for g in gastos if g.categoria == categoria]
        # Filtra por descripción si hay texto
        if texto:
            gastos = [g for g in gastos if texto in g.descripcion.lower()]
        self.tabla.setRowCount(len(gastos))
        for i, gasto in enumerate(gastos):
            self.tabla.setItem(i, 0, QTableWidgetItem(gasto.fecha))
            self.tabla.setItem(i, 1, QTableWidgetItem(gasto.descripcion))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(gasto.monto)))
            self.tabla.setItem(i, 3, QTableWidgetItem(gasto.categoria))
        self.actualizar_total_gastado()

    def mostrar_grafico_categoria(self):
        gastos = self.servicio.listar_gastos()
        categorias = {}
        for gasto in gastos:
            cat = gasto.categoria
            monto = float(gasto.monto)
            categorias[cat] = categorias.get(cat, 0) + monto

        if not categorias:
            QMessageBox.information(self, "Sin datos", "No hay gastos para graficar.")
            return

        # Paleta de colores personalizada (puedes ajustar los colores)
        colores = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700', '#C2C2F0']

        # Crear gráfico de torta
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            categorias.values(),
            labels=categorias.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=colores[:len(categorias)]
        )
        ax.set_title("Gastos por categoría")
        ax.legend(wedges, categorias.keys(), title="Categorías", loc="center left", bbox_to_anchor=(1, 0.5))
        plt.setp(autotexts, size=10, weight="bold")

        # Mostrar en ventana PyQt
        self.ventana_grafico = QMainWindow(self)
        self.ventana_grafico.setWindowTitle("Gráfico de gastos por categoría")
        canvas = FigureCanvas(fig)
        self.ventana_grafico.setCentralWidget(canvas)
        self.ventana_grafico.resize(600, 400)
        self.ventana_grafico.show()

def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())