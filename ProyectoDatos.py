import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

dfROA = pd.read_csv("formulascsvFINAL1.csv")

st.sidebar.image("https://th.bing.com/th/id/R.f0a68a9aec5f8116cb07438f2940e77e?rik=Rxot3C3ezKqjEg&pid=ImgRaw&r=0")
st.markdown("""
    ## VISUALIZADOR DE INDICADORES FINANCIEROS 
    
    #### El objetivo de este visualizador es facilitar la interpretación y análisis de indicadores financieros, permitiendo a los usuarios interactuar con las graficas.
    """)
def mostrar_indicador_financiero(titulo, formula, descripcion):
    st.header(titulo)

    col1, col2, col3 = st.columns(3)

    col1.subheader("Fórmula:")
    col1.write(formula)

    col2.subheader("Descripción:")
    col2.write(descripcion)

# Menú desplegable para agrupar las fórmulas
selected_group = st.sidebar.selectbox("Selecciona categoría", ["Indicadores financieros", "Indicadores de prueba"])

# Mostrar el menú de selección de fórmulas solo cuando se selecciona el grupo "Indicadores financieros"
if selected_group == "Indicadores financieros":
    # Menú de selección entre las fórmulas
    selected_formula = st.sidebar.selectbox("Selecciona una fórmula", [
        "ROA",
        "Gasto Operativo",
        "Solvencia Patrimonial"
    ])
    st.sidebar.markdown("""
    ---

    ### Autores
    - David Pardo
    - Jose Criollo
    - Rosa Palacios
    - Carlos Sarmiento

    @utpl
    """)
