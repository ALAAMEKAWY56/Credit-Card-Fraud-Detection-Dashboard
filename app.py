import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
# ---------------------------------------------------------------
# 1. Smoky Purple Theme 
# ---------------------------------------------------------------
smoky_extended = {
    'layout': {
        # Background
        'paper_bgcolor': '#1B1A2E',
        'plot_bgcolor': '#2E2C4B',

        # Fonts
        'font': {'color': '#D1D1E9'},
        'title': {'font': {'color': '#E4DCFF'}},

        'xaxis': { 'gridcolor': '#474568', 'zerolinecolor': '#474568', 'linecolor': '#6B6990', 'tickcolor': '#AFAACD', }, 
        'yaxis': { 'gridcolor': '#474568', 'zerolinecolor': '#474568', 'linecolor': '#6B6990', 'tickcolor': '#AFAACD', },

        # Color palette
        'colorway': [
            '#7A5CFA', '#A393FF', '#E4DCFF', '#C62300', '#F14A00',
            '#8F6DFD', '#5B4B8A', '#FFA07A', '#D1D1E9', '#F2ECFF',
            '#9A7EFF', '#B285FF', '#FF8C61', '#FF5733', '#FFB347',
            '#6E5A9B', '#4D3C75', '#2D1A58', '#FFDAA5', '#FFD3E0'
        ],

        'legend': {
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': '#474568',
        },

        'margin': {'t': 60, 'b': 40, 'l': 50, 'r': 30},
    }
}

