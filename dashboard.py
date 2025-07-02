import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Commodity Price Dashboard", layout="wide")

# Simplified CSS
st.markdown("""
<style>
    .stApp { background-color: white !important; }
    #MainMenu, footer, header { visibility: hidden; }
    
    .stSelectbox > div > div, .stMultiSelect > div > div {
        border: 2px solid #e1e5e9 !important;
        border-radius: 5px !important;
        background-color: white !important;
        color: #333 !important;
    }
    
    .stSelectbox > div > div:focus-within, .stMultiSelect > div > div:focus-within {
        border-color: #0070CC !important;
    }
    
    /* Fix dropdown text visibility */
    .stMultiSelect div[data-baseweb="select"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Dropdown menu styling */
    .stMultiSelect ul, .stSelectbox ul {
        background-color: white !important;
    }
    
    .stMultiSelect li, .stSelectbox li {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stMultiSelect li:hover, .stSelectbox li:hover {
        background-color: #f0f0f0 !important;
        color: #333 !important;
    }
    
    /* Force all popover content to have dark text */
    div[data-baseweb="popover"] {
        background-color: white !important;
    }
    
    div[data-baseweb="popover"] div {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[role="listbox"] {
        background-color: white !important;
    }
    
    div[role="option"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[role="option"]:hover {
        background-color: #f0f0f0 !important;
        color: #333 !important;
    }
    
    .stButton > button {
        background-color: #0070CC;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    
    .filter-label {
        color: #0070CC;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .chart-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e5e9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('''
<div style="text-align: center; margin-bottom: 2rem;">
    <img src="https://raw.githubusercontent.com/vijayjadhav01/commodity-dashboard/main/Logo.png" 
         style="height: 50px; margin-bottom: 1rem;" alt="IndiaSpend Logo">
    <h1 style="color: #0070CC; font-size: 2.5rem; font-weight: 700; margin: 0; border-bottom: 3px solid #0070CC; padding-bottom: 1rem;">
        Commodity Price Dashboard
    </h1>
</div>
''', unsafe_allow_html=True)

# Data loading
@st.cache_data
def load_data():
    try:
        # Your Google Sheets URL
        sheet_url = "https://docs.google.com/spreadsheets/d/18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8/edit?usp=sharing"
        # Convert to CSV export URL
        sheet_id = sheet_url.split('/d/')[1].split('/')[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        
        df = pd.read_csv(csv_url)
        df['Date'] = pd.to_datetime(df['Date'])
        return df.dropna(subset=['Date', 'Commodity', 'Group', 'Price']).sort_values('Date')
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

data = load_data()

if data is not None:
    # Filters
    st.markdown("##### 🔍 Filters")
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown('<p class="filter-label">Select Group</p>', unsafe_allow_html=True)
        selected_group = st.selectbox("Group", [''] + sorted(data['Group'].unique()), label_visibility="collapsed")
    
    with col2:
        st.markdown('<p class="filter-label">Select Commodities</p>', unsafe_allow_html=True)
        if selected_group:
            commodities = sorted(data[data['Group'] == selected_group]['Commodity'].unique())
            selected_commodities = st.multiselect("Commodities", commodities, label_visibility="collapsed")
        else:
            selected_commodities = []
            st.multiselect("Commodities", [], placeholder="Please select a group first", label_visibility="collapsed")
    
    with col3:
        st.markdown('<p class="filter-label">Apply Filters</p>', unsafe_allow_html=True)
        submit_button = st.button("Search")
    
    # Chart display
    if submit_button and selected_group and selected_commodities:
        filtered_data = data[(data['Group'] == selected_group) & (data['Commodity'].isin(selected_commodities))]
        
        if not filtered_data.empty:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown(f"### 📈 Retail Price Trends - {selected_group}")
            
            fig = go.Figure()
            colors = ['#0070CC', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
            
            for i, commodity in enumerate(selected_commodities):
                commodity_data = filtered_data[filtered_data['Commodity'] == commodity]
                fig.add_trace(go.Scatter(
                    x=commodity_data['Date'], y=commodity_data['Price'],
                    mode='lines+markers', name=commodity,
                    line=dict(color=colors[i % len(colors)], width=3),
                    hovertemplate=f'<b>{commodity}</b><br>Date: %{{x|%d %b %Y}}<br>Price: ₹%{{y:.2f}}/kg<extra></extra>'
                ))
            
            fig.update_layout(
                xaxis_title="Date", yaxis_title="Retail Price (₹/kg)",
                plot_bgcolor='white', paper_bgcolor='white', height=500,
                legend=dict(orientation="h", y=1.02, x=1, xanchor="right")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander("📋 View Raw Data"):
                st.dataframe(filtered_data[['Date', 'Commodity', 'Price']].pivot(
                    index='Date', columns='Commodity', values='Price').round(2))
        else:
            st.warning("⚠️ No data available for the selected filters.")
    
    elif submit_button:
        st.warning("⚠️ Please select a group and commodities.")
    
    else:
        st.markdown('''
        <div class="chart-container" style="text-align: center; padding: 4rem 2rem;">
            <h3 style="color: #0070CC;">Select filters and click "Search" to view price trends</h3>
            <p style="color: #666;">Choose a commodity group and commodities to get started</p>
        </div>
        ''', unsafe_allow_html=True)

else:
    st.error("Failed to load data from Google Sheets")
