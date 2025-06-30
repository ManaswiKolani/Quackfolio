from flask import Blueprint, render_template, request, session, redirect, url_for
from app.constants import get_background_url
import yfinance as yf

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    if 'selected_stocks' not in session:
        session['selected_stocks'] = []

    error_message = None

    if request.method == 'POST':
        if 'add_stock' in request.form:
            stock = request.form['add_stock'].upper().strip()
            if stock and stock not in session['selected_stocks'] and len(session['selected_stocks']) < 5:
                session['selected_stocks'].append(stock)
                session.modified = True

        elif 'remove_stock' in request.form:
            stock = request.form['remove_stock']
            if stock in session['selected_stocks']:
                session['selected_stocks'].remove(stock)
                session.modified = True

        elif 'done' in request.form:
            invalid_tickers = []
            for symbol in session['selected_stocks']:
                stock = yf.Ticker(symbol)
                try:
                    info = stock.info
                    if not info or info.get('regularMarketPrice') is None:
                        invalid_tickers.append(symbol)
                except Exception:
                    invalid_tickers.append(symbol)

            if invalid_tickers:
                error_message = f"{', '.join(invalid_tickers)} is not a valid stock symbol."
            else:
                return redirect(url_for('pond.pond'))

    background = get_background_url('search')
    return render_template('search.html',
                           selected=session['selected_stocks'],
                           background=background,
                           error_message=error_message)