# Register and set as default
pio.templates['smoky_extended'] = smoky_extended
pio.templates.default = 'smoky_extended'
# ---------------------------------------------------------------
# 2. Streamlit Page Config
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------
# 3. Global CSS Styling
# ---------------------------------------------------------------
st.markdown("""
    <style>

    /* Background */
    .main {
        background-color: #1B1A2E;
        color: #D1D1E9;
    }

    .stSidebar {
        background-color: #2E2C4B;
    }

    .stSelectbox, .stMultiSelect {
        background-color: #2E2C4B !important;
    }

    /* Big Title */
    .big-title {
        font-size: 42px !important;
        font-weight: 700;
        color: #E4DCFF;
        text-align: center;
        margin-bottom: 20px;
    }

    /* KPI Card Styling */
    .kpi-card {
        background-color: #2E2C4B;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #6B6990;
        text-align: center;
        box-shadow: 0px 0px 12px rgba(122, 92, 250, 0.25);
    }
    .kpi-number {
        font-size: 32px;
        font-weight: 700;
        color: #E4DCFF;
    }
    .kpi-label {
        font-size: 16px;
        font-weight: 500;
        color: #D1D1E9;
        margin-top: -10px;
    }

    .chart-box {
    background-color: #2E2C4B;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #6B6990;
    box-shadow: 0px 0px 12px rgba(122, 92, 250, 0.25);
    margin-bottom: 20px;
    }

    .chart-title {
    all: unset;                 /* RESET Streamlit override */
    display: block;
    text-align: center;
    font-size: 20px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;

    color: #C7BAFF !important;
    text-shadow: 0 0 6px rgba(167, 139, 250, 0.25) !important;
}

    /* Center all tabs */
    .stTabs [role="tablist"] {
        justify-content: center !important;
        gap: 22px !important;
        margin-bottom: 18px;
    }

    /* Normal tab text */
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;

        padding: 8px 6px !important;
        font-size: 18px !important;
        font-weight: 700 !important;

        color: #D1C5FF !important;
        opacity: 0.75;

        transition:
            color 0.25s ease,
            transform 0.25s ease,
            opacity 0.25s ease;
    }

    /* Hover effect */
    .stTabs [data-baseweb="tab"]:hover {
        color: #EDE5FF !important;
        opacity: 1;
        transform: translateY(-1px);
    }

    /* ACTIVE tab — FIX so gradient text stays visible */
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        border: none !important;
        opacity: 1 !important;

        /* The important part: FORCE text color to be gradient */
        color: transparent !important;
        background-image: linear-gradient(90deg, #A78BFA, #C4B5FD, #EDE5FF) !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;

        transform: translateY(-2px);
    }


section[data-testid="stSidebar"] details > summary {
    background: linear-gradient(90deg, #2E2C4B, #262042) !important;
    color: #E7E2FF !important;

    padding: 10px 14px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(199, 186, 255, 0.25) !important;

    font-weight: 600 !important;
    letter-spacing: 0.3px;

    transition:
        background 0.35s ease,
        box-shadow 0.35s ease,
        transform 0.25s ease,
        color 0.25s ease;
}


section[data-testid="stSidebar"] details[open] > summary {
    background: linear-gradient(
        90deg,
        rgba(91,78,140,0.55),
        rgba(60,51,101,0.55)
    ) !important;

    border-color: rgba(209,198,255,0.45) !important;

    box-shadow:
        0 0 15px rgba(186,169,255,0.25),
        inset 0 0 8px rgba(255,255,255,0.10);
}


section[data-testid="stSidebar"] details[open] > div {
    background: rgba(38,32,66,0.65) !important;
    padding: 12px 10px !important;
    border-radius: 0 0 12px 12px !important;

    border-left: 1px solid rgba(199,186,255,0.22) !important;
    border-right: 1px solid rgba(199,186,255,0.22) !important;
    border-bottom: 1px solid rgba(199,186,255,0.22) !important;

    backdrop-filter: blur(6px) !important;  /* soft glass look */
}

.neon-separator {
    height: 4px;
    margin: 25px;
    width: 90%;

    background: #5A3FA6;               /* solid pastel purple */

    border-radius: 12px;

    box-shadow:
        0 0 10px rgba(90, 63, 166, 0.85),
        0 0 20px rgba(90, 63, 166, 0.55),
        0 0 30px rgba(90, 63, 166, 0.35);
}

/* --- Neon Hover for ALL Inputs --- */
.stSidebar select:hover,
.stSidebar input:hover,
.stSidebar div[data-baseweb="select"] div:hover,
.stSidebar div[data-baseweb="radio"] label:hover,
.stSidebar .stMultiSelect:hover,
.stSidebar .stSelectbox:hover,
.stSidebar .stSlider:hover {
    background: rgba(167,139,250,0.15) !important;
    border-radius: 8px !important;
    transition: 0.3s ease-in-out !important;
    box-shadow: 0 0 8px rgba(167,139,250,0.35) !important;
}

/* Hover for expander titles */
section[data-testid="stSidebar"] details > summary:hover {
    background: rgba(167,139,250,0.20) !important;
    box-shadow: 0 0 10px rgba(167,139,250,0.35);
    transform: translateX(3px);
}

/* BIG Section Title (Left-Aligned, Glowing, Same Style as Chart Title) */
.big-section-title {
    all: unset;
    display: block;

    text-align: left !important;

    font-size: 28px !important;
    font-weight: 700 !important;
    margin-bottom: 12px !important;
    margin-top: 10px !important;

    color: #C7BAFF !important;
    text-shadow: 0 0 10px rgba(167, 139, 250, 0.35) !important;
}


    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# 4. Title
# ---------------------------------------------------------------
st.markdown('<p class="big-title">Credit Card Fraud Detection Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align: center; color: #D1D1E9; font-size: 18px;">'
    'Explore transaction behaviors, customer patterns, and fraud indicators interactively.'
    '</p>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------------
# 5. Load Clean Dataset
# ---------------------------------------------------------------
df = pd.read_csv("clean_transactions.csv")


us_state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

df["state_abbrev"] = df["state"].map(us_state_abbrev)

# ---------------------------------------------------------------
# 6. Sidebar Filters
# ---------------------------------------------------------------
st.sidebar.header("Filter Data")

# ---------------- Transaction Filters ----------------
with st.sidebar.expander("Transaction Filters", expanded=True):
    fraud_toggle = st.toggle("Show Fraud Only")
    fraud_filter = [1] if fraud_toggle else [0, 1]

    min_amt = int(df["amt"].min())
    max_amt = int(df["amt"].max())

    amount_range = st.slider(
        "Transaction Amount Range",
        min_value=min_amt,
        max_value=max_amt,
        value=(min_amt, max_amt)
    )

# ---------------- Time Filters ----------------
with st.sidebar.expander("Time Filters", expanded=True):

    month_filter = st.multiselect(
        "Month",
        options=df["month_name"].unique(),
        default=df["month_name"].unique()
    )

    dow_filter = st.multiselect(
        "Day of Week",
        options=df["day_of_week"].unique(),
        default=df["day_of_week"].unique()
    )

    hour_range = st.slider(
        "Hour of Day",
        min_value=0,
        max_value=23,
        value=(0, 23)
    )

# ---------------- Location Filters ----------------
with st.sidebar.expander("Location Filters"):

    state_filter = st.multiselect(
        "State",
        options=df["state"].unique(),
        default=df["state"].unique()
    )

# ---------------- Merchant Filters ----------------
with st.sidebar.expander("Merchant Filters"):

    category_filter = st.multiselect(
        "Merchant Category",
        options=df["category"].unique(),
        default=df["category"].unique()
    )

    merchant_filter = st.selectbox(
        "Search Merchant",
        options=["All"] + list(df["merchant"].unique()),
        index=0
    )

# ---------------- Customer Filters ----------------
with st.sidebar.expander("Customer Filters"):

    age_filter = st.multiselect(
        "Age Groups",
        options=df["age_groups"].unique(),
        default=df["age_groups"].unique()
    )

    gender_filter = st.radio(
        "Gender",
        options=["All", "M", "F"],
        index=0,
        horizontal=True
    )

# ---------------------------------------------------------------
# 7. Apply Filters
# ---------------------------------------------------------------
df_filtered = df[
    (df["is_fraud"].isin(fraud_filter)) &
    (df["month_name"].isin(month_filter)) &
    (df["day_of_week"].isin(dow_filter)) &
    (df["state"].isin(state_filter)) &
    (df["category"].isin(category_filter)) &
    (df["age_groups"].isin(age_filter)) &
    (df["amt"].between(amount_range[0], amount_range[1])) &
    (df["hour"].between(hour_range[0], hour_range[1]))
]

if merchant_filter != "All":
    df_filtered = df_filtered[df_filtered["merchant"] == merchant_filter]

if gender_filter != "All":
    df_filtered = df_filtered[df_filtered["gender"] == gender_filter]

# ---------------------------------------------------------------
# 8. KPI Cards
# ---------------------------------------------------------------
left, col1, col2, col3, right = st.columns([0.5, 1.5, 1.5, 1.5, 0.5])

with col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{len(df_filtered):,}</div>
            <div class="kpi-label">Total Transactions</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{df_filtered['is_fraud'].sum():,}</div>
            <div class="kpi-label">Total Fraud Cases</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    fraud_rate = df_filtered["is_fraud"].mean() * 100
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{fraud_rate:.2f}%</div>
            <div class="kpi-label">Fraud Rate</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------------
# 8. Tabs Layout 
# ---------------------------------------------------------------
tab1 , tab2 , tab3 , tab4 , tab5 , tab_summary = st.tabs([
    "Overview",
    "Customer Insights",
    "Merchant & Category Insights",
    "Geographical Analysis",
    "Time-Based Patterns",
    "Summary Dashboard"
])


# ---------------------------------------------------------------
# TAB 1 – FRAUD OVERVIEW (Side-by-Side Enhanced)
# ---------------------------------------------------------------
with tab1:

    colA, colB = st.columns([1,1], gap="large")

    # ------- Left Chart: Fraud Count -------
    with colA:
        st.markdown('<h3 class="chart-title">Fraud vs Non-Fraud Count</h3>', unsafe_allow_html=True)

        df_sample_grouped = df_filtered['is_fraud'].value_counts().reset_index()
        df_sample_grouped['is_fraud'] = df_sample_grouped['is_fraud'].astype(str)

        fig1 = px.bar(
            df_sample_grouped,
            x='is_fraud',
            y='count',
            color='is_fraud',
            width=700,
            height=500,
            text='count'
        )
        fig1.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )

        st.plotly_chart(fig1, use_container_width=False, theme=None)

    # ------- Right Chart: Age Boxplot -------
    with colB:
        st.markdown('<h3 class="chart-title">Age Distribution</h3>', unsafe_allow_html=True)

        Age_Distribution_Boxplot = px.box(
            df_filtered, 
            x='age',
            width=700,
            height=500
        )
        Age_Distribution_Boxplot.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )

        st.plotly_chart(Age_Distribution_Boxplot, use_container_width=False, theme=None)

    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)

    # ============================
    # Row 2: Transaction Amount + Placeholder
    # ============================
    colC, colD = st.columns([1,1], gap="large")

    # ------- Left Chart: Transaction Amounts -------
    with colC:
        st.markdown('<h3 class="chart-title">Transaction Amount: Fraud vs Non-Fraud</h3>', unsafe_allow_html=True)

        Transaction_Amounts = px.box(
            df_filtered,
            x='is_fraud',
            y='amt',
            points='all',
            color='is_fraud',
            width=700,
            height=500
        )
        Transaction_Amounts.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )

        st.plotly_chart(Transaction_Amounts, use_container_width=True, theme=None)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------- Right Chart: Placeholder or remove -------
    with colD:

        st.markdown('<h3 class="chart-title">Gender Distribution</h3>', unsafe_allow_html=True)
        Gender_Distribution = px.pie(
        df_filtered.replace({'M' : 'Male' , 'F' : 'Female'}),
        names='gender',
        width=700,
        height=500,
        hole=0.4
        )

        Gender_Distribution.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )


        st.plotly_chart(Gender_Distribution, use_container_width=True, theme=None)

        st.markdown('</div>', unsafe_allow_html=True) 

    st.markdown("<br>", unsafe_allow_html=True)  
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)



# ---------------------------------------------------------------
# TAB 2 – Customer Insights
# ---------------------------------------------------------------
with tab2:

    colE, colF = st.columns([1,1], gap="large")

    # ------- Left Chart: Fraud Count -------
    with colE:
        st.markdown('<h3 class="chart-title">Age Distribution of Cardholders</h3>', unsafe_allow_html=True)

        Age_Distribution_of_Cardholders = px.histogram(
        df_filtered,
        x='age',
        width=700,
        height=500,
        color_discrete_sequence=['#C1121F'],
        )
        Age_Distribution_of_Cardholders.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )

        st.plotly_chart(Age_Distribution_of_Cardholders, use_container_width=False, theme=None)

    with colF:
        st.markdown('<h3 class="chart-title">Which Age Group has Most Fraud Cases?</h3>', unsafe_allow_html=True)

        fraud_counts = df_filtered.groupby('age_groups')['is_fraud'].sum().reset_index()
        total_fraud = fraud_counts['is_fraud'].sum()
        fraud_counts['fraud_percent'] = (fraud_counts['is_fraud'] / total_fraud) * 100
        Age_fraud_percent = px.pie( fraud_counts, names='age_groups', values='fraud_percent',hole=0.3,
            width = 700 , 
            height = 500 )

        Age_fraud_percent.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )
        st.plotly_chart(Age_fraud_percent, use_container_width=False, theme=None)


    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)
    colG, colH = st.columns([1,1], gap="large")

    with colG:
        st.markdown('<h3 class="chart-title">Fraud Rate % By gender</h3>', unsafe_allow_html=True)

        df_gender_fraud_rate = (df_filtered.groupby('gender')['is_fraud'].mean()* 100).reset_index()
        gender_fraud_rate = px.bar(df_gender_fraud_rate.replace({'M' : 'Male' , 'F' : 'Female'})
           ,x = 'gender' ,
           y ='is_fraud' ,
           color = 'gender' ,
           width = 700 , height = 500 , color_discrete_sequence=['#B388EB', '#FF6F61'],
          text_auto = True)

        gender_fraud_rate.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )
        st.plotly_chart(gender_fraud_rate, use_container_width=False, theme=None)


    with colH:

        st.markdown('<h3 class="chart-title">Gender vs Average Transaction Amount</h3>', unsafe_allow_html=True)

        gender_avg_amount = (
            df_filtered.groupby("gender")["amt"]
            .mean()
            .reset_index()
            .sort_values("amt", ascending=False)
        )

        Gender_vs_Amt = px.bar(
            gender_avg_amount.replace({'M' : 'Male' , 'F' : 'Female'}),
            x="gender",
            y="amt",
            color="gender",
            text="amt",
            width=700,
            height=500,
            color_discrete_sequence=['#B388EB', '#FF6F61'],
            text_auto = True
        )


        Gender_vs_Amt.update_layout(
            paper_bgcolor="#1B1A2E",
            plot_bgcolor="#2E2C4B",
            xaxis_title="Gender",
            yaxis_title="Average Transaction Amount",
        )

        st.plotly_chart(Gender_vs_Amt, use_container_width=True , theme = None)

    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------
# TAB 3 – Customer Insights
# ---------------------------------------------------------------
with tab3:

    colL, colM = st.columns([1,1], gap="large")

    # ------- Left Chart: Fraud Count -------
    with colL:
        st.markdown('<h3 class="chart-title">Transaction Volume by Merchant Category</h3>', unsafe_allow_html=True)

        df_category = df_filtered.groupby('category')['trans_num'].count().sort_values(ascending=False).reset_index(name = 'transaction_count')
        fig_category_pie = px.pie(
        df_category,
        names='category',
        values='transaction_count',
        width=700,
        height=500,
        hole = 0.3
        )

        fig_category_pie.update_traces(
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='auto'

        )

        fig_category_pie.update_layout(
            showlegend=False,
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B'
        )

        st.plotly_chart(fig_category_pie, use_container_width=True , theme = None)


    with colM:

        st.markdown('<h3 class="chart-title">Fraud Count by Merchant Category</h3>', unsafe_allow_html=True)

        df_cateogry_fraud = df_filtered.groupby('category')['is_fraud'].sum().sort_values(ascending = False).reset_index()
        df_cateogry_fraud = df_cateogry_fraud.rename(columns = {'is_fraud' : 'fraud_count'})

        fig_cateogry_fraud = px.bar(df_cateogry_fraud , y = 'category' , x = 'fraud_count' ,color = 'fraud_count' , color_continuous_scale=['#B388EB', '#FF6F61'],
        width=700,
        height=500,
        text_auto = True)

        fig_cateogry_fraud.update_yaxes(tickangle=0 , automargin=True)  
        fig_cateogry_fraud.update_traces(
            textposition='outside',
        )

        fig_cateogry_fraud.update_layout(
            yaxis = dict(autorange = 'reversed')
        )

        fig_cateogry_fraud.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B',
            coloraxis_showscale=False
        )

        st.plotly_chart(fig_cateogry_fraud, use_container_width=True , theme = None)

    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)

    colN, colO = st.columns([1,1], gap="large")

    # ------- TOP 10 MERCHANT FRAUD -------
    with colN:
        st.markdown('<h3 class="chart-title">Top 10 Merchants with Highest Fraud Rates</h3>', unsafe_allow_html=True)

        df_merchants = df_filtered.groupby('merchant').agg(
            transaction_count=('trans_num', 'count'),
            fraud_count=('is_fraud', 'sum')
        ).reset_index()

        df_merchants['fraud_rate'] = df_merchants['fraud_count'] / df_merchants['transaction_count'] * 100
        df_merchants = df_merchants.sort_values('fraud_rate', ascending=False).head(10)

        fig_top_merchants = px.bar(
            df_merchants,
            x='merchant',
            y='fraud_rate',
            color='fraud_rate',
            text='fraud_rate',
            width=700,
            height=500,
            color_continuous_scale=['#B388EB', '#FF6F61']
        )

        fig_top_merchants.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_top_merchants.update_yaxes(tickangle=0 , automargin=True)  

        fig_top_merchants.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B',
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=60, b=120)
        )

        st.plotly_chart(fig_top_merchants, use_container_width=True, theme=None)

    # ------- AVERAGE TRANSACTION AMOUNT -------
    with colO:
        st.markdown('<h3 class="chart-title">Average Transaction Amount by Category</h3>', unsafe_allow_html=True)

        df_avg = (
            df_filtered.groupby('category')['amt']
            .mean()
            .sort_values(ascending=False)
            .reset_index(name='avg_amount')
        )

        fig_avg_amt = px.bar(
            df_avg,
            x='category',
            y='avg_amount',
            color='avg_amount',
            text='avg_amount',
            width=700,
            height=500,
            color_continuous_scale=['#7A5CFA', '#A78BFA', '#EDE5FF']
        )

        fig_avg_amt.update_yaxes(tickangle=0 , automargin=True)  
        fig_avg_amt.update_traces(texttemplate='%{text:.2f}', textposition='outside')

        fig_avg_amt.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B',
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=60, b=120)
        )

        st.plotly_chart(fig_avg_amt, use_container_width=True, theme=None)

    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)

with tab4:
    colP, colJ = st.columns([1,1], gap="large")

    with colP:
        st.markdown('<h3 class="chart-title">Distance Bands Frequency</h3>', unsafe_allow_html=True)

        df_distance_band = df_filtered['distance_band'].value_counts().reset_index()
        df_distance_band = df_distance_band.rename(columns={'distance_band': 'band', 'count': 'count'})

        fig_distance_band = px.bar(
            df_distance_band,
            y='band',
            x='count',
            color='band',
            text_auto=True,
            width=700,
            height=500,
            color_discrete_sequence=['#B388EB', '#FF6F61', '#9A7EFF', '#FFA08C']
        )

        fig_distance_band.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B',
        )

        fig_distance_band.update_yaxes(
            tickangle=0,
            automargin=True
        )

        st.plotly_chart(fig_distance_band, use_container_width=True, theme=None)

    with colJ:
        st.markdown('<h3 class="chart-title">Fraud Contribution by Distance Band</h3>', unsafe_allow_html=True)
        fig = px.pie(
        df_filtered.groupby('distance_band')['is_fraud'].sum().reset_index(),
        names='distance_band',
        values='is_fraud',
        width = 700 , 
        height = 500
        )
        fig.update_traces(
            textinfo='label+percent',
            textposition='inside',
            insidetextorientation='auto'

        )


        fig.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B',
            showlegend = False
        )

        st.plotly_chart(fig, use_container_width=True, theme=None)


    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)

    colK, colT = st.columns([1,1], gap="large")

    with colK:
        st.markdown('<h3 class="chart-title">Top 10 States with Fraud Cases</h3>', unsafe_allow_html=True)
        df_state_fraud = (
        df_filtered.groupby('state')['is_fraud']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .head(10)
        )

        fig_stats = px.bar(
        df_state_fraud,
        x='state',
        y = 'is_fraud',
        color = 'state',
        barmode = 'stack',
        width = 700 , 
        height = 500,
        text_auto = True
        )

        fig_stats.update_layout(
            paper_bgcolor='#1B1A2E',
            plot_bgcolor='#2E2C4B',
        )


        st.plotly_chart(fig_stats, use_container_width=True, theme=None)

    with colT:
        st.markdown('<h3 class="chart-title">Fraud Rate by State</h3>', unsafe_allow_html=True)

        df_state_rate = (
            df_filtered.groupby("state_abbrev")["is_fraud"]
            .mean()
            .reset_index(name="fraud_rate")
        )

        df_state_rate = df_state_rate.rename(columns={"state_abbrev": "state"})

        df_state_rate["fraud_rate_log"] = np.log1p(df_state_rate["fraud_rate"])

        fig_map = px.choropleth(
            df_state_rate,
            locations="state",
            locationmode="USA-states",
            color="fraud_rate_log",
            scope="usa",
            color_continuous_scale=[
                    "#2D1A40",  
                    "#6A46C7",  
                    "#B388EB",  
                    "#FF8C75",  
                    "#FF6F61" 
                ],

            width = 700,
            height = 500
        )

        fig_map.update_layout(
            paper_bgcolor="#1B1A2E",
            plot_bgcolor="#2E2C4B",
            margin=dict(l=10, r=10, t=40, b=10),
            coloraxis_colorbar=dict(
                title="Fraud Rate (scaled)",
                tickformat=".2f",
                thickness=8,
                len=0.6
            )
        )

        st.plotly_chart(fig_map, use_container_width=True, theme=None)

with tab5:

    colE, colR = st.columns([1,1], gap="large")

    with  colE:
        st.markdown('<h3 class="chart-title">Fraud Transactions by Hour of the Day</h3>', unsafe_allow_html=True)

        df_fraud_hour = df_filtered.groupby('hour')['is_fraud'].sum().sort_values(ascending = False).reset_index()
        df_fraud_hour = df_fraud_hour.rename(columns={'is_fraud': 'fraud_count'})

        fig_fraud_hour = px.bar(df_fraud_hour , x = 'hour' , y = 'fraud_count' , color = 'fraud_count' , color_continuous_scale=['#B388EB', '#FF6F61'],
            width=700,
            height=500)

        peak_hour = df_fraud_hour.loc[
        df_fraud_hour['fraud_count'].idxmax() , 'hour'
        ]

        fig_fraud_hour.add_vline(
            x=peak_hour,
            line_width=2,
            line_dash="dash",
            line_color="white",
            annotation_text=f"Peak Hour: {peak_hour}",
            annotation_position="top"
        )

        fig_fraud_hour.update_layout(
            coloraxis_showscale=False,
            paper_bgcolor="#1B1A2E",
            plot_bgcolor="#2E2C4B"
        )

        st.plotly_chart(fig_fraud_hour, use_container_width=True, theme=None)


    with colR:
        st.markdown('<h3 class="chart-title">Transaction Activity by Hour of the Day</h3>', unsafe_allow_html=True)

        df_hour_activity = df_filtered.groupby('hour')['trans_num'].count().reset_index(name = 'transaction_count')

        fig_hour_activity = px.bar(df_hour_activity , x = 'hour' , y = 'transaction_count', text = 'transaction_count',
        color='transaction_count',
        color_continuous_scale=['#B388EB', '#FF6F61'],
        width=700,
        height=500)


        peak_hour = df_hour_activity.loc[
        df_hour_activity['transaction_count'].idxmax() , 'hour'
        ]

        fig_hour_activity.add_vline(
            x=peak_hour,
            line_width=2,
            line_dash="dash",
            line_color="white",
            annotation_text=f"Peak Hour: {peak_hour}",
            annotation_position="top"
        )

        fig_hour_activity.update_layout(
            coloraxis_showscale=False,
            paper_bgcolor="#1B1A2E",
            plot_bgcolor="#2E2C4B"
        )
        fig_hour_activity.update_traces(textposition = 'outside')
        st.plotly_chart(fig_hour_activity, use_container_width=True, theme=None)


    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)

    colW, colQ = st.columns([1,1], gap="large")


    with colW:

        st.markdown('<h3 class="chart-title">Fraud Transactions by Day of the Week</h3>', unsafe_allow_html=True)

        df_fraud_day = df_filtered.groupby('day_of_week')['is_fraud'].sum().sort_values(ascending = False).reset_index()
        df_fraud_day = df_fraud_day.reset_index().rename(columns={'index': 'day_index'})
        df_fraud_day = df_fraud_day.rename(columns={'is_fraud': 'fraud_count'})


        fig_fraud_day = px.bar(df_fraud_day , x = 'day_of_week' , y = 'fraud_count' , color = 'fraud_count' , color_continuous_scale=['#B388EB', '#FF6F61'],
            width=700,
            height=500)

        peak_day = df_fraud_day.loc[
        df_fraud_day['fraud_count'].idxmax() , 'day_index'
        ]

        fig_fraud_day.add_vline(
            x=peak_day,
            line_width=2,
            line_dash="dash",
            line_color="white",
            annotation_text=f"Peak day: {df_fraud_day[df_fraud_day['day_index'] == peak_day]['day_of_week'][0]}",
            annotation_position="top"
        )

        fig_fraud_day.update_layout(
            coloraxis_showscale=False,
            paper_bgcolor="#1B1A2E",
            plot_bgcolor="#2E2C4B"
        )
        st.plotly_chart(fig_fraud_day, use_container_width=True, theme=None)

    with colQ:
        st.markdown('<h3 class="chart-title">Fraud Transactions by Day of the Week</h3>', unsafe_allow_html=True)

        df_fraud_season_month = df_filtered.groupby(['season', 'month_name'])['is_fraud'].sum().reset_index()
        df_fraud_season_month = df_fraud_season_month.rename(columns={'is_fraud': 'fraud_count'})

        df_fraud_season= px.histogram(
            df_fraud_season_month,
            x='season',
            y='fraud_count',
            color='month_name',
            width=700,
            height=500,
            barmode='stack',
            title='Fraud by Season Stacked by Month',
            text_auto='fraud_count',
        )


        df_fraud_season.update_layout(
            paper_bgcolor="#1B1A2E",
            plot_bgcolor="#2E2C4B"
        )
        st.plotly_chart(df_fraud_season, use_container_width=True, theme=None)

    st.markdown("<br>", unsafe_allow_html=True)  # spacing between rows
    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)

with tab_summary:
    st.markdown('<h3 class="big-section-title">Summary Dashboard</h3>', unsafe_allow_html=True)

    # --- KEY INSIGHTS SECTION ---
    st.markdown('<h3 class="big-section-title">Key Insights</h3>', unsafe_allow_html=True)

    st.markdown("""
    #### 👥 **Customer Behavior**
    - Seniors are the most vulnerable age group.
    - Fraud amounts are usually low “test transactions”.

    #### 🛍️ **Category & Merchant Patterns**
    - Fraud concentrates in **grocery_pos, shopping_net, misc_net**.
    - Certain merchants show unusually high fraud rates.

    #### 📍 **Geographical Patterns**
    - Fraud clusters in **Pennsylvania, New York, Michigan**.
    - Long-distance transactions have higher fraud risk.

    #### ⏰ **Time-Based Patterns**
    - Fraud spikes at **night (10 PM–3 AM)**.
    - Weekends & Mondays show higher fraud.
    - Winter & Spring months are peak fraud seasons.
    """)

    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)

    # --- RECOMMENDATIONS ---
    st.markdown("""
    ### 🛡️ **Recommendations**

    - Strengthen monitoring during **night hours & weekends**.
    - Apply **distance-based risk scoring**.
    - Add extra checks for **high-risk merchants**.
    - Enable enhanced authentication for **senior customers**.

    ### ⭐ **Final Takeaway**
    Fraud is not random , it follows clear patterns.  
    Understanding these trends enables smarter and more proactive fraud detection.
    """)

    st.markdown('<div class="neon-separator"></div>', unsafe_allow_html=True)



st.markdown(f"""
<div style="text-align:center; margin-top:40px; padding:15px;">
<p style="margin-bottom: 6px; font-weight:600; font-size:24px; color:#EDE5FF;">
Made with 💜 by <span style="color:#C7BAFF;">Alaa Mekawi</span>
</p><p style="margin-bottom: 0;"><a href="https://www.linkedin.com/in/alaa-mekawi-37b245221/" target="_blank"
style="color:#A78BFA; text-decoration:none; font-size:18px; margin-right:20px;">🔗 LinkedIn</a><a href="https://github.com/ALAAMEKAWY56" target="_blank"style="color:#A78BFA; text-decoration:none; font-size:18px;">🔗 GitHub</a></p></div>
""", unsafe_allow_html=True)


