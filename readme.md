### Real-time VWAP (volume-weighted average price) calculation engine


##### Brief description
This is an implementation of the real-time VWAP
(volume-weighted average price) calculation engine 
with Coinbase cryptocurrency as data source.


##### Requirements
To run project the python3 must be installed.
See requirements.txt for required packages. Use the next command to install it
```shell script
pip install -r requirements.txt
```


##### Run project instructions

###### Tests running
To run the tests the `pytest` package must be installed.
```shell script
pip install -U pytest
```
Run the next command to execute all tests.
```shell script
pytest
```
Run the next command to execute unit tests only.
```shell script
pytest -m "not integtest"
```
Run the next command to execute integration tests only.
```shell script
pytest -m integtest
```

###### Running VWAP calculation engine
Run the next command to start the engine for Coinbase
"BTC-USD", "ETH-USD", "ETH-BTC" products.
```shell script
python main.py
```
The VWAP values for these products will be printed to stdout.

###### Running in python virtual environment (optional)
Run the next commands from project directory.
```shell script
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```


##### Architectural Aspects

There are three main classes:
VWAPEngine, VWAPComputer, and CoinbaseWebsocketApi.
The last one is derived from WebsocketApiExchangeInterface.

###### VWAPEngine class
This class runs the websocket client and
receive messages from server.
It holds instances of VWAPComputer class 
one per trading product. And it uses
the WebsocketApiExchangeInterface for parsing incoming messages
and for composing outgoing messages. 

###### VWAPComputer class
This class do real-time VWAP computations.
It has an add method to add incoming price-volume pairs.
This method actually do all computations.
Complexity of the add method is O(1) and not depend on
sliding window size. And there is a get method
for getting last computed value.

###### CoinbaseWebsocketApi class
This class contains all information needed for
parsing incoming messages and composing outgoing messages.
This class extends the WebsocketApiExchangeInterface class.
So it is easy to add functionality for other exchanges by
extending the WebsocketApiExchangeInterface.


##### Project structure
The CoinbaseWebsocketApi and the WebsocketApiExchangeInterface
classes were grouped into WebsocketApi package
alongside with the unit tests for the CoinbaseWebsocketApi
and json files with the websocket API messages examples
used for testing.
The VWAPComputer class with correspondent unit tests
was packed into VWAP package.