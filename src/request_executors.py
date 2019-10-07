from apis import IEXAPI


class RequestExecutor:

    message = """{ticker_labels};{epoch_timestamps};{price_list}"""
    tickers = ['GOOG', 'AAPL', 'FB']

    def _reformat_response(self, deserialized_response):
        tickers = [item for item in deserialized_response]
        quotes = list(deserialized_response.values())
        prices = [item['quote']['latestPrice'] for item in quotes]
        epoch_timestamps = [item['quote']['latestUpdate'] for item in quotes]
        return self.message.format(
            ticker_labels=','.join(tickers),
            epoch_timestamps=','.join(epoch_timestamps),
            price_list=','.join(prices),
        )

    def retrieve_price_data(self):
        api = IEXAPI()
        response = api.get_latest_price(self.tickers)
        deserialized_response = response.json()
        print(deserialized_response)
        message_format = self._reformat_response(deserialized_response)
        return message_format
