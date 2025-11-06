🌎 Trabajo Integrador: Explorador Global de Países

💻 Programación 1 - UTN (Tecnicatura Universitaria en Programación)

Este repositorio alberga el proyecto final del Trabajo Integrador de la materia Programación 1, desarrollado bajo la guía del profesor Ariel Enferrel.

👤 Información del Alumno

Criterio

Detalle

Alumno

Facundo Cabrera

Comisión

M2025-2

📂 Detalles del Repositorio

Este repositorio ha sido creado para almacenar todos los archivos generados a partir de las consignas del Trabajo Integrador. El objetivo principal es desarrollar un código:

✅ Limpio y estructurado

💡 Interactivo y navegable

🎨 Bonito (con formato en consola)

🚀 Completamente ejecutable

💠 Descripción del Trabajo

El programa es un Explorador Geográfico interactivo desarrollado en Python (o el lenguaje de implementación). Utiliza una base de datos de países almacenada en un archivo de texto plano (.csv) y ofrece un completo menú de navegación para que el usuario pueda consultar y analizar la información global.

El programa busca ofrecer datos sobre los 250 países del mundo (Superficie, Población, Continente) y sus estadísticas asociadas.

⚙️ Funcionalidades Principales

El menú interactivo permite al usuario navegar entre las siguientes 6 opciones:

1. 🔍 Buscar un País por Nombre

Permite encontrar países que coincidan parcial o totalmente con un término de búsqueda ingresado por el usuario.

2. 🌍 Filtrar Países (Sub-menú)

Un sub-menú para refinar la lista de países basado en criterios específicos:

Por Continente

Por Rango de Población (Mínimo y Máximo)

Por Rango de Superficie (Mínimo y Máximo en km²)

3. 📉 Ordenar Países (Sub-menú)

Un sub-menú para clasificar la lista de países por un criterio y un orden definidos:

Criterio: Nombre, Continente, Población o Superficie.

Orden: Ascendente (A) o Descendente (D).

4. 📊 Mostrar Estadísticas

Calcula y presenta información resumida sobre el conjunto de datos, incluyendo:

País con Mayor y Menor Población

Promedio de Población (Total / Número de Países)

Promedio de Superficie (Total / Número de Países)

Cantidad de Países por Continente

5. 👋 Salir

🧭 Ejemplo de Interacción (Ordenamiento)

La interacción del usuario en el programa se realiza a través de la consola:

Menú Principal

Elige una opción:
 🔍 --- Buscar un país por nombre --- 🔍
 🌎 --- Filtrar por continente --- 🌍️
 👨 --- Filtrar por rango de población --- 👩
 🌲 --- Filtrar por rango de superficie --- 🌲
 📉 --- Ordenar países --- 📈
 📊 --- Mostrar estadísticas --- 📊
 👋 --- Salir ---👋


Sub-menú de Ordenamiento

Suponiendo que el usuario elige: 📉 --- Ordenar países --- 📈

El programa preguntará el criterio por el cual quiere ordenar:
  1. Nombre
  2. Continente
  3. Población
  4. Superficie
Ingrese el número del criterio (1-4): [El usuario ingresa '1']


Selección del Orden

Ascendente (A) o Descendente (D): [El usuario ingresa 'A']


Resultado: Tabla Paginada

Si el usuario elige Ascendente, el programa mostrará una tabla con formato y colores con una paginación de 10 países por página.

El usuario podrá:

Navegar entre las páginas (Anterior/Siguiente).

Volver al menú principal en cualquier momento, restableciendo la vista sin historial de navegación.

🛠️ Requisitos para Ejecutar

El programa requiere la existencia del archivo de datos (paises.csv) en el mismo directorio de ejecución.
                                 
