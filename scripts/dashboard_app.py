import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Support Ops Risk Intelligence", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    file_path = 'data/customer_support_tickets.csv'
    if not os.path.exists(file_path):
        # Fallback for different working directories
        file_path = '../data/customer_support_tickets.csv'
    
    df = pd.read_csv(file_path)
    date_cols = ['First Response Time', 'Time to Resolution']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    
    # SLA Logic
    df['RPT_hours'] = abs((df['Time to Resolution'] - df['First Response Time']).dt.total_seconds() / 3600)
    sla_rules = {'Critical': 4, 'High': 12, 'Medium': 24, 'Low': 48}
    df['SLA_Target_Hours'] = df['Ticket Priority'].map(sla_rules)
    df['Is_SLA_Breach'] = (df['RPT_hours'] > df['SLA_Target_Hours']).astype(int)
    
    # Financial Impact
    cost_map = {'Critical': 50, 'High': 50, 'Medium': 10, 'Low': 10}
    df['Breach_Cost'] = df.apply(lambda x: cost_map[x['Ticket Priority']] if x['Is_SLA_Breach'] else 0, axis=1)
    
    return df

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Executive Filters")
priority_filter = st.sidebar.multiselect("Ticket Priority", options=df['Ticket Priority'].unique(), default=df['Ticket Priority'].unique())
type_filter = st.sidebar.multiselect("Ticket Type", options=df['Ticket Type'].unique(), default=df['Ticket Type'].unique())

filtered_df = df[(df['Ticket Priority'].isin(priority_filter)) & (df['Ticket Type'].isin(type_filter))]

# --- HEADER ---
st.title("🚀 Support Operations Risk Intelligence")
st.markdown("### Operational Governance & Financial Exposure Dashboard")

# --- TOP KPI STRIP ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("SLA Breach Rate", f"{filtered_df['Is_SLA_Breach'].mean():.2%}", delta_color="inverse")
with col2:
    st.metric("Financial Exposure", f"${filtered_df['Breach_Cost'].sum():,.0f}")
with col3:
    st.metric("Avg Resolution (HRS)", f"{filtered_df['RPT_hours'].mean():.1f}h")
with col4:
    st.metric("Total Breach Tickets", len(filtered_df[filtered_df['Is_SLA_Breach'] == 1]))

st.divider()

# --- CHARTS ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("Risk Concentration by Ticket Type")
    risk_type = filtered_df.groupby('Ticket Type')['Is_SLA_Breach'].mean().reset_index()
    fig = px.bar(risk_type, x='Ticket Type', y='Is_SLA_Breach', color='Is_SLA_Breach', 
                 title="Breach Probability by Category", color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

with row2_col2:
    st.subheader("Financial Impact by Priority")
    cost_pri = filtered_df.groupby('Ticket Priority')['Breach_Cost'].sum().reset_index()
    fig = px.pie(cost_pri, values='Breach_Cost', names='Ticket Priority', color_discrete_sequence=px.colors.sequential.RdBu,
                 title="Cumulative Service Credit Risk ($)")
    st.plotly_chart(fig, use_container_width=True)

# --- DAILY TRENDS ---
st.subheader("Daily SLA Breach Volume Trends")
df['Date'] = df['First Response Time'].dt.date
daily_trends = filtered_df.groupby(filtered_df['First Response Time'].dt.date)['Is_SLA_Breach'].sum().reset_index()
fig = px.line(daily_trends, x='First Response Time', y='Is_SLA_Breach', title="Historical SLA Breach Spikes")
st.plotly_chart(fig, use_container_width=True)

# --- ACTIONABLE RED LIST ---
st.divider()
st.subheader("📋 Operational 'Red List' (High Risk Tickets)")
st.write("Immediate intervention required for the following identified risks:")
red_list = filtered_df[filtered_df['Is_SLA_Breach'] == 1][['Ticket ID', 'Ticket Priority', 'Ticket Type', 'RPT_hours', 'Breach_Cost']].sort_values(by='Breach_Cost', ascending=False)
st.dataframe(red_list.head(20), use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Mid-Senior Analyst Portfolio: Project 2 Optimization Roadmap")
