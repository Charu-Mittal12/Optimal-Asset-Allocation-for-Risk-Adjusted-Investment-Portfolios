import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
from assets.asset_factory import AssetFactory
from data_fetcher.data_factory import DataFetcherFactory
from optimizer.optimizer_factory import OptimizerFactory
from portfolio.manager import PortfolioManager
from portfolio_analyzer.portfolio_analyzer import PortfolioAnalyzer

# ----------------------------------------
# PAGE CONFIG & STYLING
# ----------------------------------------
st.set_page_config(page_title="Portfolio Optimizer", layout="wide")

st.markdown("""
<style>
body {
    background-color: #FFFFFF;
    color: #1A1A1A;
    font-family: 'Inter', sans-serif;
}
h1, h2, h3 {
    color: #008B8B;
    font-weight: 600;
    text-align: center;
}
hr {
    border: 1px solid #008B8B;
    opacity: 0.3;
}
.stButton>button {
    background-color: #008B8B;
    color: white;
    border-radius: 6px;
    border: none;
    font-weight: 600;
    padding: 0.45em 1.2em;
    transition: all 0.2s ease;
}
.stButton>button:hover {
    background-color: #006666;
}
.dataframe {
    background-color: #FAFAFA !important;
    border: 1px solid #008B8B !important;
    border-radius: 6px !important;
    text-align: center !important;
    margin: auto !important;
}
thead tr th {
    background-color: #E0FFFF !important;
    color: #004F4F !important;
    text-align: center !important;
    font-weight: 700 !important;
}
tbody tr td {
    text-align: center !important;
}
section[data-testid="stSidebar"] {
    background-color: #F8F8F8 !important;
    border-right: 1px solid #008B8B;
}
.metric-card {
    background-color: #F9FFFF;
    border: 1px solid #00A3A3;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    padding: 15px;
    text-align: center;
    transition: transform 0.2s ease;
}
.metric-card:hover {
    transform: scale(1.02);
}
.metric-title {
    font-size: 14px;
    color: #005555;
    font-weight: 600;
}
.metric-value {
    font-size: 20px;
    font-weight: 700;
    color: #008B8B;
}
.center-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# TITLE
# ----------------------------------------
st.title("Portfolio Optimizer")
st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------
# SIDEBAR SETTINGS
# ----------------------------------------
st.sidebar.title("Optimization Settings")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-01-01"))
optimizer_method = st.sidebar.selectbox("Optimizer Method", ["mean_variance", "covariance"])
risk_free_rate = st.sidebar.slider("Risk-Free Rate", 0.0, 0.10, 0.02, step=0.005)
save_config = st.sidebar.checkbox("Save config.json after optimization", value=False)

# ----------------------------------------
# TABLE DATA
# ----------------------------------------
def get_top_companies_table():
    data = [
        {"Company": "Apple", "Symbol": "AAPL", "Asset Type": "stock"},
        {"Company": "Microsoft", "Symbol": "MSFT", "Asset Type": "stock"},
        {"Company": "Nvidia", "Symbol": "NVDA", "Asset Type": "stock"},
        {"Company": "Google", "Symbol": "GOOGL", "Asset Type": "stock"},
        {"Company": "Tesla", "Symbol": "TSLA", "Asset Type": "stock"},
        {"Company": "Amazon", "Symbol": "AMZN", "Asset Type": "stock"},
    ]
    return pd.DataFrame(data)

# ----------------------------------------
# LAYOUT
# ----------------------------------------
left_col, right_col = st.columns([1, 1])  # 50% left, 50% right

# LEFT SIDE: Config Panel
with left_col:
    # Center-align all content
    st.markdown("""
        <div style='text-align: center;'>
            <h3 style='color:#008B8B; font-weight:600;'>Configuration Panel</h3>
        </div>
    """, unsafe_allow_html=True)

    # Center buttons
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Load", use_container_width=True):
            try:
                with open("config.json", "r") as f:
                    cfg = json.load(f)
                st.session_state["asset_entries"] = cfg
                st.success("Configuration loaded successfully.")
            except Exception as e:
                st.error(f"Failed to load config.json: {e}")
    with c2:
        if st.button("Save", use_container_width=True):
            try:
                with open("config.json", "w") as f:
                    json.dump(st.session_state.get("asset_entries", []), f, indent=2)
                st.success("Configuration saved successfully.")
            except Exception as e:
                st.error(f"Failed to save config.json: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Session initialization
    if "asset_entries" not in st.session_state:
        st.session_state["asset_entries"] = []

    # Input section (centered)
    st.markdown("""
        <div style='text-align: center;'>
            <h4 style='color:#005555;'>Add Custom Assets</h4>
        </div>
    """, unsafe_allow_html=True)

    new_type = st.selectbox("Asset Type", ["stock", "etf", "crypto", "bond"])
    new_name = st.text_input("Name", key="new_name")
    new_symbol = st.text_input("Symbol", key="new_symbol")

    if st.button("Add Asset", use_container_width=True):
        if not new_name or not new_symbol:
            st.warning("Please enter both name and symbol.")
        else:
            st.session_state["asset_entries"].append({
                "asset_type": new_type,
                "name": new_name,
                "symbol": new_symbol
            })
            st.success(f"Added {new_symbol} ({new_type}).")

    # Center dataframe display
    if st.session_state["asset_entries"]:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state["asset_entries"]), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Clear All Assets", use_container_width=True):
            st.session_state["asset_entries"] = []
            st.info("Cleared all assets.")


# RIGHT SIDE: Centered Table + Selection
with right_col:
    # Center alignment styling
    st.markdown("""
        <style>
        .center-content {
            text-align: center;
        }
        .asset-table {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .asset-row {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 85%;
            background-color: #F9FFFF;
            border: 1px solid #00A3A3;
            border-radius: 8px;
            margin: 6px 0;
            padding: 8px 0;
            box-shadow: 0 1px 4px rgba(0, 139, 139, 0.1);
        }
        .asset-header {
            font-weight: 700;
            color: #004F4F;
            text-align: center;
            margin-bottom: 10px;
        }
        .asset-header div {
            padding: 4px 0;
        }
        .asset-cell {
            text-align: center;
            flex: 2;
        }
        .asset-checkbox {
            display: flex;
            justify-content: center;
            align-items: center;
            flex: 1;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<div class='center-content'><h3 style='color:#008B8B;'>Select Assets from Top Companies</h3></div>", unsafe_allow_html=True)

    # Define top companies
    top_table = pd.DataFrame([
        {"Company": "Apple", "Symbol": "AAPL", "Asset Type": "Stock"},
        {"Company": "Microsoft", "Symbol": "MSFT", "Asset Type": "Stock"},
        {"Company": "Nvidia", "Symbol": "NVDA", "Asset Type": "Stock"},
        {"Company": "Google", "Symbol": "GOOGL", "Asset Type": "Stock"},
        {"Company": "Tesla", "Symbol": "TSLA", "Asset Type": "Stock"},
        {"Company": "Amazon", "Symbol": "AMZN", "Asset Type": "Stock"},
    ])

    # Table Header
    st.markdown("""
        <div class='asset-table'>
            <div class='asset-row asset-header'>
                <div class='asset-cell'>Company</div>
                <div class='asset-cell'>Symbol</div>
                <div class='asset-cell'>Asset Type</div>
                <div class='asset-cell'>Select</div>
            </div>
    """, unsafe_allow_html=True)

    selected_symbols = []
    # Render rows
    for i, row in top_table.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            st.markdown(f"<div style='text-align:center;'>{row['Company']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align:center;'>{row['Symbol']}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='text-align:center;'>{row['Asset Type']}</div>", unsafe_allow_html=True)
        with col4:
            st.markdown("<div style='display:flex;justify-content:center;align-items:center;'>", unsafe_allow_html=True)
            if st.checkbox("", key=f"chk_{i}"):
                selected_symbols.append(row["Symbol"])
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Centered Load Button
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("Load Selected Assets", use_container_width=False):
        if "asset_entries" not in st.session_state:
            st.session_state["asset_entries"] = []
        for sym in selected_symbols:
            comp = top_table[top_table["Symbol"] == sym].iloc[0]
            st.session_state["asset_entries"].append({
                "asset_type": comp["Asset Type"],
                "name": comp["Company"],
                "symbol": comp["Symbol"]
            })
        st.success(f"Loaded {len(selected_symbols)} selected assets into portfolio.")
    st.markdown("</div>", unsafe_allow_html=True)



# ----------------------------------------
# RUN OPTIMIZATION
# ----------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Run Portfolio Optimization")

def plot_donut_3d(weights: Dict):
    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(
        weights.values(), labels=weights.keys(),
        autopct='%1.1f%%', startangle=90,
        colors=plt.cm.winter(np.linspace(0.2, 0.8, len(weights))),
        wedgeprops=dict(width=0.35, edgecolor='white')
    )
    for w in wedges:
        w.set_linewidth(1.5)
        w.set_edgecolor("white")
        w.set_alpha(0.95)
    ax.set_facecolor("#FFFFFF")
    centre_circle = plt.Circle((0, 0), 0.30, fc='white', ec='#008B8B', lw=2)
    fig.gca().add_artist(centre_circle)
    plt.tight_layout()
    return fig

if st.button("Run Optimization"):
    if not st.session_state.get("asset_entries"):
        st.error("No assets defined. Please add at least one asset.")
    else:
        specs: List[Dict] = st.session_state["asset_entries"]
        manager = PortfolioManager(
            asset_factory=AssetFactory,
            data_factory=DataFetcherFactory,
            optimizer_factory=OptimizerFactory,
            analyzer=PortfolioAnalyzer(risk_free_rate=risk_free_rate)
        )

        try:
            with st.spinner("Fetching data..."):
                collection = manager.build_collection_from_specs(specs)
                price_df = manager.fetch_prices(collection, str(start_date), str(end_date))
                st.success(f"Fetched price data successfully! (Shape: {price_df.shape})")

            expected_returns, covariance, _ = manager.compute_expected_returns_covariance(price_df)
            weights = manager.optimize(expected_returns, covariance, method=optimizer_method)
            weights = weights / weights.sum()

            alloc = pd.DataFrame({
                "weight": weights,
                "expected_return": expected_returns
            })
            alloc["contribution"] = alloc["weight"] * alloc["expected_return"]

            st.markdown("### Portfolio Allocation")
            st.dataframe(
                alloc.style.format({"weight": "{:.4f}", "expected_return": "{:.4%}", "contribution": "{:.4%}"}),
                use_container_width=True
            )

            # Centered donut chart
            fig = plot_donut_3d(dict(zip(alloc.index, alloc["weight"])))
            left_space, center_col, right_space = st.columns([1, 2, 1])
            with center_col:
                st.pyplot(fig, use_container_width=False)

            with st.spinner("Analyzing portfolio..."):
                analysis = manager.analyze_portfolio(price_df, weights)

            # Compact summary boxes
            st.markdown("### Portfolio Summary")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>Expected Return</div><div class='metric-value'>{analysis.get('expected_return', 0):.2%}</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>Volatility</div><div class='metric-value'>{analysis.get('volatility', 0):.2%}</div></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>Sharpe Ratio</div><div class='metric-value'>{analysis.get('sharpe_ratio', 0):.2f}</div></div>", unsafe_allow_html=True)

            csv = alloc.to_csv(index=True)
            st.download_button("Download Allocation CSV", data=csv, file_name="allocation.csv")

        except Exception as exc:
            st.error(f"Pipeline failed: {exc}")
            st.exception(exc)