# Mostrar la fórmula seleccionada
    if selected_formula == "ROA":
        mostrar_indicador_financiero(
            "Rentabilidad sobre el activo (ROA)",
            "ROA = Utilidad Neta / Activos Totales Promedio",
            "Esta fórmula mide la eficiencia con la que una empresa utiliza sus activos para generar ganancias."
        )

        # Calcular ROA por trimestre
        dfROA['SALDO'] = pd.to_numeric(dfROA['SALDO'].replace('[\$,]', '', regex=True), errors='coerce')
        dfROA['FECHA'] = pd.to_datetime(dfROA['FECHA'], format='%m/%d/%Y')
        dfROA['AÑO'] = dfROA['FECHA'].dt.year
        dfROA['ROA'] = dfROA.groupby('AÑO')['SALDO'].pct_change(4) * 100

        # Crear un gráfico interactivo con una línea por cada año para ROA
        fig_roa = make_subplots(rows=1, cols=1, shared_xaxes=True)

        # Filtrar solo los datos que tienen ROA (descartando NaN)
        df_filtered_roa = dfROA.dropna(subset=['ROA'])

        for year in df_filtered_roa['AÑO'].unique():
            data_year = df_filtered_roa[df_filtered_roa['AÑO'] == year]
            fig_roa.add_trace(go.Scatter(x=data_year['FECHA'], y=data_year['ROA'], mode='lines+markers', name=f'ROA - {year}'))

        # Actualizar diseño del gráfico ROA
        fig_roa.update_layout(title='ROA por Trimestre',
                            xaxis_title='Fecha',
                            yaxis_title='ROA')

        st.subheader("Gráfico de ROA por Trimestre")
        st.plotly_chart(fig_roa)

        # Filtrar los datos para cada año
        df_2021 = dfROA[dfROA['FECHA'].dt.year == 2021]
        df_2022 = dfROA[dfROA['FECHA'].dt.year == 2022]
        df_2023 = dfROA[dfROA['FECHA'].dt.year == 2023]

        # Calcular el ROA para cada año
        roa_2021 = (df_2021[df_2021['TIPO'] == 5].groupby('FECHA')['SALDO'].sum() - df_2021[df_2021['TIPO'] == 4].groupby('FECHA')['SALDO'].sum()) / df_2021[df_2021['TIPO'] == 1].groupby('FECHA')['SALDO'].mean() * 100
        roa_2022 = (df_2022[df_2022['TIPO'] == 5].groupby('FECHA')['SALDO'].sum() - df_2022[df_2022['TIPO'] == 4].groupby('FECHA')['SALDO'].sum()) / df_2022[df_2022['TIPO'] == 1].groupby('FECHA')['SALDO'].mean() * 100
        roa_2023 = (df_2023[df_2023['TIPO'] == 5].groupby('FECHA')['SALDO'].sum() - df_2023[df_2023['TIPO'] == 4].groupby('FECHA')['SALDO'].sum()) / df_2023[df_2023['TIPO'] == 1].groupby('FECHA')['SALDO'].mean() * 100

        # Combinar los resultados en un solo DataFrame
        df_combined = pd.DataFrame({'2021': roa_2021, '2022': roa_2022, '2023': roa_2023})

        # Resetear el índice para evitar problemas
        df_combined = df_combined.reset_index()

        # Crear el gráfico con las líneas superpuestas
        fig = px.line(df_combined, x='FECHA', y=['2021', '2022', '2023'], title='ROA over Time', labels={'value': 'ROA (%)'})
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='ROA (%)')

        st.subheader("ROA a lo largo del tiempo")
        st.plotly_chart(fig)
    elif selected_formula == "Gasto Operativo":
        mostrar_indicador_financiero(
            "Eficiencia en Gasto Operativo",
            "Eficiencia en Gasto Operativo = (Ingresos - Gastos Operativos) / Ingresos",
            "Evalúa qué tan eficientemente una empresa está administrando sus gastos operativos en relación con sus ingresos. Un valor más alto indica mayor eficiencia."
        )

        # Convertir la columna 'SALDO' a tipo numérico
        dfROA['SALDO'] = pd.to_numeric(dfROA['SALDO'].replace('[\$,]', '', regex=True), errors='coerce')

        # Convertir la columna 'FECHA' a tipo datetime
        dfROA['FECHA'] = pd.to_datetime(dfROA['FECHA'], format='%m/%d/%Y')

        # Crear una nueva columna para el año
        dfROA['AÑO'] = dfROA['FECHA'].dt.year

        # Calcular Gasto Operativo por trimestre
        dfROA['GASTO_OPERATIVO'] = dfROA[dfROA['NombreCuenta'] == 'GASTOS DE OPERACION'].groupby('AÑO')['SALDO'].pct_change(4) * 100

        # Crear un gráfico interactivo con una línea por cada año para Gasto Operativo
        fig_gasto_operativo = make_subplots(rows=1, cols=1, shared_xaxes=True)

        # Filtrar solo los datos que tienen Gasto Operativo (descartando NaN)
        df_filtered_gasto_operativo = dfROA.dropna(subset=['GASTO_OPERATIVO'])

        for year in df_filtered_gasto_operativo['AÑO'].unique():
            data_year = df_filtered_gasto_operativo[df_filtered_gasto_operativo['AÑO'] == year]
            fig_gasto_operativo.add_trace(go.Scatter(x=data_year['FECHA'], y=data_year['GASTO_OPERATIVO'], mode='lines+markers', name=f'Gasto Operativo - {year}'))

        # Actualizar diseño del gráfico Gasto Operativo
        fig_gasto_operativo.update_layout(title='Gasto Operativo por Trimestre',
                                        xaxis_title='Fecha',
                                        yaxis_title='Gasto Operativo')
        st.subheader("Gráfico de Gasto Operativo por Trimestre")
        st.plotly_chart(fig_gasto_operativo)

        gastos_operativos_categoria = dfROA[dfROA['NombreCuenta'] == 'GASTOS DE OPERACION']
        fig_gastos_operativos_categoria = px.bar(gastos_operativos_categoria, x='FECHA', y='SALDO',
                                                labels={'SALDO': 'Gasto Operativo'},
                                                title='Desglose del Gasto Operativo a lo largo del tiempo')
        fig_gastos_operativos_categoria.update_xaxes(title_text='Fecha')
        fig_gastos_operativos_categoria.update_yaxes(title_text='Gasto Operativo')

        # Mostrar el gráfico
        st.subheader("Gráfico de barras de Gasto Operativo")
        st.plotly_chart(fig_gastos_operativos_categoria)

    elif selected_formula == "Solvencia Patrimonial":
        mostrar_indicador_financiero(
            "Solvencia Patrimonial",
            "Solvencia = Patrimonio / Activos Totales",
            "Mide la proporción del patrimonio en relación con los activos totales, indicando el nivel de seguridad financiera y la capacidad para absorber pérdidas."
        )

        # Convertir la columna 'SALDO' a tipo numérico
        dfROA['SALDO'] = pd.to_numeric(dfROA['SALDO'].replace('[\$,]', '', regex=True), errors='coerce')

        # Convertir la columna 'FECHA' a tipo datetime
        dfROA['FECHA'] = pd.to_datetime(dfROA['FECHA'], format='%m/%d/%Y')

        # Crear una nueva columna para el año
        dfROA['AÑO'] = dfROA['FECHA'].dt.year

        # Calcular Solvencia Patrimonial
        df_solvencia = dfROA.pivot(index='FECHA', columns='NombreCuenta', values='SALDO').reset_index()
        df_solvencia['SOLVENCIA_PATRIMONIAL'] = df_solvencia['PATRIMONIO'] / df_solvencia['ACTIVO'] * 100

        # Crear un gráfico interactivo
        fig_solvencia = make_subplots(rows=1, cols=1, shared_xaxes=True)

        # Añadir la línea de Solvencia Patrimonial al gráfico
        fig_solvencia.add_trace(go.Scatter(x=df_solvencia['FECHA'], y=df_solvencia['SOLVENCIA_PATRIMONIAL'], mode='lines+markers', name='Solvencia Patrimonial'))

        # Actualizar diseño del gráfico
        fig_solvencia.update_layout(title='Solvencia Patrimonial',
                                    xaxis_title='Fecha',
                                    yaxis_title='Solvencia Patrimonial (%)')

        # Mostrar el gráfico
        st.subheader("Gráfico de Solvencia Patrimonial")
        st.plotly_chart(fig_solvencia)
        solvencia = dfROA[dfROA['TIPO'].isin([1, 3])] 
        solvencia['SOLVENCIA_PATRIMONIAL'] = solvencia.groupby(['FECHA', 'NombreCuenta'])['SALDO'].transform('sum')
        fig_solvencia = px.line(solvencia, x='FECHA', y='SOLVENCIA_PATRIMONIAL', color='NombreCuenta',
                                labels={'SOLVENCIA_PATRIMONIAL': 'Solvencia Patrimonial', 'NombreCuenta': 'Cuenta'},
                                title='Solvencia Patrimonial a lo largo del tiempo')
        fig_solvencia.update_xaxes(title_text='Fecha')
        fig_solvencia.update_yaxes(title_text='Monto')
        st.subheader("Gráfico comparativa de activo y patrimonio de Solvencia Patrimonial")
        st.plotly_chart(fig_solvencia)
