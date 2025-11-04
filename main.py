from funciones import (
    cargar_datos, 
    mostrar_menu, 
    buscar_por_nombre, 
    filtrar_por_continente,
    filtrar_por_poblacion,
    filtrar_por_superficie,
    ordenar_paises,
    mostrar_estadisticas,
    console # NECESARIO para que console.print funcione
)

def main():
    paises = cargar_datos()
    if not paises:
        print("No se pudieron cargar los datos. Saliendo del programa.")
        return

    # Usar console.print para el mensaje de éxito
    console.print(f"[bold green]Se cargaron {len(paises)} países correctamente.[/bold green]") 
    
    # ASEGÚRATE de que estas claves sean STRINGS y estén perfectas
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
        
        # Captura la entrada y la limpia de espacios y caracteres invisibles
        opcion = input("Seleccione una opción: ").strip() 
        
        if opcion == '0':
            console.print("[bold red]👋 Saliendo del programa...[/bold red]")
            break
        
        # Validación: intenta obtener la función del diccionario
        accion = opciones.get(opcion) 
        
        if accion:
            # Si se encuentra la función, se ejecuta
            accion(paises)
        else:
            # Si la opción no es '0' y no está en el diccionario
            console.print("[bold red]Opción no válida. Intente de nuevo.[/bold red]")

if __name__ == "__main__":
    main()