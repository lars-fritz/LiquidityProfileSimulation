import streamlit as st
import numpy as np
import plotly.graph_objects as go

def generate_liquidity_profile(price, lower_bound, upper_bound, points=50, A=0, B=0, C=0, D=0, E=1):
    prices = np.linspace(lower_bound, upper_bound, points)
    x = np.abs(prices - price)  # x is the absolute difference from the current price
    liquidity = np.maximum(0, A + B * x + C * x**2 + D * np.exp(-x**2 / max(E, 0.1)))
    return prices, liquidity

def bin_liquidity_profile(prices, liquidity, num_bins):
    bins = np.linspace(prices.min(), prices.max(), num_bins + 1)
    binned_liquidity = np.histogram(prices, bins, weights=liquidity)[0] / np.histogram(prices, bins)[0]
    bin_centers = (bins[:-1] + bins[1:]) / 2
    return bin_centers, binned_liquidity

st.title("Liquidity Profile Generator")

# User inputs
price = st.number_input("Enter the current price:", min_value=0.01, value=100.0)
lower_bound = st.number_input("Enter the lower bound of the price range:", min_value=0.01, value=80.0)
upper_bound = st.number_input("Enter the upper bound of the price range:", min_value=0.01, value=120.0)

st.subheader("Liquidity Profile Below Price")
A_below = st.slider("A (Flat Liquidity Below)", 0.0, 10.0, 1.0)
B_below = st.slider("B (Linear Coefficient Below)", 0.0, 1.0, 0.1)
C_below = st.slider("C (Quadratic Coefficient Below)", 0.0, 0.1, 0.01)
D_below = st.slider("D (Gaussian Height Below)", 0.0, 10.0, 1.0)
E_below = st.slider("E (Gaussian Width Below)", 0.1, 10.0, 1.0)
bins_below = st.slider("Number of Bins Below", 1, 20, 10)

st.subheader("Liquidity Profile Above Price")
A_above = st.slider("A (Flat Liquidity Above)", 0.0, 10.0, 1.0)
B_above = st.slider("B (Linear Coefficient Above)", 0.0, 1.0, 0.1)
C_above = st.slider("C (Quadratic Coefficient Above)", 0.0, 0.1, 0.01)
D_above = st.slider("D (Gaussian Height Above)", 0.0, 10.0, 1.0)
E_above = st.slider("E (Gaussian Width Above)", 0.1, 10.0, 1.0)
bins_above = st.slider("Number of Bins Above", 1, 20, 10)

# Auto-update on slider change
prices_below, liquidity_below = generate_liquidity_profile(price, lower_bound, price, A=A_below, B=B_below, C=C_below, D=D_below, E=E_below)
prices_above, liquidity_above = generate_liquidity_profile(price, price, upper_bound, A=A_above, B=B_above, C=C_above, D=D_above, E=E_above)

# Binned approximations
bin_centers_below, binned_liquidity_below = bin_liquidity_profile(prices_below, liquidity_below, bins_below)
bin_centers_above, binned_liquidity_above = bin_liquidity_profile(prices_above, liquidity_above, bins_above)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=prices_below, y=liquidity_below, mode='lines',
    name='Below Price', line=dict(dash='dash')
))
fig.add_trace(go.Scatter(
    x=prices_above, y=liquidity_above, mode='lines',
    name='Above Price'
))
fig.add_trace(go.Bar(
    x=bin_centers_below, y=binned_liquidity_below,
    name='Binned Below Price', opacity=0.6
))
fig.add_trace(go.Bar(
    x=bin_centers_above, y=binned_liquidity_above,
    name='Binned Above Price', opacity=0.6
))

fig.update_layout(
    title="Liquidity Profile with Binned Approximation",
    xaxis_title="Price",
    yaxis_title="Liquidity",
    dragmode="pan",
    barmode="overlay"
)

st.plotly_chart(fig, use_container_width=True)
