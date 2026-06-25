import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

from st_aggrid import AgGrid
from st_aggrid import GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

from backend import *
from login import show_login



# PAGE CONFIG

st.set_page_config(
    page_title="MedCare Pro : Medicine Inventory Management",
    page_icon="🏥",
    layout="wide",
)


# LOGIN SYSTEM
 

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""
 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    show_login()
    st.stop()




if "inventory_df" not in st.session_state:
    st.session_state.inventory_df = load_data()

df = st.session_state.inventory_df
 

# CSS 

st.markdown("""
<style>
 
/*GLOBAL THEME */
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
 
.stApp {
    background:
    radial-gradient(circle at top left,#3b82f620,transparent 25%),
    radial-gradient(circle at top right,#8b5cf620,transparent 25%),
    linear-gradient(135deg,#07111f,#0f172a,#111827);
}
 
/* SIDEBAR */
 
.sidebar-header{
    text-align:center;
    font-size:22px;
    font-weight:700;
    color:white;
    margin-bottom:15px;
    padding:14px;
 
    background:linear-gradient(
        135deg,
        rgba(59,130,246,0.35),
        rgba(139,92,246,0.35)
    );
 
    border:1px solid rgba(96,165,250,0.25);
    border-radius:18px;
 
    backdrop-filter:blur(15px);
 
    box-shadow:
    0 8px 25px rgba(59,130,246,0.20);
}
 
.sidebar-card{
 
    background:
    linear-gradient(
        135deg,
        rgba(59,130,246,0.18),
        rgba(139,92,246,0.15)
    );
 
    border:1px solid rgba(96,165,250,0.20);
 
    border-radius:18px;
 
    padding:16px;
 
    margin-bottom:12px;
 
    backdrop-filter:blur(15px);
 
    box-shadow:
    0 8px 20px rgba(59,130,246,0.15);
 
    transition:0.3s;
}
 
.sidebar-card:hover{
 
    transform:translateY(-3px);
 
    box-shadow:
    0 12px 28px rgba(96,165,250,0.25);
 
    border:1px solid rgba(96,165,250,0.35);
}
 
.sidebar-label{
 
    color:#bfdbfe;
 
    font-size:11px;
 
    letter-spacing:1.2px;
 
    font-weight:700;
}
 
.sidebar-value{
 
    color:white;
 
    font-size:26px;
 
    font-weight:800;
 
    margin-top:6px;
 
    text-shadow:
    0 0 10px rgba(96,165,250,0.4);
}
 
[data-testid="stSidebar"]{
 
    background:
    radial-gradient(circle at top left,
        rgba(59,130,246,0.25),
        transparent 35%
    ),
    radial-gradient(circle at bottom right,
        rgba(139,92,246,0.25),
        transparent 35%
    ),
    linear-gradient(
        180deg,
        #07111f,
        #0f172a,
        #111827
    );
 
    border-right:1px solid rgba(96,165,250,0.15);
 
    box-shadow:
    inset -1px 0 0 rgba(255,255,255,0.05),
    10px 0 30px rgba(59,130,246,0.10);
}
            
/*HERO CARD */
 
.hero-card{
    position:relative;
    overflow:hidden;
 
    background:rgba(255,255,255,0.08);
 
    backdrop-filter:blur(16px);
 
    border:1px solid rgba(255,255,255,0.12);
 
    border-radius:28px;
 
    padding:35px;
 
    margin-bottom:25px;
 
    box-shadow:
    0 10px 40px rgba(0,0,0,.35);
}
 
.hero-card:before{
    content:"";
    position:absolute;
    width:400px;
    height:400px;
    background:radial-gradient(
        #60a5fa,
        transparent 70%
    );
    top:-150px;
    right:-150px;
    opacity:.15;
}
 
.hero-title{
    font-size:42px;
    font-weight:800;
 
    background:
    linear-gradient(
    90deg,
    #60a5fa,
    #a855f7,
    #22c55e
    );
 
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
 
.hero-sub{
    color:#cbd5e1;
    font-size:15px;
}
 
/*
   KPI CARDS */
 
.kpi-card{
    background:rgba(255,255,255,0.07);
 
    backdrop-filter:blur(15px);
 
    border-radius:24px;
 
    padding:22px;
 
    transition:0.3s;
 
    border:1px solid rgba(255,255,255,.08);
 
    box-shadow:
    0px 10px 25px rgba(0,0,0,.25);
}
 
.kpi-card:hover{
    transform:translateY(-6px) scale(1.02);
    box-shadow:
    0 15px 35px rgba(96,165,250,.2);
}
 
.kpi-title{
    color:#94a3b8;
    font-size:13px;
}
 
.kpi-value{
    font-size:clamp(18px,2vw,34px);
    font-weight:800;
    color:white;
    white-space:nowrap;
}
 
.green{
    border-left:5px solid #22c55e;
}
 
.red{
    border-left:5px solid #ef4444;
}
 
.yellow{
    border-left:5px solid #facc15;
}
 
.blue{
    border-left:5px solid #60a5fa;
}
 
.purple{
    border-left:5px solid #a855f7;
}
            
/* SECTION HEADERS */
 
.section-header{
    font-size:24px;
    font-weight:700;
    color:white;
 
    margin-top:20px;
    margin-bottom:15px;
 
    padding-bottom:10px;
 
    border-bottom:
    1px solid rgba(255,255,255,.08);
}
 
/*ALERT CARDS */
 
.alert-card{
    border-radius:18px;
    padding:20px;
    color:white;
    text-align:center;
    font-weight:600;
    cursor:pointer;
 
    transition:all 0.3s ease;
}
 
.alert-card:hover{
    transform:translateY(-8px) scale(1.02);
 
    box-shadow:
    0 15px 35px rgba(255,255,255,0.15);
 
    filter:brightness(1.1);
}
 
.alert-red{
    background:linear-gradient(135deg,#991b1b,#dc2626);
}
 
.alert-yellow{
    background:linear-gradient(135deg,#92400e,#f59e0b);
}
 
.alert-green{
    background:linear-gradient(135deg,#14532d,#22c55e);
}
 
/*TABLES */
 
[data-testid="stDataFrame"]{
    border-radius:20px;
    overflow:hidden;
    border:1px solid rgba(255,255,255,.08);
}
 
/*BUTTONS */
 
.stButton button,
.stDownloadButton button{
 
    border:none !important;
 
    border-radius:14px !important;
 
    background:
    linear-gradient(
    135deg,
    #3b82f6,
    #8b5cf6
    ) !important;
 
    color:white !important;
 
    font-weight:700 !important;
 
    transition:.3s !important;
}
 
.stButton button:hover,
.stDownloadButton button:hover{
 
    transform:translateY(-2px);
 
    box-shadow:
    0 10px 25px rgba(96,165,250,.4);
}
 
/*FOOTER */
 
.footer-card{
    background:rgba(255,255,255,0.06);
    backdrop-filter:blur(14px);
    border-radius:24px;
    padding:30px;
    text-align:center;
    border:1px solid rgba(255,255,255,.08);
}
 
/*ANIMATION */
 
@keyframes float {
    0%{
        transform:translateY(0px);
    }
    50%{
        transform:translateY(-4px);
    }
    100%{
        transform:translateY(0px);
    }
}
 
.hero-card{
    animation:float 5s ease-in-out infinite;
}
 
</style>
""", unsafe_allow_html=True)


