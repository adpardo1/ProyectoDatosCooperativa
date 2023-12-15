import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# Leer el dataset
df = pd.read_csv('datos_financieros1.csv')
df2 = pd.read_csv('dataset_generado.csv')

# Obtener los años disponibles en el dataset
anios_disponibles = df['Año'].unique()

# Menú de selección de año
selected_year = st.sidebar.selectbox("Selecciona un año", anios_disponibles)

# Filtrar el DataFrame por el año seleccionado
df_filtered = df[df['Año'] == selected_year]

# Función para mostrar cada indicador financiero
def mostrar_indicador_financiero(titulo, formula, descripcion, resultado, x, y, customdata, color=None, tipo_grafico='lines+markers'):
    st.header(titulo)

    col1, col2, col3 = st.columns(3)

    col1.subheader("Fórmula:")
    col1.write(formula)

    col2.subheader("Descripción:")
    col2.write(descripcion)

    col3.subheader("Resultado:")
    col3.write(resultado)

    if tipo_grafico == 'lines+markers':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            hovertemplate=customdata,
            customdata=customdata,
            mode=tipo_grafico,
            line=dict(color=color),
        ))
    elif tipo_grafico == 'bar':
        fig = px.bar(x=x, y=y, hover_data={'customdata': customdata}, labels={'y': titulo})
    elif tipo_grafico == 'bar_with_error':
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x,
            y=y,
            hovertemplate=customdata,
            customdata=customdata,
            marker_color=color,
            error_y=dict(
                type='data',
                array=[0.1] * len(y),  # Puedes ajustar el valor del error según tus necesidades
                visible=True
            )
        ))
    elif tipo_grafico == 'dotplot':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            hovertemplate=customdata,
            customdata=customdata,
            mode='markers',
            marker=dict(color=color, size=10),
        ))

    if fig:  # Asegurarse de que fig no sea None antes de intentar actualizar el diseño
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
    # Filtrar el DataFrame df2 por el año seleccionado
    df2_filtered = df2[df2['anio'] == selected_year]
    
    # Calcular ROA
    df2_filtered['ROA'] = df2_filtered['Ingresos Totales'] / ((df2_filtered['Activos Inicio Ano'] + df2_filtered['Activos Fin Ano']) / 2)
    
    # Preparar datos para el gráfico
    melted_df = pd.melt(df2_filtered, id_vars=['periodo', 'Tipo'], value_vars=['Ingresos Totales', 'Gastos Totales', 'ROA'])

    # Crear un gráfico de barras agrupadas por periodo y tipo de transacción
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='periodo', y='value', hue='Tipo', data=melted_df, ci=None, palette="viridis", ax=ax)

    # Agregar una línea para el ROA
    sns.lineplot(x='periodo', y='ROA', data=df2_filtered, label='ROA', color='black', marker='o', ax=ax)

    # Configurar el gráfico
    plt.title(f'Rentabilidad en {selected_year}')
    plt.xlabel('Periodo')
    plt.ylabel('Monto')
    plt.legend(title='Tipo de Transacción')

    # Mostrar gráfico
    st.pyplot(fig)
   # Filtrar el DataFrame df2 por el año seleccionado
    df2_filtered = df2[df2['anio'] == selected_year]
    
    # Ajustar el cálculo de ROA para evitar divisiones por 0
    df2_filtered['ROA'] = df2_filtered['Ingresos Totales'] / np.maximum(1, ((df2_filtered['Activos Inicio Ano'] + df2_filtered['Activos Fin Ano']) / 2))

    # Crear un gráfico de barras apiladas con etiquetas
    fig, ax = plt.subplots(figsize=(12, 8))

    bar_width = 0.8
    index = range(len(df2_filtered['periodo']))

    # Barras apiladas para Ingresos Totales y Gastos Totales
    plt.bar(index, df2_filtered['Ingresos Totales'], bar_width, label='Ingresos Totales', color='green')
    plt.bar(index, df2_filtered['Gastos Totales'], bar_width, label='Gastos Totales', color='red', bottom=df2_filtered['Ingresos Totales'])

    # Línea adicional para el ROA
    ax.plot(index, df2_filtered['ROA'], marker='o', color='blue', label='ROA')

    plt.xlabel('Periodo')
    plt.ylabel('Monto')
    plt.title(f'Rentabilidad en {selected_year}')
    plt.legend()
    #---------------------------------------------------------
    df2["ROA"] = df2["Ingresos Totales"] / ((df2["Activos Inicio Ano"] + df2["Activos Fin Ano"]) / 2)
    fig = px.scatter(
        df2,
        x="periodo",  
        y="ROA",
        color="Tipo",
        size="ROA",  
        animation_frame="anio",
        range_y=[0, df2["ROA"].max() + 0.1],  
        labels={"ROA": "ROA", "periodo": "Periodo", "anio": "Año"},
        title="ROA por tipo a lo largo de los periodos",
    )
    st.plotly_chart(fig)
    
    #-------------------------------------------------------
    df2['ROA'] = df2['Ingresos Totales'] / ((df2['Activos Inicio Ano'] + df2['Activos Fin Ano']) / 2)

    # Convertir 'anio' y 'periodo' a un formato de fecha
    df2['Fecha'] = pd.to_datetime(df2['anio'].astype(str) + '-' + df2['periodo'], format='%Y-Q%m')

    # Menú de selección de años
    anios_seleccionados = st.slider("Selecciona un rango de años", min_value=df2["anio"].min(), max_value=df2["anio"].max(), value=(df2["anio"].min(), df2["anio"].max()))

    # Filtrar el DataFrame por el rango de años seleccionado
    df2_filtrado = df2[(df2["anio"] >= anios_seleccionados[0]) & (df2["anio"] <= anios_seleccionados[1])]

    # Crear un gráfico interactivo de puntos con selección de componentes y rango de tiempo
    fig_roa_tipo = px.scatter(df2_filtrado, x='Fecha', y='ROA', color='Tipo', labels={'ROA': 'ROA por Tipo'})
    fig_roa_tipo.update_layout(title=f'ROA por Tipo en el Rango de Años Seleccionado')

    # Mostrar la barra de rango de años debajo de la gráfica
    st.plotly_chart(fig_roa_tipo)

    #--------------------------------------------------------------
    
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

    # Calcular Eficiencia en Gasto Operativo
    eficiencia_gasto_operativo = (df_filtered['Ingresos Totales'] - df_filtered['Gasto Operativo']) / df_filtered['Ingresos Totales']

    # Mostrar indicador financiero
    mostrar_indicador_financiero(
        "Eficiencia en Gasto Operativo",
        "Eficiencia en Gasto Operativo = (Ingresos Totales - Gasto Operativo) / Ingresos Totales",
        "Evalúa qué tan eficientemente una empresa está administrando sus gastos operativos en relación con sus ingresos. Un valor más alto indica mayor eficiencia.",
        f"Eficiencia en Gasto Operativo: {eficiencia_gasto_operativo.iloc[-1]:.2%}",
        df_filtered['Periodo'],
        eficiencia_gasto_operativo,
        customdata=[[ingresos, gasto] for ingresos, gasto in zip(df_filtered['Ingresos Totales'], df_filtered['Gasto Operativo'])],
        color='green'  # Puedes personalizar el color si lo deseas
    )

