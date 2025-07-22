import calendar
import os

def validar_descripcion(descripcion):
    """Valida que la descripción no esté vacía."""
    return bool(descripcion.strip())

def validar_monto(monto):
    """Valida que el monto sea un número mayor a cero."""
    try:
        monto_float = float(monto)
        return monto_float > 0
    except ValueError:
        return False

def filtrar_gastos(gastos, texto, categoria, mes_nombre):
    """Filtra la lista de gastos por texto, categoría y mes."""
    if mes_nombre != "Todos":
        mes_num = str(list(calendar.month_name).index(mes_nombre)).zfill(2)
        gastos = [g for g in gastos if g.fecha[5:7] == mes_num]
    if categoria != "Todas":
        gastos = [g for g in gastos if g.categoria == categoria]
    if texto:
        gastos = [g for g in gastos if texto in g.descripcion.lower()]
    return gastos

def ruta_recurso(rel_path):
    """
    Devuelve la ruta absoluta de un recurso, partiendo desde la raíz del proyecto.
    rel_path: ruta relativa desde la raíz (ej: 'resources/estilos.qss')
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, rel_path)