elif selected_group == "Indicadores de prueba":
    st.header("Fórmulas de prueba para el grupo Indicadores de prueba")

    # Menú de selección para el grupo "Indicadores de prueba"
    selected_formula_group2 = st.sidebar.selectbox("Selecciona una fórmula", [
        "Fórmula de Prueba 1",
        "Fórmula de Prueba 2"
    ])

    # Mostrar la fórmula seleccionada para el grupo "Indicadores de prueba"
    if selected_formula_group2 == "Fórmula de Prueba 1":
        st.subheader("Fórmula de Prueba 1")
        st.write("Esta es una fórmula de prueba para el grupo Indicadores de prueba.")

        # Gráfico de prueba
        data = {'X': np.arange(10), 'Y': np.random.rand(10)}
        df_test = pd.DataFrame(data)
        fig_test = px.scatter(df_test, x='X', y='Y', title='Gráfico de prueba para Fórmula de Prueba 1')
        st.plotly_chart(fig_test)

    elif selected_formula_group2 == "Fórmula de Prueba 2":
        st.subheader("Fórmula de Prueba 2")
        st.write("Otra fórmula de prueba para el grupo Indicadores de prueba.")

        # Otro gráfico de prueba
        data = {'X': np.arange(10), 'Y': np.random.rand(10)}
        df_test = pd.DataFrame(data)
        fig_test = px.line(df_test, x='X', y='Y', title='Gráfico de prueba para Fórmula de Prueba 2')
        st.plotly_chart(fig_test)

