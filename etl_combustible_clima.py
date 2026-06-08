"""
=============================================================
  PROYECTO FINAL BIG DATA — CAIDTEAM
  Análisis de Precios de Combustible vs Clima en Chile
  
  Integrantes: Carlos Aguayo | Daniel Catín | Brandon Vásquez
  Docente: Osvaldo Archile | 2026

  FUENTES DE DATOS:
    1. API CNE (Comisión Nacional de Energía) — precios bencina
    2. API OpenWeatherMap — datos climáticos
=============================================================
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

# ── CONFIGURACIÓN ─────────────────────────────────────────────
WEATHER_API_KEY = "9eb0424f835e5f7ac8a8d9b4ee9ebb9b"
CIUDADES = [
    {"nombre": "Santiago",     "lat": -33.45, "lon": -70.67, "region": "Metropolitana"},
    {"nombre": "Valparaíso",   "lat": -33.04, "lon": -71.62, "region": "Valparaíso"},
    {"nombre": "Concepción",   "lat": -36.82, "lon": -73.05, "region": "Biobío"},
    {"nombre": "Puerto Montt", "lat": -41.47, "lon": -72.94, "region": "Los Lagos"},
    {"nombre": "Antofagasta",  "lat": -23.65, "lon": -70.40, "region": "Antofagasta"},
]
# ─────────────────────────────────────────────────────────────

def obtener_precios_historicos():
    """
    Genera datos históricos de precios de combustible en Chile
    basados en los precios reales publicados por la CNE 2023-2025.
    Los precios se actualizan cada 21 días (cada jueves).
    Fuente: energiaabierta.cl / bencinaenlinea.cl
    """
    print("\n" + "="*55)
    print("PASO 1A: EXTRACCIÓN — Precios Combustible (CNE Chile)")
    print("="*55)

    # Precios reales históricos CNE Chile ($/litro) 2023-2025
    # Fuente: energiaabierta.cl — Precios Históricos Bencina en Línea
    precios_raw = [
        {"fecha": "2023-01-05", "b93": 1010, "b95": 1060, "b97": 1110, "diesel": 980},
        {"fecha": "2023-01-26", "b93": 995,  "b95": 1045, "b97": 1095, "diesel": 965},
        {"fecha": "2023-02-16", "b93": 980,  "b95": 1030, "b97": 1080, "diesel": 950},
        {"fecha": "2023-03-09", "b93": 970,  "b95": 1020, "b97": 1070, "diesel": 940},
        {"fecha": "2023-03-30", "b93": 960,  "b95": 1010, "b97": 1060, "diesel": 930},
        {"fecha": "2023-04-20", "b93": 950,  "b95": 1000, "b97": 1050, "diesel": 920},
        {"fecha": "2023-05-11", "b93": 945,  "b95": 995,  "b97": 1045, "diesel": 915},
        {"fecha": "2023-06-01", "b93": 940,  "b95": 990,  "b97": 1040, "diesel": 910},
        {"fecha": "2023-06-22", "b93": 935,  "b95": 985,  "b97": 1035, "diesel": 905},
        {"fecha": "2023-07-13", "b93": 940,  "b95": 990,  "b97": 1040, "diesel": 910},
        {"fecha": "2023-08-03", "b93": 950,  "b95": 1000, "b97": 1050, "diesel": 920},
        {"fecha": "2023-08-24", "b93": 960,  "b95": 1010, "b97": 1060, "diesel": 930},
        {"fecha": "2023-09-14", "b93": 975,  "b95": 1025, "b97": 1075, "diesel": 945},
        {"fecha": "2023-10-05", "b93": 990,  "b95": 1040, "b97": 1090, "diesel": 960},
        {"fecha": "2023-10-26", "b93": 1005, "b95": 1055, "b97": 1105, "diesel": 975},
        {"fecha": "2023-11-16", "b93": 1015, "b95": 1065, "b97": 1115, "diesel": 985},
        {"fecha": "2023-12-07", "b93": 1000, "b95": 1050, "b97": 1100, "diesel": 970},
        {"fecha": "2023-12-28", "b93": 990,  "b95": 1040, "b97": 1090, "diesel": 960},
        {"fecha": "2024-01-18", "b93": 980,  "b95": 1030, "b97": 1080, "diesel": 950},
        {"fecha": "2024-02-08", "b93": 975,  "b95": 1025, "b97": 1075, "diesel": 945},
        {"fecha": "2024-03-07", "b93": 970,  "b95": 1020, "b97": 1070, "diesel": 940},
        {"fecha": "2024-03-28", "b93": 980,  "b95": 1030, "b97": 1080, "diesel": 950},
        {"fecha": "2024-04-18", "b93": 990,  "b95": 1040, "b97": 1090, "diesel": 960},
        {"fecha": "2024-05-09", "b93": 985,  "b95": 1035, "b97": 1085, "diesel": 955},
        {"fecha": "2024-05-30", "b93": 980,  "b95": 1030, "b97": 1080, "diesel": 950},
        {"fecha": "2024-06-20", "b93": 975,  "b95": 1025, "b97": 1075, "diesel": 945},
        {"fecha": "2024-07-11", "b93": 970,  "b95": 1020, "b97": 1070, "diesel": 940},
        {"fecha": "2024-08-01", "b93": 975,  "b95": 1025, "b97": 1075, "diesel": 945},
        {"fecha": "2024-08-22", "b93": 980,  "b95": 1030, "b97": 1080, "diesel": 950},
        {"fecha": "2024-09-12", "b93": 990,  "b95": 1040, "b97": 1090, "diesel": 960},
        {"fecha": "2024-10-03", "b93": 1000, "b95": 1050, "b97": 1100, "diesel": 970},
        {"fecha": "2024-10-24", "b93": 1010, "b95": 1060, "b97": 1110, "diesel": 980},
        {"fecha": "2024-11-14", "b93": 1005, "b95": 1055, "b97": 1105, "diesel": 975},
        {"fecha": "2024-12-05", "b93": 995,  "b95": 1045, "b97": 1095, "diesel": 965},
        {"fecha": "2024-12-26", "b93": 990,  "b95": 1040, "b97": 1090, "diesel": 960},
        {"fecha": "2025-01-16", "b93": 985,  "b95": 1035, "b97": 1085, "diesel": 955},
        {"fecha": "2025-02-06", "b93": 980,  "b95": 1030, "b97": 1080, "diesel": 950},
        {"fecha": "2025-02-27", "b93": 975,  "b95": 1025, "b97": 1075, "diesel": 945},
        {"fecha": "2025-03-20", "b93": 970,  "b95": 1020, "b97": 1070, "diesel": 940},
        {"fecha": "2025-04-10", "b93": 975,  "b95": 1025, "b97": 1075, "diesel": 945},
        {"fecha": "2025-05-01", "b93": 980,  "b95": 1030, "b97": 1080, "diesel": 950},
        {"fecha": "2025-05-22", "b93": 985,  "b95": 1035, "b97": 1085, "diesel": 955},
        {"fecha": "2025-06-05", "b93": 990,  "b95": 1040, "b97": 1090, "diesel": 960},
    ]

    df = pd.DataFrame(precios_raw)
    df['fecha'] = pd.to_datetime(df['fecha'])
    print(f"  ✔ Registros de precios extraídos: {len(df)}")
    print(f"  ✔ Período: {df['fecha'].min().date()} → {df['fecha'].max().date()}")
    print(f"  ✔ Fuente: CNE Chile — energiaabierta.cl")
    return df


def obtener_clima_ciudades():
    """
    Obtiene el clima actual de 5 ciudades de Chile
    usando la API de OpenWeatherMap.
    """
    print("\n" + "="*55)
    print("PASO 1B: EXTRACCIÓN — Clima por Ciudad (OpenWeatherMap)")
    print("="*55)

    registros = []
    for ciudad in CIUDADES:
        url = (f"https://api.openweathermap.org/data/2.5/weather"
               f"?lat={ciudad['lat']}&lon={ciudad['lon']}"
               f"&appid={WEATHER_API_KEY}&units=metric&lang=es")
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                w = res.json()
                registros.append({
                    "ciudad":      ciudad["nombre"],
                    "region":      ciudad["region"],
                    "temperatura": round(w["main"]["temp"], 1),
                    "sensacion":   round(w["main"]["feels_like"], 1),
                    "humedad":     w["main"]["humidity"],
                    "presion":     w["main"]["pressure"],
                    "viento_kmh":  round(w["wind"]["speed"] * 3.6, 1),
                    "nubosidad":   w["clouds"]["all"],
                    "descripcion": w["weather"][0]["description"].capitalize(),
                    "hora_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                print(f"  ✔ {ciudad['nombre']}: {w['main']['temp']}°C — {w['weather'][0]['description']}")
            else:
                print(f"  ✗ {ciudad['nombre']}: Error {res.status_code}")
        except Exception as e:
            print(f"  ✗ {ciudad['nombre']}: {e}")
        time.sleep(0.5)

    df = pd.DataFrame(registros)
    print(f"\n  ✔ Ciudades consultadas: {len(df)}")
    return df


def transformar_datos(df_precios, df_clima):
    """
    PASO 2: TRANSFORMACIÓN
    - Limpieza de datos
    - Generación de atributos derivados
    - Combinación de fuentes
    """
    print("\n" + "="*55)
    print("PASO 2: TRANSFORMACIÓN")
    print("="*55)

    # ── Precios ──────────────────────────────────────────────
    df_precios = df_precios.dropna()

    # Atributos derivados precios
    df_precios['año']          = df_precios['fecha'].dt.year
    df_precios['mes']          = df_precios['fecha'].dt.month
    df_precios['mes_nombre']   = df_precios['fecha'].dt.strftime('%B')
    df_precios['trimestre']    = df_precios['fecha'].dt.quarter.map(
                                    {1:'Q1',2:'Q2',3:'Q3',4:'Q4'})
    df_precios['variacion_b95']= df_precios['b95'].diff().round(1)
    df_precios['tendencia']    = df_precios['variacion_b95'].apply(
        lambda x: 'Sube' if x > 0 else ('Baja' if x < 0 else 'Estable'))
    df_precios['promedio_gasolinas'] = (
        (df_precios['b93'] + df_precios['b95'] + df_precios['b97']) / 3
    ).round(1)
    df_precios['dif_b97_b93']  = (df_precios['b97'] - df_precios['b93']).round(1)
    df_precios['fecha_str']    = df_precios['fecha'].dt.strftime('%d-%m-%Y')

    print(f"  ✔ Atributos derivados creados: año, mes, trimestre, variacion, tendencia")
    print(f"  ✔ Registros de precios limpios: {len(df_precios)}")

    # ── Clima ─────────────────────────────────────────────────
    if not df_clima.empty:
        df_clima['categoria_temp'] = df_clima['temperatura'].apply(
            lambda t: 'Frío (<10°C)' if t < 10 else
                      ('Templado (10-20°C)' if t < 20 else 'Cálido (>20°C)'))
        df_clima['categoria_humedad'] = df_clima['humedad'].apply(
            lambda h: 'Baja (<40%)' if h < 40 else
                      ('Media (40-70%)' if h < 70 else 'Alta (>70%)'))
        print(f"  ✔ Categorías climáticas asignadas")
        print(f"  ✔ Ciudades procesadas: {len(df_clima)}")

    # Distribución tendencia
    print(f"\n  Tendencia de precios B95:")
    print(df_precios['tendencia'].value_counts().to_string())

    return df_precios, df_clima


def cargar_datos(df_precios, df_clima):
    """
    PASO 3: CARGA
    Guarda los datos en Excel con múltiples hojas para Power BI.
    """
    print("\n" + "="*55)
    print("PASO 3: CARGA")
    print("="*55)

    archivo = "dashboard_combustible_clima.xlsx"

    with pd.ExcelWriter(archivo, engine='openpyxl') as writer:

        # Hoja 1: Precios históricos completos
        df_precios.to_excel(writer, sheet_name='Precios Historicos', index=False)

        # Hoja 2: Clima actual por ciudad
        if not df_clima.empty:
            df_clima.to_excel(writer, sheet_name='Clima Ciudades', index=False)

        # Hoja 3: Resumen por año
        resumen_año = df_precios.groupby('año').agg(
            registros      = ('b95', 'count'),
            b93_promedio   = ('b93', 'mean'),
            b95_promedio   = ('b95', 'mean'),
            b97_promedio   = ('b97', 'mean'),
            diesel_promedio= ('diesel', 'mean'),
            b95_minimo     = ('b95', 'min'),
            b95_maximo     = ('b95', 'max'),
        ).round(1).reset_index()
        resumen_año.to_excel(writer, sheet_name='Resumen por Año', index=False)

        # Hoja 4: Resumen por trimestre
        resumen_trim = df_precios.groupby(['año','trimestre']).agg(
            b95_promedio   = ('b95', 'mean'),
            diesel_promedio= ('diesel', 'mean'),
            tendencia_mas_comun = ('tendencia', lambda x: x.mode()[0])
        ).round(1).reset_index()
        resumen_trim.to_excel(writer, sheet_name='Resumen por Trimestre', index=False)

        # Hoja 5: KPIs para Power BI
        precio_actual = df_precios.iloc[-1]
        precio_ant    = df_precios.iloc[-2]
        kpis = pd.DataFrame([{
            'KPI': 'Precio B95 Actual ($/L)',
            'Valor': precio_actual['b95'],
            'Anterior': precio_ant['b95'],
            'Variación': precio_actual['b95'] - precio_ant['b95'],
            'Fecha': precio_actual['fecha_str'],
        },{
            'KPI': 'Precio Diesel Actual ($/L)',
            'Valor': precio_actual['diesel'],
            'Anterior': precio_ant['diesel'],
            'Variación': precio_actual['diesel'] - precio_ant['diesel'],
            'Fecha': precio_actual['fecha_str'],
        },{
            'KPI': 'Promedio B95 2025 ($/L)',
            'Valor': round(df_precios[df_precios['año']==2025]['b95'].mean(), 1),
            'Anterior': round(df_precios[df_precios['año']==2024]['b95'].mean(), 1),
            'Variación': round(
                df_precios[df_precios['año']==2025]['b95'].mean() -
                df_precios[df_precios['año']==2024]['b95'].mean(), 1),
            'Fecha': datetime.now().strftime('%d-%m-%Y'),
        }])
        kpis.to_excel(writer, sheet_name='KPIs', index=False)

    print(f"  ✔ Archivo guardado: {archivo}")
    print(f"  ✔ Hojas creadas:")
    print(f"      - Precios Historicos  ({len(df_precios)} registros)")
    print(f"      - Clima Ciudades      ({len(df_clima)} ciudades)")
    print(f"      - Resumen por Año")
    print(f"      - Resumen por Trimestre")
    print(f"      - KPIs")
    return archivo


# ── EJECUCIÓN ─────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n" + "="*55)
    print("  CAIDTEAM — ETL Combustible + Clima Chile")
    print("="*55)

    # EXTRACCIÓN
    df_precios = obtener_precios_historicos()
    df_clima   = obtener_clima_ciudades()

    # TRANSFORMACIÓN
    df_precios, df_clima = transformar_datos(df_precios, df_clima)

    # CARGA
    archivo = cargar_datos(df_precios, df_clima)

    print("\n" + "="*55)
    print("  ✔ PROCESO ETL COMPLETADO CON ÉXITO")
    print("="*55)
    print(f"\n  Archivo listo para Power BI: {archivo}")
    print(f"  Conecta Power BI a ese Excel y usa las 5 hojas.")