elif selected_functionality == "Eficiencia Operativa":
    st.subheader("Fórmulas de Eficiencia Operativa")
    mostrar_indicador_financiero(
        "Grado de Absorción",
        "Grado Absorción = Gastos de Operación / Margen Operativo",
        "Indica qué proporción del margen operativo se consume en gastos operativos. Un valor más bajo sugiere una mejor eficiencia operativa.",
        f"Grado de Absorción: {df_filtered['Gastos de Operación'].iloc[-1] / df_filtered['Margen Operativo'].iloc[-1]:.2%}",
        df_filtered['Periodo'],
        df_filtered['Gastos de Operación'] / df_filtered['Margen Operativo'],
        customdata=[[gastos, margen] for gastos, margen in zip(df_filtered['Gastos de Operación'], df_filtered['Margen Operativo'])],
        color='blue',
        tipo_grafico='bar'
    )

    
    mostrar_indicador_financiero(
        "Eficiencia Operativa",
        "Eficiencia Operativa = Gasto Operativo / Ingresos Operativos",
        "Calcula qué porcentaje de los ingresos operativos se utiliza para cubrir los gastos operativos. Un valor más bajo es preferible.",
        f"Eficiencia Operativa: {df['Gasto Operativo'].iloc[-1] / df['Ingresos Operativos'].iloc[-1]:.2%}",
        df['Periodo'],
        df['Gasto Operativo'] / df['Ingresos Operativos'],
        customdata=[[gasto, ingresos] for gasto, ingresos in zip(df['Gasto Operativo'], df['Ingresos Operativos'])],
        color='green',
        tipo_grafico='bar_with_error'
    )
    # Continuar con más fórmulas de eficiencia operativa si es necesario
