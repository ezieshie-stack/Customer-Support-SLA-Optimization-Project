
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SLA Intelligence Suite",
    page_icon="🤖",
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
    file_path = "customer_support_sla_dashboard.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # Fallback to outputs folder if running locally
        try:
             df = pd.read_csv("outputs/dashboard/customer_support_sla_dashboard.csv")
        except:
             import os
             st.error(f"❌ Data file not found. Current Directory: {os.getcwd()}")
             st.error(f"Files in root: {os.listdir('.')}")
             return None
            
    df['Ticket_Date'] = pd.to_datetime(df['Ticket_Date'])
    return df

df = load_data()

if df is not None:
    st.title("🤖 SLA Intelligence & Decision Suite")
    st.markdown("**Project Goal:** Minimize financial loss from SLA breaches using predictive AI.")
    
    # --- TABS FOR STORYTELLING ---
    tab1, tab2 = st.tabs(["📊 Strategic Context (The Problem)", "🎯 Sniper Command Center (The Solution)"])

    # ==============================================================================
    # TAB 1: STRATEGIC CONTEXT (DIAGNOSTICS)
    # ==============================================================================
    with tab1:
        st.header("1. Diagnostic Intelligence")
        st.markdown("Understanding *where* and *why* we are losing money.")
        st.markdown("---")
        
        # KPIS
        col1, col2, col3, col4 = st.columns(4)
        total_loss = df['Breach_Cost'].sum()
        breach_rate = df['Is_SLA_Breach'].mean()
        high_risk_vol = len(df[df['Ticket Priority'] == 'Critical'])
        
        col1.metric("Total Financial Exposure", f"${total_loss:,.0f}", delta_color="inverse")
        col2.metric("Overall Breach Rate", f"{breach_rate:.1%}", delta_color="inverse")
        col3.metric("Critical Volume", f"{high_risk_vol:,}")
        col4.metric("Audited Tickets", f"{len(df):,}")
        
        st.markdown("---")
        
        # ROW 1: PRIORITY vs CHANNEL
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("⚠️ Breach Rate by Priority")
            prio_data = df.groupby("Ticket Priority")['Is_SLA_Breach'].mean().reset_index()
            fig_prio = px.bar(prio_data, x="Ticket Priority", y="Is_SLA_Breach", color="Is_SLA_Breach", 
                              color_continuous_scale="Reds", title="Critical Tickets Fail Most Often")
            fig_prio.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig_prio, use_container_width=True)
            
        with c2:
            st.subheader("📡 Breach Rate by Channel")
            chan_data = df.groupby("Ticket Channel")['Is_SLA_Breach'].mean().reset_index()
            fig_chan = px.bar(chan_data, x="Ticket Channel", y="Is_SLA_Breach", color="Is_SLA_Breach",
                              color_continuous_scale="OrRd", title="Channel Impact is Negligible (Myth Busted)")
            fig_chan.update_layout(yaxis_tickformat=".0%")
            st.plotly_chart(fig_chan, use_container_width=True)
            
        # ROW 2: FINANCIAL TREND
        st.subheader("💰 Weekly Cost of Failure Trend")
        cost_trend = df.resample('W', on='Ticket_Date')['Breach_Cost'].sum().reset_index()
        fig_trend = px.area(cost_trend, x='Ticket_Date', y='Breach_Cost', 
                            title="Accumulated Financial Loss Over Time (Baseline)", markers=True)
        fig_trend.update_traces(line_color="#e74c3c")
        st.plotly_chart(fig_trend, use_container_width=True)

    # ==============================================================================
    # TAB 2: OPERATIONAL COMMAND (THE SNIPER)
    # ==============================================================================
    with tab2:
        st.header("2. Operational Intervention")
        st.markdown("Deploying 'The Sniper' model to intercept high-risk tickets *before* they breach.")
        
        # --- SIDEBAR CONTROLS MOVED HERE FOR CONTEXT ---
        st.markdown("#### ⚙️ Configuration")
        col_ctrl1, col_ctrl2 = st.columns(2)
        
        with col_ctrl1:
            capacity = st.select_slider(
                "Daily Escalation Capacity (Tickets/Day)",
                options=[10, 25, 50, 75, 100, "All"],
                value=50,
                key="capacity_slider"
            )
            
        with col_ctrl2:
            intervention_cost = st.number_input("Intervention Cost per Ticket ($)", value=2, min_value=0)

        st.markdown("---")
        
        # --- SIMULATION LOGIC ---
        total_dates = df['Ticket_Date'].nunique()
        baseline_loss = df['Breach_Cost'].sum()
        sim_df = df.copy()
        
        def apply_sniper_logic(group):
            group = group.sort_values('Pred_Breach_Prob', ascending=False)
            group['Flagged'] = False
            limit = len(group) if capacity == "All" else int(capacity)
            if len(group) > 0:
                group.iloc[:limit, group.columns.get_loc('Flagged')] = True
            return group

        sim_df = sim_df.groupby('Ticket_Date', group_keys=False).apply(apply_sniper_logic)
        
        flagged_tickets = sim_df[sim_df['Flagged']]
        caught_breaches = flagged_tickets[flagged_tickets['Is_SLA_Breach'] == True]
        
        tickets_reviewed = len(flagged_tickets)
        breaches_prevented = len(caught_breaches)
        operational_cost = tickets_reviewed * intervention_cost
        gross_savings = caught_breaches['Breach_Cost'].sum()
        net_savings = gross_savings - operational_cost
        roi = (net_savings / operational_cost) if operational_cost > 0 else 0

        # --- ROI METRICS ---
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🔍 Targeted Reviews", f"{tickets_reviewed:,}")
        c2.metric("🛡️ Breaches Prevented", f"{breaches_prevented:,}")
        c3.metric("💸 Operations Cost", f"${operational_cost:,.0f}")
        c4.metric("💰 NET SAVINGS", f"${net_savings:,.0f}", delta=f"{roi:.1f}x ROI")
        
        st.markdown("---")

        # --- RISK CURVE ---
        st.subheader("Why 'Top 50'? (The Risk Capture Curve)")
        sorted_risk = df.sort_values('Pred_Breach_Prob', ascending=False)
        sorted_risk['Cumulative_Cost'] = sorted_risk['Breach_Cost'].cumsum()
        sorted_risk['Total_Cost'] = sorted_risk['Breach_Cost'].sum()
        sorted_risk['Pct_Captured'] = sorted_risk['Cumulative_Cost'] / sorted_risk['Total_Cost']
        sorted_risk['Tickets_Reviewed'] = range(1, len(sorted_risk) + 1)
        
        chart_data = sorted_risk.iloc[::10, :][['Tickets_Reviewed', 'Pct_Captured']]
        fig_curve = px.area(chart_data, x='Tickets_Reviewed', y='Pct_Captured',
                            labels={'Pct_Captured': '% Risk Captured'},
                            title="Diminishing Returns: 80% of Risk is in the Top 20% of Tickets")
        if capacity != "All":
             fig_curve.add_vline(x=int(capacity)*total_dates, line_dash="dash", line_color="red", annotation_text="Limit")
        st.plotly_chart(fig_curve, use_container_width=True)

        # --- LIVE LIST ---
        st.subheader("📋 Live Daily 'Kill List'")
        latest_date = sim_df['Ticket_Date'].max()
        todays_list = sim_df[(sim_df['Ticket_Date'] == latest_date) & (sim_df['Flagged'])].sort_values('Pred_Breach_Prob', ascending=False)
        
        st.dataframe(
            todays_list[['Ticket ID', 'Ticket Priority', 'Pred_Breach_Prob', 'Breach_Cost']].style.format({
                'Pred_Breach_Prob': '{:.1%}',
                'Breach_Cost': '${:,.0f}'
            }).background_gradient(subset=['Pred_Breach_Prob'], cmap='Reds'),
            use_container_width=True
        )
