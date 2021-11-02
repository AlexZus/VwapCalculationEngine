import asyncio, json
from typing import List, Type, Dict, Union, Callable, Any
from websockets import connect
from WebsocketApi.baseExchange import WebsocketApiExchangeInterface as WebsocketApiExchangeInterface
from VWAP.computer import VWAPComputer


# This class runs the websocket client and
# receive messages from server.
# It holds instances of VWAPComputer class
# one per trading product. And it uses
# the WebsocketApiExchangeInterface for parsing incoming messages
# and for composing outgoing messages.
class VWAPEngine:
    exchange_websocket_api_class: Type[WebsocketApiExchangeInterface]
    product_ids: List[str]
    vwap_computers: Dict[str, VWAPComputer]
    output_callback: Union[None, Callable[[Dict[str, Any]], None]]
    port: Union[None, int]

    def __init__(self, exchange_websocket_api_class: Type[WebsocketApiExchangeInterface],
                 product_ids: List[str], window_size: int, port: Union[None, int] = None,
                 output_callback: Union[None, Callable[[Dict[str, Any]], None]] = None):
        self.exchange_websocket_api_class = exchange_websocket_api_class
        self.product_ids = product_ids
        self.vwap_computers = {product_id: VWAPComputer(window_size) for product_id in product_ids}
        self.port = port
        self.output_callback = output_callback

    def run(self):
        asyncio.run(self.start_client())

    def __await__(self):
        return self.start_client().__await__()

    async def start_client(self):
        api = self.exchange_websocket_api_class
        uri = api.get_uri()
        if self.port is not None:
            uri += f':{self.port}'
        async with connect(uri) as websocket:
            print(f'Connected to {api.__name__} [{websocket.remote_address}]')
            await websocket.send(api.compose_subscribe_matches(self.product_ids))
            async for message in websocket:
                await self.process(api, message)
            print(f'Disconnected from {api.__name__} [{websocket.remote_address}]')

    async def process(self, api: WebsocketApiExchangeInterface, message: str):
        input_data = json.loads(message)
        if "match" == api.get_input_msg_type(input_data):
            product_id = api.get_input_msg_product_id(input_data)
            if product_id not in self.vwap_computers:
                raise ValueError("The not requested product id was received")
            vwap_computer = self.vwap_computers[product_id]
            vwap_computer.add(*api.get_input_msg_match_price_and_volume(input_data))
            if self.output_callback is not None:
                self.output_callback({
                    "product_id": product_id,
                    "vwap": vwap_computer.get()})
            else:
                print(f'vwap{vwap_computer.get_current_window()} for {product_id} is {vwap_computer.get()}')
