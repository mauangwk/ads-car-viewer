import streamlit as st
import pandas as pd
import plotly.express as px


st.header(
    'This is a :blue[vehicle ad viewer] :sunglasses:', divider='rainbow'
)

car_data = pd.read_csv('vehicles_us.csv')  # leer los datos

# se crearán casillas de verificacion para seleccionar el tipo de grafico
build_histogram = st.checkbox(
    'Include General Odometer Histogram')
build_dispersion = st.checkbox(
    'Include General Odometer and price relation')

options = []
for i in range(13):
    options.append((i+1)*1000)

ad_count = st.select_slider(
    "Select minimum ads that manufactures must have to be shown",
    options=options, value=1000)


# Obteniendo las manufacturas con menos de 1000 ads
manufacture_resume = car_data["manufacture"].value_counts().reset_index()
manufacture_resume = manufacture_resume[manufacture_resume["count"] < ad_count]

# Filtrando a partir del subconjunto de manufacturas
manufacture_resume = car_data.query(
    "manufacture in @manufacture_resume.manufacture")[[
        "manufacture", "model", "model_year", "price", "condition",
        "cylinders", "fuel", "odometer", "transmission", "type", "paint_color",
        "date_posted", "days_listed"]
]


st.write(
    "Car manufacture data that have less than", ad_count, "ads")

st.dataframe(manufacture_resume,
             column_config={
                 "manufacture": "Manufacture",
                 "model": "Model",
                 "model_year": "Year",
                 "price": "Price",
                 "condition": "Condition",
                 "cylinders": "Cylinders",
                 "fuel": "Fuel",
                 "odometer": "Odometer",
                 "transmission": "Transmission",
                 "type": "Type",
                 "paint_color": "Color",
                 "date_posted": "Posted",
                 "days_listed": "Days Listed"
             },
             hide_index=True
             )

manufacture_year = manufacture_resume.groupby(["manufacture", "model_year"])[
    "model"].count().reset_index()
manufacture_year.rename(
    columns={"model": "count", "model_year": "year"}, inplace=True)

fig = px.bar(manufacture_year, x="year", y="count", color="manufacture")
st.plotly_chart(fig, use_container_width=True)

manufacture_type = manufacture_resume.groupby(["manufacture", "type"])[
    "model"].count().reset_index()
manufacture_type.rename(
    columns={"model": "count"}, inplace=True)

fig = px.bar(data_frame=manufacture_type,
             x="manufacture", y="count", color="type")

st.plotly_chart(fig, use_container_width=True)

year_condition = manufacture_resume.groupby(["model_year", "condition"])[
    "model"].count().reset_index()
year_condition.rename(
    columns={"model": "count", "model_year": "year"}, inplace=True
)

fig = px.histogram(data_frame=year_condition,
                   x="year", y="count", color="condition")

st.plotly_chart(fig, use_container_width=True)


if build_histogram:  # si la casilla de verificación está seleccionada
    # escribir un mensaje
    st.write(
        'Odometer Histogram from car ads data')

    # crear un histograma
    fig = px.histogram(car_data, x="odometer")

    # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig, use_container_width=True)

if build_dispersion:  # si la casilla de verificación está seleccionada
    # escribir un mensaje
    st.write(
        'Dispersion and price relation from the car ads data')

    # crear un histograma
    # crear un gráfico de dispersión
    fig = px.scatter(car_data,
                     x="odometer",
                     y="price"
                     )

    # mostrar un gráfico Plotly interactivo
    st.plotly_chart(fig, use_container_width=True)
