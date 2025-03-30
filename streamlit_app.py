import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

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
        # Generate two separate liquidity profiles
        prices_below, liquidity_below = generate_liquidity_profile(price, lower_bound, price)
        prices_above, liquidity_above = generate_liquidity_profile(price, price, upper_bound)
        
        df_below = pd.DataFrame({"Price": prices_below, "Liquidity": liquidity_below})
        df_above = pd.DataFrame({"Price": prices_above, "Liquidity": liquidity_above})
        
        st.write("Liquidity Profile Below Price:")
        st.write(df_below)
        
        st.write("Liquidity Profile Above Price:")
        st.write(df_above)
        
        # Create interactive scatter plot with editable points
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_below["Price"], y=df_below["Liquidity"], mode='markers',
            name='Below Price', marker=dict(size=10),
        ))
        fig.add_trace(go.Scatter(
            x=df_above["Price"], y=df_above["Liquidity"], mode='markers',
            name='Above Price', marker=dict(size=10),
        ))
        
        fig.update_layout(
            title="Interactive Liquidity Profile",
            xaxis_title="Price",
            yaxis_title="Liquidity",
            dragmode="pan",
            editable=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