elif selected_functionality == "Gasto":
    st.subheader("Fórmulas de Gasto")

    mostrar_indicador_financiero(
        "Gasto Personal",
        "Gasto de Personal / Ingresos = (Gasto de Personal / Ingresos Totales)",
        "Mide qué porcentaje de los ingresos totales se destina a gastos de personal. Un valor más bajo indica una mayor eficiencia en la gestión de los costos de personal.",
        f"Gasto Personal: {df_filtered['Gasto de Personal'].iloc[-1] / df_filtered['Ingresos Totales'].iloc[-1]:.2%}",
        df_filtered['Periodo'],
        df_filtered['Gasto de Personal'] / df_filtered['Ingresos Totales'],
        customdata=[[gasto, ingresos] for gasto, ingresos in zip(df_filtered['Gasto de Personal'], df_filtered['Ingresos Totales'])],
        color='green',
        tipo_grafico='bar'
    )
elif selected_functionality == "Calidad de Cartera":
    st.subheader("Fórmulas de Calidad de Cartera")

    mostrar_indicador_financiero(
        "Morosidad de Cartera Total",
        "Tasa de Morosidad = (Préstamos Morosos / Préstamos Totales)",
        "Mide el porcentaje de la cartera de préstamos que está en mora. Una tasa más baja indica una mejor calidad de la cartera de créditos.",
        f"Tasa de Morosidad: {df_filtered['Préstamos Morosos'].iloc[-1] / df_filtered['Préstamos Totales'].iloc[-1]:.2%}",
        df_filtered['Periodo'],
        df_filtered['Préstamos Morosos'] / df_filtered['Préstamos Totales'],
        customdata=[[morosos, totales] for morosos, totales in zip(df_filtered['Préstamos Morosos'], df_filtered['Préstamos Totales'])],
        color='orange',
        tipo_grafico='dotplot'
    )
    # Continuar con más fórmulas de calidad de cartera si es necesario
