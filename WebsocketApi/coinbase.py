from WebsocketApi.baseExchange import WebsocketApiExchangeInterface, overrides
from typing import List, Dict, Any, Callable
import json


# This class contains all information needed for
# parsing incoming messages and composing outgoing messages.
class CoinbaseWebsocketApi(WebsocketApiExchangeInterface):
    uri = "wss://ws-feed.exchange.coinbase.com"
    send_coroutine: Callable[[str], Any]

    def __init__(self, send_coroutine: Callable[[str], Any]):
        self.send_coroutine = send_coroutine

    @staticmethod
    @overrides(WebsocketApiExchangeInterface)
    def compose_subscribe_matches(product_ids: List[str]) -> str:
        return json.dumps({
            "type": "subscribe",
            "product_ids": product_ids,
            "channels": ["matches"]
        })

    @staticmethod
    @overrides(WebsocketApiExchangeInterface)
    def get_input_msg_type(parsed_json_input: Dict[str, Any]) -> str:
        return parsed_json_input["type"]

    @staticmethod
    @overrides(WebsocketApiExchangeInterface)
    def get_input_msg_match_price_and_volume(parsed_json_input: Dict[str, Any]) -> (float, float):
        return float(parsed_json_input["price"]), float(parsed_json_input["size"])

    @staticmethod
    @overrides(WebsocketApiExchangeInterface)
    def get_input_msg_product_id(parsed_json_input: Dict[str, Any]) -> str:
        return parsed_json_input["product_id"]
