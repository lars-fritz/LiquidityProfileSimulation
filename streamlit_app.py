import streamlit as st
import numpy as np
import plotly.graph_objects as go

def generate_liquidity_profile(price, lower_bound, upper_bound, points=50, A=0, B=0, C=0, D=0, E=1):
    prices = np.linspace(lower_bound, upper_bound, points)
    x = np.abs(prices - price)  # x is the absolute difference from the current price
    liquidity = A + B * x + C * x**2 + D * np.exp(-x**2 / E)
    return prices, liquidity

st.title("Liquidity Profile Generator")

# User inputs
price = st.number_input("Enter the current price:", min_value=0.01, value=100.0)
lower_bound = st.number_input("Enter the lower bound of the price range:", min_value=0.01, value=80.0)
upper_bound = st.number_input("Enter the upper bound of the price range:", min_value=0.01, value=120.0)

st.subheader("Liquidity Profile Below Price")
A_below = st.slider("A (Flat Liquidity Below)", 0.0, 10.0, 1.0)
B_below = st.slider("B (Linear Coefficient Below)", -1.0, 1.0, 0.1)
C_below = st.slider("C (Quadratic Coefficient Below)", -0.1, 0.1, 0.01)
D_below = st.slider("D (Gaussian Height Below)", 0.0, 10.0, 1.0)
E_below = st.slider("E (Gaussian Width Below)", 0.1, 10.0, 1.0)

st.subheader("Liquidity Profile Above Price")
A_above = st.slider("A (Flat Liquidity Above)", 0.0, 10.0, 1.0)
B_above = st.slider("B (Linear Coefficient Above)", -1.0, 1.0, 0.1)
C_above = st.slider("C (Quadratic Coefficient Above)", -0.1, 0.1, 0.01)
D_above = st.slider("D (Gaussian Height Above)", 0.0, 10.0, 1.0)
E_above = st.slider("E (Gaussian Width Above)", 0.1, 10.0, 1.0)

if st.button("Generate Liquidity Profile"):
    prices_below, liquidity_below = generate_liquidity_profile(price, lower_bound, price, A=A_below, B=B_below, C=C_below, D=D_below, E=E_below)
    prices_above, liquidity_above = generate_liquidity_profile(price, price, upper_bound, A=A_above, B=B_above, C=C_above, D=D_above, E=E_above)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prices_below, y=liquidity_below, mode='lines',
        name='Below Price', line=dict(dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=prices_above, y=liquidity_above, mode='lines',
        name='Above Price'
    ))
    
    fig.update_layout(
        title="Liquidity Profile",
        xaxis_title="Price",
        yaxis_title="Liquidity",
        dragmode="pan"
    )
    
    st.plotly_chart(fig, use_container_width=True)
