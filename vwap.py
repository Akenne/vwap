import cbpro
from numba import jit
import time
import numpy as np

v = []
p = []

def vwap():
    tmp1 = np.zeros_like(v)
    tmp2 = np.zeros_like(v)

    for i in range(0,len(v)):
        tmp1[i] = tmp1[i-1] + v[i] * p[i]
        tmp2[i] = tmp2[i-1] + v[i]

    return tmp1[-1] / tmp2[-1]

class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ["BTC-USD"]
        self.channels = ["matches"]
        print("Lets count the messages!")

    def on_message(self, msg):
    	print(msg)
    	if msg and msg['type'] == 'match':
    		v.append(float(msg["size"]))
    		p.append(float(msg["price"]))

    		print(vwap())
    		
    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
print(wsClient.url, wsClient.products)
while (1):
    time.sleep(1)
wsClient.close()