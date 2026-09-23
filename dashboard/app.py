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

    .action-card,
    .explain-card {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-top: 6px solid var(--coral);
        border-radius: 5px;
        padding: 1rem 1.05rem;
        min-height: 245px;
        box-shadow: 0 7px 20px rgba(24,36,51,0.055);
        margin-bottom: 1rem;
    }

    .action-card h4,
    .explain-card h4 {
        margin-top: 0.2rem;
        margin-bottom: 0.7rem;
        color: var(--ink) !important;
    }

    .action-card p,
    .explain-card p {
        color: #4F5C68 !important;
        line-height: 1.5;
    }

    .action-count {
        display: inline-block;
        background: #EFE7DC;
        color: var(--ink);
        padding: 0.25rem 0.55rem;
        border-radius: 999px;
        font-weight: 800;
        margin-bottom: 0.65rem;
    }

    .step-number {
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        background: var(--coral);
        color: #FFFFFF;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
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


st.title("Customer Priorities & Revenue Opportunities")
st.caption(
    "Use past buying behaviour to decide who needs attention, what action to take, "
    "and where future revenue may come from."
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


overview_tab, priority_tab, planning_tab, explanation_tab = st.tabs(
    [
        "What is happening?",
        "Who needs attention?",
        "What should we do?",
        "What do the numbers mean?",
    ]
)

with overview_tab:
    st.subheader("A quick view for management")
    st.write(
        "This page turns past customer activity into a practical view of likely future "
        "revenue. Use the filters on the left to focus on a country, customer group, "
        "or level of buying interest."
    )

    customers = len(filtered)
    total_value = filtered["PredictedCLV"].sum()
    average_probability = filtered["RepeatProbability"].mean()
    at_risk = filtered[filtered["BusinessAction"] == "Win back now"]
    protected = filtered[filtered["BusinessAction"] == "Protect loyalty"]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(
        "Customers in this view",
        f"{customers:,}",
        help="Number of customers remaining after the filters are applied.",
    )
    kpi2.metric(
        "Likely future revenue",
        money(total_value),
        help="Estimated revenue from these customers during the future period.",
    )
    kpi3.metric(
        "Average chance of buying again",
        f"{average_probability:.0%}",
        help="The average predicted chance that a selected customer returns.",
    )
    kpi4.metric(
        "Valuable customers needing attention",
        f"{len(at_risk):,}",
        help="Customers with strong spending potential but a lower chance of returning.",
    )

    country_value = (
        filtered.groupby("PrimaryCountry", observed=True)["PredictedCLV"]
        .sum()
        .sort_values(ascending=False)
    )
    leading_country = country_value.index[0]
    st.markdown(
        f"""
        <div class='business-note'>
        <b>What management can take from this view</b><br>
        • <b>{len(at_risk):,}</b> valuable customers may need a reason to return.<br>
        • <b>{len(protected):,}</b> valuable and loyal customers should receive reliable service and recognition.<br>
        • <b>{leading_country}</b> contributes the largest share of likely future revenue in the current view.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        segment_summary = (
            filtered.groupby("CLVSegment", observed=False)
            .agg(
                Customers=("CustomerID", "count"),
                LikelyRevenue=("PredictedCLV", "sum"),
            )
            .reset_index()
        )
        segment_summary["Label"] = segment_summary["LikelyRevenue"].map(money)
        figure = px.bar(
            segment_summary,
            x="CLVSegment",
            y="LikelyRevenue",
            color="CLVSegment",
            category_orders={"CLVSegment": SEGMENT_ORDER},
            color_discrete_map=SEGMENT_COLORS,
            text="Label",
            title="Where is the likely revenue?",
            labels={
                "CLVSegment": "Customer value group",
                "LikelyRevenue": "Likely future revenue",
            },
        )
        figure.update_traces(textposition="outside", cliponaxis=False)
        figure.update_layout(showlegend=False, height=500, bargap=0.28)
        figure.update_yaxes(tickprefix=CURRENCY)
        st.plotly_chart(figure, use_container_width=True)
        st.caption(
            "Taller bars represent customer groups expected to contribute more future revenue."
        )

    with right:
        action_summary = (
            filtered.groupby("BusinessAction", observed=True)
            .agg(Customers=("CustomerID", "count"))
            .reindex(ACTION_ORDER)
            .fillna(0)
            .reset_index()
        )
        figure = px.bar(
            action_summary,
            x="Customers",
            y="BusinessAction",
            orientation="h",
            color="BusinessAction",
            category_orders={"BusinessAction": ACTION_ORDER[::-1]},
            color_discrete_map=ACTION_COLORS,
            text="Customers",
            title="What action does each customer need?",
            labels={
                "BusinessAction": "Suggested action",
                "Customers": "Number of customers",
            },
        )
        figure.update_traces(textposition="outside", cliponaxis=False)
        figure.update_layout(showlegend=False, height=500)
        st.plotly_chart(figure, use_container_width=True)
        st.caption(
            "Use these groups to choose the right level and type of customer contact."
        )

    st.subheader("See the opportunity and risk together")
    st.write(
        "Each circle is one customer. Move right for a greater chance of buying again; "
        "move upward for greater spending potential. Larger circles represent more likely revenue."
    )

    probability_cutoff = data["RepeatProbability"].median()
    revenue_cutoff = data["ConditionalFutureRevenue"].median()
    visible_limit = filtered["ConditionalFutureRevenue"].quantile(0.99)
    display_scatter = filtered[
        filtered["ConditionalFutureRevenue"] <= visible_limit
    ].copy()
    display_scatter["ChanceOfReturn"] = display_scatter["RepeatProbability"] * 100

    scatter = px.scatter(
        display_scatter,
        x="ChanceOfReturn",
        y="ConditionalFutureRevenue",
        size="PredictedCLV",
        color="BusinessAction",
        color_discrete_map=ACTION_COLORS,
        hover_name="CustomerID",
        hover_data={
            "PrimaryCountry": True,
            "CLVSegment": True,
            "ChanceOfReturn": ":.0f",
            "ConditionalFutureRevenue": ":,.0f",
            "PredictedCLV": ":,.0f",
        },
        title="Customer opportunity map",
        labels={
            "ChanceOfReturn": "Chance of buying again (%)",
            "ConditionalFutureRevenue": "Potential spending if the customer returns",
            "BusinessAction": "Suggested action",
        },
        size_max=28,
        opacity=0.62,
    )
    scatter.add_vline(
        x=probability_cutoff * 100,
        line_dash="dash",
        line_color="#5B6570",
        line_width=2,
    )
    scatter.add_hline(
        y=revenue_cutoff,
        line_dash="dash",
        line_color="#5B6570",
        line_width=2,
    )
    quadrant_style = dict(
        showarrow=False,
        font=dict(size=13, color="#182433"),
        bgcolor="rgba(255,255,255,0.88)",
        bordercolor="#DED5C8",
        borderpad=5,
    )
    scatter.add_annotation(xref="paper", yref="paper", x=0.02, y=0.96, text="WIN BACK", **quadrant_style)
    scatter.add_annotation(xref="paper", yref="paper", x=0.98, y=0.96, text="PROTECT LOYALTY", xanchor="right", **quadrant_style)
    scatter.add_annotation(xref="paper", yref="paper", x=0.98, y=0.04, text="GROW VALUE", xanchor="right", **quadrant_style)
    scatter.add_annotation(xref="paper", yref="paper", x=0.02, y=0.04, text="LOW-COST NURTURE", **quadrant_style)
    scatter.update_layout(height=650, legend=dict(orientation="h", y=1.12))
    scatter.update_xaxes(range=[0, 100], ticksuffix="%")
    scatter.update_yaxes(tickprefix=CURRENCY, range=[0, visible_limit * 1.05])
    st.plotly_chart(scatter, use_container_width=True)
    st.caption(
        "For readability, the chart hides the most extreme 1% of spending estimates. "
        "They remain included in all totals, tables and calculations."
    )

with priority_tab:
    st.subheader("Turn the customer groups into actions")
    st.write(
        "The same offer should not be sent to everyone. These four groups indicate the "
        "purpose of the contact—not a guaranteed customer response."
    )

    action_columns = st.columns(4)
    action_text = [
        ("Protect loyalty", "High return chance and high value", "Recognise loyalty, protect service quality and avoid preventable loss."),
        ("Win back now", "Lower return chance but high value", "Use a personal reminder, service call or carefully chosen return offer."),
        ("Grow customer value", "High return chance but lower value", "Recommend useful bundles, related products or a larger next purchase."),
        ("Low-cost nurture", "Lower return chance and lower value", "Use affordable email or automated communication rather than costly offers."),
    ]
    for column, (name, meaning, action) in zip(action_columns, action_text):
        count = int((filtered["BusinessAction"] == name).sum())
        with column:
            st.markdown(
                f"""
                <div class='action-card' style='border-top-color:{ACTION_COLORS[name]}'>
                <h4>{name}</h4>
                <div class='action-count'>{count:,} customers</div>
                <p><b>Meaning:</b> {meaning}</p>
                <p><b>Practical action:</b> {action}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("Customer contact list")
    st.write(
        "Choose how to rank the list, then download it for campaign planning. "
        "Start from the top and work within your available budget and staff capacity."
    )
    sort_choice = st.selectbox(
        "Show the most important customers first based on:",
        [
            "Likely future revenue",
            "Potential spending if they return",
            "Chance of buying again",
            "Longest time since last purchase",
        ],
    )
    sort_map = {
        "Likely future revenue": ("PredictedCLV", False),
        "Potential spending if they return": ("ConditionalFutureRevenue", False),
        "Chance of buying again": ("RepeatProbability", False),
        "Longest time since last purchase": ("RecencyDays", False),
    }
    sort_column, ascending = sort_map[sort_choice]
    ranked = filtered.sort_values(sort_column, ascending=ascending).copy()
    next_step = {
        "Protect loyalty": "Recognition and reliable service",
        "Win back now": "Personal return campaign",
        "Grow customer value": "Cross-sell or useful bundle",
        "Low-cost nurture": "Automated low-cost contact",
    }
    ranked["SuggestedNextStep"] = ranked["BusinessAction"].map(next_step)

    table = ranked[
        [
            "CustomerID",
            "PrimaryCountry",
            "BusinessAction",
            "SuggestedNextStep",
            "RepeatProbability",
            "ConditionalFutureRevenue",
            "PredictedCLV",
            "RecencyDays",
            "Frequency",
        ]
    ].rename(
        columns={
            "PrimaryCountry": "Country",
            "BusinessAction": "Customer group",
            "SuggestedNextStep": "Suggested next step",
            "RepeatProbability": "Chance of buying again",
            "ConditionalFutureRevenue": "Potential spending if returned",
            "PredictedCLV": "Likely future revenue",
            "RecencyDays": "Days since last purchase",
            "Frequency": "Previous orders",
        }
    )
    table["Chance of buying again"] = table["Chance of buying again"] * 100
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Chance of buying again": st.column_config.ProgressColumn(
                format="%.0f%%", min_value=0, max_value=100
            ),
            "Potential spending if returned": st.column_config.NumberColumn(
                format=f"{CURRENCY}%.0f"
            ),
            "Likely future revenue": st.column_config.NumberColumn(
                format=f"{CURRENCY}%.0f"
            ),
        },
        height=600,
    )
    st.download_button(
        "Download this customer list",
        ranked.to_csv(index=False).encode("utf-8"),
        file_name="customer_action_list.csv",
        mime="text/csv",
    )

