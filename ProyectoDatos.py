import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# Leer el dataset
data = {
    'Año': [2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023],
    'Periodo': ['Q1', 'Q2', 'Q3', 'Q4'] * 3,
    'Utilidad Neta': [150000, 200000, 180000, 220000, 250000, 280000, 260000, 300000, 320000, 340000, 360000, 380000],
    'Activos Promedio': [1800000, 1900000, 2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000, 2700000, 2800000, 2900000],
    'Ingresos': [3000000, 3500000, 3200000, 3800000, 4000000, 4200000, 4400000, 4600000, 4800000, 5000000, 5200000, 5400000],
    'Gasto Operativo': [500000, 600000, 550000, 620000, 650000, 700000, 680000, 750000, 800000, 820000, 850000, 900000],
    'Ingresos Totales': [3000000, 3500000, 3200000, 3800000, 4000000, 4200000, 4400000, 4600000, 4800000, 5000000, 5200000, 5400000],
    'Gasto de Personal': [500000, 600000, 550000, 620000, 650000, 700000, 680000, 750000, 800000, 820000, 850000, 900000],
    'Gastos de Operación': [800000, 900000, 850000, 950000, 1000000, 1100000, 1050000, 1200000, 1300000, 1400000, 1500000, 1600000],
    'Margen Operativo': [2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000, 2700000, 2800000, 2900000, 3000000, 3100000],
    'Préstamos Morosos': [200000, 180000, 220000, 250000, 240000, 260000, 280000, 300000, 320000, 340000, 360000, 380000],
    'Préstamos Totales': [5000000, 5200000, 5400000, 5600000, 5800000, 6000000, 6200000, 6400000, 6600000, 6800000, 7000000, 7200000],
    'Cartera en Riesgo': [120000, 100000, 130000, 110000, 140000, 120000, 150000, 130000, 160000, 140000, 180000, 160000],
    'Cartera Bruta': [3000000, 3200000, 3400000, 3600000, 3800000, 4000000, 4200000, 4400000, 4600000, 4800000, 5000000, 5200000],
    'Patrimonio': [900000, 950000, 1000000, 1050000, 1100000, 1150000, 1200000, 1250000, 1300000, 1350000, 1400000, 1450000],
    'Cartera Actual': [2800000, 3100000, 3300000, 3500000, 3600000, 3800000, 4000000, 4200000, 4400000, 4600000, 4800000, 5000000],
    'Cartera Anterior': [2600000, 2900000, 3000000, 3200000, 3400000, 3600000, 3800000, 4000000, 4200000, 4400000, 4600000, 4800000],
    'Ingresos Operativos': [2900000, 3400000, 3100000, 3700000, 3800000, 4000000, 4200000, 4400000, 4600000, 4800000, 5000000, 5200000],
    'Número de Empleados': [50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105],
    'Depósitos Actuales': [2000000, 2200000, 2400000, 2600000, 2800000, 3000000, 3200000, 3400000, 3600000, 3800000, 4000000, 4200000],
    'Depósitos Anteriores': [1800000, 2000000, 2200000, 2400000, 2600000, 2800000, 3000000, 3200000, 3400000, 3600000, 3800000, 4000000],
    'Activos Líquidos': [2400000, 2500000, 2600000, 2700000, 2800000, 2900000, 3000000, 3100000, 3200000, 3300000, 3400000, 3500000],
    'Pasivos de Corto Plazo': [1000000, 1100000, 1200000, 1300000, 1400000, 1500000, 1600000, 1700000, 1800000, 1900000, 2000000, 2100000],
    'Solvencia': [0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72],
}

df = pd.DataFrame(data)
# Obtener los años disponibles en el dataset
anios_disponibles = df['Año'].unique()

# Menú de selección de año
selected_year = st.sidebar.selectbox("Selecciona un año", anios_disponibles)

# Filtrar el DataFrame por el año seleccionado
df_filtered = df[df['Año'] == selected_year]

# Función para mostrar cada indicador financiero
def mostrar_indicador_financiero(titulo, formula, descripcion, resultado, x, y, customdata, color=None):
    st.header(titulo)

    col1, col2, col3 = st.columns(3)

    col1.subheader("Fórmula:")
    col1.write(formula)

    col2.subheader("Descripción:")
    col2.write(descripcion)

    col3.subheader("Resultado:")
    col3.write(resultado)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        hovertemplate=customdata,
        customdata=customdata,
        mode='lines+markers',
        line=dict(color=color),
    ))

    fig.update_layout(
        yaxis=dict(title=titulo),
        title=titulo,
        xaxis=dict(title='Periodo'),
    )

    st.subheader(f"Gráfica interactiva de {titulo}")
    st.plotly_chart(fig)

