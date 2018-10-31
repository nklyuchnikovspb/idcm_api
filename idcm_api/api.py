from .transport import IDCMTransport
from decimal import Decimal


class IDCMApi(IDCMTransport):

    @staticmethod
    def _get_pair(currency, base_currency):
        return f"{currency.upper()}-{base_currency.upper()}"

    @staticmethod
    def _get_side(is_buy):
        return {
            True: 0,
            False: 1
        }[is_buy]

    @staticmethod
    def _get_order_type(rate):
        # 0 - market price, 1 - limit price
        if rate is not None:
            return 1
        else:
            return 0

    def get_ticker(self, currency: str, base_currency: str):
        """
        Example of input data:
        {
            "Symbol":"BCH-BTC"//Trade pair
        }
        #Response
        {
            "result": 1,//1 success,0 failure
            "code": "200",//Error code. See error code for details.
            "data": {
                "timestamp": 62135625600,//Timestamp
                "buy": 0.002,//Offer price 1
                "high": 0.0,//Highest price
                "last": 0.0,//Last price
                "low": 0.0,//Lowest price
                "sell": 0.002,//Ask price 1
                "vol": 0.0 //Trading volume (past 24 hours)
            }
        }
        """
        path = 'getticker'
        data = {
            'Symbol': self._get_pair(currency, base_currency)
        }
        return self._request(path=path, data=data)

    def get_depth(self, currency: str, base_currency: str):
        """
        Example of input data:
        {
           "Symbol":"BCH-BTC"//Trade pair
        }
        #Response
        {
           "result": 1,//1 success, 0 failure
           "code": "200",//Error code. See error code for details.
           "data": {
                "asks": [{
                "symbol": "BTC-BCH",
                 "price": 0.01,
                 "amount": 1
                  }],
             "bids": [{
                 "symbol": "BTC-BCH",
                 "price": 0.01,
                 "amount": 1
                  }]
            }
        }
        """
        path = 'getdepth'
        data = {
            'Symbol': self._get_pair(currency, base_currency)
        }
        return self._request(path=path, data=data)

    def get_trades(self, currency: str, base_currency: str, since: int):
        """
        Example of input data:
        {
           "Symbol":"BCH-BTC",//Trade pair
           "Since":100//Timestamp. Maximum of 500 points of data returned after the timestamp is returned
        }
        #Response
        {
            "result": 1,//1 success, 0 failure
            "code": "200",//Error code. See error code for details.
            "data": {
                [{
                    "date": "2018-05-10 11:15:59",//Trading time
                    "price": 0.01,//Trading price
                    "amount": 1,//Amount
                    "side":"sell"//buy/sell
                }]
            }
        }
        """
        path = 'gettrades'
        data = {
            'Symbol': self._get_pair(currency, base_currency),
            'Since': since
        }
        return self._request(path=path, data=data)

    def get_user_info(self):
        """
        Example of input data:
        1 (random data, cannot be left blank)

        #Response
        {
            "result": 1,//1 success, 0 failure
            "code": "200",//Error code. See error code for details.
            "data": {
                [{
                    "code": "BCH",//currency type
                    "free": 0.01,//available
                    "freezed": 1,//frozen
                }]
            }
        }
        """
        path = 'getuserinfo'
        data = {}
        return self._request(path=path, data=data)

    def trade(self,
              currency: str,
              base_currency: str,
              amount: str,
              is_buy: bool,
              rate: str,
              ):
        """
        Example of input data:
        {
            "Symbol":"BCH-BTC",//Trade pair
            "Size":100//Trade amount
            "Price":100,//Order price
            "Side": 0,//Trade direction (check the trade direction list)
            "Type":0,//(check order type chart)
        }

        #Response
        {
            "result": 1,//1 success, 0 failure
            "code": "200",//Error code. See error code for details.
            "data": {
                "orderid":"21321321321334"//Order ID
            }
        }
        """
        path = 'trade'
        data = {
            "Symbol": self._get_pair(currency, base_currency),
            "Size": amount,
            "Side": self._get_side(is_buy),
            "Type": 1,  # limit deals only
            "Price": rate
        }

        return self._request(path, data=data)
