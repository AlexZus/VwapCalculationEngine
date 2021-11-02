from WebsocketApi.coinbase import CoinbaseWebsocketApi
import json, os

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json_file(file_path: str):
    with open(TEST_DIR + '/coinbaseMessagesExamples/' + file_path) as json_file:
        return json.load(json_file)


class TestWebsocketApiForCoinbase:
    def test_subscribe_matches(self):
        msg_to_send = CoinbaseWebsocketApi.compose_subscribe_matches([
            "BTC-USD",
            "ETH-USD",
            "ETH-BTC"
        ])
        assert json.loads(msg_to_send) == load_json_file('out_msg_subscribe_matches_BTCUSD_ETHUSD_ETHBTC.json')

    def test_get_input_msg_type_match(self):
        assert "match" == CoinbaseWebsocketApi.get_input_msg_type(
            load_json_file('in_msg_match_BTCUSD_price58000_volume5.json'))

    def test_get_input_msg_type_heartbeat(self):
        assert "heartbeat" == CoinbaseWebsocketApi.get_input_msg_type(
            load_json_file('in_msg_heartbeat.json'))

    def test_get_input_msg_match_price_and_volume(self):
        price, volume = CoinbaseWebsocketApi.get_input_msg_match_price_and_volume(
            load_json_file('in_msg_match_BTCUSD_price58000_volume5.json'))
        assert price == 58000
        assert volume == 5

    def test_get_input_msg_product_id(self):
        assert "BTC-USD" == CoinbaseWebsocketApi.get_input_msg_product_id(
            load_json_file('in_msg_match_BTCUSD_price58000_volume5.json'))