# HEADER

st.markdown("""
<style>
 
.ticker-container{
    width:100%;
    overflow:hidden;
    white-space:nowrap;
    margin-top:15px;
}
 
.ticker-text{
    display:inline-block;
    padding-left:100%;
    color:#cbd5e1;
    font-size:15px;
    font-weight:500;
    animation:scrollText 25s linear infinite;
}
 
@keyframes scrollText{
    0%{
        transform:translateX(0%);
    }
    100%{
        transform:translateX(-100%);
    }
}
 
</style>
 
<div style="
background:rgba(255,255,255,0.08);
padding:30px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.1);
text-align:center;
overflow:hidden;
">
 
<h4 style="
color:white;
font-size:42px;
font-weight:800;
">
MedCare Pro : Medicine Inventory Management 
</h4>
 
<div class="ticker-container">
 
<div class="ticker-text">
 
 Inventory Monitoring &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
 Smart Reordering &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
 Expiry Prediction &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
 Supplier Intelligence &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
 Inventory Health Analytics &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
 Real-Time Monitoring &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
 Automated Healthcare Insights
 
</div>
 
</div>
 
</div>
""", unsafe_allow_html=True)

st.markdown("---")

low_stock_df, expiring_df, expired_df = (
    get_inventory_alerts(df)
)



