from funciones import (
    cargar_datos, 
    mostrar_menu, 
    buscar_por_nombre, 
    filtrar_por_continente,
    filtrar_por_poblacion,
    filtrar_por_superficie,
    ordenar_paises,
    mostrar_estadisticas,
    console,
    limpiar_consola,
    pausa_para_continuar
)

def main():
    paises = cargar_datos()
    if not paises:
        console.print("[bold red]No se pudieron cargar los datos. Saliendo.[/bold red]")
        return

    console.print(f"[bold green]Se cargaron {len(paises)} países correctamente.[/bold green]") 
    
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
            limpiar_consola()
            console.print("[bold red]👋 Saliendo del programa...[/bold red]")
            break
        
        accion = opciones.get(opcion) 
        
        if accion:
            accion(paises) 
            
        else:
            limpiar_consola()
            console.print("[bold red]Opción no válida. Intente de nuevo.[/bold red]")

            pausa_para_continuar()

if __name__ == "__main__":
    main()