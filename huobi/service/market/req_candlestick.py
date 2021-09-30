import time
import logging
from huobi.utils import *
from huobi.constant import CandlestickInterval

from huobi.connection.websocket_req_client import *
from huobi.model.market import *
from huobi.utils.channels_request import *
from datetime import datetime, timedelta

logger = logging.getLogger("huobi-client")

class ReqCandleStickService:
    def __init__(self, params):
        self.params = params

    def subscribe(self, callback, error_handler, **kwargs):
        symbol_list = self.params["symbol_list"]
        interval = self.params["interval"]
        from_ts_second = self.params.get("from_ts_second", None)
        end_ts_second = self.params.get("end_ts_second", None)

        def subscription(connection):
            increment_level = {
                CandlestickInterval.MIN1: 0.5,
                CandlestickInterval.MIN5: 1,
                CandlestickInterval.MIN15: 2,
                CandlestickInterval.MIN30: 4,
                CandlestickInterval.MIN60: 8,
                CandlestickInterval.HOUR4: 32,
                CandlestickInterval.DAY1: 360
            }

            for symbol in symbol_list:
                if from_ts_second != None:
                    increment = timedelta(days=increment_level[interval])
                    _cursor_from = from_ts_second
                    _next_day = datetime.timestamp(datetime.fromtimestamp(from_ts_second) + increment)
                    _cursor_to = _next_day if _next_day < end_ts_second else end_ts_second

                    while _cursor_to and _cursor_to <= end_ts_second:
                        logger.info(f"==> send req for [{symbol}]: {_cursor_from} - {_cursor_to}]")
                        connection.send(request_kline_channel(symbol, interval, _cursor_from, _cursor_to))

                        _cursor_from = _cursor_to
                        if _cursor_from >= end_ts_second:
                            break

                        _next_day = datetime.timestamp(datetime.fromtimestamp(_cursor_from) + increment)
                        _cursor_to = _next_day if _next_day < end_ts_second else end_ts_second
                        time.sleep(0.5)
                else:
                    connection.send(request_kline_channel(symbol, interval))
                    time.sleep(0.01)

        def parse(dict_data):
            return default_parse(dict_data, CandlestickReq, Candlestick)

        WebSocketReqClient(**kwargs).execute_subscribe_v1(subscription,
                                            parse,
                                            callback,
                                            error_handler)
        logger.info(f'websocket_manage connect for req_candlestick [{symbol_list}, {interval}]')



