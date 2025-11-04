from funciones import (
    cargar_datos, 
    seleccionar_opcion, 
    buscar_por_nombre, 
    filtrar_por_continente,
    filtrar_por_poblacion,
    filtrar_por_superficie,
    ordenar_paises,
    mostrar_estadisticas
)

def main():
    paises = cargar_datos()

    opciones = {
        '1': buscar_por_nombre,
        '6': mostrar_estadisticas,
    }

    while True:
        opcion = seleccionar_opcion() 
        
        if opcion == '0':
            console.print("[bold red]👋 Saliendo del programa...[/bold red]")
            break
        
        accion = opciones.get(opcion)
        
        if accion:
            accion(paises)

if __name__ == "__main__":
    main()