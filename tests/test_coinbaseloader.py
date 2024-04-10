from dataloader.coinbaseloader import CoinbaseLoader, Granularity

class TestClass:

    @classmethod
    def setup_class(cls):
        cls._loader = CoinbaseLoader()

    def test_get_pairs(self):
        data = self._loader.get_pairs()
        
        assert data is not None and len(data) != 0, "Empty pairs list received"
        assert isinstance(data, list), "Pandas DataFrame expected"
        assert isinstance(data[0], dict), "Pandas DataFrame expected"

        base_currencies = [item["base_currency"] for item in data]
        assert "BTC" in base_currencies, "BTC base currency not found"

    def test_get_stats(self):
        pass

    def test_get_historical_data(self):
        pass
