import streamlit as st
import numpy as np
import plotly.graph_objects as go

def generate_liquidity_profile(price, lower_bound, upper_bound, points=10, components={}):
    prices = np.linspace(lower_bound, upper_bound, points)
    liquidity = np.zeros_like(prices)
    
    for comp, params in components.items():
        if comp == 'flat':
            height, range_start, range_end = params
            mask = (prices >= range_start) & (prices <= range_end)
            liquidity[mask] += height
        elif comp == 'gauss':
            height, width, center = params
            liquidity += height * np.exp(-((prices - center) ** 2) / (2 * width ** 2))
        elif comp == 'linear':
            coeff, range_start, range_end = params
            mask = (prices >= range_start) & (prices <= range_end)
            liquidity[mask] += coeff * (prices[mask] - range_start)
        elif comp == 'quadratic':
            coeff, range_start, range_end = params
            mask = (prices >= range_start) & (prices <= range_end)
            liquidity[mask] += coeff * (prices[mask] - range_start) ** 2
    
    return prices, liquidity

st.title("Liquidity Profile Generator")

# User inputs
price = st.number_input("Enter the current price:", min_value=0.01, value=100.0)
lower_bound = st.number_input("Enter the lower bound of the price range:", min_value=0.01, value=80.0)
upper_bound = st.number_input("Enter the upper bound of the price range:", min_value=0.01, value=120.0)

# Define component inputs for below price
st.subheader("Liquidity Components Below Price")
below_components = {}
if st.checkbox("Add Flat Component Below"):
    height = st.number_input("Flat Height (Below):", value=1.0)
    range_start = st.number_input("Flat Range Start (Below):", value=lower_bound)
    range_end = st.number_input("Flat Range End (Below):", value=price)
    below_components['flat'] = (height, range_start, range_end)
if st.checkbox("Add Gaussian Component Below"):
    height = st.number_input("Gaussian Height (Below):", value=1.0)
    width = st.number_input("Gaussian Width (Below):", value=5.0)
    center = st.number_input("Gaussian Center (Below):", value=price - 5)
    below_components['gauss'] = (height, width, center)
if st.checkbox("Add Linear Component Below"):
    coeff = st.number_input("Linear Coefficient (Below):", value=0.1)
    range_start = st.number_input("Linear Range Start (Below):", value=lower_bound)
    range_end = st.number_input("Linear Range End (Below):", value=price)
    below_components['linear'] = (coeff, range_start, range_end)
if st.checkbox("Add Quadratic Component Below"):
    coeff = st.number_input("Quadratic Coefficient (Below):", value=0.01)
    range_start = st.number_input("Quadratic Range Start (Below):", value=lower_bound)
    range_end = st.number_input("Quadratic Range End (Below):", value=price)
    below_components['quadratic'] = (coeff, range_start, range_end)

# Define component inputs for above price
st.subheader("Liquidity Components Above Price")
above_components = {}
if st.checkbox("Add Flat Component Above"):
    height = st.number_input("Flat Height (Above):", value=1.0)
    range_start = st.number_input("Flat Range Start (Above):", value=price)
    range_end = st.number_input("Flat Range End (Above):", value=upper_bound)
    above_components['flat'] = (height, range_start, range_end)
if st.checkbox("Add Gaussian Component Above"):
    height = st.number_input("Gaussian Height (Above):", value=1.0)
    width = st.number_input("Gaussian Width (Above):", value=5.0)
    center = st.number_input("Gaussian Center (Above):", value=price + 5)
    above_components['gauss'] = (height, width, center)
if st.checkbox("Add Linear Component Above"):
    coeff = st.number_input("Linear Coefficient (Above):", value=0.1)
    range_start = st.number_input("Linear Range Start (Above):", value=price)
    range_end = st.number_input("Linear Range End (Above):", value=upper_bound)
    above_components['linear'] = (coeff, range_start, range_end)
if st.checkbox("Add Quadratic Component Above"):
    coeff = st.number_input("Quadratic Coefficient (Above):", value=0.01)
    range_start = st.number_input("Quadratic Range Start (Above):", value=price)
    range_end = st.number_input("Quadratic Range End (Above):", value=upper_bound)
    above_components['quadratic'] = (coeff, range_start, range_end)

if st.button("Generate Liquidity Profile"):
    prices_below, liquidity_below = generate_liquidity_profile(price, lower_bound, price, components=below_components)
    prices_above, liquidity_above = generate_liquidity_profile(price, price, upper_bound, components=above_components)
    
    # Create interactive scatter plot
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
