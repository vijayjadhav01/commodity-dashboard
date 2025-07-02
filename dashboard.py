import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Food Commodity Price Tracker", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp {
        background-color: #ffffff !important;
    }
    
    .main .block-container {
        background-color: #ffffff !important;
        padding-top: 0rem !important;
    }
    
    :root {
        --primary-color: #0070CC;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .chart-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e1e5e9;
    }
    
    .stSelectbox > div > div, .stMultiSelect > div > div, .stDateInput > div > div {
        border: 2px solid #e1e5e9 !important;
        border-radius: 5px !important;
        background-color: white !important;
    }
    
    .stSelectbox > div > div:focus-within, .stMultiSelect > div > div:focus-within, .stDateInput > div > div:focus-within {
        border-color: #0070CC !important;
    }
    
    .stSelectbox div[data-baseweb="select"], .stMultiSelect div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stSelectbox ul, .stMultiSelect ul {
        background-color: white !important;
    }
    
    .stSelectbox li, .stMultiSelect li {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stSelectbox li:hover, .stMultiSelect li:hover {
        background-color: #f0f0f0 !important;
    }
    
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    div[data-baseweb="popover"] {
        background-color: white !important;
    }
    
    div[role="listbox"], div[role="option"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    div[role="option"]:hover {
        background-color: #f0f0f0 !important;
    }
    
    .stButton > button {
        background-color: #0070CC;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #005aa3;
    }
    
    .filter-label {
        color: #0070CC;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .stSelectbox label, .stMultiSelect label, .stDateInput label {
        color: #0070CC !important;
    }
    
    .stDateInput div[data-baseweb="popover"] {
        background-color: white !important;
        border: 1px solid #e1e5e9 !important;
        border-radius: 5px !important;
    }
    
    .stDateInput div[data-baseweb="calendar"] button {
        background-color: #0070CC !important;
        color: white !important;
        border: none !important;
    }
    
    .stDateInput div[data-baseweb="calendar"] div[aria-selected="true"] {
        background-color: #0070CC !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('''
<div style="text-align: center; margin-bottom: 2rem; margin-top: -2rem;">
    <img src="https://raw.githubusercontent.com/vijayjadhav01/commodity-dashboard/main/Logo.png" 
         style="height: 50px; margin-bottom: 1rem;" alt="IndiaSpend Logo">
    <h1 style="color: #0070CC; font-size: 2.5rem; font-weight: 700; margin: 0; border-bottom: 3px solid #0070CC; padding-bottom: 1rem;">
        Food Commodity Price Tracker
    </h1>
</div>
''', unsafe_allow_html=True)

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

data = load_data()

if data is not None:
    if 'selected_group' not in st.session_state:
        st.session_state.selected_group = ''
    if 'selected_commodities' not in st.session_state:
        st.session_state.selected_commodities = []
    
    col1, col2, col3, col4, col5, col6 = st.columns([1.5, 3, 1.2, 1.2, 1, 1])
    
    with col1:
        selected_group = st.selectbox("Group", [''] + sorted(data['Group'].unique()), 
                                    key="group_select", 
                                    index=([''] + sorted(data['Group'].unique())).index(st.session_state.selected_group) if st.session_state.selected_group in ([''] + sorted(data['Group'].unique())) else 0,
                                    placeholder="Select Group")
        st.session_state.selected_group = selected_group
    
    with col2:
        if selected_group:
            commodities = sorted(data[data['Group'] == selected_group]['Commodity'].unique())
            valid_commodities = [comm for comm in st.session_state.selected_commodities if comm in commodities]
            selected_commodities = st.multiselect("Commodities", commodities, 
                                                default=valid_commodities,
                                                key="commodity_select",
                                                placeholder="Select Commodities")
            st.session_state.selected_commodities = selected_commodities
        else:
            selected_commodities = []
            st.multiselect("Commodities", [], placeholder="Select Commodities", 
                         key="commodity_select_empty")
            st.session_state.selected_commodities = []
    
    with col3:
        from_date = st.date_input("From Date", value=None, key="from_date")
    
    with col4:
        to_date = st.date_input("To Date", value=None, key="to_date")
    
    with col5:
        submit_button = st.button("Search")
    
    with col6:
        clear_button = st.button("Clear", key="clear_btn")
        if clear_button:
            st.session_state.selected_group = ''
            st.session_state.selected_commodities = []
            st.rerun()
    
    if submit_button and selected_group and selected_commodities:
        filtered_data = data[(data['Group'] == selected_group) & (data['Commodity'].isin(selected_commodities))]
        
        if from_date and to_date:
            from_date_pd = pd.to_datetime(from_date)
            to_date_pd = pd.to_datetime(to_date)
            filtered_data = filtered_data[(filtered_data['Date'] >= from_date_pd) & (filtered_data['Date'] <= to_date_pd)]
        elif from_date:
            from_date_pd = pd.to_datetime(from_date)
            filtered_data = filtered_data[filtered_data['Date'] >= from_date_pd]
        elif to_date:
            to_date_pd = pd.to_datetime(to_date)
            filtered_data = filtered_data[filtered_data['Date'] <= to_date_pd]
        
        if not filtered_data.empty:
            st.markdown(f'''
            <h3 style="color: #0070CC; margin-top: 0; text-align: center; margin-bottom: 1rem; font-size: 1.5rem;">Retail Price Trends - {selected_group}</h3>
            ''', unsafe_allow_html=True)
            
            fig = go.Figure()
            colors = ['#0070CC', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE']
            
            for i, commodity in enumerate(selected_commodities):
                commodity_data = filtered_data[filtered_data['Commodity'] == commodity]
                fig.add_trace(go.Scatter(
                    x=commodity_data['Date'], y=commodity_data['Price'],
                    mode='lines', name=commodity,
                    line=dict(color=colors[i % len(colors)], width=1.5),
                    hovertemplate=f'<b>{commodity}</b><br>Date: %{{x|%d %b %Y}}<br>Retail Price: ₹%{{y:.2f}}/kg<br><extra></extra>'
                ))
            
            fig.update_layout(
                xaxis_title="Date", yaxis_title="Retail Price (₹/kg)", hovermode='x unified',
                plot_bgcolor='white', paper_bgcolor='white', height=500,
                font=dict(family="Arial, sans-serif", size=12, color='#333333'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                           bgcolor="rgba(255,255,255,0.8)", bordercolor="#0070CC", borderwidth=1,
                           font=dict(color='#333333')),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', 
                          showline=True, linecolor='#0070CC',
                          title_font=dict(color='#333333'), tickfont=dict(color='#333333'),
                          fixedrange=False),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)', 
                          showline=True, linecolor='#0070CC',
                          title_font=dict(color='#333333'), tickfont=dict(color='#333333'),
                          fixedrange=False),
                dragmode='zoom'
            )
            
            config = {
                'displayModeBar': True,
                'modeBarButtonsToRemove': [
                    'select2d', 'lasso2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
                    'toggleSpikelines', 'toggleHover'
                ],
                'displaylogo': False,
                'scrollZoom': True,
                'doubleClick': 'reset',
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'commodity_prices_{selected_group}',
                    'height': 500,
                    'width': 1200,
                    'scale': 2
                }
            }
            
            st.plotly_chart(fig, use_container_width=True, config=config)
        else:
            st.warning("⚠️ No data available for the selected filters.")
    
    elif submit_button:
        st.warning("⚠️ Please select a group and at least one commodity.")
    
    else:
        st.markdown('''
        <div class="chart-container" style="text-align: center; padding: 4rem 2rem;">
            <h3 style="color: #0070CC;">Select filters and click "Search" to view price trends</h3>
            <p style="color: #666; font-size: 1.1rem;">Choose a commodity group and one or more commodities to get started</p>
        </div>
        ''', unsafe_allow_html=True)

else:
    st.error("❌ Unable to load data. Please check your internet connection and try again.")
