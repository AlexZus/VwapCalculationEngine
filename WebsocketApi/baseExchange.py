from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any


def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider


# This is base class for specific exchange websocket API.
# So it is easy to add functionality for other exchanges by
# extending this class.
class WebsocketApiExchangeInterface(metaclass=ABCMeta):
    uri = ""

    @classmethod
    def get_uri(cls) -> str:
        return cls.uri

    @staticmethod
    @abstractmethod
    def compose_subscribe_matches(self, product_ids: List[str]) -> str:
        return ''

    @staticmethod
    @abstractmethod
    def get_input_msg_type(_parsed_json_input: Dict[str, Any]) -> str:
        return ''

    @staticmethod
    @abstractmethod
    def get_input_msg_match_price_and_volume(_parsed_json_input: Dict[str, Any]) -> (float, float):
        return 0, 0

    @staticmethod
    @abstractmethod
    def get_input_msg_product_id(_parsed_json_input: Dict[str, Any]) -> str:
        return ''
