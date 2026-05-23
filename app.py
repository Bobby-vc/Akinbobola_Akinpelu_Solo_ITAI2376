import streamlit as st
import sys
import os
import contextlib
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Trading Advisor",
    page_icon="📈",
    layout="wide",
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .report-box {
        background: #0e1117;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("📈 AI Trading Advisor")
st.caption("Multi-Agent Investment Analysis System — powered by CrewAI & GPT-4o")
st.divider()

# ── Sidebar — Portfolio ────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📊 Portfolio")
    if st.button("🔄 Refresh Portfolio", use_container_width=True):
        with st.spinner("Fetching portfolio..."):
            try:
                import alpaca_trade_api as tradeapi
                api = tradeapi.REST(
                    os.getenv("APCA_API_KEY_ID"),
                    os.getenv("APCA_API_SECRET_KEY"),
                    base_url=os.getenv("APCA_API_BASE_URL"),
                )
                account = api.get_account()
                positions = api.list_positions()

                st.metric("💵 Cash", f"${float(account.cash):,.2f}")
                st.metric("📦 Portfolio Value", f"${float(account.portfolio_value):,.2f}")
                st.metric("⚡ Buying Power", f"${float(account.buying_power):,.2f}")

                st.subheader("Open Positions")
                if positions:
                    for p in positions:
                        pnl = float(p.unrealized_pl)
                        color = "🟢" if pnl >= 0 else "🔴"
                        st.markdown(
                            f"{color} **{p.symbol}** — {p.qty} shares  \n"
                            f"Avg: ${float(p.avg_entry_price):.2f} | "
                            f"Now: ${float(p.current_price):.2f} | "
                            f"P&L: ${pnl:.2f}"
                        )
                else:
                    st.info("No open positions.")
            except Exception as e:
                st.error(f"Could not load portfolio: {e}")

    st.divider()
    st.caption("All trades use Alpaca paper trading — no real money.")

# ── Main — Input Form ──────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    question = st.text_input(
        "💬 Investment Question",
        placeholder="Is NVDA a good buy right now?",
    )
with col2:
    ticker = st.text_input("📌 Ticker", placeholder="NVDA").upper().strip()

experience = st.radio(
    "🎓 Experience Level",
    ["beginner", "intermediate", "advanced"],
    horizontal=True,
)

run_btn = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

# ── Run the Crew ───────────────────────────────────────────────────────────────
if run_btn:
    if not question:
        st.warning("Please enter an investment question.")
    elif not ticker:
        st.warning("Please enter a stock ticker.")
    else:
        log_output = StringIO()
        status = st.status("🤖 Agents are working...", expanded=True)

        try:
            # Add src to path so the package resolves correctly
            src_path = os.path.join(os.path.dirname(__file__), "src")
            if src_path not in sys.path:
                sys.path.insert(0, src_path)

            from first_ai_agents.crew import FirstAiAgents

            inputs = {
                "question": question,
                "ticker": ticker,
                "experience_level": experience,
                "confidence_threshold": 0.7,
            }

            with status:
                st.write("**Stock Analyst** — fetching live data & news...")
                with contextlib.redirect_stdout(log_output):
                    FirstAiAgents().crew().kickoff(inputs=inputs)
                st.write("**Trading Advisor** — evaluating signal & executing...")

            status.update(label="✅ Analysis complete!", state="complete", expanded=False)

            # ── Trade Report ───────────────────────────────────────────────────
            report_path = os.path.join(os.path.dirname(__file__), "trade_report.md")
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    report = f.read()
                st.markdown("## 📋 Trade Report")
                st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
            else:
                st.info("No trade report generated.")

            # ── Agent Logs (collapsible) ───────────────────────────────────────
            logs = log_output.getvalue()
            if logs:
                with st.expander("🔍 View Agent Logs"):
                    st.code(logs, language=None)

        except Exception as e:
            status.update(label="❌ Error", state="error", expanded=True)
            st.error(f"Something went wrong: {e}")
            logs = log_output.getvalue()
            if logs:
                with st.expander("Logs"):
                    st.code(logs, language=None)
