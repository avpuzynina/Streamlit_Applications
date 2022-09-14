import yfinance as yf
import streamlit as st
import pandas as ps

st.write("""
# Apple
#### Данные о котировках компании
Показывает графики **цены открытия** и **цены закрытия** компании Apple!
""")

tickerSymbol = 'AAPL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1y', start='2021-9-12', end='2022-9-13')

st.write("""
##  Open Price
*Цена открытия* - цена, по которой товары или товары продаются или должны быть проданы и открыта для всех заинтересованных предприятий.
""")
st.line_chart(tickerDf.Open)

st.write("""
## Close Price
*Цена закрытия* - цена последней сделки, зарегистрированная при закрытии срочной биржи по окончании рабочего дня.
""")
st.line_chart(tickerDf.Close)

