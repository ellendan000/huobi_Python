from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.exception.huobi_api_exception import HuobiApiException

def callback(candlestick_req: 'CandlestickReq'):
    candlestick_req.print_object()

def error(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

sub_client = MarketClient(init_log=True)
sub_client.req_candlestick("htusdt", CandlestickInterval.MIN15, callback, from_ts_second=1620748800, end_ts_second=1620835200)
# sub_client.req_candlestick("btcusdt", CandlestickInterval.MIN1, callback)
