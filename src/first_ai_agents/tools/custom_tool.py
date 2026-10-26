import os
import yfinance as yf
import alpaca_trade_api as tradeapi
from crewai.tools import tool
from dotenv import load_dotenv

from first_ai_agents.database import (
    cache_stock_data, get_cached_stock, log_trade, log_portfolio_snapshot,
)

load_dotenv()


@tool("Get Stock Price Data")
def get_stock_data(ticker: str) -> str:
    """Fetches current price, 52-week high/low, volume, P/E ratio,
    and recent 5-day closing prices for a given stock ticker."""
    cached = get_cached_stock(ticker)
    if cached:
        return cached["formatted"]

    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="5d")
    closes = [round(c, 2) for c in hist['Close'].tolist()]
    formatted = f"""
    Ticker: {ticker}
    Current Price: ${info.get('currentPrice', 'N/A')}
    52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}
    52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}
    P/E Ratio: {info.get('trailingPE', 'N/A')}
    Volume: {info.get('volume', 'N/A')}
    Recent 5-Day Closes: {closes}
    """
    cache_stock_data(ticker, {
        "formatted": formatted,
        "currentPrice": info.get('currentPrice'),
        "fiftyTwoWeekHigh": info.get('fiftyTwoWeekHigh'),
        "fiftyTwoWeekLow": info.get('fiftyTwoWeekLow'),
        "trailingPE": info.get('trailingPE'),
        "volume": info.get('volume'),
        "closes": closes,
    })
    return formatted


@tool("Get Stock News")
def get_stock_news(ticker: str) -> str:
    """Fetches the most recent news headlines for a given stock ticker
    using Yahoo Finance. Useful for sentiment analysis."""
    stock = yf.Ticker(ticker)
    news = stock.news[:5]
    if not news:
        return f"No recent news found for {ticker}."
    headlines = "\n".join([f"- {n['content']['title']}" for n in news])
    return f"Recent news for {ticker}:\n{headlines}"


@tool("Execute Paper Trade")
def execute_paper_trade(ticker: str, qty: int, side: str) -> str:
    """Executes a paper trade on Alpaca Markets.
    ticker: stock symbol (e.g. 'AAPL')
    qty: number of shares to trade
    side: must be 'buy' or 'sell'
    All trades go to the paper trading sandbox — no real money involved."""
    api = tradeapi.REST(
        os.getenv("APCA_API_KEY_ID"),
        os.getenv("APCA_API_SECRET_KEY"),
        base_url=os.getenv("APCA_API_BASE_URL")
    )
    try:
        order = api.submit_order(
            symbol=ticker,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        log_trade(ticker, qty, side, order.id, order.status)
        return (
            f"Order submitted successfully!\n"
            f"Action: {side.upper()} {qty} shares of {ticker}\n"
            f"Order ID: {order.id}\n"
            f"Status: {order.status}\n"
            f"Disclaimer: This is a simulated paper trade. Not real financial advice."
        )
    except Exception as e:
        return f"Trade execution failed: {str(e)}"


@tool("Check Portfolio")
def get_portfolio() -> str:
    """Returns the current paper trading portfolio from Alpaca,
    including cash balance, total portfolio value, and open positions."""
    api = tradeapi.REST(
        os.getenv("APCA_API_KEY_ID"),
        os.getenv("APCA_API_SECRET_KEY"),
        base_url=os.getenv("APCA_API_BASE_URL")
    )
    try:
        account = api.get_account()
        positions = api.list_positions()
        log_portfolio_snapshot(
            cash=float(account.cash),
            portfolio_value=float(account.portfolio_value),
            buying_power=float(account.buying_power),
            positions=[
                {
                    "symbol": p.symbol,
                    "qty": p.qty,
                    "avg_entry_price": p.avg_entry_price,
                    "current_price": p.current_price,
                    "unrealized_pl": p.unrealized_pl,
                }
                for p in positions
            ],
        )
        if positions:
            pos_str = "\n".join([
                f"  {p.symbol}: {p.qty} shares @ avg ${p.avg_entry_price} "
                f"(current: ${p.current_price}, P&L: ${p.unrealized_pl})"
                for p in positions
            ])
        else:
            pos_str = "  No open positions."
        return (
            f"Cash Available: ${account.cash}\n"
            f"Portfolio Value: ${account.portfolio_value}\n"
            f"Buying Power: ${account.buying_power}\n"
            f"Open Positions:\n{pos_str}"
        )
    except Exception as e:
        return f"Failed to retrieve portfolio: {str(e)}"