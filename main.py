from WebsocketApi.coinbase import CoinbaseWebsocketApi
from vwapEngine import VWAPEngine

if __name__ == '__main__':
    engine = VWAPEngine(CoinbaseWebsocketApi, [
            "BTC-USD",
            "ETH-USD",
            "ETH-BTC"
        ], window_size=200)
    engine.run()
