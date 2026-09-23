from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


st.set_page_config(
    page_title="Customer Value & Retention Dashboard",
    page_icon="📈",
    layout="wide",
)

CURRENCY = "£"
SEGMENT_ORDER = ["Low", "Medium", "High", "Very High"]
ACTION_ORDER = [
    "Protect loyalty",
    "Win back now",
    "Grow customer value",
    "Low-cost nurture",
]
ACTION_COLORS = {
    "Protect loyalty": "#3A7D6F",
    "Win back now": "#C65D47",
    "Grow customer value": "#D6A84B",
    "Low-cost nurture": "#7E8793",
}
SEGMENT_COLORS = {
    "Low": "#BCC4CC",
    "Medium": "#7FA4B5",
    "High": "#D6A84B",
    "Very High": "#C65D47",
}

# Executive editorial chart theme: warm canvas, ink-blue type and coral/gold accents.
pio.templates["executive_editorial"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Arial, sans-serif", color="#182433", size=13),
        title=dict(font=dict(color="#182433", size=19)),
        paper_bgcolor="#F6F2EA",
        plot_bgcolor="#FFFFFF",
        colorway=["#355C7D", "#C65D47", "#D6A84B", "#3A7D6F", "#7E8793"],
        xaxis=dict(
            gridcolor="#E7E0D5",
            linecolor="#CFC6B8",
            zerolinecolor="#CFC6B8",
            title_font=dict(color="#344250"),
        ),
        yaxis=dict(
            gridcolor="#E7E0D5",
            linecolor="#CFC6B8",
            zerolinecolor="#CFC6B8",
            title_font=dict(color="#344250"),
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.80)",
            bordercolor="#DED5C8",
            borderwidth=1,
        ),
        margin=dict(l=35, r=25, t=65, b=35),
    )
)
pio.templates.default = "executive_editorial"

