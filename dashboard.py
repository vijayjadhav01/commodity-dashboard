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
    
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
    
    :root {
        --primary-color: #0070CC;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main-title {
        color: #0070CC;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #0070CC;
        padding-bottom: 1rem;
    }
    
    .chart-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e1e5e9;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #e1e5e9 !important;
        border-radius: 5px !important;
        background-color: white !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #0070CC !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
    }
    
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
    
    .stMultiSelect > div > div {
        border: 2px solid #e1e5e9 !important;
        border-radius: 5px !important;
        background-color: white !important;
    }
    
    .stMultiSelect > div > div:focus-within {
        border-color: #0070CC !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] {
        background-color: white !important;
    }
    
    .stMultiSelect div[data-baseweb="select"] > div {
        background-color: white !important;
        color: #333 !important;
    }
    
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
    
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    .stMultiSelect div[data-baseweb="tag"] span {
        color: #333 !important;
    }
    
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #dee2e6 !important;
    }
    
    div[data-testid="stMultiSelect"] div[data-baseweb="tag"] * {
        color: #333 !important;
    }
    
    div[data-baseweb="popover"] {
        background-color: white !important;
    }
    
    div[data-baseweb="popover"] div {
        background-color: white !important;
        color: #333 !important;
    }
    
    .css-1wa3eu0-placeholder, .css-12jo7m5, .css-1hb7zxy-IndicatorContainer {
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
    }
    
    .st-emotion-cache-1y4p8pa, 
    .st-emotion-cache-12fmjuu,
    .st-emotion-cache-1rtdyuf {
        background-color: white !important;
        color: #333 !important;
    }
    
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
    
    .clear-button > button {
        background-color: #6c757d !important;
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
    }
    
    .clear-button > button:hover {
        background-color: #5a6268 !important;
        color: white !important;
    }
    
    .stButton > button * {
        color: white !important;
    }
    
    .stButton > button:hover * {
        color: white !important;
    }
    
    .clear-button > button * {
        color: white !important;
    }
    
    .clear-button > button:hover * {
        color: white !important;
    }
    
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    
    .filter-label {
        color: #0070CC;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .info-box {
        background-color: white;
        border: 1px solid #e1e5e9;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #333;
    }
    
    .stMarkdown, .stText, p, div, span {
        color: #333 !important;
    }
    
    .stSelectbox label {
        color: #0070CC !important;
    }
    
    .stMultiSelect label {
        color: #0070CC !important;
    }
    
    .stDateInput > div > div {
        border: 2px solid #e1e5e9 !important;
        border-radius: 5px !important;
        background-color: white !important;
    }
    
    .stDateInput > div > div:focus-within {
        border-color: #0070CC !important;
    }
    
    .stDateInput label {
        color: #0070CC !important;
    }
    
    /* Date picker calendar styling */
    .stDateInput div[data-baseweb="calendar"] {
        background-color: white !important;
        border: 1px solid #e1e5e9 !important;
        border-radius: 8px !important;
    }
    
    .stDateInput div[data-baseweb="calendar"] * {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Calendar header */
    .stDateInput div[data-baseweb="calendar"] div[data-baseweb="calendar-header"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Calendar days */
    .stDateInput div[data-baseweb="calendar"] div[role="button"] {
        background-color: white !important;
        color: #333 !important;
    }
    
    .stDateInput div[data-baseweb="calendar"] div[role="button"]:hover {
        background-color: #f0f0f0 !important;
        color: #333 !important;
    }
    
    /* Selected date */
    .stDateInput div[data-baseweb="calendar"] div[aria-selected="true"] {
        background-color: #0070CC !important;
        color: white !important;
    }
    
    /* Today's date */
    .stDateInput div[data-baseweb="calendar"] div[data-date] {
        background-color: white !important;
        color: #333 !important;
    }
    
    /* Calendar navigation buttons */
    .stDateInput button {
        background-color: white !important;
        color: #333 !important;
        border: none !important;
    }
    
    .stDateInput button:hover {
        background-color: #f0f0f0 !important;
        color: #333 !important;
    }
    
    /* Force all calendar elements to be visible */
    .stDateInput div[data-baseweb="popover"] {
        background-color: white !important;
        border: 1px solid #e1e5e9 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .stDateInput div[data-baseweb="popover"] * {
        color: #333 !important;
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
        st.markdown('<p class="filter-label">Select Group</p>', unsafe_allow_html=True)
        selected_group = st.selectbox("Group", [''] + sorted(data['Group'].unique()), 
                                    key="group_select", 
                                    index=([''] + sorted(data['Group'].unique())).index(st.session_state.selected_group) if st.session_state.selected_group in ([''] + sorted(data['Group'].unique())) else 0,
                                    label_visibility="collapsed")
        st.session_state.selected_group = selected_group
    
    with col2:
        st.markdown('<p class="filter-label">Select Commodities</p>', unsafe_allow_html=True)
        if selected_group:
            commodities = sorted(data[data['Group'] == selected_group]['Commodity'].unique())
            valid_commodities = [comm for comm in st.session_state.selected_commodities if comm in commodities]
            selected_commodities = st.multiselect("Commodities", commodities, 
                                                default=valid_commodities,
                                                key="commodity_select",
                                                label_visibility="collapsed")
            st.session_state.selected_commodities = selected_commodities
        else:
            selected_commodities = []
            st.multiselect("Commodities", [], placeholder="Please select a group first", 
                         key="commodity_select_empty",
                         label_visibility="collapsed")
            st.session_state.selected_commodities = []
    
    with col3:
        st.markdown('<p class="filter-label">From Date</p>', unsafe_allow_html=True)
        from_date = st.date_input("From Date", value=None, key="from_date", label_visibility="collapsed")
    
    with col4:
        st.markdown('<p class="filter-label">To Date</p>', unsafe_allow_html=True)
        to_date = st.date_input("To Date", value=None, key="to_date", label_visibility="collapsed")
    
    with col5:
        st.markdown('<p class="filter-label">&nbsp;</p>', unsafe_allow_html=True)
        submit_button = st.button("Search")
    
    with col6:
        st.markdown('<p class="filter-label">&nbsp;</p>', unsafe_allow_html=True)
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
    st.markdown('''
    <div style="background-color: white; border: 1px solid #e1e5e9; border-radius: 8px; padding: 1rem; margin-bottom: 2rem; color: #333;">
        <h3>🌐 Google Sheets Integration:</h3>
        <p><strong>Current Sheet:</strong> <a href="https://docs.google.com/spreadsheets/d/18LVYFWEGfgLNqlo_mY5A70cSmXQBXjd8Lry0ivj2AO8/edit?usp=sharing" target="_blank">View Google Sheet</a></p>
        <p><strong>Requirements:</strong> Google Sheet must be shared publicly with required columns: Date, Commodity, Group, Price</p>
        <p><strong>To update data:</strong> Simply edit the Google Sheet and refresh this dashboard</p>
    </div>
    ''', unsafe_allow_html=True)
