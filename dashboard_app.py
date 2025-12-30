
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SLA Optimization Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- CSS FOR STYLING ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stMetric {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. LOAD DATA ---
@st.cache_data
def load_data():
    # Try different paths to be robust
    try:
        df = pd.read_csv("outputs/dashboard/customer_support_sla_dashboard.csv")
    except FileNotFoundError:
        try:
            df = pd.read_csv("../outputs/dashboard/customer_support_sla_dashboard.csv")
        except FileNotFoundError:
            st.error("❌ Data file not found. Please run 'generate_dashboard_csv.py' first.")
            return None
            
    df['Ticket_Date'] = pd.to_datetime(df['Ticket_Date'])
    return df

df = load_data()

if df is not None:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🔍 Filters")
    
    # Date Filter
    min_date = df['Ticket_Date'].min()
    max_date = df['Ticket_Date'].max()
    
    start_date, end_date = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Priority Filter
    all_priorities = ['All'] + sorted(df['Ticket Priority'].unique().tolist())
    priority = st.sidebar.selectbox("Ticket Priority", all_priorities)
    
    # Channel Filter
    all_channels = ['All'] + sorted(df['Ticket Channel'].unique().tolist())
    channel = st.sidebar.selectbox("Ticket Channel", all_channels)

    # Apply Filters
    mask = (df['Ticket_Date'] >= pd.to_datetime(start_date)) & (df['Ticket_Date'] <= pd.to_datetime(end_date))
    
    if priority != 'All':
        mask = mask & (df['Ticket Priority'] == priority)
    if channel != 'All':
        mask = mask & (df['Ticket Channel'] == channel)
        
    df_filtered = df[mask]

    # --- MAIN DASHBOARD ---
    st.title("📊 Support Operations & SLA Optimization")
    st.markdown("### Executive Risk & Financial Dashboard")
    st.markdown("---")

    # --- ROW 1: KPI CARDS ---
    col1, col2, col3, col4 = st.columns(4)
    
    breach_rate = df_filtered['Is_SLA_Breach'].mean()
    total_tickets = len(df_filtered)
    total_cost = df_filtered['Breach_Cost'].sum()
    
    # Calculate High Risk Share if bucket exists
    if 'Risk_Bucket' in df_filtered.columns:
        high_risk_count = len(df_filtered[df_filtered['Risk_Bucket'] == 'High Risk'])
        high_risk_share = high_risk_count / total_tickets if total_tickets > 0 else 0
    else:
        high_risk_share = 0

    col1.metric("🚨 SLA Breach Rate", f"{breach_rate:.1%}", delta_color="inverse")
    col2.metric("🎫 Total Tickets", f"{total_tickets:,}")
    col3.metric("💸 Est. Financial Loss", f"${total_cost:,.0f}", delta_color="inverse")
    col4.metric("🔥 High Risk Tickets", f"{high_risk_share:.1%}", help="Share of tickets predicted as High Risk by AI")

    st.markdown("---")

    # --- ROW 2: TRENDS ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📈 Breach Rate Trend (Weekly)")
        trend_data = df_filtered.resample('W', on='Ticket_Date')['Is_SLA_Breach'].mean().reset_index()
        fig_trend = px.line(trend_data, x='Ticket_Date', y='Is_SLA_Breach', markers=True, 
                            labels={'Is_SLA_Breach': 'Breach Rate'}, line_shape='spline')
        fig_trend.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.subheader("💰 Financial Loss Trend (Weekly)")
        cost_trend = df_filtered.resample('W', on='Ticket_Date')['Breach_Cost'].sum().reset_index()
        fig_cost = px.bar(cost_trend, x='Ticket_Date', y='Breach_Cost', 
                          labels={'Breach_Cost': 'Lost Revenue ($)'})
        fig_cost.update_traces(marker_color='salmon')
        st.plotly_chart(fig_cost, use_container_width=True)

    # --- ROW 3: DRIVERS ---
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("⚠️ Breach Rate by Priority")
        prio_risk = df_filtered.groupby('Ticket Priority')['Is_SLA_Breach'].mean().reset_index().sort_values('Is_SLA_Breach', ascending=False)
        fig_prio = px.bar(prio_risk, x='Ticket Priority', y='Is_SLA_Breach', color='Is_SLA_Breach', 
                          color_continuous_scale='Reds')
        fig_prio.update_layout(yaxis_tickformat='.0%')
        st.plotly_chart(fig_prio, use_container_width=True)
        
    with col_r:
        st.subheader("📡 Breach Rate by Channel")
        chan_risk = df_filtered.groupby('Ticket Channel')['Is_SLA_Breach'].mean().reset_index().sort_values('Is_SLA_Breach', ascending=False)
        fig_chan = px.bar(chan_risk, x='Is_SLA_Breach', y='Ticket Channel', orientation='h',
                          color='Is_SLA_Breach', color_continuous_scale='OrRd')
        fig_chan.update_layout(xaxis_tickformat='.0%')
        st.plotly_chart(fig_chan, use_container_width=True)

    # --- ROW 4: HEATMAP & DRILLDOWN ---
    st.subheader("🔥 Risk Heatmap (Priority x Channel)")
    heatmap_data = df_filtered.pivot_table(index='Ticket Priority', columns='Ticket Channel', values='Is_SLA_Breach', aggfunc='mean')
    fig_heat = px.imshow(heatmap_data, text_auto='.0%', color_continuous_scale='RdYlGn_r', aspect="auto")
    st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("📋 Top Risk Drivers (Drilldown)")
    # Group by Type & Product to find pockets of failure
    drilldown = df_filtered.groupby(['Ticket Type', 'Product Purchased']).agg(
        Tickets=('Ticket ID', 'count'),
        Breach_Rate=('Is_SLA_Breach', 'mean'),
        Avg_Resolution=('Resolution_Hours', 'mean'),
        Total_Cost=('Breach_Cost', 'sum')
    ).reset_index()
    
    # Filter for significant volume
    drilldown = drilldown[drilldown['Tickets'] > 10].sort_values('Total_Cost', ascending=False).head(10)
    
    st.dataframe(
        drilldown.style.format({
            'Breach_Rate': '{:.1%}',
            'Avg_Resolution': '{:.1f} hrs',
            'Total_Cost': '${:,.0f}'
        }),
        use_container_width=True
    )