with planning_tab:
    st.subheader("Test a campaign idea before spending money")
    st.write(
        "Adjust the assumptions below to see whether a campaign could be worthwhile. "
        "The result is a planning estimate, not a promise of profit."
    )

    controls, results = st.columns([1, 2])
    with controls:
        st.markdown("#### Your campaign assumptions")
        campaign_actions = st.multiselect(
            "Which customer groups will receive the campaign?",
            ACTION_ORDER,
            default=["Win back now"],
            key="campaign_actions",
        )
        uplift_points = st.slider(
            "How much could the campaign improve the chance of return?",
            0.0,
            20.0,
            5.0,
            0.5,
            help="Five points means that a 40% return chance is assumed to become 45%.",
        )
        gross_margin = st.slider(
            "How much of sales revenue becomes gross profit?",
            0,
            100,
            30,
            1,
        )
        contact_cost = st.number_input(
            "Cost to contact one customer",
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
    campaign["ExtraRevenue"] = (
        campaign["EffectiveUplift"] * campaign["ConditionalFutureRevenue"]
    )
    campaign["ExtraProfit"] = (
        campaign["ExtraRevenue"] * (gross_margin / 100) - contact_cost
    )
    recommended = campaign[campaign["ExtraProfit"] > 0]

    with results:
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Customers considered", f"{len(campaign):,}")
        r2.metric("Worth contacting under these assumptions", f"{len(recommended):,}")
        total_extra_profit = recommended["ExtraProfit"].sum()
        r3.metric("Possible extra profit", money(total_extra_profit))
        campaign_spend = len(recommended) * contact_cost
        roi = total_extra_profit / campaign_spend if campaign_spend > 0 else np.nan
        r4.metric("Possible return per campaign pound", "N/A" if np.isnan(roi) else f"{roi:.1f}×")

        if campaign.empty:
            st.info("Select at least one customer group to calculate the scenario.")
        else:
            scenario_chart = campaign.nlargest(20, "ExtraProfit").sort_values("ExtraProfit")
            colors = np.where(scenario_chart["ExtraProfit"] > 0, "#3A7D6F", "#C65D47")
            figure = go.Figure(
                go.Bar(
                    x=scenario_chart["ExtraProfit"],
                    y=scenario_chart["CustomerID"],
                    orientation="h",
                    marker_color=colors,
                    text=scenario_chart["ExtraProfit"].map(money),
                    textposition="outside",
                    cliponaxis=False,
                    hovertemplate="Customer %{y}<br>Possible extra profit: £%{x:,.0f}<extra></extra>",
                )
            )
            figure.update_layout(
                title="Customers with the strongest campaign opportunity",
                xaxis_title="Possible extra profit",
                yaxis_title="Customer",
                xaxis_tickprefix=CURRENCY,
                height=620,
                margin=dict(l=70, r=100, t=70, b=45),
            )
            st.plotly_chart(figure, use_container_width=True)

    st.markdown(
        "<div class='warning-note'><b>Use this as a planning guide.</b> "
        "The dashboard assumes that your campaign improves the chance of return by the amount "
        "you selected. Run a small controlled campaign before committing a large budget.</div>",
        unsafe_allow_html=True,
    )

    with st.expander("How is the campaign estimate calculated?"):
        st.write(
            "For each customer, the dashboard estimates additional sales from the assumed "
            "improvement in return chance. It then keeps the gross-profit portion and subtracts "
            "the cost of contacting that customer."
        )
        st.code(
            "Possible extra profit = improvement in return chance × potential spending "
            "× gross margin − contact cost",
            language=None,
        )

    country_summary = (
        filtered.groupby("PrimaryCountry", observed=True)
        .agg(
            Customers=("CustomerID", "count"),
            LikelyRevenue=("PredictedCLV", "sum"),
        )
        .reset_index()
        .nlargest(12, "LikelyRevenue")
        .sort_values("LikelyRevenue")
    )
    country_summary["Label"] = country_summary["LikelyRevenue"].map(money)
    country_figure = px.bar(
        country_summary,
        x="LikelyRevenue",
        y="PrimaryCountry",
        orientation="h",
        text="Label",
        color="LikelyRevenue",
        color_continuous_scale=["#F0E4D1", "#355C7D"],
        title="Countries with the greatest likely future revenue",
        labels={
            "LikelyRevenue": "Likely future revenue",
            "PrimaryCountry": "Country",
        },
    )
    country_figure.update_traces(textposition="outside", cliponaxis=False)
    country_figure.update_layout(height=600, coloraxis_showscale=False)
    country_figure.update_xaxes(tickprefix=CURRENCY)
    st.plotly_chart(country_figure, use_container_width=True)

with explanation_tab:
    st.subheader("What the dashboard did—in everyday language")
    st.write(
        "The dashboard reviewed each customer’s past buying pattern. It then answered two "
        "simple questions and combined the answers into one useful revenue estimate."
    )

    step1, step2, step3 = st.columns(3)
    with step1:
        st.markdown(
            """
            <div class='explain-card'>
            <div class='step-number'>1</div>
            <h4>Will this customer buy again?</h4>
            <p>We estimate a chance from 0% to 100% using the customer’s previous buying behaviour.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step2:
        st.markdown(
            """
            <div class='explain-card'>
            <div class='step-number'>2</div>
            <h4>If they return, how much might they spend?</h4>
            <p>We estimate possible future spending from order size, frequency and product variety.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step3:
        st.markdown(
            """
            <div class='explain-card'>
            <div class='step-number'>3</div>
            <h4>What revenue can we reasonably expect?</h4>
            <p>We combine the chance of return with the amount the customer may spend.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    median_value = filtered["PredictedCLV"].median()
    example_index = (filtered["PredictedCLV"] - median_value).abs().idxmin()
    example = filtered.loc[example_index]
    st.subheader("A simple customer example")
    e1, e2, e3 = st.columns(3)
    e1.metric("Chance of buying again", f"{example['RepeatProbability']:.0%}")
    e2.metric("Possible spending if they return", money(example["ConditionalFutureRevenue"]))
    e3.metric("Likely future revenue", money(example["PredictedCLV"]))
    st.markdown(
        f"""
        <div class='business-note'>
        For customer <b>{example['CustomerID']}</b>, the dashboard combines a
        <b>{example['RepeatProbability']:.0%}</b> chance of buying again with approximately
        <b>{money(example['ConditionalFutureRevenue'])}</b> of possible spending.
        This gives approximately <b>{money(example['PredictedCLV'])}</b> in likely future revenue.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("How much confidence should management place in it?")
    q1, q2, q3 = st.columns(3)
    q1.metric("Return-customer ranking score", "79 / 100")
    q2.metric("Future revenue pattern explained", "68%")
    q3.metric("Average revenue estimation error", f"{CURRENCY}1,048")
    st.write(
        "The 79/100 score means the model is generally good at ranking a returning customer "
        "above a non-returning customer. Overall, these results are useful for prioritising "
        "customers, but they are not perfect forecasts or guarantees."
    )

    st.markdown(
        """
        <div class='warning-note'>
        <b>Important limits</b><br>
        • The dashboard learns from past behaviour; unusual future events may change customer decisions.<br>
        • “Likely future revenue” is revenue, not final profit.<br>
        • A high score does not guarantee that one customer will return.<br>
        • Campaign results should be tested with a small control group before a large rollout.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Technical details for anyone who wants them"):
        st.write(
            "The return estimate comes from a logistic regression. The spending estimate "
            "comes from a conditional linear regression trained only on returning customers. "
            "The final expected value is the return probability multiplied by conditional revenue."
        )
        st.markdown(
            "**Information used:** days since last purchase, previous order frequency, "
            "past spending, average order size, quantity, product variety and UK/non-UK location."
        )
