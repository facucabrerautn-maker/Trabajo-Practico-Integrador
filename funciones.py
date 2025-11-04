import csv
import os
import requests
import sys
from rich.console import Console
from rich.table import Table
from thefuzz import fuzz, process

console = Console()

NOMBRE_ARCHIVO = 'paises.csv'
URL_API = 'https://restcountries.com/v3.1/all?fields=name,population,area,region'

def descargar_y_crear_csv():
    console.print("[bold blue]:cloud: Descargando datos desde la API de restcountries.com...[/bold blue]")
    try:
        respuesta = requests.get(URL_API)
        respuesta.raise_for_status()
        datos = respuesta.json()
        
        filas_escritas = 0
        
        with open(NOMBRE_ARCHIVO, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['nombre', 'poblacion', 'superficie', 'continente'])
            
            for pais in datos:
                nombre = pais.get('name', {}).get('common', 'N/A')
                poblacion = pais.get('population', 0)
                # Usa 0 si 'area' es None
                superficie = int(pais.get('area', 0) or 0)
                continente = pais.get('region', 'N/A')
                
                if nombre != 'N/A' and continente != 'N/A' and superficie > 0:
                    writer.writerow([nombre, poblacion, superficie, continente])
                    filas_escritas += 1
        
        if filas_escritas == 0:
            console.print("[bold red]Error: La descarga fue exitosa, pero no se escribió ningún país. Verifique los datos de la API.[/bold red]")
            return False
            
        console.print(f"[bold green]:white_check_mark: Archivo '{NOMBRE_ARCHIVO}' creado exitosamente con {filas_escritas} países.[/bold green]")
        
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error al conectar con la API o la API devolvió un error: {e}[/bold red]")
        return False
    except IOError as e:
        console.print(f"[bold red]Error al escribir el archivo CSV: {e}[/bold red]")
        return False
    except Exception as e:
        console.print(f"[bold red]Error inesperado durante la descarga/creación: {e}[/bold red]")
        return False
        
    return True

def cargar_datos():
    if not os.path.exists(NOMBRE_ARCHIVO):
        console.print(f"[bold yellow]El archivo '{NOMBRE_ARCHIVO}' no existe. Iniciando descarga.[/bold yellow]")
        if not descargar_y_crear_csv():
            return []

    paises = []
    try:
        with open(NOMBRE_ARCHIVO, 'r', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)
            filas_con_error = 0
            for fila in reader:
                try:
                    fila['poblacion'] = int(fila['poblacion'])
                    fila['superficie'] = int(fila['superficie'])
                    paises.append(fila)
                except (ValueError, TypeError):
                    filas_con_error += 1
            if filas_con_error > 0:
                 console.print(f"[bold yellow]Advertencia: Se omitieron {filas_con_error} filas con formato incorrecto en el CSV.[/bold yellow]")
                 
    except FileNotFoundError:
        console.print("[bold red]Error: No se pudo encontrar el archivo CSV después de intentar crearlo.[/bold red]")
        return []
    except Exception as e:
        console.print(f"[bold red]Error inesperado al leer el CSV: {e}[/bold red]")
        return []
        
    return paises

def mostrar_paises(lista_paises):
    if not lista_paises:
        console.print("[bold red]:x: No se encontraron países que coincidan con los criterios.[/bold red]")
        return
    
    tabla = Table(title="--- Resultados de Países ---", show_lines=True, header_style="bold cyan")
    
    tabla.add_column("Nombre", style="magenta", width=30)
    tabla.add_column("Continente", justify="left")
    tabla.add_column("Población", justify="right", style="green")
    tabla.add_column("Superficie (km²)", justify="right", style="yellow")
    
    for pais in lista_paises:
        poblacion_str = f"{pais['poblacion']:,}"
        superficie_str = f"{pais['superficie']:,}"
        
        tabla.add_row(
            pais['nombre'],
            pais['continente'],
            poblacion_str,
            superficie_str
        )

    console.print(tabla)
    console.print(f"\n[bold magenta]Total: {len(lista_paises)} países.[/bold magenta]")

def buscar_por_nombre(paises):
    nombre_buscado = input("Ingrese el nombre (o parte del nombre) del país: ").strip()
    
    if not nombre_buscado:
        console.print("[bold red]Error: La búsqueda no puede estar vacía.[/bold red]")
        return
        
    nombres_paises = [pais['nombre'] for pais in paises]
    
    coincidencias_fuzz = process.extract(
        query=nombre_buscado, 
        choices=nombres_paises, 
        scorer=fuzz.partial_ratio, 
        limit=10 
    )
    
    UMBRAL_PUNTAJE = 85
    resultados = []
    
    for nombre_coincidente, puntaje in coincidencias_fuzz: 
        if puntaje >= UMBRAL_PUNTAJE: 
            pais_encontrado = next(
                (p for p in paises if p['nombre'] == nombre_coincidente), 
                None
            )
            
            if pais_encontrado:
                 resultados.append(pais_encontrado)

    if not resultados:
        console.print(f"[bold red]:x: No se encontraron coincidencias para '{nombre_buscado}' con un puntaje mínimo de {UMBRAL_PUNTAJE}.[/bold red]")
        return
        
    mostrar_paises(resultados)

def validar_entero(mensaje):
    while True:
        try:
            valor_str = input(mensaje).strip()
            
            if not valor_str:
                console.print("[bold red]Error: El valor no puede estar vacío. Vuelva a intentar.[/bold red]")
                continue
            
            return int(valor_str)
        
        except ValueError:
            console.print("[bold red]Error: Por favor, ingrese un número entero válido.[/bold red]")
            
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold yellow]Operación cancelada. Regresando al menú principal.[/bold yellow]")
            return None

