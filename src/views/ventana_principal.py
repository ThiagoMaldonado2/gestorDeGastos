from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QComboBox, QPushButton, QWidget,
    QVBoxLayout, QHBoxLayout, QMessageBox, QDialog, QTableWidgetItem
)
from PyQt5.QtGui import QIcon, QFontDatabase, QPixmap, QMovie
from PyQt5.QtCore import Qt
import calendar
from src.gastoservice import GastoService
from src.utils import validar_descripcion, validar_monto, filtrar_gastos, ruta_recurso
from src.widgets import TablaGastos
from src.views.crear_gasto_dialog import CrearGastoDialog
import os

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Gastos")
        self.setGeometry(100, 100, 340, 350)
        self.servicio = GastoService()

        # --- Carga la fuente InterVariable.ttf ---
        ruta_fuente = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "resources", "fonts", "InterVariable.ttf"
        )
        QFontDatabase.addApplicationFont(ruta_fuente)

        # --- Aplica la fuente globalmente ---
        self.setStyleSheet("""
            * {
                font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
                font-size: 13px;
            }
        """)

        # --- Total gastado ---
        self.label_total_texto = QLabel("Total gastado según filtros:", self)
        self.label_total_texto.setStyleSheet("font-size: 18px; font-weight: bold; color: #212121;")
        self.label_total = QLabel("$0", self)
        self.label_total.setStyleSheet("font-size: 36px; font-weight: bold; color: #212121;")
        self.label_total.setAlignment(Qt.AlignCenter)
        self.actualizar_total_gastado()

        # --- Tabla de gastos personalizada ---
        self.tabla = TablaGastos(self)
        self.tabla.setStyleSheet("font-size: 13px;")
        self.tabla.horizontalHeader().setStyleSheet(
            "QHeaderView::section {"
            "font-size: 13px; font-weight: bold; color: #212121; background: #f5f5f5; border: none;}"
        )
        self.tabla.setMinimumWidth(360)
        self.tabla.setMaximumWidth(420)
        self.tabla.verticalHeader().setDefaultSectionSize(24)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.verticalHeader().setVisible(False)  # Oculta la numeración de filas
        self.tabla.setColumnCount(4)  # Solo 4 columnas
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Descripción", "Monto", "Categoría"])
        self.tabla.setColumnWidth(0, 110)  # Fecha más ancha
        self.tabla.setColumnWidth(2, 70)   # Monto más flaca

        # --- Botones principales ---
        # --- Botón "Crear gasto" con GIF ---
        self.boton = QPushButton(self)
        boton_layout = QHBoxLayout(self.boton)
        boton_layout.setContentsMargins(12, 0, 12, 0)
        boton_layout.setSpacing(8)
        boton_layout.setAlignment(Qt.AlignVCenter)  # Centra verticalmente

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(ruta_recurso("resources/img/add.png")).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setFixedSize(18, 18)
        icon_label.setStyleSheet("background: transparent;")  # Fondo transparente
        boton_layout.addWidget(icon_label)

        boton_texto = QLabel("Crear gasto")
        boton_texto.setStyleSheet("color: white; font-weight: bold; font-size: 15px; padding-left: 4px; background: transparent;")
        boton_layout.addWidget(boton_texto)

        boton_layout.addStretch()

        self.boton.setFixedHeight(38)
        self.boton.setMinimumWidth(150)
        self.boton.clicked.connect(self.crear_gasto)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
                border: none;
                padding: 0 12px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)

        self.boton_grafico = QPushButton(self)
        grafico_layout = QHBoxLayout(self.boton_grafico)
        grafico_layout.setContentsMargins(12, 0, 12, 0)
        grafico_layout.setSpacing(8)
        grafico_layout.setAlignment(Qt.AlignVCenter)

        icon_graph = QLabel()
        icon_graph.setPixmap(QPixmap(ruta_recurso("resources/img/graph.png")).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_graph.setFixedSize(18, 18)
        icon_graph.setStyleSheet("background: transparent;")
        grafico_layout.addWidget(icon_graph)

        texto_graph = QLabel("Ver gráfico")
        texto_graph.setStyleSheet("color: #d32f2f; font-weight: bold; font-size: 15px; padding-left: 4px; background: transparent;")
        grafico_layout.addWidget(texto_graph)

        grafico_layout.addStretch()

        self.boton_grafico.setFixedHeight(38)
        self.boton_grafico.setMinimumWidth(150)
        self.boton_grafico.clicked.connect(self.mostrar_grafico_categoria)
        self.boton_grafico.setObjectName("boton_grafico")
        self.boton_grafico.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #d32f2f;
                border: 2px solid #d32f2f;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #ffeaea;
            }
        """)

        # --- Filtros ---
        self.filtro_mes = QComboBox(self)
        self.filtro_mes.addItem("Todos")
        for m in range(1, 13):
            self.filtro_mes.addItem(calendar.month_name[m])
        self.filtro_mes.setFixedWidth(120)
        self.filtro_mes.currentIndexChanged.connect(self.filtrar_gastos)

        self.filtro_categoria = QComboBox(self)
        self.filtro_categoria.addItem("Todas")
        self.filtro_categoria.addItems(["Comida", "Transporte", "Ocio", "Salud", "Gustitos", "Otros"])
        self.filtro_categoria.setFixedWidth(120)
        self.filtro_categoria.currentIndexChanged.connect(self.filtrar_gastos)

        # --- Layouts ---
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # --- Total gastado centrado ---
        total_layout = QVBoxLayout()
        total_layout.addWidget(self.label_total_texto, alignment=Qt.AlignCenter)
        total_layout.addWidget(self.label_total, alignment=Qt.AlignCenter)
        main_layout.addLayout(total_layout)

        # --- Botones principales alineados horizontalmente ---
        botones_layout = QHBoxLayout()
        botones_layout.addStretch()
        botones_layout.addWidget(self.boton)
        botones_layout.addSpacing(16)
        botones_layout.addWidget(self.boton_grafico)
        botones_layout.addStretch()
        main_layout.addLayout(botones_layout)

        # --- Filtros alineados horizontalmente y compactos ---
        filtros_layout = QHBoxLayout()
        filtros_layout.addStretch()
        filtros_layout.addWidget(QLabel("Mes:"))
        filtros_layout.addWidget(self.filtro_mes)
        filtros_layout.addSpacing(8)
        filtros_layout.addWidget(QLabel("Categoría:"))
        filtros_layout.addWidget(self.filtro_categoria)
        filtros_layout.addStretch()
        main_layout.addLayout(filtros_layout)

        # --- Tabla de gastos ---
        main_layout.addWidget(self.tabla, alignment=Qt.AlignCenter)

        central_widget.setLayout(main_layout)

        # --- Estilos e iconos ---
        ruta_estilos = ruta_recurso("resources/estilos.qss")
        with open(ruta_estilos, "r") as f:
            self.setStyleSheet(f.read())
        self.setWindowIcon(QIcon(ruta_recurso("resources/img/app_icon.png")))

        self.setStyleSheet(self.styleSheet() + "QWidget { background: white; }")

        self.setStyleSheet("""
            QWidget {
                background: white;
            }
            QLabel, QComboBox, QTableWidget, QHeaderView::section {
                color: #212121;
                font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
            }
            QComboBox {
                background-color: #f5f5f5;
                border: 1px solid #d1d1d1;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 13px;
                min-width: 80px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 24px;
                border-left: 1px solid #d1d1d1;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background: #e0e0e0;
            }
            QComboBox::down-arrow {
                image: url(resources/img/down-arrow.png);
                width: 16px;
                height: 16px;
                margin-right: 6px;
            }
            QComboBox QAbstractItemView {
                background: #fff;
                border-radius: 6px;
                selection-background-color: #e0e0e0;
                color: #212121;
            }
            QTableWidget {
                font-size: 13px;
            }
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
                border: none;
            }
            QPushButton#boton_grafico {
                background-color: white;
                color: #d32f2f;
                border: 2px solid #d32f2f;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton#boton_grafico:hover {
                background-color: #ffeaea;
            }
            QHeaderView::section {
                font-size: 13px;
                font-weight: bold;
                color: #212121;
                background: #f5f5f5;
                border: none;
            }
        """)

        self.cargar_gastos_en_tabla()

    def crear_gasto(self):
        dialog = CrearGastoDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            fecha, descripcion, monto, categoria = dialog.get_datos()
            if not validar_descripcion(descripcion):
                QMessageBox.warning(self, "Validación", "La descripción no puede estar vacía.")
                return
            if not validar_monto(monto):
                QMessageBox.warning(self, "Validación", "El monto debe ser un número válido y mayor a cero.")
                return
            try:
                self.servicio.crear_gasto(fecha, descripcion, monto, categoria)
                QMessageBox.information(self, "Éxito", "¡Gasto creado correctamente!")
                self.cargar_gastos_en_tabla()
                self.actualizar_total_gastado()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def cargar_gastos_en_tabla(self):
        gastos = self.servicio.listar_gastos()
        self.tabla.setRowCount(len(gastos))  # Asegúrate de ajustar el número de filas
        self.actualizar_total_gastado(gastos)

        for row, gasto in enumerate(gastos):
            # --- Fecha con botón editar ---
            fecha_widget = QWidget()
            fecha_layout = QHBoxLayout(fecha_widget)
            fecha_layout.setContentsMargins(0, 0, 0, 0)
            fecha_layout.setSpacing(4)

            btn_editar = QPushButton()
            btn_editar.setIcon(QIcon(ruta_recurso("resources/img/pencil.png")))  # Usa tu icono de lápiz
            btn_editar.setStyleSheet("border: none; background: transparent;")
            btn_editar.setCursor(Qt.PointingHandCursor)
            btn_editar.setFixedSize(18, 18)
            btn_editar.clicked.connect(lambda _, r=row: self.editar_gasto(r))
            fecha_layout.addWidget(btn_editar)

            label_fecha = QLabel(gasto.fecha)
            label_fecha.setAlignment(Qt.AlignCenter)
            fecha_layout.addWidget(label_fecha)

            self.tabla.setCellWidget(row, 0, fecha_widget)

            # Descripción alineada a la izquierda
            item_desc = QTableWidgetItem(gasto.descripcion)
            item_desc.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tabla.setItem(row, 1, item_desc)

            # Monto alineado a la derecha with $
            item_monto = QTableWidgetItem(f"${float(gasto.monto):.2f}")
            item_monto.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabla.setItem(row, 2, item_monto)

            # Categoría + botón borrar en la misma celda
            cat_widget = QWidget()
            cat_layout = QHBoxLayout(cat_widget)
            cat_layout.setContentsMargins(0, 0, 0, 0)
            cat_layout.setSpacing(4)
            cat_layout.setAlignment(Qt.AlignCenter)  # <-- Esto centra todo el contenido

            label_cat = QLabel(gasto.categoria)
            label_cat.setAlignment(Qt.AlignCenter)
            cat_layout.addWidget(label_cat)

            btn_borrar = QPushButton()
            btn_borrar.setIcon(QIcon(ruta_recurso("resources/img/delete.png")))
            btn_borrar.setStyleSheet("border: none; background: transparent;")
            btn_borrar.setCursor(Qt.PointingHandCursor)
            btn_borrar.setFixedSize(18, 18)
            btn_borrar.clicked.connect(lambda _, r=row: self.borrar_gasto(r))
            cat_layout.addWidget(btn_borrar)

            self.tabla.setCellWidget(row, 3, cat_widget)

    def actualizar_total_gastado(self, gastos=None):
        if gastos is None:
            gastos = self.servicio.listar_gastos()
        total = sum(float(g.monto) for g in gastos)
        self.label_total.setText(f"${total:.2f}")

    def filtrar_gastos(self):
        categoria = self.filtro_categoria.currentText()
        mes_nombre = self.filtro_mes.currentText()
        gastos = filtrar_gastos(self.servicio.listar_gastos(), "", categoria, mes_nombre)
        self.tabla.cargar_gastos(gastos)
        self.actualizar_total_gastado(gastos)

    def mostrar_grafico_categoria(self):
        from src.views.grafico_ventana import GraficoVentana
        # Guarda la ventana como atributo de la clase
        self.ventana_grafico = GraficoVentana(self.servicio, self.filtro_mes)
        self.ventana_grafico.show()

    def borrar_gasto(self, fila):
        reply = QMessageBox.question(
            self,
            "Confirmar borrado",
            "¿Estás seguro que quieres borrar este gasto?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self.servicio.eliminar_gasto(fila)
                QMessageBox.information(self, "Éxito", "¡Gasto eliminado correctamente!")
                self.cargar_gastos_en_tabla()
                self.actualizar_total_gastado()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def editar_gasto(self, fila):
        gasto = self.servicio.listar_gastos()[fila]
        dialog = CrearGastoDialog(self)
        # Si tu dialog tiene método para setear datos:
        if hasattr(dialog, "set_datos"):
            dialog.set_datos(gasto.fecha, gasto.descripcion, gasto.monto, gasto.categoria)
        if dialog.exec_() == QDialog.Accepted:
            fecha, descripcion, monto, categoria = dialog.get_datos()
            if not validar_descripcion(descripcion):
                QMessageBox.warning(self, "Validación", "La descripción no puede estar vacía.")
                return
            if not validar_monto(monto):
                QMessageBox.warning(self, "El monto debe ser un número válido y mayor a cero.")
                return
            try:
                self.servicio.actualizar_gasto(fila, fecha, descripcion, monto, categoria)
                QMessageBox.information(self, "Éxito", "¡Gasto actualizado correctamente!")
                self.cargar_gastos_en_tabla()
                self.actualizar_total_gastado()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
