import websocket
import zlib
from persistance.default import DefaultPersister
import ast

class OkcoinClient:
    def __init__(self, host=None, channel=None, persister=None):
        websocket.enableTrace(False)
        if host is not None:
            self.host = host
        else:
            self.host = 'wss://real.okcoin.com:10440/websocket/okcoinapi'

        if channel is not None:
            self.channel = channel
        else:
            self.channel = 'ok_sub_spotusd_btc_ticker'

        if persister is not None:
            self.persister = persister
        else:
            self.persister = DefaultPersister()

        self.ws = websocket.WebSocketApp(self.host,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close,
                                         on_open=self.on_open)

    @staticmethod
    def inflate(data):
        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated.decode()

    def on_open(self, ws):
        def on_open_impl(ws):
            ws.send("{'event':'addChannel','channel':'%s','binary':'true'}" % self.channel)
        return on_open_impl(ws)

    def on_message(self, ws, evt):
        def on_message_impl(ws, evt):
            if isinstance(evt, str):
                pass
            else:
                data = self.inflate(evt)
                data = ast.literal_eval(data)
                data = [item['data'] for item in data]
                self.persister(data)
        return on_message_impl(ws, evt)

    def on_error(self, ws, evt):
        def on_error_impl(ws, evt):
            print(evt)
        return on_error_impl(ws, evt)

    def on_close(self, ws):
        def on_close_impl(ws):
            print('DISCONNECT')
        return on_close_impl(ws)

    def run(self):
        self.ws.run_forever(ping_interval=25)
