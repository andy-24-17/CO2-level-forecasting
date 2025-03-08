import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas.tseries.offsets import DateOffset
import warnings
warnings.filterwarnings("ignore") 

data2 = pd.read_excel('CO2 dataset.xlsx')

st.title("Forecast CO2 Levels For An Organization")
st.subheader("Welcome to the CO2 Forecasting App")
st.write("This app utilizes ARIMA modeling to forecast CO2 levels for an organization.")

st.sidebar.title("Input Data")
input_values = []
for i in range(10):
    year = st.sidebar.number_input(f'Year {i+1}', min_value=2015 + i, key=f'year_{i}', format='%d')
    co2 = st.sidebar.number_input(f'CO2 Value {i+1}', min_value=15.0, format="%.1f", step=0.1, key=f'co2_{i}')
    input_values.append((year, co2))

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

def toggle_button_state():
    st.session_state.button_clicked = not st.session_state.button_clicked

def reset_button_state():
    st.session_state.button_clicked = False

if st.sidebar.button("Convert to DataFrame"):
    toggle_button_state()

if st.session_state.button_clicked:
    input_values.sort()  
    appdata = pd.DataFrame(input_values, columns=['Year', 'CO2'])

    st.write("Data Preview:")
    st.write(appdata)

    st.sidebar.title("Forecast Settings")
    periods_input = st.sidebar.number_input('How many years forecast do you want?', min_value=5, max_value=365)

    if st.sidebar.button("Run Forecast"):
        if not appdata.empty:
            combined_data = pd.concat([data2.set_index('Year'), appdata.set_index('Year')], axis=0)
        else:
            combined_data = data2.set_index('Year')

        start_year = combined_data.index.max() + 1

        fm = ARIMA(combined_data['CO2'], order=(3, 1, 4))
        fm = fm.fit()

        forecast_values = fm.forecast(steps=periods_input)

        future_years = pd.date_range(start=str(start_year), periods=periods_input, freq='Y').year

        future = pd.DataFrame(index=future_years, columns=combined_data.columns)
        future['CO2'] = forecast_values.values  

        st.subheader("Forecasted CO2 Levels based on Input:")
        st.write(future)

        plt.figure(figsize=(20, 12))
        # plt.plot(combined_data.index, combined_data['CO2'], label='Historical Data')
        plt.plot(future.index, forecast_values, label='Forecasted Data')  
        plt.xlabel('Year')
        plt.ylabel('CO2 Levels')
        plt.title('CO2 Levels Forecast')
        plt.legend()
        st.pyplot(plt)

if st.sidebar.button("Reset Button State"):
    reset_button_state()
