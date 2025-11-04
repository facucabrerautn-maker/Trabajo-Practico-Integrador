from funciones import (
    cargar_datos, 
    mostrar_menu, 
    buscar_por_nombre, 
    filtrar_por_continente,
    filtrar_por_poblacion,
    filtrar_por_superficie,
    ordenar_paises,
    mostrar_estadisticas
)

def main():
    paises = cargar_datos()
    if not paises:
        print("No se pudieron cargar los datos. Saliendo del programa.")
        return

    print(f"Se cargaron {len(paises)} países correctamente.")

    opciones = {
        '1': buscar_por_nombre,
        '2': filtrar_por_continente,
        '3': filtrar_por_poblacion,
        '4': filtrar_por_superficie,
        '5': ordenar_paises,
        '6': mostrar_estadisticas,
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == '0':
            print("Saliendo del programa...")
            break
        
        accion = opciones.get(opcion)
        
        if accion:
            accion(paises)
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()