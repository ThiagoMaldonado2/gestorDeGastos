from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class TablaGastos(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Fecha", "Descripción", "Monto", "Categoría"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.verticalHeader().setDefaultSectionSize(28)  # Altura de fila más pequeña

    def cargar_gastos(self, gastos):
        self.setRowCount(len(gastos))
        for i, gasto in enumerate(gastos):
            self.setItem(i, 0, QTableWidgetItem(gasto.fecha))
            self.setItem(i, 1, QTableWidgetItem(gasto.descripcion))
            self.setItem(i, 2, QTableWidgetItem(str(gasto.monto)))
            self.setItem(i, 3, QTableWidgetItem(gasto.categoria))