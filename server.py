from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/price/<ticker>', methods=['GET'])
def get_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['last_price']
        return jsonify({"ticker": ticker.upper(), "price": float(price)})
    except Exception as e:
        try:
            data = stock.history(period="1d")
            if not data.empty:
                price = data['Close'].iloc[-1]
                return jsonify({"ticker": ticker.upper(), "price": float(price)})
            else:
                return jsonify({"error": "종목 데이터를 찾을 수 없습니다."}), 404
        except Exception as e2:
            return jsonify({"error": str(e2)}), 400

if __name__ == '__main__':
    # 클라우드 서버가 지정해 주는 포트 번호를 사용하도록 수정
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)