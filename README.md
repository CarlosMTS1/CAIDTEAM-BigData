⛽🌦️ CAIDTEAM - Análisis de Combustible y Clima en Chile

Proyecto Integrador de Big Data (IEI-095) desarrollado por el equipo CAIDTEAM, enfocado en el análisis de precios históricos de combustibles en Chile y datos climáticos obtenidos en tiempo real mediante APIs públicas.

📋 Descripción

Este proyecto implementa un proceso ETL (Extract, Transform, Load) utilizando Python para integrar información proveniente de:

Comisión Nacional de Energía (CNE)
OpenWeatherMap

Los datos son procesados, transformados y almacenados en un archivo Excel estructurado para posteriormente ser analizados mediante un dashboard interactivo en Power BI.

🎯 Objetivo

Analizar la evolución de los precios de los combustibles en Chile y relacionarlos con condiciones climáticas actuales para apoyar la toma de decisiones basada en datos.

🏗️ Arquitectura de la Solución
API CNE + OpenWeatherMap
            ↓
       Python ETL
            ↓
 Excel (.xlsx)
            ↓
   Power BI Dashboard
🛠️ Tecnologías Utilizadas
Python 3
Pandas
Requests
OpenPyXL
Power BI Desktop
Git
GitHub
📊 Fuentes de Datos
Comisión Nacional de Energía (CNE)
Fuente: https://energiaabierta.cl
Datos históricos de combustibles líquidos.
Periodo analizado: Enero 2023 - Junio 2025.
OpenWeatherMap
Fuente: https://openweathermap.org/api
Datos climáticos en tiempo real.
Ciudades analizadas:
Santiago
Valparaíso
Concepción
Puerto Montt
Antofagasta
⚙️ Proceso ETL
Extracción

Obtención de:

Precios de bencina 93, 95 y 97 octanos.
Precio de diésel.
Temperatura.
Humedad.
Presión atmosférica.
Velocidad del viento.
Transformación

Se aplicaron las siguientes transformaciones:

Eliminación de valores nulos.
Generación de atributos temporales.
Cálculo de variaciones de precios.
Clasificación de tendencias.
Cálculo de promedios.
Categorización de temperatura.
Categorización de humedad.
Carga

Generación del archivo:

dashboard_combustible_clima.xlsx

Con las siguientes hojas:

Precios Historicos
Clima Ciudades
Resumen por Año
Resumen por Trimestre
KPIs
📈 Dashboard Power BI

El dashboard incluye:

KPIs
Máximo precio B95
Máximo precio Diesel
Promedio de Gasolinas
Visualizaciones
Evolución histórica de precios B95
Temperatura por ciudad
Distribución de tendencias de precios
📌 Resultados
43 registros históricos de combustibles procesados.
5 ciudades chilenas monitoreadas en tiempo real.
8 atributos derivados generados.
5 hojas de análisis en Excel.
Dashboard interactivo desarrollado en Power BI.
Hallazgos
La bencina 95 osciló entre $935 y $1.065 por litro.
El 55,6% de las actualizaciones mostraron disminución de precio.
La diferencia promedio entre bencina 97 y 93 fue de aproximadamente $100 por litro.
El diésel se mantuvo entre $50 y $70 por litro por debajo de la bencina 95.
📂 Estructura del Proyecto
CAIDTEAM-BigData/
│
├── etl_combustible_clima.py
├── dashboard_combustible_clima.xlsx
├── dashboard.pbix
├── INFORME_FINAL_CAIDTEAM.docx
└── README.md
👥 Integrantes
Carlos Aguayo
Brandon Vásquez

Carrera: Ingeniería en Informática

Asignatura: Big Data (IEI-095)

Docente: Osvaldo Antoine Archile Aguilar

🔗 Repositorio

GitHub:
https://github.com/CarlosMTS1/CAIDTEAM-BigData

🚀 Mejoras Futuras
Integrar precio del petróleo WTI.
Incorporar tipo de cambio USD/CLP.
Automatizar actualizaciones desde APIs.
Publicar el dashboard en Power BI Service.
Implementar modelos predictivos de precios.
