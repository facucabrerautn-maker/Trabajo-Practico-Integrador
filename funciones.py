import csv
import os
import requests

NOMBRE_ARCHIVO = 'paises.csv'
URL_API = 'https://restcountries.com/v3.1/all?fields=name,population,area,region'

def descargar_y_crear_csv():
    print("Descargando datos desde la API de restcountries.com...")
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
                superficie = int(pais.get('area', 0) or 0) # Usa 0 si 'area' es None
                continente = pais.get('region', 'N/A')
                
                # Aplica el filtro: nombre, continente y superficie deben ser válidos
                if nombre != 'N/A' and continente != 'N/A' and superficie > 0:
                    writer.writerow([nombre, poblacion, superficie, continente])
                    filas_escritas += 1
        
        if filas_escritas == 0:
            print("Error: La descarga fue exitosa, pero no se escribió ningún país. Verifique los datos de la API.")
            return False
            
        print(f"Archivo '{NOMBRE_ARCHIVO}' creado exitosamente con {filas_escritas} países.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API o la API devolvió un error: {e}")
        return False
    except IOError as e:
        print(f"Error al escribir el archivo CSV: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado durante la descarga/creación: {e}")
        return False
        
    return True

def cargar_datos():
    if not os.path.exists(NOMBRE_ARCHIVO):
        print(f"El archivo '{NOMBRE_ARCHIVO}' no existe.")
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
                 print(f"Advertencia: Se omitieron {filas_con_error} filas con formato incorrecto en el CSV.")
                 
    except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo CSV después de intentar crearlo.")
        return []
    except Exception as e:
        print(f"Error inesperado al leer el CSV: {e}")
        return []
        
    return paises

def mostrar_paises(lista_paises):
    if not lista_paises:
        print("No se encontraron países que coincidan con los criterios.")
        return
    
    print("\n--- Resultados ---")
    print(f"{'Nombre':<35} | {'Continente':<15} | {'Población':>15} | {'Superficie (km²)':>18}")
    print("-" * 88)
    for pais in lista_paises:
        print(f"{pais['nombre']:<35} | {pais['continente']:<15} | {pais['poblacion']:>15,} | {pais['superficie']:>18,}")
    print("-" * 88)
    print(f"Total: {len(lista_paises)} países.")

def buscar_por_nombre(paises):
    nombre = input("Ingrese el nombre (o parte del nombre) del país: ").lower().strip()
    if not nombre:
        print("Error: La búsqueda no puede estar vacía.")
        return
    resultados = [pais for pais in paises if nombre in pais['nombre'].lower()]
    mostrar_paises(resultados)

def validar_entero(mensaje):
    while True:
        valor_str = input(mensaje).strip()
        if not valor_str:
            print("Error: El valor no puede estar vacío.")
            continue
        try:
            return int(valor_str)
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")

def filtrar_por_continente(paises):
    continente_buscado = input("Ingrese el nombre del continente: ").lower().strip()
    if not continente_buscado:
        print("Error: El nombre del continente no puede estar vacío.")
        return
    
    continentes_disponibles = sorted(list(set(p['continente'].lower() for p in paises)))
    print(f"Continentes disponibles: {', '.join(c.capitalize() for c in continentes_disponibles)}")

    resultados = [pais for pais in paises if continente_buscado == pais['continente'].lower()]
    mostrar_paises(resultados)

def filtrar_por_poblacion(paises):
    min_pob = validar_entero("Ingrese la población mínima: ")
    max_pob = validar_entero("Ingrese la población máxima: ")
    
    if min_pob > max_pob:
        print("Error: La población mínima no puede ser mayor que la máxima.")
        return

    resultados = [pais for pais in paises if min_pob <= pais['poblacion'] <= max_pob]
    mostrar_paises(resultados)

def filtrar_por_superficie(paises):
    min_sup = validar_entero("Ingrese la superficie mínima (km²): ")
    max_sup = validar_entero("Ingrese la superficie máxima (km²): ")

    if min_sup > max_sup:
        print("Error: La superficie mínima no puede ser mayor que la máxima.")
        return

    resultados = [pais for pais in paises if min_sup <= pais['superficie'] <= max_sup]
    mostrar_paises(resultados)

def ordenar_paises(paises):
    print("Seleccione el criterio de ordenamiento:")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    criterio_op = input("Opción (1-3): ").strip()
    
    criterios = {
        '1': 'nombre',
        '2': 'poblacion',
        '3': 'superficie'
    }
    
    if criterio_op not in criterios:
        print("Error: Opción inválida.")
        return

    criterio = criterios[criterio_op]
    
    orden = input("Seleccione el orden (ASC / DESC): ").upper().strip()
    if orden not in ['ASC', 'DESC']:
        print("Error: Orden inválido. Se usará ASC por defecto.")
        orden = 'ASC'
        
    descendente = (orden == 'DESC')
    
    if criterio == 'nombre':
        key_sort = lambda pais: pais[criterio].lower()
    else:
        key_sort = lambda pais: pais[criterio]
        
    resultados_ordenados = sorted(paises, key=key_sort, reverse=descendente)
    mostrar_paises(resultados_ordenados)

def mostrar_estadisticas(paises):
    if not paises:
        print("No hay datos para calcular estadísticas.")
        return

    total_paises = len(paises)
    total_poblacion = sum(p['poblacion'] for p in paises)
    total_superficie = sum(p['superficie'] for p in paises)
    
    pais_max_pob = max(paises, key=lambda p: p['poblacion'])
    pais_min_pob = min(paises, key=lambda p: p['poblacion'])
    
    prom_poblacion = total_poblacion / total_paises if total_paises > 0 else 0
    prom_superficie = total_superficie / total_paises if total_paises > 0 else 0
    
    paises_por_continente = {}
    for pais in paises:
        continente = pais['continente']
        paises_por_continente[continente] = paises_por_continente.get(continente, 0) + 1
        
    print("\n--- Estadísticas Globales ---")
    print(f"País con mayor población: {pais_max_pob['nombre']} ({pais_max_pob['poblacion']:,})")
    print(f"País con menor población: {pais_min_pob['nombre']} ({pais_min_pob['poblacion']:,})")
    print(f"Población promedio: {prom_poblacion:,.2f}")
    print(f"Superficie promedio: {prom_superficie:,.2f} km²")
    
    print("\nCantidad de países por continente:")
    for continente, cantidad in sorted(paises_por_continente.items()):
        print(f"- {continente}: {cantidad} países")

def mostrar_menu():
    print("\n--- Gestión de Datos de Países (UTN TPI) ---")
    print("1. Buscar país por nombre")
    print("2. Filtrar por continente")
    print("3. Filtrar por rango de población")
    print("4. Filtrar por rango de superficie")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("0. Salir")