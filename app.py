import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

.main {
    background-color: #f3f4f6;
}

.block-container {
    padding-top: 2rem;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #111827,
        #1f2937
    );
}

div[data-testid="stSidebar"] * {
    color: white;
}

.chart-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- PREMIUM HEADER ---------------- #

st.markdown("""
<div style="
    background: linear-gradient(90deg,#667eea,#764ba2);
    padding:25px;
    border-radius:20px;
    text-align:center;
    color:white;
    box-shadow:0 8px 20px rgba(0,0,0,0.2);
">

<h1 style="margin-bottom:5px;">
📊 Business Analytics Dashboard
</h1>

<p style="font-size:18px;">
Real-time Sales & Profit Insights
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.markdown("""
<h2 style='text-align:center; color:black;'>
🍭 Nassau Candy
</h2>

<p style='text-align:center; color:black;'>
Analytics Platform
</p>

<hr>
""", unsafe_allow_html=True)

st.sidebar.title("🔍 Filters")

division = st.sidebar.selectbox(
    "Select Division",
    ["All", "Chocolate", "Sugar", "Other"]
)

margin = st.sidebar.slider(
    "Margin Threshold",
    0,
    100,
    20
)

product = st.sidebar.text_input(
    "Search Product"
)

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv(
    r"C:\Users\hp\Videos\project\nassau_candy.csv"
)

# ---------------- DATE CONVERSION ---------------- #

df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    format='mixed',
    dayfirst=True
)

# ---------------- DATE FILTER ---------------- #

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(
        df['Order Date'].min(),
        df['Order Date'].max()
    )
)

# ---------------- DATA CLEANING ---------------- #

df['Gross Profit'] = df['Gross Profit'].fillna(0)

df['Sales'] = df['Sales'].fillna(1)

df['Gross Margin %'] = (
    df['Gross Profit'] / df['Sales']
) * 100

# ---------------- FILTERS ---------------- #

filtered_df = df.copy()

# DIVISION FILTER
if division != "All":
    filtered_df = filtered_df[
        filtered_df['Division'] == division
    ]

# DATE FILTER
if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])

    end_date = pd.to_datetime(
        date_range[1]
    ) + pd.Timedelta(days=1)

    filtered_df = filtered_df[
        (filtered_df['Order Date'] >= start_date) &
        (filtered_df['Order Date'] < end_date)
    ]

# MARGIN FILTER
filtered_df = filtered_df[
    filtered_df['Gross Margin %'] >= margin
]

# PRODUCT SEARCH
if product:
    filtered_df = filtered_df[
        filtered_df['Product Name'].str.contains(
            product,
            case=False
        )
    ]

# ---------------- METRICS ---------------- #

total_sales = filtered_df['Sales'].sum()

total_profit = filtered_df['Gross Profit'].sum()

avg_margin = filtered_df[
    'Gross Margin %'
].mean()

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#36d1dc,#5b86e5);
        padding:25px;
        border-radius:20px;
        color:white;
        box-shadow:0 4px 15px rgba(0,0,0,0.2);
    ">
        <h4>💰 Total Sales</h4>
        <h2>${total_sales:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#11998e,#38ef7d);
        padding:25px;
        border-radius:20px;
        color:white;
        box-shadow:0 4px 15px rgba(0,0,0,0.2);
    ">
        <h4>📈 Total Profit</h4>
        <h2>${total_profit:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#fc466b,#3f5efb);
        padding:25px;
        border-radius:20px;
        color:white;
        box-shadow:0 4px 15px rgba(0,0,0,0.2);
    ">
        <h4>📊 Avg Margin</h4>
        <h2>{avg_margin:.2f}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- PROGRESS BAR ---------------- #

st.subheader("🎯 Profit Target Progress")

progress = min(int(avg_margin), 100)

st.progress(progress)

st.write(f"{progress}% Target Achieved")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- DATASET ---------------- #

with st.container():

    st.markdown("""
    <div class='chart-card'>
    """, unsafe_allow_html=True)

    st.subheader("📋 Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- LEADERBOARD ---------------- #

leaderboard = filtered_df.groupby(
    'Product Name'
).agg({
    'Sales':'sum',
    'Gross Profit':'sum',
    'Gross Margin %':'mean'
}).sort_values(
    by='Gross Margin %',
    ascending=False
)

with st.container():

    st.markdown("""
    <div class='chart-card'>
    """, unsafe_allow_html=True)

    st.subheader("🏆 Product Leaderboard")

    st.dataframe(
        leaderboard,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CHARTS ---------------- #

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sales",
    "📈 Profit",
    "📉 Margins",
    "🧠 Insights"
])

# ---------------- PIE CHART ---------------- #

fig1 = px.pie(
    filtered_df,
    names='Product Name',
    values='Gross Profit',
    title='Profit Contribution'
)

fig1.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------------- BAR CHART ---------------- #

division_analysis = filtered_df.groupby(
    'Division'
).agg({
    'Sales':'sum',
    'Gross Profit':'sum'
}).reset_index()

fig2 = px.bar(
    division_analysis,
    x='Division',
    y=['Sales','Gross Profit'],
    barmode='group',
    title='Revenue vs Profit'
)

fig2.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------------- BOX PLOT ---------------- #

fig3 = px.box(
    filtered_df,
    x='Division',
    y='Gross Margin %',
    title='Margin Distribution'
)

fig3.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------------- SCATTER PLOT ---------------- #

fig4 = px.scatter(
    filtered_df,
    x='Cost',
    y='Sales',
    color='Division',
    hover_name='Product Name',
    size='Gross Profit',
    title='Cost vs Sales'
)

fig4.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------------- PARETO ANALYSIS ---------------- #

pareto = filtered_df.groupby(
    'Product Name'
)['Gross Profit'].sum().sort_values(
    ascending=False
)

pareto_df = pareto.reset_index()

pareto_df['Cumulative %'] = (
    pareto_df['Gross Profit'].cumsum()
    / pareto_df['Gross Profit'].sum()
) * 100

fig5 = px.line(
    pareto_df,
    x='Product Name',
    y='Cumulative %',
    title='Pareto Analysis'
)

fig5.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# ---------------- TABS ---------------- #

with tab1:

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with tab2:

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

with tab3:

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

with tab4:

    st.success(
        f"Top Performing Division: {division_analysis.iloc[0]['Division']}"
    )

    st.info(
        f"Average Margin: {avg_margin:.2f}%"
    )

    st.warning(
        f"Highest Product Margin: {filtered_df['Gross Margin %'].max():.2f}%"
    )

# ---------------- SUMMARY BOX ---------------- #

st.markdown(f"""
<div style="
    background:#111827;
    padding:25px;
    border-radius:20px;
    color:white;
    margin-top:20px;
">

<h2>📌 Dashboard Summary</h2>

<ul>
<li>Total Products: {filtered_df['Product Name'].nunique()}</li>
<li>Total Divisions: {filtered_df['Division'].nunique()}</li>
<li>Total Orders: {len(filtered_df)}</li>
<li>Highest Margin: {filtered_df['Gross Margin %'].max():.2f}%</li>
</ul>

</div>
""", unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #

st.markdown("""
<hr>

<div style='text-align:center'>
    Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)
