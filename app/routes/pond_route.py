from flask import Blueprint, render_template, session
from app.constants import get_background_url, get_duck_image_url
import yfinance as yf
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

pond_bp = Blueprint('pond', __name__)

@pond_bp.route('/pond')
def pond():
    selected = session.get('selected_stocks', [])
    duck_urls = []
    stock_details = []
    stock_changes = []
    stock_data = []

    graphs_dir = os.path.join('app', 'static', 'graphs')
    os.makedirs(graphs_dir, exist_ok=True)

    for ticker in selected:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='2d')
        info = stock.info

        if len(hist) < 2:
            change = 0
            current_price = hist['Close'].iloc[-1] if not hist.empty else 0
            previous_close = current_price
        else:
            previous_close = hist['Close'].iloc[-2]
            current_price = hist['Close'].iloc[-1]
            change = current_price - previous_close

        percent_change = (change / previous_close) * 100 if previous_close != 0 else 0
        mood = 'good' if change >= 0 else 'bad'

        def fmt_millions(val):
            return f"{val / 1_000_000:.2f}M" if isinstance(val, (int, float)) else "--"

        def fmt_billions(val):
            return f"{val / 1_000_000_000:.2f}B" if isinstance(val, (int, float)) else "--"

        volume_fmt = fmt_millions(info.get('volume'))
        avg_volume_fmt = fmt_millions(info.get('averageVolume'))
        market_cap_fmt = fmt_billions(info.get('marketCap'))
        pe_ratio = info.get('trailingPE')
        pe_ratio_fmt = f"{pe_ratio:.2f}" if pe_ratio else "--"
        change_52wk = info.get('52WeekChange')
        change_52wk_fmt = f"{change_52wk * 100:.2f}%" if change_52wk else "--"

        duck_urls.append(get_duck_image_url(mood))
        stock_changes.append(change)
        stock_details.append(f"{ticker.upper()}: {change:+.2f}\nPrice: ${current_price:.2f}")

        #stock graph
        graph_filename = f"{ticker.upper()}.png"
        graph_path = os.path.join(graphs_dir, graph_filename)
        graph_url = f"/static/graphs/{graph_filename}"

        hist_graph = stock.history(period='1mo')
        if not hist_graph.empty:
            plt.figure(figsize=(4, 2))
            plt.plot(hist_graph.index, hist_graph['Close'], color='black', linewidth=2)
            plt.title(f"{ticker.upper()} - Last 30 Days")
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.savefig(graph_path)
            plt.close()

        stock_data.append({
            "ticker": ticker.upper(),
            "price": f"${current_price:.2f}",
            "change": f"{change:+.2f}",
            "percent_change": f"{percent_change:+.2f}%",
            "volume": volume_fmt,
            "avg_volume": avg_volume_fmt,
            "market_cap": market_cap_fmt,
            "pe_ratio": pe_ratio_fmt,
            "change_52wk": change_52wk_fmt,
            "graph_url": graph_url
        })

    return render_template(
        'pond.html',
        background=get_background_url('pond'),
        duck_urls=duck_urls,
        stock_details=stock_details,
        stock_changes=stock_changes,
        stock_data=stock_data,
        current_date=datetime.now().strftime("%B %d, %Y"),
        current_time=datetime.now().strftime("%I:%M %p")
    )