def filtrar_por_continente(paises):
    continente_buscado = input("Ingrese el nombre del continente: ").strip()
    
    if not continente_buscado:
        console.print("[bold red]Error: El nombre del continente no puede estar vacío.[/bold red]")
        return
    
    continentes_disponibles = sorted(list(set(p['continente'] for p in paises)))
    console.print(f"[bold magenta]Continentes disponibles:[/bold magenta] {', '.join(c for c in continentes_disponibles)}")

    resultados = [pais for pais in paises if continente_buscado.lower() == pais['continente'].lower()]
    mostrar_paises(resultados)

def filtrar_por_poblacion(paises):
    console.print("[bold yellow]Filtro por Rango de Población:[/bold yellow]")
    min_pob = validar_entero("Ingrese la población mínima: ")
    
    if min_pob is None: return
    
    max_pob = validar_entero("Ingrese la población máxima: ")

    if max_pob is None: return
    
    if min_pob > max_pob:
        console.print("[bold red]Error: La población mínima no puede ser mayor que la máxima.[/bold red]")
        return

    resultados = [pais for pais in paises if min_pob <= pais['poblacion'] <= max_pob]
    mostrar_paises(resultados)

def filtrar_por_superficie(paises):
    console.print("[bold yellow]Filtro por Rango de Superficie (km²):[/bold yellow]")
    min_sup = validar_entero("Ingrese la superficie mínima (km²): ")
    
    if min_sup is None: return
    
    max_sup = validar_entero("Ingrese la superficie máxima (km²): ")

    if max_sup is None: return

    if min_sup > max_sup:
        console.print("[bold red]Error: La superficie mínima no puede ser mayor que la máxima.[/bold red]")
        return

    resultados = [pais for pais in paises if min_sup <= pais['superficie'] <= max_sup]
    mostrar_paises(resultados)

def ordenar_paises(paises):
    console.print("Seleccione el criterio de ordenamiento:")
    console.print("1. Nombre")
    console.print("2. Población")
    console.print("3. Superficie")
    criterio_op = input("Opción (1-3): ").strip()
    
    criterios = {
        '1': 'nombre',
        '2': 'poblacion',
        '3': 'superficie'
    }
    
    if criterio_op not in criterios:
        console.print("[bold red]Error: Opción inválida.[/bold red]")
        return

    criterio = criterios[criterio_op]
    
    orden = input("Seleccione el orden (ASC / DESC): ").upper().strip()
    if orden not in ['ASC', 'DESC']:
        console.print("[bold yellow]Advertencia: Orden inválido. Se usará ASC por defecto.[/bold yellow]")
        orden = 'ASC'
        
    descendente = (orden == 'DESC')
    
    if criterio == 'nombre':
        key_sort = lambda pais: pais[criterio].lower()
    else:
        key_sort = lambda pais: pais[criterio]
        
    resultados_ordenados = sorted(paises, key=key_sort, reverse=descendente)
    console.print(f"\n[bold magenta]Ordenado por {criterio.capitalize()} ({orden})[/bold magenta]")
    mostrar_paises(resultados_ordenados)

def mostrar_estadisticas(paises):
    if not paises:
        console.print("[bold red]No hay datos para calcular estadísticas.[/bold red]")
        return

    total_paises = len(paises)
    total_poblacion = sum(p['poblacion'] for p in paises)
        
    pais_max_pob = max(paises, key=lambda p: p['poblacion'])
    pais_min_pob = min(paises, key=lambda p: p['poblacion'])
    
    prom_poblacion = total_poblacion / total_paises if total_paises > 0 else 0
    
    paises_por_continente = {}
    for pais in paises:
        continente = pais['continente']
        paises_por_continente[continente] = paises_por_continente.get(continente, 0) + 1
        
    console.print("\n[bold blue]📈 --- Estadísticas Globales ---[/bold blue]")
    console.print(f"País con mayor población: [green]{pais_max_pob['nombre']} ({pais_max_pob['poblacion']:,})[/green]")
    console.print(f"País con menor población: [red]{pais_min_pob['nombre']} ({pais_min_pob['poblacion']:,})[/red]")
    console.print(f"Población promedio: {prom_poblacion:,.2f}")
    
    console.print("\n[bold yellow]Cantidad de países por continente:[/bold yellow]")
    for continente, cantidad in sorted(paises_por_continente.items()):
        console.print(f"- {continente}: [magenta]{cantidad} países[/magenta]")

def mostrar_menu():
    console.print("\n[bold blue]🌐--- Gestión de Datos de Países ---🌐[/bold blue]")
    console.print("1. [bold gray]🔍 --- Buscar país por nombre --- 🔍[/bold gray]")
    console.print("2. [bold cyan]🌎 --- Filtrar por continente --- 🌍[/bold cyan]")
    console.print("3. [bold yellow]👨 --- Filtrar por rango de población --- 👩[/bold yellow]")
    console.print("4. [bold green]🌲 --- Filtrar por rango de superficie --- 🌲[/bold green]")
    console.print("5. [bold magenta] :up_arrow: --- Ordenar países --- :down_arrow:[/bold magenta]")
    console.print("6. [bold white]📊 --- Mostrar estadísticas --- 📊[/bold white]")
    console.print("0. [bold red] 👋  --- Salir ---👋[/bold red]")