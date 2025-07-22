from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QDate

class CrearGastoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear nuevo gasto")
        self.setFixedSize(340, 270)
        self.setStyleSheet("QDialog { background: white; }")

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        label_style = "font-size: 13px;"
        field_style = "font-size: 13px; padding: 2px;"

        self.fecha_edit = QDateEdit(self)
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setDisplayFormat("yyyy-MM-dd")
        self.fecha_edit.setStyleSheet(field_style)

        self.desc_edit = QLineEdit(self)
        self.desc_edit.setStyleSheet(field_style)
        self.monto_edit = QLineEdit(self)
        self.monto_edit.setStyleSheet(field_style)
        self.categoria_combo = QComboBox(self)
        self.categoria_combo.addItems(["Comida", "Transporte", "Ocio", "Salud", "Gustitos", "Otros"])
        self.categoria_combo.setStyleSheet(field_style)

        layout.addWidget(QLabel("Fecha:", self, styleSheet=label_style))
        layout.addWidget(self.fecha_edit)
        layout.addWidget(QLabel("Descripción:", self, styleSheet=label_style))
        layout.addWidget(self.desc_edit)
        layout.addWidget(QLabel("Monto:", self, styleSheet=label_style))
        layout.addWidget(self.monto_edit)
        layout.addWidget(QLabel("Categoría:", self, styleSheet=label_style))
        layout.addWidget(self.categoria_combo)

        botones_layout = QHBoxLayout()
        self.boton_guardar = QPushButton("Guardar", self)
        self.boton_guardar.setStyleSheet(field_style)
        self.boton_guardar.clicked.connect(self.accept)
        self.boton_cancelar = QPushButton("Cancelar", self)
        self.boton_cancelar.setStyleSheet(field_style)
        self.boton_cancelar.clicked.connect(self.reject)
        botones_layout.addWidget(self.boton_guardar)
        botones_layout.addWidget(self.boton_cancelar)
        layout.addLayout(botones_layout)

    def get_datos(self):
        fecha = self.fecha_edit.date().toString("yyyy-MM-dd")
        descripcion = self.desc_edit.text().strip()
        monto = self.monto_edit.text().strip()
        categoria = self.categoria_combo.currentText()
        return fecha, descripcion, monto, categoria