st.markdown(
    """
    <style>
    :root {
        --ink: #182433;
        --slate: #355C7D;
        --coral: #C65D47;
        --gold: #D6A84B;
        --ivory: #F6F2EA;
        --paper: #FFFFFF;
        --muted: #66717C;
        --line: #DED5C8;
    }

    .stApp {
        background: var(--ivory);
        color: var(--ink);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, h5, h6,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    label {
        color: var(--ink) !important;
    }

    h1 {
        font-family: Georgia, "Times New Roman", serif !important;
        font-size: clamp(2.2rem, 4vw, 3.7rem) !important;
        letter-spacing: -0.035em;
        line-height: 1.05 !important;
        border-bottom: 4px solid var(--coral);
        padding-bottom: 0.55rem;
        max-width: 950px;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
        font-size: 1rem;
    }

    /* Deep ink navigation rail */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #182433 0%, #25384A 100%);
        border-right: 5px solid var(--gold);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #F8F3EA !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        color: var(--ink) !important;
        border-color: rgba(255,255,255,0.28) !important;
    }

    /* High-contrast KPI cards. Explicit text colors prevent dark-theme conflicts. */
    [data-testid="stMetric"] {
        background: var(--paper) !important;
        border: 1px solid var(--line);
        border-top: 5px solid var(--coral);
        border-radius: 4px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 24px rgba(24,36,51,0.07);
        min-height: 118px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #5A6672 !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: var(--ink) !important;
        font-family: Georgia, "Times New Roman", serif !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] * {
        color: #3A7D6F !important;
    }

    /* Pill tabs with a strong selected state */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.55rem;
        background: #E9E1D5;
        padding: 0.45rem;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 46px;
        border-radius: 6px;
        padding: 0 1.1rem;
        color: var(--ink) !important;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: var(--coral) !important;
        color: #FFFFFF !important;
        box-shadow: none;
    }

    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }

    /* Business callouts */
    .business-note {
        background: #FFF8EF;
        color: var(--ink);
        border: 1px solid #E5D3AF;
        border-left: 7px solid var(--gold);
        padding: 1rem 1.15rem;
        border-radius: 4px;
        margin: 0.7rem 0 1.2rem 0;
        box-shadow: 0 5px 18px rgba(24,36,51,0.05);
    }

    .warning-note {
        background: #F9EDE8;
        color: var(--ink);
        border: 1px solid #E4C1B7;
        border-left: 7px solid var(--coral);
        padding: 1rem 1.15rem;
        border-radius: 4px;
    }

    /* Buttons and downloads */
    .stButton > button,
    .stDownloadButton > button {
        background: var(--coral) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--coral) !important;
        border-radius: 4px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1rem !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #A94A39 !important;
        border-color: #A94A39 !important;
    }

    /* Dataframe and chart surfaces */
    [data-testid="stDataFrame"],
    [data-testid="stPlotlyChart"] {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 5px;
        box-shadow: 0 7px 20px rgba(24,36,51,0.055);
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        color: var(--ink) !important;
    }

    code {
        color: #A94A39 !important;
        background: #EFE7DC !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def money(value: float) -> str:
    """Format monetary values compactly for executive KPIs."""
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"{CURRENCY}{value / 1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"{CURRENCY}{value / 1_000:,.1f}K"
    return f"{CURRENCY}{value:,.0f}"


@st.cache_data
def load_data() -> pd.DataFrame:
    candidates = [
        Path(__file__).with_name("customer_clv_dashboard.csv"),
        Path.cwd() / "customer_clv_dashboard.csv",
    ]
    data_path = next((path for path in candidates if path.exists()), None)
    if data_path is None:
        raise FileNotFoundError(
            "Place customer_clv_dashboard.csv in the same folder as app.py."
        )

    frame = pd.read_csv(data_path)
    required = {
        "CustomerID",
        "Frequency",
        "MonetaryValue",
        "AverageOrderValue",
        "ProductDiversity",
        "RecencyDays",
        "PrimaryCountry",
        "RepeatProbability",
        "ConditionalFutureRevenue",
        "PredictedCLV",
        "CLVSegment",
        "Location",
        "BusinessAction",
    }
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    frame["CustomerID"] = frame["CustomerID"].astype(str)
    frame["CLVSegment"] = pd.Categorical(
        frame["CLVSegment"], categories=SEGMENT_ORDER, ordered=True
    )
    return frame


try:
    data = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()


st.title("Customer Value & Retention Dashboard")
st.caption(
    "Prioritise customers using predicted return likelihood and expected future value."
)

with st.sidebar:
    st.header("Business filters")

    selected_segments = st.multiselect(
        "Customer value segment",
        SEGMENT_ORDER,
        default=SEGMENT_ORDER,
    )
    selected_actions = st.multiselect(
        "Recommended action",
        ACTION_ORDER,
        default=ACTION_ORDER,
    )
    selected_locations = st.multiselect(
        "Location",
        sorted(data["Location"].unique()),
        default=sorted(data["Location"].unique()),
    )

    probability_range = st.slider(
        "Return likelihood",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=1,
        help="Predicted probability that the customer makes a future purchase.",
    )

    clv_cap = float(np.ceil(data["PredictedCLV"].quantile(0.99) / 100) * 100)
    clv_range = st.slider(
        "Expected customer value",
        min_value=0.0,
        max_value=clv_cap,
        value=(0.0, clv_cap),
        step=max(10.0, clv_cap / 100),
        format=f"{CURRENCY}%.0f",
        help="The upper limit is set to the 99th percentile so extreme values do not make the filter unusable.",
    )

upper_clv_mask = data["PredictedCLV"] <= clv_range[1]
if clv_range[1] == clv_cap:
    # The right-most slider position means “no upper limit”, so the default
    # view retains the exceptional top 1% of customers.
    upper_clv_mask = pd.Series(True, index=data.index)

filtered = data[
    data["CLVSegment"].isin(selected_segments)
    & data["BusinessAction"].isin(selected_actions)
    & data["Location"].isin(selected_locations)
    & data["RepeatProbability"].between(
        probability_range[0] / 100, probability_range[1] / 100
    )
    & (data["PredictedCLV"] >= clv_range[0])
    & upper_clv_mask
].copy()

if filtered.empty:
    st.warning("No customers match the current filters. Broaden the sidebar selections.")
    st.stop()


overview_tab, priority_tab, planning_tab, model_tab = st.tabs(
    [
        "Business overview",
        "Customer priorities",
        "Revenue planning",
        "How the score works",
    ]
)

with overview_tab:
    customers = len(filtered)
    total_value = filtered["PredictedCLV"].sum()
    average_probability = filtered["RepeatProbability"].mean()
    at_risk = filtered[filtered["BusinessAction"] == "Win back now"]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Customers selected", f"{customers:,}")
    kpi2.metric("Expected future value", money(total_value))
    kpi3.metric("Average return likelihood", f"{average_probability:.1%}")
    kpi4.metric("High-value customers at risk", f"{len(at_risk):,}")

    st.markdown(
        "<div class='business-note'><b>Management focus:</b> "
        "Protect high-value loyal customers and prioritise ‘Win back now’ customers "
        "for targeted retention campaigns.</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        segment_summary = (
            filtered.groupby("CLVSegment", observed=False)
            .agg(Customers=("CustomerID", "count"), ExpectedValue=("PredictedCLV", "sum"))
            .reset_index()
        )
        figure = px.bar(
            segment_summary,
            x="CLVSegment",
            y="ExpectedValue",
            color="CLVSegment",
            category_orders={"CLVSegment": SEGMENT_ORDER},
            color_discrete_map=SEGMENT_COLORS,
            text_auto=".3s",
            title="Expected value by customer segment",
            labels={"CLVSegment": "Segment", "ExpectedValue": "Expected future value"},
        )
        figure.update_layout(showlegend=False, yaxis_tickprefix=CURRENCY)
        st.plotly_chart(figure, use_container_width=True)

    with right:
        action_summary = (
            filtered.groupby("BusinessAction", observed=True)
            .agg(Customers=("CustomerID", "count"))
            .reset_index()
        )
        figure = px.bar(
            action_summary,
            x="Customers",
            y="BusinessAction",
            orientation="h",
            color="BusinessAction",
            category_orders={"BusinessAction": ACTION_ORDER},
            color_discrete_map=ACTION_COLORS,
            text="Customers",
            title="Customers by recommended action",
            labels={"BusinessAction": "Recommended action"},
        )
        figure.update_layout(showlegend=False)
        st.plotly_chart(figure, use_container_width=True)

    display_scatter = filtered.nlargest(min(len(filtered), 1500), "PredictedCLV")
    probability_cutoff = data["RepeatProbability"].median()
    revenue_cutoff = data["ConditionalFutureRevenue"].median()
    scatter = px.scatter(
        display_scatter,
        x="RepeatProbability",
        y="ConditionalFutureRevenue",
        size="PredictedCLV",
        color="BusinessAction",
        color_discrete_map=ACTION_COLORS,
        hover_name="CustomerID",
        hover_data={
            "CLVSegment": True,
            "PrimaryCountry": True,
            "PredictedCLV": ":,.0f",
            "RepeatProbability": ":.1%",
            "ConditionalFutureRevenue": ":,.0f",
        },
        title="Customer opportunity map",
        labels={
            "RepeatProbability": "Return likelihood",
            "ConditionalFutureRevenue": "Revenue if the customer returns",
            "BusinessAction": "Recommended action",
        },
        log_y=True,
        size_max=38,
    )
    scatter.add_vline(x=probability_cutoff, line_dash="dash", line_color="#75808A")
    scatter.add_hline(y=revenue_cutoff, line_dash="dash", line_color="#75808A")
    scatter.update_xaxes(tickformat=".0%")
    scatter.update_yaxes(tickprefix=CURRENCY)
    st.plotly_chart(scatter, use_container_width=True)
    st.caption(
        "Dashed lines show the portfolio medians used to form the four action groups. "
        "The revenue axis uses a log scale because a small number of customers have exceptionally high values."
    )

with priority_tab:
    st.subheader("Customer action list")
    st.write(
        "Start with customers carrying the highest expected value, then use the recommended "
        "action to select the appropriate campaign."
    )

    sort_choice = st.selectbox(
        "Rank customers by",
        ["Expected value", "Revenue if returned", "Return likelihood", "Recency"],
    )
    sort_map = {
        "Expected value": ("PredictedCLV", False),
        "Revenue if returned": ("ConditionalFutureRevenue", False),
        "Return likelihood": ("RepeatProbability", False),
        "Recency": ("RecencyDays", True),
    }
    sort_column, ascending = sort_map[sort_choice]
    ranked = filtered.sort_values(sort_column, ascending=ascending).copy()

    table = ranked[
        [
            "CustomerID",
            "PrimaryCountry",
            "CLVSegment",
            "BusinessAction",
            "RepeatProbability",
            "ConditionalFutureRevenue",
            "PredictedCLV",
            "RecencyDays",
            "Frequency",
            "MonetaryValue",
        ]
    ].rename(
        columns={
            "PrimaryCountry": "Country",
            "CLVSegment": "Value segment",
            "BusinessAction": "Recommended action",
            "RepeatProbability": "Return likelihood",
            "ConditionalFutureRevenue": "Revenue if returned",
            "PredictedCLV": "Expected value",
            "RecencyDays": "Days since purchase",
            "Frequency": "Past orders",
            "MonetaryValue": "Past spending",
        }
    )
    table["Return likelihood"] = table["Return likelihood"] * 100
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Return likelihood": st.column_config.ProgressColumn(
                format="%.1f%%", min_value=0, max_value=100
            ),
            "Revenue if returned": st.column_config.NumberColumn(format=f"{CURRENCY}%.2f"),
            "Expected value": st.column_config.NumberColumn(format=f"{CURRENCY}%.2f"),
            "Past spending": st.column_config.NumberColumn(format=f"{CURRENCY}%.2f"),
        },
        height=520,
    )
    st.download_button(
        "Download selected customer list",
        ranked.to_csv(index=False).encode("utf-8"),
        file_name="selected_customer_priorities.csv",
        mime="text/csv",
    )

with planning_tab:
    st.subheader("Campaign scenario calculator")
    st.write(
        "Estimate the commercial value of a proposed campaign before launch. "
        "This is a planning scenario—not a measured causal effect."
    )

    controls, results = st.columns([1, 2])
    with controls:
        campaign_actions = st.multiselect(
            "Target action groups",
            ACTION_ORDER,
            default=["Win back now"],
            key="campaign_actions",
        )
        uplift_points = st.slider(
            "Assumed increase in return probability",
            0.0,
            20.0,
            5.0,
            0.5,
            help="For example, 5% means an assumed five-percentage-point increase.",
        )
        gross_margin = st.slider("Gross margin", 0, 100, 30, 1)
        contact_cost = st.number_input(
            "Campaign cost per customer",
            min_value=0.0,
            value=5.0,
            step=0.5,
            format="%.2f",
        )

    campaign = filtered[filtered["BusinessAction"].isin(campaign_actions)].copy()
    uplift = uplift_points / 100
    campaign["EffectiveUplift"] = np.minimum(
        uplift, 1 - campaign["RepeatProbability"]
    )
    campaign["IncrementalRevenue"] = (
        campaign["EffectiveUplift"] * campaign["ConditionalFutureRevenue"]
    )
    campaign["IncrementalProfit"] = (
        campaign["IncrementalRevenue"] * (gross_margin / 100) - contact_cost
    )
    campaign["RecommendedForCampaign"] = campaign["IncrementalProfit"] > 0
    recommended = campaign[campaign["RecommendedForCampaign"]]

    with results:
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Customers targeted", f"{len(campaign):,}")
        r2.metric("Positive-profit customers", f"{len(recommended):,}")
        r3.metric("Estimated incremental profit", money(recommended["IncrementalProfit"].sum()))
        spend = len(recommended) * contact_cost
        roi = recommended["IncrementalProfit"].sum() / spend if spend > 0 else np.nan
        r4.metric("Estimated ROI", "N/A" if np.isnan(roi) else f"{roi:.1%}")

        if campaign.empty:
            st.info("Select at least one action group to calculate a scenario.")
        else:
            scenario_chart = campaign.nlargest(25, "IncrementalProfit").sort_values(
                "IncrementalProfit"
            )
            colors = np.where(
                scenario_chart["IncrementalProfit"] > 0, "#3A7D6F", "#C65D47"
            )
            figure = go.Figure(
                go.Bar(
                    x=scenario_chart["IncrementalProfit"],
                    y=scenario_chart["CustomerID"],
                    orientation="h",
                    marker_color=colors,
                    hovertemplate="Customer %{y}<br>Estimated profit: £%{x:,.2f}<extra></extra>",
                )
            )
            figure.update_layout(
                title="Top campaign opportunities under this scenario",
                xaxis_title="Estimated incremental profit",
                yaxis_title="Customer ID",
                xaxis_tickprefix=CURRENCY,
                height=550,
            )
            st.plotly_chart(figure, use_container_width=True)

    st.markdown(
        "<div class='warning-note'><b>Scenario formula:</b> assumed probability uplift × "
        "revenue if returned × gross margin − contact cost. The uplift is a management "
        "assumption and must be validated through a controlled experiment.</div>",
        unsafe_allow_html=True,
    )

    country_summary = (
        filtered.groupby("PrimaryCountry", observed=True)
        .agg(
            Customers=("CustomerID", "count"),
            ExpectedValue=("PredictedCLV", "sum"),
            AverageReturnLikelihood=("RepeatProbability", "mean"),
        )
        .reset_index()
        .nlargest(12, "ExpectedValue")
    )
    country_figure = px.bar(
        country_summary.sort_values("ExpectedValue"),
        x="ExpectedValue",
        y="PrimaryCountry",
        orientation="h",
        color="AverageReturnLikelihood",
        color_continuous_scale=["#F0E4D1", "#355C7D"],
        title="Markets contributing the most expected value",
        labels={
            "ExpectedValue": "Expected future value",
            "PrimaryCountry": "Country",
            "AverageReturnLikelihood": "Avg. return likelihood",
        },
    )
    country_figure.update_xaxes(tickprefix=CURRENCY)
    st.plotly_chart(country_figure, use_container_width=True)

with model_tab:
    st.subheader("How the customer score is calculated")
    st.markdown(
        """
        The dashboard combines two predictions for each customer:

        1. **Return likelihood:** a logistic regression estimates the probability that the
           customer purchases again.
        2. **Revenue if returned:** a conditional revenue regression estimates how much
           revenue the customer may generate if they return.

        **Expected customer value = Return likelihood × Revenue if returned**
        """
    )

    example = filtered.sort_values("PredictedCLV", ascending=False).iloc[0]
    e1, e2, e3 = st.columns(3)
    e1.metric("Example return likelihood", f"{example['RepeatProbability']:.1%}")
    e2.metric("Example revenue if returned", money(example["ConditionalFutureRevenue"]))
    e3.metric("Example expected value", money(example["PredictedCLV"]))

    st.latex(
        r"\widehat{CLV}_i = \widehat{P}(\mathrm{return}_i) "
        r"\times \widehat{E}(\mathrm{future\ revenue}_i\mid\mathrm{return}_i)"
    )

    left, right = st.columns(2)
    with left:
        st.markdown(
            """
            **Inputs used for return likelihood**

            - Days since the last purchase
            - Purchase frequency
            - Historical monetary value
            - Average order value
            - Total quantity purchased
            - Product diversity
            - UK/non-UK indicator
            """
        )
    with right:
        st.markdown(
            """
            **Inputs used for conditional revenue**

            - Days since the last purchase
            - Purchase frequency
            - Average order value
            - Total quantity purchased
            - Product diversity
            - UK/non-UK indicator
            """
        )

    m1, m2, m3 = st.columns(3)
    m1.metric("Return-model ROC–AUC", "0.790")
    m2.metric("Revenue-model R²", "0.681")
    m3.metric("Revenue-model MAE", f"{CURRENCY}1,048")

    st.info(
        "This score estimates future-period revenue, not complete lifetime profit. "
        "It supports prioritisation but should be combined with commercial judgement, "
        "campaign capacity and controlled testing."
    )
