import streamlit as st
import pandas as pd
import plotly.express as px


# Título principal
st.set_page_config(page_title="Dashboard Ventas - Tiendas de Conveniencia", layout="wide")
st.title("Análisis de Ventas de una Cadena de Tiendas de Conveniencia")
st.markdown("""
Este dashboard permite explorar el desempeño comercial de una **cadena de tiendas de conveniencia**. 
Analiza datos clave por tienda, línea de producto y preferencias de clientes.
""")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv", parse_dates=["Date"])
    return df

df = load_data()

# Filtros generales en el sidebar
st.sidebar.header("Filtros Generales")
branches = st.sidebar.multiselect("Sucursal", df["Branch"].unique(), default=df["Branch"].unique())
date_range = st.sidebar.date_input("Rango de Fechas", [df["Date"].min(), df["Date"].max()])

# Filtrado base
filtered_df = df[
    (df["Branch"].isin(branches)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# 1. Evolución diaria de ventas

st.header("Evolución Diaria de Ventas Totales")
with st.expander("Filtrar por línea de producto"):
    selected_lines_1 = st.multiselect(
        "Selecciona líneas de producto",
        df["Product line"].unique(),
        default=df["Product line"].unique()
    )

ventas_diarias = filtered_df[filtered_df["Product line"].isin(selected_lines_1)]
ventas_diarias = ventas_diarias.groupby("Date")["Total"].sum().reset_index()
fig1 = px.line(ventas_diarias, x="Date", y="Total", title="Ventas Diarias Totales")
st.plotly_chart(fig1, use_container_width=True)



# 2. Ingreso Total por Línea de Producto

st.header("Ingreso Total por Línea de Producto")
with st.expander("Filtrar por sucursal específica"):
    branch_linea = st.selectbox("Selecciona una sucursal", df["Branch"].unique())

df_linea = filtered_df[filtered_df["Branch"] == branch_linea]
linea_grouped = df_linea.groupby("Product line")["Total"].sum().sort_values()
fig2 = px.bar(
    linea_grouped,
    x=linea_grouped.values,
    y=linea_grouped.index,
    orientation="h",
    title=f"Ingreso por Línea de Producto - Sucursal {branch_linea}",
    labels={"x": "Ingresos", "y": "Línea"}
)
st.plotly_chart(fig2, use_container_width=True)



# 3. Métodos de Pago más Utilizados

st.header("Preferencias de Pago del Cliente")
with st.expander("Filtrar por línea de producto"):
    selected_lines_3 = st.multiselect(
        "Selecciona líneas de producto (para ver preferencias de pago)",
        df["Product line"].unique(),
        default=df["Product line"].unique()
    )

df_payment = filtered_df[filtered_df["Product line"].isin(selected_lines_3)]
payment_counts = df_payment["Payment"].value_counts().reset_index()
payment_counts.columns = ["Método de Pago", "Cantidad"]
fig3 = px.pie(
    payment_counts,
    names="Método de Pago",
    values="Cantidad",
    title="Distribución de Métodos de Pago por Línea"
)
st.plotly_chart(fig3, use_container_width=True)



# 4. Ingreso Bruto por Línea de Producto y Sucursal

st.header("Ingreso Bruto por Línea y Sucursal")
with st.expander("Filtrar por método de pago"):
    payment_method = st.selectbox("Selecciona un método de pago", df["Payment"].unique())

df_income = filtered_df[filtered_df["Payment"] == payment_method]
income_grouped = df_income.groupby(["Branch", "Product line"])["gross income"].sum().reset_index()

fig4 = px.bar(
    income_grouped,
    x="Product line",
    y="gross income",
    color="Branch",
    barmode="stack",
    title=f"Ingreso Bruto por Línea y Sucursal (Pago: {payment_method})",
    labels={"gross income": "Ingreso Bruto", "Product line": "Línea de Producto"}
)
st.plotly_chart(fig4, use_container_width=True)