# Menú de selección de funcionalidad
selected_functionality = st.sidebar.selectbox("Selecciona una categoria", [
    "Rentabilidad",
    "Eficiencia Operativa",
    "Gasto",
    "Calidad de Cartera",
    "Otros Indicadores",  # Agregado para nuevas fórmulas
])

# Mostrar la funcionalidad seleccionada
if selected_functionality == "Rentabilidad":
    st.subheader("Fórmulas de Rentabilidad")
    
    mostrar_indicador_financiero(
        "Rentabilidad sobre el activo (ROA)",
        "ROA = Utilidad Neta / Activos Totales Promedio",
        "Esta fórmula mide la eficiencia con la que una empresa utiliza sus activos para generar ganancias.",
        f"ROA: {df_filtered['Utilidad Neta'].iloc[-1] / df_filtered['Activos Promedio'].iloc[-1]:.2%}",
        df_filtered['Periodo'],
        df_filtered['Utilidad Neta'] / df_filtered['Activos Promedio'],
        customdata=[[utilidad, activos] for utilidad, activos in zip(df_filtered['Utilidad Neta'], df_filtered['Activos Promedio'])],
        color='blue'
    )
    mostrar_indicador_financiero(
        "Rentabilidad sobre el activo (ROA)",
        "ROA = Utilidad Neta / Activos Totales Promedio",
        "Esta fórmula mide la eficiencia con la que una empresa utiliza sus activos para generar ganancias.",
        f"ROA: {df_filtered['Utilidad Neta'].iloc[-1] / df_filtered['Activos Promedio'].iloc[-1]:.2%}",
        'Periodo',
        'Utilidad Neta / Activos Promedio',
        customdata=['Utilidad Neta', 'Activos Promedio'],
    )
    # Continuar con más fórmulas de rentabilidad si es necesario
elif selected_functionality == "Eficiencia Operativa":
    st.subheader("Fórmulas de Eficiencia Operativa")
    mostrar_indicador_financiero(
        "Grado de Absorción",
        "Grado Absorción = Gastos de Operación / Margen Operativo",
        "Indica qué proporción del margen operativo se consume en gastos operativos. Un valor más bajo sugiere una mejor eficiencia operativa.",
        f"Grado de Absorción: {df['Gastos de Operación'].iloc[-1] / df['Margen Operativo'].iloc[-1]:.2%}",
        df['Periodo'],
        df['Gastos de Operación'] / df['Margen Operativo'],
        customdata=[[gastos, margen] for gastos, margen in zip(df['Gastos de Operación'], df['Margen Operativo'])],
        color='blue'
    )
    
    mostrar_indicador_financiero(
        "Eficiencia Operativa",
        "Eficiencia Operativa = Gasto Operativo / Ingresos Operativos",
        "Calcula qué porcentaje de los ingresos operativos se utiliza para cubrir los gastos operativos. Un valor más bajo es preferible.",
        f"Eficiencia Operativa: {df['Gasto Operativo'].iloc[-1] / df['Ingresos Operativos'].iloc[-1]:.2%}",
        df['Periodo'],
        df['Gasto Operativo'] / df['Ingresos Operativos'],
        customdata=[[gasto, ingresos] for gasto, ingresos in zip(df['Gasto Operativo'], df['Ingresos Operativos'])],
        color='green'
    )
    # Continuar con más fórmulas de eficiencia operativa si es necesario
elif selected_functionality == "Gasto":
    st.subheader("Fórmulas de Gasto")
    mostrar_indicador_financiero(
        "Gasto Personal",
        "Gasto de Personal / Ingresos = (Gasto de Personal / Ingresos Totales)",
        "Mide qué porcentaje de los ingresos totales se destina a gastos de personal. Un valor más bajo indica una mayor eficiencia en la gestión de los costos de personal.",
        f"Gasto Personal / Ingresos: {df['Gasto de Personal'].iloc[-1] / df['Ingresos Totales'].iloc[-1]:.2%}",
        df['Periodo'],
        df['Gasto de Personal'] / df['Ingresos Totales'],
        customdata=[[gasto, ingresos] for gasto, ingresos in zip(df['Gasto de Personal'], df['Ingresos Totales'])],
        color='green'
    )
    # Continuar con más fórmulas de gasto si es necesario
