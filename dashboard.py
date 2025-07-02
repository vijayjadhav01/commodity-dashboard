import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Commodity Price Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        background-color: transparent;
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Header Section */
    .header-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        color: #6b7280;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Filter Cards */
    .filter-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .filter-section-title {
        color: #1f2937;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Chart container */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Modern form controls */
    .stSelectbox > div > div {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stMultiSelect > div > div {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Date input styling */
    .stDateInput > div > div {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        background: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .stDateInput > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        text-transform: none;
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Clear button styling */
    .clear-button > button {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
    }
    
    .clear-button > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.6);
    }
    
    /* Labels */
    .stSelectbox label, .stMultiSelect label, .stDateInput label {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Metrics cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
    }
    
    /* Placeholder styling */
    .placeholder-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 4rem 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 2rem 0;
    }
    
    .placeholder-title {
        color: #1f2937;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .placeholder-text {
        color: #6b7280;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Info box styling */
    .info-container {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('''
<div class="header-container">
    <h1 class="main-title">📈 Commodity Price Dashboard</h1>
    <p class="subtitle">Real-time commodity price analysis and trends</p>
</div>
''', unsafe_allow_html=True)

# Configuration - Google Sheets URL
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8/edit?usp=sharing"

# Load data function with better error handling
@st.cache_data
def load_data_from_google_sheets(sheet_url):
    try:
        if 'docs.google.com/spreadsheets' in sheet_url:
            if '/d/' in sheet_url:
                sheet_id = sheet_url.split('/d/')[1].split('/')[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            else:
                st.error("❌ Invalid Google Sheets URL format")
                return None
        else:
            csv_url = sheet_url
        
        df = pd.read_csv(csv_url)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        df = df.dropna(subset=['Date', 'Commodity', 'Group', 'Price'])
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None

# Load the data
with st.spinner('Loading data...'):
    data = load_data_from_google_sheets(GOOGLE_SHEET_URL)

if data is not None:
    # Initialize session state for filters
    if 'selected_group' not in st.session_state:
        st.session_state.selected_group = ''
    if 'selected_commodities' not in st.session_state:
        st.session_state.selected_commodities = []
    if 'date_range' not in st.session_state:
        min_date = data['Date'].min().date()
        max_date = data['Date'].max().date()
        st.session_state.date_range = (min_date, max_date)
    
    # Filters section
    st.markdown('''
    <div class="filter-container">
        <h2 class="filter-section-title">🎛️ Filters & Controls</h2>
    </div>
    ''', unsafe_allow_html=True)
    
    # Create filter layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Filter controls in a nice grid
        filter_col1, filter_col2, filter_col3 = st.columns([1, 2, 1])
        
        with filter_col1:
            st.markdown("**📊 Select Group**")
            groups = [''] + sorted(data['Group'].unique().tolist())
            selected_group = st.selectbox(
                "Group",
                groups,
                index=groups.index(st.session_state.selected_group) if st.session_state.selected_group in groups else 0,
                key="group_select",
                label_visibility="collapsed"
            )
            st.session_state.selected_group = selected_group
        
        with filter_col2:
            st.markdown("**🛒 Select Commodities**")
            if selected_group:
                available_commodities = sorted(data[data['Group'] == selected_group]['Commodity'].unique())
                # Filter session state commodities to only include available ones
                valid_commodities = [c for c in st.session_state.selected_commodities if c in available_commodities]
                selected_commodities = st.multiselect(
                    "Commodities",
                    available_commodities,
                    default=valid_commodities,
                    key="commodity_select",
                    label_visibility="collapsed"
                )
                st.session_state.selected_commodities = selected_commodities
            else:
                st.multiselect(
                    "Commodities",
                    [],
                    placeholder="Please select a group first",
                    key="commodity_select_disabled",
                    label_visibility="collapsed"
                )
                st.session_state.selected_commodities = []
        
        with filter_col3:
            st.markdown("**📅 Date Range**")
            min_date = data['Date'].min().date()
            max_date = data['Date'].max().date()
            
            # Date range inputs
            start_date = st.date_input(
                "Start Date",
                value=st.session_state.date_range[0],
                min_value=min_date,
                max_value=max_date,
                key="start_date",
                label_visibility="collapsed"
            )
            
            end_date = st.date_input(
                "End Date",
                value=st.session_state.date_range[1],
                min_value=min_date,
                max_value=max_date,
                key="end_date",
                label_visibility="collapsed"
            )
            
            st.session_state.date_range = (start_date, end_date)
    
    with col2:
        st.markdown("**⚡ Actions**")
        
        # Action buttons
        search_col, clear_col = st.columns(2)
        
        with search_col:
            search_button = st.button("🔍 Search", key="search_btn", use_container_width=True)
        
        with clear_col:
            if st.button("🗑️ Clear", key="clear_btn", use_container_width=True):
                st.session_state.selected_group = ''
                st.session_state.selected_commodities = []
                st.session_state.date_range = (min_date, max_date)
                st.rerun()
    
    # Show results
    if search_button and selected_group and st.session_state.selected_commodities:
        # Filter data by date range and selections
        filtered_data = data[
            (data['Group'] == selected_group) & 
            (data['Commodity'].isin(st.session_state.selected_commodities)) &
            (data['Date'].dt.date >= start_date) &
            (data['Date'].dt.date <= end_date)
        ]
        
        if not filtered_data.empty:
            # Display metrics
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Key Metrics")
            
            # Calculate metrics
            latest_data = filtered_data.groupby('Commodity')['Date'].transform('max') == filtered_data['Date']
            current_prices = filtered_data[latest_data]
            
            metric_cols = st.columns(len(st.session_state.selected_commodities))
            
            for i, commodity in enumerate(st.session_state.selected_commodities):
                commodity_data = filtered_data[filtered_data['Commodity'] == commodity]
                if not commodity_data.empty:
                    current_price = commodity_data.iloc[-1]['Price']
                    if len(commodity_data) > 1:
                        previous_price = commodity_data.iloc[-2]['Price']
                        change = current_price - previous_price
                        change_pct = (change / previous_price) * 100
                    else:
                        change = 0
                        change_pct = 0
                    
                    with metric_cols[i]:
                        st.metric(
                            label=commodity,
                            value=f"₹{current_price:.2f}/kg",
                            delta=f"{change_pct:+.1f}%"
                        )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chart section
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown(f"### 📈 Price Trends - {selected_group}")
            
            # Create enhanced plot
            fig = go.Figure()
            
            # Modern color palette
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', 
                     '#00f2fe', '#43e97b', '#38f9d7', '#ffecd2', '#fcb69f']
            
            for i, commodity in enumerate(st.session_state.selected_commodities):
                commodity_data = filtered_data[filtered_data['Commodity'] == commodity]
                
                fig.add_trace(go.Scatter(
                    x=commodity_data['Date'],
                    y=commodity_data['Price'],
                    mode='lines+markers',
                    name=commodity,
                    line=dict(color=colors[i % len(colors)], width=3),
                    marker=dict(size=6, symbol='circle'),
                    hovertemplate=f'<b>{commodity}</b><br>' +
                                 'Date: %{x|%d %b %Y}<br>' +
                                 'Price: ₹%{y:.2f}/kg<br>' +
                                 '<extra></extra>'
                ))
            
            # Enhanced layout
            fig.update_layout(
                title=None,
                xaxis_title="📅 Date",
                yaxis_title="💰 Price (₹/kg)",
                hovermode='x unified',
                plot_bgcolor='rgba(255,255,255,0.1)',
                paper_bgcolor='transparent',
                font=dict(family="Inter, sans-serif", size=12, color='#374151'),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="rgba(102,126,234,0.3)",
                    borderwidth=1,
                    font=dict(color='#374151')
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(107,114,128,0.2)',
                    showline=True,
                    linecolor='rgba(102,126,234,0.5)',
                    title_font=dict(color='#374151'),
                    tickfont=dict(color='#374151')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='rgba(107,114,128,0.2)',
                    showline=True,
                    linecolor='rgba(102,126,234,0.5)',
                    title_font=dict(color='#374151'),
                    tickfont=dict(color='#374151')
                ),
                height=600,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Enhanced data table
            with st.expander("📋 View Detailed Data"):
                pivot_table = filtered_data[['Date', 'Commodity', 'Price']].pivot(
                    index='Date', columns='Commodity', values='Price'
                ).round(2)
                st.dataframe(pivot_table, use_container_width=True)
                
                # Download button
                csv = pivot_table.to_csv()
                st.download_button(
                    label="📥 Download Data as CSV",
                    data=csv,
                    file_name=f"commodity_prices_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )
        
        else:
            st.warning("⚠️ No data available for the selected filters and date range.")
    
    elif search_button:
        if not selected_group:
            st.warning("⚠️ Please select a group.")
        elif not st.session_state.selected_commodities:
            st.warning("⚠️ Please select at least one commodity.")
    
    else:
        # Enhanced placeholder
        st.markdown('''
        <div class="placeholder-container">
            <div class="placeholder-title">🎯 Ready to Explore Price Trends?</div>
            <div class="placeholder-text">
                Select your filters above and click "Search" to visualize commodity price movements.<br>
                Use the date range filter to focus on specific time periods.
            </div>
        </div>
        ''', unsafe_allow_html=True)

else:
    # Enhanced info section
    st.markdown('''
    <div class="info-container">
        <h3>🌐 Data Source Information</h3>
        <p><strong>Google Sheets Integration:</strong> <a href="https://docs.google.com/spreadsheets/d/18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8/edit?usp=sharing" target="_blank">View Source Sheet</a></p>
        <p><strong>Requirements:</strong></p>
        <ul>
            <li>✅ Public access (Anyone with link can view)</li>
            <li>✅ Required columns: Date, Commodity, Group, Price</li>
            <li>✅ Automatic cloud synchronization</li>
        </ul>
        <p><strong>💡 Tip:</strong> Edit the Google Sheet to update data automatically!</p>
    </div>
    ''', unsafe_allow_html=True)
