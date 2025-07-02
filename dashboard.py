import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Commodity Price Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for styling
st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Main content area */
    .main .block-container {
        background-color: #ffffff !important;
        padding-top: 1 rem !important;
    }
    
    /* Sidebar (if any) */
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
    
    /* Main theme color */
    :root {
        --primary-color: #0070CC;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title styling */
    .main-title {
        color: #0070CC;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #0070CC;
        padding-bottom: 1rem;
    }
    
    /* Chart container */
    .chart-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e1e5e9;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border: 2px solid #e1e5e9 !important;
        border-radius: 5px !important;
        background-color: white !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #0070CC !important;
    }
    
    /* Selectbox dropdown options */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Selectbox dropdown menu */
    .stSelectbox ul {
        background-color: white !important;
    }
    
    .stSelectbox li {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stSelectbox li:hover {
        background-color: #f0f0f0 !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        border: 2px solid #e1e5e9 !important;
        border-radius: 5px !important;
        background-color: white !important;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #0070CC !important;
    }
    
    /* Multiselect dropdown */
    .stMultiSelect div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Multiselect options */
    .stMultiSelect ul {
        background-color: white !important;
    }
    
    .stMultiSelect li {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stMultiSelect li:hover {
        background-color: #f0f0f0 !important;
    }
    
    /* Multiselect selected tags styling */
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    .stMultiSelect div[data-baseweb="tag"] span {
        color: #333 !important;
    }
    
    /* Additional multiselect tag overrides */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    /* Target all tag elements in multiselect */
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    /* Force override for tag text */
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"] * {
        color: #333 !important;
    }
    
    /* Force all dropdown menus to be white */
    div[data-baseweb="popover"] {
        background-color: white !important;
    }
    
    div[data-baseweb="popover"] div {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Additional overrides for stubborn elements */
    .css-1wa3eu0-placeholder, .css-12jo7m5, .css-1hb7zxy-IndicatorContainer {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Override any remaining dark backgrounds */
    div[role="listbox"] {
        background-color: white !important;
    }
    
    div[role="option"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[role="option"]:hover {
        background-color: #f0f0f0 !important;
    }
    
    /* Target specific Streamlit classes */
    .st-emotion-cache-1y4p8pa, 
    .st-emotion-cache-12fmjuu,
    .st-emotion-cache-1rtdyuf {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0070CC;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #005aa3;
        color: white !important;
    }
    
    /* Additional button text override */
    .stButton > button * {
        color: white !important;
    }
    
    .stButton > button:hover * {
        color: white !important;
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    
    /* Filter labels */
    .filter-label {
        color: #0070CC;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    /* Info box */
    .info-box {
        background-color: white;
        border: 1px solid #e1e5e9;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #333;
    }
    
    /* Force text colors */
    .stMarkdown, .stText, p, div, span {
        color: #333 !important;
    }
    
    /* Fix selectbox text */
    .stSelectbox label {
        color: #0070CC !important;
    }
    
    /* Fix multiselect text */
    .stMultiSelect label {
        color: #0070CC !important;
    }
</style>
""", unsafe_allow_html=True)

# Logo and Title
st.markdown('''
<div style="text-align: center; margin-bottom: 2rem;">
    <img src="https://raw.githubusercontent.com/vijayjadhav01/commodity-dashboard/main/Logo.png" 
         style="height: 50px; margin-bottom: 1rem;" alt="IndiaSpend Logo">
    <h1 style="color: #0070CC; font-size: 2.5rem; font-weight: 700; margin: 0; border-bottom: 3px solid #0070CC; padding-bottom: 1rem;">
        Commodity Price Dashboard
    </h1>
</div>
''', unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        sheet_id = "18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(csv_url)
        df['Date'] = pd.to_datetime(df['Date'])
        return df.sort_values('Date').dropna(subset=['Date', 'Commodity', 'Group', 'Price'])
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# Load data
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
    
    # Show results
    if submit_button and selected_group and selected_commodities:
        filtered_data = data[(data['Group'] == selected_group) & (data['Commodity'].isin(selected_commodities))]
        
        if not filtered_data.empty:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown(f"### 📈 Retail Price Trends - {selected_group}")
            
            # Create plot
            fig = go.Figure()
            colors = ['#0070CC', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE']
            
            for i, commodity in enumerate(selected_commodities):
                commodity_data = filtered_data[filtered_data['Commodity'] == commodity]
                fig.add_trace(go.Scatter(
                    x=commodity_data['Date'], y=commodity_data['Price'],
                    mode='lines+markers', name=commodity,
                    line=dict(color=colors[i % len(colors)], width=3), marker=dict(size=4),
                    hovertemplate=f'<b>{commodity}</b><br>Date: %{{x|%d %b %Y}}<br>Retail Price: ₹%{{y:.2f}}/kg<br><extra></extra>'
                ))
            
            # Update layout
            fig.update_layout(
                xaxis_title="Date", yaxis_title="Retail Price (₹/kg)", hovermode='x unified',
                plot_bgcolor='white', paper_bgcolor='white', height=500,
                font=dict(family="Arial, sans-serif", size=12, color='#333333'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                           bgcolor="rgba(255,255,255,0.8)", bordercolor="#0070CC", borderwidth=1,
                           font=dict(color='#333333')),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', 
                          showline=True, linecolor='#0070CC',
                          title_font=dict(color='#333333'), tickfont=dict(color='#333333')),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', 
                          showline=True, linecolor='#0070CC',
                          title_font=dict(color='#333333'), tickfont=dict(color='#333333'))
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No data available for the selected filters.")
    
    elif submit_button:
        st.warning("⚠️ Please select a group and at least one commodity.")
    
    else:
        # Placeholder
        st.markdown('''
        <div class="chart-container" style="text-align: center; padding: 4rem 2rem;">
            <h3 style="color: #0070CC;">Select filters and click "Search" to view price trends</h3>
            <p style="color: #666; font-size: 1.1rem;">Choose a commodity group and one or more commodities to get started</p>
        </div>
        ''', unsafe_allow_html=True)

else:
    st.markdown('''
    <div style="background-color: white; border: 1px solid #e1e5e9; border-radius: 8px; padding: 1rem; margin-bottom: 2rem; color: #333;">
        <h3>🌐 Google Sheets Integration:</h3>
        <p><strong>Current Sheet:</strong> <a href="https://docs.google.com/spreadsheets/d/18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8/edit?usp=sharing" target="_blank">View Google Sheet</a></p>
        <p><strong>Requirements:</strong> Google Sheet must be shared publicly with required columns: Date, Commodity, Group, Price</p>
        <p><strong>To update data:</strong> Simply edit the Google Sheet and refresh this dashboard</p>
    </div>
    ''', unsafe_allow_html=True)
