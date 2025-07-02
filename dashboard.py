import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Commodity Price Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        padding-top: 2rem !important;
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
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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
        box-shadow: 0 0 0 1px #0070CC !important;
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
        box-shadow: 0 0 0 1px #0070CC !important;
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
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #005aa3;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 112, 204, 0.3);
    }
    
    /* Metrics styling */
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
    <img src="https://raw.githubusercontent.com/yourusername/your-repo-name/main/Logo.png" 
         style="height: 80px; margin-bottom: 1rem;" alt="IndiaSpend Logo">
    <h1 style="color: #0070CC; font-size: 2.5rem; font-weight: 700; margin: 0; border-bottom: 3px solid #0070CC; padding-bottom: 1rem;">
        Commodity Price Dashboard
    </h1>
</div>
''', unsafe_allow_html=True)

# Configuration - Google Sheets URL (Updated with public access)
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8/edit?usp=sharing"

# Load data function from Google Sheets
@st.cache_data
def load_data_from_google_sheets(sheet_url):
    try:
        # Convert Google Sheets URL to CSV export URL
        if 'docs.google.com/spreadsheets' in sheet_url:
            # Extract the sheet ID from the URL
            if '/d/' in sheet_url:
                sheet_id = sheet_url.split('/d/')[1].split('/')[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            else:
                st.error("❌ Invalid Google Sheets URL format")
                return None
        else:
            csv_url = sheet_url
        
        # Load data from Google Sheets
        df = pd.read_csv(csv_url)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Clean the data - remove rows with missing essential data
        df = df.dropna(subset=['Date', 'Commodity', 'Group', 'Price'])
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data from Google Sheets: {str(e)}")
        st.info("💡 Make sure your Google Sheet is shared publicly (Anyone with the link can view)")
        return None

# Load the data from Google Sheets
data = load_data_from_google_sheets(GOOGLE_SHEET_URL)

if data is not None:
    # Filters section (no container box)
    st.markdown("### 🔍 Filters")
    
    # Create horizontal layout for filters
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown('<p class="filter-label">Select Group</p>', unsafe_allow_html=True)
        groups = [''] + sorted(data['Group'].unique().tolist())
        selected_group = st.selectbox(
            "Group",
            groups,
            key="group_select",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<p class="filter-label">Select Commodities</p>', unsafe_allow_html=True)
        if selected_group:
            available_commodities = sorted(data[data['Group'] == selected_group]['Commodity'].unique())
            selected_commodities = st.multiselect(
                "Commodities",
                available_commodities,
                key="commodity_select",
                label_visibility="collapsed"
            )
        else:
            selected_commodities = []
            st.multiselect(
                "Commodities",
                [],
                placeholder="Please select a group first",
                key="commodity_select_disabled",
                label_visibility="collapsed"
            )
    
    with col3:
        st.markdown('<p class="filter-label">Apply Filters</p>', unsafe_allow_html=True)
        submit_button = st.button("📊 Show Chart", key="submit_btn")
    
    # Show chart only when button is clicked and selections are made
    if submit_button and selected_group and selected_commodities:
        # Filter data
        filtered_data = data[
            (data['Group'] == selected_group) & 
            (data['Commodity'].isin(selected_commodities))
        ]
        
        if not filtered_data.empty:
            # Chart section
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown(f"### 📈 Retail Price Trends - {selected_group}")
            
            # Create the plot
            fig = go.Figure()
            
            # Color palette
            colors = ['#0070CC', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
                     '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE']
            
            for i, commodity in enumerate(selected_commodities):
                commodity_data = filtered_data[filtered_data['Commodity'] == commodity]
                
                fig.add_trace(go.Scatter(
                    x=commodity_data['Date'],
                    y=commodity_data['Price'],
                    mode='lines+markers',
                    name=commodity,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=4),
                    hovertemplate=f'<b>{commodity}</b><br>' +
                                 'Date: %{x}<br>' +
                                 'Retail Price: ₹%{y:.2f}/kg<br>' +
                                 '<extra></extra>'
                ))
            
            # Update layout
            fig.update_layout(
                title=None,
                xaxis_title="Date",
                yaxis_title="Retail Price (₹/kg)",
                hovermode='x unified',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Arial, sans-serif", size=12, color='#333333'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#0070CC",
                    borderwidth=1,
                    font=dict(color='#333333')
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)',
                    showline=True,
                    linecolor='#0070CC',
                    title_font=dict(color='#333333'),
                    tickfont=dict(color='#333333')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(128,128,128,0.2)',
                    showline=True,
                    linecolor='#0070CC',
                    title_font=dict(color='#333333'),
                    tickfont=dict(color='#333333')
                ),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Data table (optional)
            with st.expander("📋 View Raw Data"):
                st.dataframe(
                    filtered_data[['Date', 'Commodity', 'Price']].pivot(
                        index='Date', columns='Commodity', values='Price'
                    ).round(2),
                    use_container_width=True
                )
        
        else:
            st.warning("⚠️ No data available for the selected filters.")
    
    elif submit_button:
        if not selected_group:
            st.warning("⚠️ Please select a group.")
        elif not selected_commodities:
            st.warning("⚠️ Please select at least one commodity.")
    
    else:
        # Show placeholder when no filters applied
        st.markdown('''
        <div class="chart-container" style="text-align: center; padding: 4rem 2rem;">
            <h3 style="color: #0070CC;">📊 Select filters and click "Show Chart" to view price trends</h3>
            <p style="color: #666; font-size: 1.1rem;">Choose a commodity group and one or more commodities to get started</p>
        </div>
        ''', unsafe_allow_html=True)

else:
    st.markdown('''
    <div style="background-color: white; border: 1px solid #e1e5e9; border-radius: 8px; padding: 1rem; margin-bottom: 2rem; color: #333;">
        <h3>🌐 Google Sheets Integration:</h3>
        <p><strong>Current Sheet:</strong> <a href="https://docs.google.com/spreadsheets/d/18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8/edit?usp=sharing" target="_blank">View Google Sheet</a></p>
        <p><strong>Requirements:</strong></p>
        <ul>
            <li>Google Sheet must be shared publicly (Anyone with the link can view)</li>
            <li>Required columns: Date, Commodity, Group, Price</li>
            <li>Data automatically syncs from the cloud</li>
        </ul>
        <p><strong>To update data:</strong> Simply edit the Google Sheet and refresh this dashboard</p>
    </div>
    ''', unsafe_allow_html=True)