elif selected_functionality == "Otros Indicadores":
    st.subheader("Otras Fórmulas")

    mostrar_indicador_financiero(
        "Crecimiento de Cartera",
        "Crecimiento de Cartera = ((Cartera Actual - Cartera Anterior) / Cartera Anterior) * 100",
        "Mide el porcentaje de crecimiento de la cartera de préstamos de un período a otro. Un crecimiento positivo indica expansión.",
        f"Crecimiento de Cartera: {((df_filtered['Cartera Actual'].iloc[-1] - df_filtered['Cartera Anterior'].iloc[-1]) / df_filtered['Cartera Anterior'].iloc[-1]) * 100:.2f}%",
        df_filtered['Periodo'],
        ((df_filtered['Cartera Actual'] - df_filtered['Cartera Anterior']) / df_filtered['Cartera Anterior']) * 100,
        customdata=[[actual, anterior] for actual, anterior in zip(df_filtered['Cartera Actual'], df_filtered['Cartera Anterior'])],
        color='purple'
    )

    mostrar_indicador_financiero(
        "Productividad por Empleado",
        "Productividad por Empleado = Ingresos Totales / Número de Empleados",
        "Muestra cuánto ingreso genera cada empleado. Mayor productividad por empleado es indicativa de una fuerza laboral más eficiente.",
        f"Productividad por Empleado: {df_filtered['Ingresos Totales'].iloc[-1] / df_filtered['Número de Empleados'].iloc[-1]:,.2f}",
        df_filtered['Periodo'],
        df_filtered['Ingresos Totales'] / df_filtered['Número de Empleados'],
        customdata=[[ingresos, empleados] for ingresos, empleados in zip(df_filtered['Ingresos Totales'], df_filtered['Número de Empleados'])],
        color='brown'
    )

    # Agregamos la nueva fórmula como gráfico de líneas
    mostrar_indicador_financiero(
        "Crecimiento de Depósitos",
        "Crecimiento de Depósitos = ((Depósitos Actuales - Depósitos Anteriores) / Depósitos Anteriores) * 100",
        "Mide el porcentaje de cambio en el total de depósitos de un período a otro, indicando la capacidad de la cooperativa para atraer y retener depósitos.",
        f"Crecimiento de Depósitos: {((df_filtered['Depósitos Actuales'].iloc[-1] - df_filtered['Depósitos Anteriores'].iloc[-1]) / df_filtered['Depósitos Anteriores'].iloc[-1]) * 100:.2f}%",
        df_filtered['Periodo'],
        ((df_filtered['Depósitos Actuales'] - df_filtered['Depósitos Anteriores']) / df_filtered['Depósitos Anteriores']) * 100,
        customdata=[[actuales, anteriores] for actuales, anteriores in zip(df['Depósitos Actuales'], df_filtered['Depósitos Anteriores'])],
        color='pink',
        tipo_grafico='lines+markers'
    )

    # Agregamos otra nueva fórmula como gráfico de barras
    mostrar_indicador_financiero(
        "Liquidez",
        "Liquidez = Activos Líquidos / Pasivos de Corto Plazo",
        "Evalúa la capacidad de la cooperativa para cubrir sus obligaciones a corto plazo con activos líquidos. Una mayor liquidez es un signo de solidez financiera.",
        f"Liquidez: {df_filtered['Activos Líquidos'].iloc[-1] / df_filtered['Pasivos de Corto Plazo'].iloc[-1]:.2f}",
        df_filtered['Periodo'],
        df_filtered['Activos Líquidos'] / df_filtered['Pasivos de Corto Plazo'],
        customdata=[[liquidez, pasivos] for liquidez, pasivos in zip(df_filtered['Activos Líquidos'], df_filtered['Pasivos de Corto Plazo'])],
        color='gray',
        tipo_grafico='bar'
    )

    # Agregamos otra nueva fórmula como gráfico de puntos con barras de error
    mostrar_indicador_financiero(
        "Solvencia",
        "Solvencia = Patrimonio / Activos Totales",
        "Mide la proporción del patrimonio en relación con los activos totales, indicando el nivel de seguridad financiera y la capacidad para absorber pérdidas.",
        f"Solvencia: {df_filtered['Patrimonio'].iloc[-1] / df_filtered['Ingresos Totales'].iloc[-1]:.2%}",
        df_filtered['Periodo'],
        df_filtered['Patrimonio'] / df_filtered['Ingresos Totales'],
        customdata=[[patrimonio, activos] for patrimonio, activos in zip(df_filtered['Patrimonio'], df_filtered['Ingresos Totales'])],
        color='cyan',
        tipo_grafico='bar_with_error'
    )
