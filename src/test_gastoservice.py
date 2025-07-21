import unittest
import os
from gastoservice import GastoService

class TestGastoService(unittest.TestCase):
    def setUp(self):
        # Usar un archivo temporal para pruebas
        self.test_file = "test_gastos.csv"
        self.service = GastoService(self.test_file)

    def tearDown(self):
        # Eliminar el archivo de prueba después de cada test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_crear_gasto(self):
        gasto = self.service.crear_gasto("2025-01-01", "Prueba", 100)
        self.assertEqual(gasto.fecha, "2025-01-01")
        self.assertEqual(gasto.descripcion, "Prueba")
        self.assertEqual(gasto.monto, 100)

    def test_listar_gastos(self):
        self.service.crear_gasto("2025-01-01", "Prueba", 100)
        gastos = self.service.listar_gastos()
        self.assertEqual(len(gastos), 1)
        self.assertEqual(gastos[0].descripcion, "Prueba")

    def test_actualizar_gasto(self):
        self.service.crear_gasto("2025-01-01", "Prueba", 100)
        gasto_actualizado = self.service.actualizar_gasto(0, "2025-02-01", "Actualizado", 200)
        self.assertEqual(gasto_actualizado.fecha, "2025-02-01")
        self.assertEqual(gasto_actualizado.descripcion, "Actualizado")
        self.assertEqual(gasto_actualizado.monto, 200)

    def test_eliminar_gasto(self):
        self.service.crear_gasto("2025-01-01", "Prueba", 100)
        self.service.eliminar_gasto(0)
        gastos = self.service.listar_gastos()
        self.assertEqual(len(gastos), 0)

    def test_crear_gasto_monto_negativo(self):
        with self.assertRaises(ValueError):
            self.service.crear_gasto("2025-01-01", "Prueba", -50)

    def test_crear_gasto_fecha_invalida(self):
        with self.assertRaises(ValueError):
            self.service.crear_gasto("2025-99-99", "Prueba", 100)

    def test_actualizar_gasto_indice_fuera_de_rango(self):
        with self.assertRaises(IndexError):
            self.service.actualizar_gasto(0, "2025-01-01", "Desc", 100)

    def test_eliminar_gasto_indice_fuera_de_rango(self):
        with self.assertRaises(IndexError):
            self.service.eliminar_gasto(0)

    def test_crear_gasto_descripcion_vacia(self):
        with self.assertRaises(ValueError):
            self.service.crear_gasto("2025-01-01", "", 100)

    def test_crear_gasto_monto_no_numerico(self):
        with self.assertRaises(ValueError):
            self.service.crear_gasto("2025-01-01", "Prueba", "no-numero")

    def test_actualizar_solo_descripcion(self):
        self.service.crear_gasto("2025-01-01", "Prueba", 100)
        gasto_actualizado = self.service.actualizar_gasto(0, None, "Solo descripción", None)
        self.assertEqual(gasto_actualizado.descripcion, "Solo descripción")
        self.assertEqual(gasto_actualizado.fecha, "2025-01-01")
        self.assertEqual(gasto_actualizado.monto, 100)
if __name__ == "__main__":
    unittest.main()