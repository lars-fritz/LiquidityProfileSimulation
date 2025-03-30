import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def generate_liquidity_profile(price, lower_bound, upper_bound, points=10):
    prices = np.linspace(lower_bound, upper_bound, points)
    liquidity = np.exp(-((prices - price) ** 2) / (2 * ((upper_bound - lower_bound) / 5) ** 2))
    return prices, liquidity

st.title("Liquidity Profile Generator")

# User inputs
price = st.number_input("Enter the current price:", min_value=0.01, value=100.0)
lower_bound = st.number_input("Enter the lower bound of the price range:", min_value=0.01, value=80.0)
upper_bound = st.number_input("Enter the upper bound of the price range:", min_value=0.01, value=120.0)

def validate_inputs():
    if lower_bound >= upper_bound:
        st.error("Lower bound must be less than upper bound.")
        return False
    if price < lower_bound or price > upper_bound:
        st.error("Price should be within the range of lower and upper bounds.")
        return False
    return True

if st.button("Generate Liquidity Profile"):
    if validate_inputs():
        prices, liquidity = generate_liquidity_profile(price, lower_bound, upper_bound)
        df = pd.DataFrame({"Price": prices, "Liquidity": liquidity})
        st.write(df)
        
        # Plotting the liquidity profile with Plotly
        fig = px.line(df, x="Price", y="Liquidity", markers=True, title="Liquidity Profile")
        fig.update_layout(xaxis_title="Price", yaxis_title="Liquidity")
        st.plotly_chart(fig)
