import pytest

from VWAP.computer import VWAPComputer


class TestVWAPComputer:
    def test_window_size_zero(self):
        with pytest.raises(AssertionError):
            VWAPComputer(0)

    def test_window_size_negative(self):
        with pytest.raises(AssertionError):
            VWAPComputer(-1)

    def test_current_window_initial(self):
        comp = VWAPComputer(2)
        assert comp.window_size == 2
        assert comp.get_current_window() == 0

    def test_current_window_common(self):
        comp = VWAPComputer(2)
        comp.add(100, 10)
        assert comp.get_current_window() == 1

    def test_current_window_max(self):
        comp = VWAPComputer(2)
        comp.add(100, 10)
        comp.add(200, 5)
        assert comp.get_current_window() == 2

    def test_current_window_overflow(self):
        comp = VWAPComputer(1)
        comp.add(100, 10)
        comp.add(200, 5)
        assert comp.get_current_window() == 1

    def test_get_initial_value(self):
        comp = VWAPComputer(1)
        assert comp.get() == 0

    def test_get_first_value(self):
        comp = VWAPComputer(1)
        comp.add(100, 10)
        assert comp.get() == 100

    def test_get_value(self):
        comp = VWAPComputer(2)
        comp.add(100, 9)
        comp.add(200, 3)
        assert comp.get() == 125

    def test_get_updated_value(self):
        comp = VWAPComputer(2)
        comp.add(100, 9)
        comp.add(200, 3)
        comp.add(300, 1)
        assert comp.get() == 225

    def test_add_zero_volume(self):
        with pytest.raises(ValueError):
            comp = VWAPComputer(1)
            comp.add(100, 0)

    def test_add_negative_volume(self):
        with pytest.raises(ValueError):
            comp = VWAPComputer(1)
            comp.add(100, -1)
