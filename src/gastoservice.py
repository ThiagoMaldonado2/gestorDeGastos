from src.gasto import Gasto
import pandas as pd
import os
from datetime import datetime
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QLineEdit

class GastoService:
    """
    Servicio para manejar gastos personales.
    Permite crear, listar, actualizar y eliminar gastos almacenados en un archivo CSV.
    """

    def __init__(self, archivo_csv=None):
        """
        Inicializa el servicio y carga los gastos desde el archivo CSV.
        
        Args:
            archivo_csv (str): Nombre del archivo CSV donde se almacenan los gastos.
        """
        # Si no se pasa un archivo, usa la ruta por defecto en la carpeta data
        if archivo_csv is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))  # Sube un nivel desde src
            data_dir = os.path.join(base_dir, "data")
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)  # Crea la carpeta data si no existe
            self.archivo_csv = os.path.join(data_dir, "gastos.csv")
        else:
            self.archivo_csv = archivo_csv

        if os.path.exists(self.archivo_csv):
            self.df = pd.read_csv(self.archivo_csv)
            if 'categoria' not in self.df.columns:
                self.df['categoria'] = 'Otros'
        else:
            self.df = pd.DataFrame(columns=["fecha", "descripcion", "monto", "categoria"])
            #archivo no existe, creo un DataFrame vacío
    
    def crear_gasto(self, fecha, descripcion, monto, categoria):
        """
        Crea un nuevo gasto y lo guarda en el archivo CSV.

        Args:
            fecha (str): fecha del gasto en formato YYYY-MM-DD
            descripcion (str): descripción del gasto
            monto (float): monto del gasto
            categoria (str): categoría del gasto

        Returns:
            Gasto: objeto Gasto creado

        Raises:
            ValueError: si la fecha o descripción están vacías, o si el monto es negativo
        """
        #Validaciones de datos
        if not fecha or not descripcion:
            raise ValueError("Fecha y descripción son obligatorias.")
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Fecha debe estar en formato YYYY-MM-DD.")
        try:
            monto = float(monto)
        except ValueError:
            raise ValueError("Monto debe ser un número.")
        if monto < 0:
            raise ValueError("El monto debe ser positivo.")
        
        #Aqui creamos el nuevo gasto
        nuevo = {'fecha': fecha, 'descripcion': descripcion, 'monto': monto, 'categoria': categoria}
        self.df = pd.concat([self.df, pd.DataFrame([nuevo])], ignore_index=True)
        self.df.to_csv(self.archivo_csv, index=False)
        return Gasto(fecha, descripcion, monto, categoria)
    
    def listar_gastos(self):
        """
        Devuelve una lista de todos los gastos almacenados.

        Returns:
            list: lista de objetos Gasto
        """
        return [Gasto(row['fecha'], row['descripcion'], row['monto'], row['categoria']) for _, row in self.df.iterrows()]
    
    def actualizar_gasto(self, index, fecha, descripcion, monto, categoria):
        """
        Actualiza un gasto existente.

        Args:
            index (int): índice del gasto a actualizar
            fecha (str): nueva fecha del gasto en formato YYYY-MM-DD (opcional)
            descripcion (str): nueva descripción del gasto (opcional)
            monto (float): nuevo monto del gasto (opcional)

        Returns:
            Gasto: objeto Gasto actualizado

        Raises:
            IndexError: si el índice está fuera de rango
        """
        if 0 <= index < len(self.df):
            if fecha:
                self.df.at[index, 'fecha'] = fecha
            if descripcion:
                self.df.at[index, 'descripcion'] = descripcion
            if monto is not None:
                self.df.at[index, 'monto'] = monto
            if categoria:
                self.df.at[index, 'categoria'] = categoria
            self.df.to_csv(self.archivo_csv, index=False)
            row = self.df.iloc[index]
            return Gasto(row['fecha'], row['descripcion'], row['monto'], row['categoria'])
        else:
            raise IndexError("Índice fuera de rango")
        
    def eliminar_gasto(self, index):
        """
        Elimina un gasto existente.

        Args:
            index (int): índice del gasto a eliminar

        Returns:
            Gasto: objeto Gasto eliminado

        Raises:
            IndexError: si el índice está fuera de rango
        """
        if 0 <= index < len(self.df):
            row = self.df.iloc[index]
            self.df = self.df.drop(index).reset_index(drop=True)
            self.df.to_csv(self.archivo_csv, index=False)
            return Gasto(row['fecha'], row['descripcion'], row['monto'], row['categoria'])
        else:
            raise IndexError("Índice fuera de rango")
    
    def total_gastado(self):
        """
        Calcula el total gastado sumando todos los montos.

        Returns:
            float: Total gastado.
        """
        return self.df["monto"].astype(float).sum()