elif selected_functionality == "Calidad de Cartera":
    st.subheader("Fórmulas de Calidad de Cartera")
    mostrar_indicador_financiero(
        "Morosidad de Cartera Total",
        "Tasa de Morosidad = (Préstamos Morosos / Préstamos Totales)",
        "Mide el porcentaje de la cartera de préstamos que está en mora. Una tasa más baja indica una mejor calidad de la cartera de créditos.",
        f"Tasa de Morosidad: {df['Préstamos Morosos'].iloc[-1] / df['Préstamos Totales'].iloc[-1]:.2%}",
        df['Periodo'],
        df['Préstamos Morosos'] / df['Préstamos Totales'],
        customdata=[[morosos, totales] for morosos, totales in zip(df['Préstamos Morosos'], df['Préstamos Totales'])],
        color='orange'
    )
    # Continuar con más fórmulas de calidad de cartera si es necesario
elif selected_functionality == "Otros Indicadores":
    st.subheader("Otras Fórmulas")
    mostrar_indicador_financiero(
        "Crecimiento de Cartera",
        "Crecimiento de Cartera = ((Cartera Actual - Cartera Anterior) / Cartera Anterior) * 100",
        "Mide el porcentaje de crecimiento de la cartera de préstamos de un período a otro. Un crecimiento positivo indica expansión.",
        f"Crecimiento de Cartera: {((df['Cartera Actual'].iloc[-1] - df['Cartera Anterior'].iloc[-1]) / df['Cartera Anterior'].iloc[-1]) * 100:.2f}%",
        df['Periodo'],
        ((df['Cartera Actual'] - df['Cartera Anterior']) / df['Cartera Anterior']) * 100,
        customdata=[[actual, anterior] for actual, anterior in zip(df['Cartera Actual'], df['Cartera Anterior'])],
        color='purple'
    )

    mostrar_indicador_financiero(
        "Productividad por Empleado",
        "Productividad por Empleado = Ingresos Totales / Número de Empleados",
        "Muestra cuánto ingreso genera cada empleado. Mayor productividad por empleado es indicativa de una fuerza laboral más eficiente.",
        f"Productividad por Empleado: {df['Ingresos Totales'].iloc[-1] / df['Número de Empleados'].iloc[-1]:,.2f}",
        df['Periodo'],
        df['Ingresos Totales'] / df['Número de Empleados'],
        customdata=[[ingresos, empleados] for ingresos, empleados in zip(df['Ingresos Totales'], df['Número de Empleados'])],
        color='brown'
    )

    mostrar_indicador_financiero(
        "Crecimiento de Depósitos",
        "Crecimiento de Depósitos = ((Depósitos Actuales - Depósitos Anteriores) / Depósitos Anteriores) * 100",
        "Mide el porcentaje de cambio en el total de depósitos de un período a otro, indicando la capacidad de la cooperativa para atraer y retener depósitos.",
        f"Crecimiento de Depósitos: {((df['Depósitos Actuales'].iloc[-1] - df['Depósitos Anteriores'].iloc[-1]) / df['Depósitos Anteriores'].iloc[-1]) * 100:.2f}%",
        df['Periodo'],
        ((df['Depósitos Actuales'] - df['Depósitos Anteriores']) / df['Depósitos Anteriores']) * 100,
        customdata=[[actuales, anteriores] for actuales, anteriores in zip(df['Depósitos Actuales'], df['Depósitos Anteriores'])],
        color='pink'
    )

    mostrar_indicador_financiero(
        "Liquidez",
        "Liquidez = Activos Líquidos / Pasivos de Corto Plazo",
        "Evalúa la capacidad de la cooperativa para cubrir sus obligaciones a corto plazo con activos líquidos. Una mayor liquidez es un signo de solidez financiera.",
        f"Liquidez: {df['Activos Líquidos'].iloc[-1] / df['Pasivos de Corto Plazo'].iloc[-1]:.2f}",
        df['Periodo'],
        df['Activos Líquidos'] / df['Pasivos de Corto Plazo'],
        customdata=[[liquidez, pasivos] for liquidez, pasivos in zip(df['Activos Líquidos'], df['Pasivos de Corto Plazo'])],
        color='gray'
    )

    mostrar_indicador_financiero(
        "Solvencia",
        "Solvencia = Patrimonio / Activos Totales",
        "Mide la proporción del patrimonio en relación con los activos totales, indicando el nivel de seguridad financiera y la capacidad para absorber pérdidas.",
        f"Solvencia: {df['Patrimonio'].iloc[-1] / df['Activos Totales'].iloc[-1]:.2%}",
        df['Periodo'],
        df['Patrimonio'] / df['Activos Totales'],
        customdata=[[patrimonio, activos] for patrimonio, activos in zip(df['Patrimonio'], df['Activos Totales'])],
        color='cyan'
    )
