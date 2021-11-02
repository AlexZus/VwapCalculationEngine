from collections import deque


# This class do real-time VWAP computations.
# It has an add method to add incoming price-volume pairs.
# This method actually do all computations.
# Complexity of the add method is O(1) and not depend on
# sliding window size. And there is a get method
# for getting last computed value.
class VWAPComputer:
    window_size: int
    prices: deque
    volumes: deque
    numerator: float
    denominator: float
    value: float

    def __init__(self, window_size: int):
        assert window_size > 0
        self.window_size = window_size
        self.prices = deque()
        self.volumes = deque()
        self.numerator = 0
        self.denominator = 0
        self.value = 0

    def add(self, price: float, volume: float) -> None:
        if volume <= 0:
            raise ValueError("The volume must be positive number")  # preventing dividing by zero
        self.prices.append(price)
        self.volumes.append(volume)
        self.numerator += price * volume
        self.denominator += volume
        if len(self.prices) > self.window_size:
            old_price = self.prices.popleft()
            old_volume = self.volumes.popleft()
            self.numerator -= old_price * old_volume
            self.denominator -= old_volume
        self.value = self.numerator / self.denominator

    def get(self) -> float:
        return self.value

    def get_current_window(self):
        return len(self.prices)

