from src.gastoservice import GastoService

def menu():
    servicio = GastoService()
    opcion = 0
    while opcion != 5:
        print("\nGestor de Gastos")
        print("1. Crear Gasto")
        print("2. Listar Gastos")
        print("3. Actualizar Gasto")
        print("4. Eliminar Gasto")
        print("5. Salir")
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
        
        if opcion == 1:
            try:
                fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
                descripcion = input("Ingrese la descripción: ")
                monto = float(input("Ingrese el monto: "))
                servicio.crear_gasto(fecha, descripcion, monto)
                print("Gasto creado exitosamente.")
            except Exception as e:
                print(f"Error al crear el gasto: {e}")
        elif opcion == 2:
            gastos = servicio.listar_gastos()
            if gastos:
                for i, gasto in enumerate(gastos):
                    print(f"{i}. Fecha: {gasto.fecha}, Descripción: {gasto.descripcion}, Monto: {gasto.monto}")
            else:
                print("No hay gastos registrados.")
        elif opcion == 3:
            try:
                index = int(input("Ingrese el índice del gasto a actualizar: "))
                fecha = input("Ingrese la nueva fecha (o deje en blanco para no cambiar): ")
                descripcion = input("Ingrese la nueva descripción (o deje en blanco para no cambiar): ")
                monto_input = input("Ingrese el nuevo monto (o deje en blanco para no cambiar): ")
                monto = float(monto_input) if monto_input else None
                servicio.actualizar_gasto(index, fecha or None, descripcion or None, monto)
                print("Gasto actualizado exitosamente.")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == 4:
            try:
                index = int(input("Ingrese el índice del gasto a eliminar: "))
                servicio.eliminar_gasto(index)
                print("Gasto eliminado exitosamente.")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == 5:
            print("Saliendo del gestor de gastos.")
        else:
            print("Opción no válida. Por favor, intente de nuevo.")