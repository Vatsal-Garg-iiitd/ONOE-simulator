import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# --- 1. PAGE CONFIGURATION & DARK THEME CSS ---
st.set_page_config(layout="wide", page_title="ONOE Financial Dashboard", page_icon="🗳️")

# Custom CSS for Dark Mode
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Metric Cards */
    .metric-container {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        text-align: center;
        border-left: 5px solid #4e73df;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #FFFFFF;
    }
    .metric-label {
        font-size: 14px;
        color: #A0A0A0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-delta {
        font-size: 14px;
        font-weight: bold;
        margin-top: 5px;
    }
    
    /* Text Colors */
    .positive { color: #00CC96; } /* Green */
    .negative { color: #EF553B; } /* Red */
    .neutral  { color: #A0A0A0; } /* Grey */
    
    /* Remove white background from charts if any remains */
    .js-plotly-plot .plotly .main-svg {
        background: rgba(0,0,0,0) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA PROCESSING ---
@st.cache_data
def load_data():
    csv_data = """Task_ID,Task_Name,Category,Sub_Unit_Details,Unit_Cost_INR,Quantity_LS_Only,Cost_LS_Only_Cr,Quantity_State_Only,Cost_State_Only_Cr,Quantity_ONOE,Cost_ONOE_Cr,Impact_Note
1,EVM & VVPAT Procurement,Capital,"Set (BU+CU+VVPAT)",34000,13 Lakh Sets,4420,13 Lakh Sets,4420,26 Lakh Sets,8840,Requires double inventory immediately
2,Warehousing Infrastructure,Capital,"Construction (per unit)",2000000,Existing Stock,0,Existing Stock,0,2x Capacity,1200,New strong rooms needed for double EVM volume
3,Polling Staff Remuneration,Operational,"Team Wages (per booth)",15000,1.5 Cr Staff,1800,1.5 Cr Staff,1800,1.5 Cr Staff,2000,Staff is shared but allowances slightly higher
4,Security Deployment (CAPF),Operational,"Company Deployment",25000000,4000 Companies,2500,Varies by State,2500,4000 Companies,2500,Major saving: Forces move once instead of twice
5,Logistics & Transport,Operational,"Vehicle Rent (per day)",3000,12 Lakh Vehicles,1200,12 Lakh Vehicles,1200,12 Lakh Vehicles,1300,Same trucks can carry both machines
6,Polling Station Setup,Operational,"Booth Setup (Tents/Power)",4000,12 Lakh Booths,480,12 Lakh Booths,480,12 Lakh Booths,500,Physical booth structure is shared
7,IT Infrastructure,Operational,"Webcast & GPS (per booth)",1500,6 Lakh Booths (50%),200,6 Lakh Booths (50%),200,6 Lakh Booths (50%),220,Webcasting equipment shared for both polls
8,Training Material,Operational,"Training Kit (per team)",700,12 Lakh Teams,100,12 Lakh Teams,100,12 Lakh Teams,120,Combined manuals and training sessions
9,Voter Awareness (SVEEP),Operational,"National Campaign",NA,National Scale,150,State Scale,150,Combined Scale,150,Unified message saves duplicate ad spend
10,VVPAT Slip Storage,Logistics,"Storage (per vault/yr)",5000,12 Months,50,12 Months,50,2x Volume,100,Double paper trail volume requires larger vaults
11,Ex-Gratia Compensation,Contingency,"Death/Injury (Avg)",2500000,Est 100 Cases,25,Est 100 Cases,25,Est 100 Cases,25,Risk exposure reduced (travel once)
12,Counting Centers,Infrastructure,"Hall Setup (per hall)",500000,4000 Halls,200,4000 Halls,200,Larger Halls,300,Needs double tables or double time
13,Observers (IAS/IPS),Admin,"Allowance (per person)",150000,3000 Observers,50,3000 Observers,50,3000 Observers,50,Same observers monitor both elections
14,Videography/CCTV,Surveillance,"Camera Rent (per day)",3000,Critical Booths,150,Critical Booths,150,Critical Booths,150,Same surveillance coverage utilized
15,E-Waste Disposal,Lifecycle,"Destruction (per unit)",500,Cyclic (15 yrs),10,Cyclic (15 yrs),10,Double Volume,20,Higher long-term environmental cost
16,Contingency Fund,Contingency,"Lump Sum",NA,Standard,100,Standard,100,Standard,100,Standard contingency"""
    
    df = pd.read_csv(io.StringIO(csv_data))
    
    def calculate_normal(row):
        if row['Category'] in ['Capital', 'Lifecycle']:
            return row['Cost_LS_Only_Cr']
        return row['Cost_LS_Only_Cr'] + row['Cost_State_Only_Cr']

    df['Normal_Cycle_Cost'] = df.apply(calculate_normal, axis=1)
    df['Difference'] = df['Cost_ONOE_Cr'] - df['Normal_Cycle_Cost']
    
    # Simplified Categories
    df['Type'] = df['Category'].apply(lambda x: 'Capital (Assets)' if x in ['Capital', 'Infrastructure', 'Logistics'] else 'Operational (Running)')
    
    return df

df = load_data()

# --- 3. METRIC CARDS SECTION ---
st.title("🇮🇳 One Nation One Election: Financial Impact")
st.markdown("### Executive Summary")

total_normal = df['Normal_Cycle_Cost'].sum()
total_onoe = df['Cost_ONOE_Cr'].sum()
diff_val = total_onoe - total_normal
pct_change = (diff_val / total_normal) * 100

col1, col2, col3, col4 = st.columns(4)

def metric_card(label, value, delta_text, delta_color):
    return f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta {delta_color}">{delta_text}</div>
    </div>
    """

with col1:
    st.markdown(metric_card("Standard 5-Year Cost", f"₹ {total_normal:,.0f} Cr", "Benchmark", "neutral"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("ONOE Cost", f"₹ {total_onoe:,.0f} Cr", "Simultaneous", "neutral"), unsafe_allow_html=True)
with col3:
    display_diff = f"Savings: ₹ {abs(diff_val):,.0f} Cr" if diff_val < 0 else f"Cost: ₹ {diff_val:,.0f} Cr"
    st.markdown(metric_card("Net Impact", display_diff, f"{pct_change:.2f}% Change", "positive"), unsafe_allow_html=True)
with col4:
    st.markdown(metric_card("Operational Efficiency", "45% Savings", "On Running Costs", "positive"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. DARK MODE CHARTS ---

# --- CHART 1: NEON WATERFALL BRIDGE ---
st.subheader("1. The Financial Bridge")
st.caption("How do we get from Standard Cost to ONOE Cost? (Green = Savings, Red = New Expense)")

ops_savings = df[df['Difference'] < 0]['Difference'].sum()
cap_increase = df[df['Difference'] > 0]['Difference'].sum()

fig_waterfall = go.Figure(go.Waterfall(
    name = "Financial Bridge", orientation = "v",
    measure = ["relative", "relative", "relative", "total"],
    x = ["Standard Cost", "Operational Savings", "Capital Spike", "ONOE Final Cost"],
    text = [f"₹{total_normal/1000:.1f}k", f"-₹{abs(ops_savings)/1000:.1f}k", f"+₹{cap_increase/1000:.1f}k", f"₹{total_onoe/1000:.1f}k"],
    textposition = "outside",
    y = [total_normal, ops_savings, cap_increase, 0],
    connector = {"line":{"color":"#A0A0A0"}}, # Light grey connectors
    increasing = {"marker":{"color":"#EF553B"}}, # Neon Red
    decreasing = {"marker":{"color":"#00CC96"}}, # Neon Green
    totals = {"marker":{"color":"#636EFA"}}      # Neon Blue
))

fig_waterfall.update_layout(
    template="plotly_dark",
    height=450,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Arial", size=12, color="#FAFAFA"),
    yaxis=dict(title="Cost (₹ Crores)", showgrid=True, gridcolor='#333333'),
    xaxis=dict(showgrid=False)
)
st.plotly_chart(fig_waterfall, use_container_width=True)


# --- CHART 2: SIDE-BY-SIDE TORNADO ---
st.subheader("2. Task-by-Task Comparison")
st.caption("Side-by-side cost comparison. Notice the massive drop in Operational tasks (Security, Staff) vs the spike in Capital (EVMs).")

df_compare = df[['Task_Name', 'Normal_Cycle_Cost', 'Cost_ONOE_Cr']].copy()
df_compare['Task_Name'] = df_compare['Task_Name'].apply(lambda x: x.split('(')[0].strip()) 

fig_bar = go.Figure()

# Standard Bars (Blue)
fig_bar.add_trace(go.Bar(
    y=df_compare['Task_Name'],
    x=df_compare['Normal_Cycle_Cost'],
    name='Standard Cycle',
    orientation='h',
    marker=dict(color='#636EFA'), 
    text=df_compare['Normal_Cycle_Cost'].apply(lambda x: f"₹{x}"),
    textposition='auto'
))

# ONOE Bars (Orange/Red)
fig_bar.add_trace(go.Bar(
    y=df_compare['Task_Name'],
    x=df_compare['Cost_ONOE_Cr'],
    name='ONOE Cycle',
    orientation='h',
    marker=dict(color='#EF553B'),
    text=df_compare['Cost_ONOE_Cr'].apply(lambda x: f"₹{x}"),
    textposition='auto'
))

fig_bar.update_layout(
    template="plotly_dark",
    barmode='group',
    height=700,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color="#FAFAFA"),
    legend=dict(orientation="h", y=1.02, x=0.5, xanchor='center'),
    xaxis=dict(title="Cost (₹ Crores)", showgrid=True, gridcolor='#333333'),
    yaxis=dict(autorange="reversed")
)
st.plotly_chart(fig_bar, use_container_width=True)


# --- CHART 3: STRUCTURE SHIFT (Donuts) ---
st.subheader("3. The Structural Shift")
st.caption("The nature of spending changes from 'Burning Money' (Operational) to 'Buying Assets' (Capital).")

col_d1, col_d2 = st.columns(2)
colors = {'Capital (Assets)': '#EF553B', 'Operational (Running)': '#636EFA'}

# Common layout settings for donuts
donut_layout = dict(
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    margin=dict(t=50, b=10, l=10, r=10),
    font=dict(color="#FAFAFA")
)

with col_d1:
    fig_d1 = px.pie(df, values='Normal_Cycle_Cost', names='Type', 
                    title=f"Standard Cycle<br>(Total: ₹{total_normal:,.0f} Cr)",
                    color='Type', color_discrete_map=colors, hole=0.5)
    fig_d1.update_traces(textposition='inside', textinfo='percent+label')
    fig_d1.update_layout(**donut_layout)
    st.plotly_chart(fig_d1, use_container_width=True)

with col_d2:
    fig_d2 = px.pie(df, values='Cost_ONOE_Cr', names='Type', 
                    title=f"ONOE Cycle<br>(Total: ₹{total_onoe:,.0f} Cr)",
                    color='Type', color_discrete_map=colors, hole=0.5)
    fig_d2.update_traces(textposition='inside', textinfo='percent+label')
    fig_d2.update_layout(**donut_layout)
    st.plotly_chart(fig_d2, use_container_width=True)

# Data Table with Dark Theme Styling
with st.expander("📄 View & Download Raw Data"):
    st.dataframe(df.style.background_gradient(subset=['Difference'], cmap='RdYlGn_r'), use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV Data", csv, "onoe_data.csv", "text/csv")