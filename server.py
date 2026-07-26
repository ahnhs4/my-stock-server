from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import requests
import os

app = Flask(__name__)
CORS(app)

# 1. 공포/탐욕 지수 (Fear & Greed) API
@app.route('/api/fear-greed', methods=['GET'])
def get_fear_greed():
    try:
        # CNN 서버에서 실제 공포/탐욕 지수 가져오기
        headers = {'User-Agent': 'Mozilla/5.0'}
        url = "https://production.api.cnn.io/metrics/quotes/centers/index_fear_and_greed"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        score = data['fear_and_greed']['score']
        rating = data['fear_and_greed']['rating']
        
        return jsonify({"score": round(score), "rating": rating})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 2. 주식 실시간 가격 (Stock Price) API
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
    # 클라우드 서버(Render)가 지정해 주는 포트 번호를 사용
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
