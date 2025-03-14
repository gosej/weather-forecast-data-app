import streamlit as st
import plotly.express as px
from backend import get_data

# Add UI elements
st.title("Weather Forecast")
place = st.text_input("Place: ")
days = st.slider("Forcast Days", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))

st.subheader(f"{option} for the next {days} day(s) in {place}")

# test data used for GUI testing. Will delete after backend completion
# def get_data(days):
#     #temp data will get from weather data later
#     dates = ["2022-25-10", "2022-26-10", "2022-27-10"]
#     temperatures = [10,11,15]
#     temperatures = [days * i for i in temperatures]
#     return dates, temperatures
# data = get_data(place, days, option)


if place:
    # get temp or sky data
    try:
        filtered_data = get_data(place, days)
        if option == "Temperature":
            #plot temp data
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperatures (F)"})
            st.plotly_chart(figure)

        if option == "Sky":
            sky_images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                          "Rain": "images/rain.png", "Snow": "images/snow.png"}
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            image_paths = ([sky_images[condition] for condition in sky_conditions])
            st.image(image_paths, width=115)

            # st.image([sky_images[condition] for condition in sky_conditions])
            # same as above
            # for condition in sky_conditions:
            #     st.image(sky_images[condition])
    except KeyError:
        st.write(f"We have no data on the city '{place}'")