st.sidebar.success(
    f"Logged in as : {st.session_state.username}"
)
st.sidebar.markdown("---")


# PROFESSIONAL SIDEBAR
 
st.sidebar.markdown(
"""
<div class="sidebar-header">
Inventory Control Center
</div>
""",
unsafe_allow_html=True
)
 
st.sidebar.markdown(
f"""
<div class="sidebar-card">
<div class="sidebar-label">TOTAL MEDICINES</div>
<div class="sidebar-value">{len(df):,}</div>
</div>
""",
unsafe_allow_html=True
)
 
st.sidebar.markdown(
f"""
<div class="sidebar-card">
<div class="sidebar-label">SUPPLIERS</div>
<div class="sidebar-value">{df["Supplier"].nunique()}</div>
</div>
""",
unsafe_allow_html=True
)
 
st.sidebar.markdown(
f"""
<div class="sidebar-card">
<div class="sidebar-label">CATEGORIES</div>
<div class="sidebar-value">{df["Category"].nunique()}</div>
</div>
""",
unsafe_allow_html=True
)
 
st.sidebar.markdown(
f"""
<div class="sidebar-card">
<div class="sidebar-label">INVENTORY VALUE</div>
<div class="sidebar-value">{format_currency(df["Total_Value"].sum())}</div>
</div>
""",
unsafe_allow_html=True
)
 
st.sidebar.markdown("---")
 

# Filters

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)
 
selected_supplier = st.sidebar.selectbox(
    "Supplier",
    ["All"] + sorted(df["Supplier"].unique().tolist())
)
 
stock_status = st.sidebar.selectbox(
    "Stock Status",
    [
        "All",
        "Low Stock",
        "Healthy Stock"
    ]
)
 
expiry_status = st.sidebar.selectbox(
    "Expiry Status",
    [
        "All",
        "Expired",
        "Expiring Soon",
        "Safe"
    ]
)
 
 
if st.sidebar.button("Logout"):
 
    st.session_state.logged_in = False
 
    st.session_state.username = ""
 
    st.rerun()
st.sidebar.markdown("---")
filtered_df = apply_filters(
    df,
    selected_category,
    selected_supplier,
    stock_status,
    expiry_status
)

kpis = calculate_kpis(filtered_df)

total_items = kpis["total_items"]
inventory_value = kpis["inventory_value"]
low_stock = kpis["low_stock"]
expiring = kpis["expiring"]
expired = kpis["expired"]
healthy_items = kpis["healthy_items"]


