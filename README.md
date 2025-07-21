# Gestor de Gastos

Aplicación de escritorio para gestionar tus gastos personales de forma sencilla y visual.  
Permite registrar, editar, eliminar y filtrar gastos, ver totales y analizar tus gastos por categoría con gráficos.

## Características

- Registro de gastos con fecha, descripción, monto y categoría.
- Edición y eliminación de gastos existentes.
- Filtros por descripción y categoría.
- Visualización del total gastado.
- Gráfico de torta por categoría.
- Validaciones visuales y mensajes claros.
- Interfaz moderna y adaptable (PyQt5 + QSS).

## Capturas de pantalla

<!-- Reemplaza las rutas por las de tus imágenes -->
![Pantalla principal](gestorDeGastos/img/VentanaPrincipal.png)  
![Gráfico de categorías](gestorDeGastos/img/GraficoCategorias.png)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/ThiagoMaldonado2
/gestorDeGastos.git
   cd gestorDeGastos


Instala las dependencias:
pip install -r requirements.txt

Ejecuta la aplicación:
python main.py

## Estructura del proyecto
gestorDeGastos/
├── app_gastos.py
├── gastoservice.py
├── estilos.qss
├── requirements.txt
├── README.md
├── gastos.csv  # Se crea automáticamente
└── ...

## Requisitos previos

- Python 3.7 o superior

## Licencia

Este proyecto está licenciado bajo los términos de la [Licencia MIT](LICENSE).

