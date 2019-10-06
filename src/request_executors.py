from apis import IEXAPI


class RequestExecutor:

    message = """{ticker},{epoch_timestamp},{price}"""
    tickers = ['BTCUSDT']

    def _reformat_response(self, deserialized_response):
        tickers = next(item for item in deserialized_response)
        quotes = list(deserialized_response.values())
        prices = next(item['quote']['latestPrice'] for item in quotes)
        epoch_timestamps = next(item['quote']['latestUpdate'] for item in quotes)
        return self.message.format(
            ticker=tickers,
            epoch_timestamp=epoch_timestamps,
            price=prices
        )

    def retrieve_price_data(self):
        api = IEXAPI()
        response = api.get_latest_price(self.tickers)
        deserialized_response = response.json()
        print(deserialized_response)
        message_format = self._reformat_response(deserialized_response)
        return message_format