# KPI CARDS

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card blue">
            <div class="kpi-title">TOTAL ITEMS</div>
            <div class="kpi-value">{total_items}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card green">
            <div class="kpi-title">HEALTHY</div>
            <div class="kpi-value">{healthy_items}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card yellow">
            <div class="kpi-title">EXPIRING</div>
            <div class="kpi-value">{expiring}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card red">
            <div class="kpi-title">LOW STOCK</div>
            <div class="kpi-value">{low_stock}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k5:
    st.markdown(
        f"""
        <div class="kpi-card purple">
            <div class="kpi-title">VALUE</div>
            <div class="kpi-value">{format_currency(inventory_value)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("---")
st.sidebar.success("🟢 System Status: Online")
def apply_dashboard_theme(fig, height=450):

    fig.update_layout(
        template="plotly_dark",
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        transition_duration=1500,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    )

    return fig


# CHARTS

category_chart, supplier_value = get_chart_data(filtered_df)

col1,col2 = st.columns(2)

with col1:

    st.subheader("Inventory by Category")

    fig = px.bar(
        category_chart,
        x="Category",
        y="Quantity",
        color="Quantity",
        color_continuous_scale="blues"
    )

    fig = apply_dashboard_theme(fig, 500)

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("Inventory Value Distribution")

    fig2 = px.pie(
        supplier_value,
        names="Supplier",
        values="Total_Value",
        hole=0.55
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        transition_duration=1500
    )

    st.plotly_chart(fig2, use_container_width=True)


# EXPIRY ANALYTICS

expiry_data = get_expiry_data(filtered_df)

st.subheader("Expiry Analytics")

fig3 = px.line(
    expiry_data,
    x="Category",
    y="Days_To_Expiry",
    markers=True
)

fig3.update_layout(
    template="plotly_dark",
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    transition_duration=1500,
    hovermode="x unified"
)

fig3.update_xaxes(
    gridcolor="rgba(255,255,255,0.08)"
)

fig3.update_yaxes(
    gridcolor="rgba(255,255,255,0.08)"
)

st.plotly_chart(fig3, use_container_width=True)


# STOCK HEALTH SCORE

st.subheader("Inventory Health Score")

health_score = calculate_health_score(
    total_items,
    low_stock,
    expired
)

st.markdown(
f"""
<h1 style='
color:#22c55e;
font-size:50px;
text-align:center;
'>
{health_score:.1f}%
</h1>
""",
unsafe_allow_html=True
)

st.progress(int(health_score))

st.success(
    f"Current Inventory Health Score: {health_score:.2f}%"
)


# AI REORDER RECOMMENDATIONS

st.subheader("Reorder Recommendations")

reorder_df = get_reorder_recommendations(
    filtered_df
)

if not reorder_df.empty:

    st.dataframe(
        reorder_df[
            [
                "Medicine",
                "Supplier",
                "Quantity",
                "Min_Stock",
                "Recommended_Order"
            ]
        ],
        use_container_width=True
    )

else:
    st.success("No Reorder Required")


# TOP VALUABLE MEDICINES

st.subheader("Top 10 High Value Medicines")

top10 = get_top10_medicines(filtered_df)

st.dataframe(
    top10[
        [
            "Medicine",
            "Category",
            "Quantity",
            "Unit_Price",
            "Total_Value"
        ]
    ],
    use_container_width=True
)


# SUPPLIER PERFORMANCE

st.subheader("Supplier Analytics")

supplier_summary = get_supplier_summary(
    filtered_df
)

st.dataframe(
    supplier_summary,
    use_container_width=True
)

bubble_chart = px.scatter(
    supplier_summary,
    x="Product_Count",
    y="Inventory_Value",
    size="Total_Inventory",
    color="Inventory_Value",
    hover_name="Supplier",
    size_max=80,
    color_continuous_scale=[
        "#3b82f6",
        "#6366f1",
        "#8b5cf6",
        "#ec4899"
    ]
)

bubble_chart.update_traces(
    marker=dict(
        sizemode="area",
        line=dict(
            width=2,
            color="white"
        ),
        opacity=0.85
    )
)

bubble_chart.update_layout(
    template="plotly_dark",
    height=700,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    bubble_chart,
    use_container_width=True
)


# INVENTORY DATABASE CENTER

st.markdown(
    '<div class="section-header">Inventory Database Center</div>',
    unsafe_allow_html=True
)

db_df = prepare_database_view(filtered_df)

gb = GridOptionsBuilder.from_dataframe(db_df)

gb.configure_pagination(
    paginationAutoPageSize=False,
    paginationPageSize=15
)

gb.configure_side_bar()

gb.configure_default_column(
    sortable=True,
    filter=True,
    resizable=True,
    floatingFilter=True
)

gb.configure_selection(
    "single",
    use_checkbox=True
)

gb.configure_column(
    "Total_Value",
    type=["numericColumn"]
)

gb.configure_column(
    "Unit_Price",
    type=["numericColumn"]
)

gb.configure_column(
    "Quantity",
    type=["numericColumn"]
)

grid_options = gb.build()

AgGrid(
    db_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    fit_columns_on_grid_load=True,
    height=650,
    allow_unsafe_jscode=True,
    theme="streamlit"
)


# DOWNLOAD REPORT

st.subheader("Export Inventory Report")

csv = generate_csv(filtered_df)

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="inventory_report.csv",
    mime="text/csv"
)


# FOOTER

st.markdown("---")
st.markdown("""
<div class="footer-card">
© 2026 Healthcare Automation Suite | Enterprise level Inventory Solution
</div>
""", unsafe_allow_html=True)