import pytest, json, asyncio, random, websockets
from typing import List, Dict, Any
from websockets import client, server
from VWAP.computer import VWAPComputer
from WebsocketApi.baseExchange import overrides
from WebsocketApi.coinbase import CoinbaseWebsocketApi
from vwapEngine import VWAPEngine


class ExchangeWebsocketApiMock(CoinbaseWebsocketApi):
    uri = "ws://localhost"


class ExchangeWebsocketServerMock:
    port: int
    connections: List[server.WebSocketServerProtocol]
    server: server.WebSocketServer
    data: List[Dict[str, Any]]

    def __init__(self, data_len: int, product_ids: List[str]):
        self.connections = []
        self.server = asyncio.get_event_loop().run_until_complete(websockets.serve(
            lambda connection, path, this=self: this.connection_handler(connection, path), 'localhost', 0))
        self.port = self.server.sockets[0].getsockname()[1]
        self.data = []
        random.seed(1)
        print()
        self.generate_data(data_len, product_ids)

    def generate_data(self, data_len: int, product_ids: List[str]):
        product_base_prices = [random.uniform(100, 10000) for _ in range(len(product_ids))]
        for _ in range(data_len):
            product_indx = random.randrange(0, len(product_ids))
            product_id = product_ids[product_indx]
            price = product_base_prices[product_indx] + random.uniform(-100, 100)
            volume = random.uniform(0.1, 100)
            object_to_send = {
                "type": "match",
                "product_id": product_id,
                "price": price,
                "size": volume
            }
            msg_to_send = json.dumps(object_to_send)
            self.data.append({"object_to_send": object_to_send, "msg_to_send": msg_to_send})

    def __await__(self):
        return self.server.wait_closed().__await__()

    async def connection_handler(self, connection, _path):
        print(f'server got new connection')
        self.connections.append(connection)  # add connection to pool
        async for msg in connection:
            print(f'server got: {msg}')
            for data_to_send in self.data:
                await connection.send(data_to_send["msg_to_send"])
            self.server.close()
            print(f'server finished')

        self.connections.remove(connection)  # remove connection from pool, when client disconnects
        print(f'server lost connection')


@pytest.mark.integtest
def test_vwap_engine_one_product():
    product_ids = ["BTC-USD"]
    window_size = 10

    exchange_server = ExchangeWebsocketServerMock(data_len=20, product_ids=product_ids)

    engine_output_data = []
    engine = VWAPEngine(ExchangeWebsocketApiMock, product_ids, window_size, exchange_server.port,
                        lambda output: engine_output_data.append(output))

    finished, unfinished = asyncio.get_event_loop().run_until_complete(
        asyncio.wait([engine, exchange_server], return_when=asyncio.FIRST_COMPLETED))
    for task in finished:
        task.result()  # raise exceptions if any

    reference_output_data = []
    vwap_computer = VWAPComputer(window_size)
    for input_data in exchange_server.data:
        obj = input_data["object_to_send"]
        vwap_computer.add(obj["price"], obj["size"])
        reference_output_data.append({
                        "product_id": product_ids[0],
                        "vwap": vwap_computer.get()})

    assert reference_output_data == engine_output_data


@pytest.mark.integtest
def test_vwap_engine():
    product_ids = [
        "BTC-USD",
        "ETH-USD",
        "ETH-BTC"
    ]
    window_size = 10

    exchange_server = ExchangeWebsocketServerMock(
        data_len=window_size * 2 * len(product_ids),
        product_ids=product_ids)

    engine_output_data = []
    engine = VWAPEngine(ExchangeWebsocketApiMock, product_ids, window_size, exchange_server.port,
                        lambda output: engine_output_data.append(output))

    finished, unfinished = asyncio.get_event_loop().run_until_complete(
        asyncio.wait([engine, exchange_server], return_when=asyncio.FIRST_COMPLETED))
    for task in finished:
        task.result()  # raise exceptions if any

    reference_output_data = []
    vwap_computers = {product_id: VWAPComputer(window_size) for product_id in product_ids}
    for input_data in exchange_server.data:
        obj = input_data["object_to_send"]
        vwap_computer = vwap_computers[obj["product_id"]]
        vwap_computer.add(obj["price"], obj["size"])
        reference_output_data.append({
            "product_id": obj["product_id"],
            "vwap": vwap_computer.get()})

    assert reference_output_data == engine_output_data


@pytest.mark.integtest
def test_vwap_engine_wrong_product():
    requested_product_ids = ["BTC-USD"]
    server_product_ids = ["ETH-USD"]
    window_size = 10

    exchange_server = ExchangeWebsocketServerMock(
        data_len=window_size * 2 * len(server_product_ids),
        product_ids=server_product_ids)

    engine_output_data = []
    engine = VWAPEngine(ExchangeWebsocketApiMock, requested_product_ids, window_size, exchange_server.port,
                        lambda output: engine_output_data.append(output))

    finished, unfinished = asyncio.get_event_loop().run_until_complete(
        asyncio.wait([engine, exchange_server], return_when=asyncio.FIRST_COMPLETED))
    with pytest.raises(ValueError) as exception:
        for task in finished:
            task.result()  # raise exceptions if any

    assert str(exception.value) == "The not requested product id was received"
