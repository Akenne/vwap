import cbpro
from numba import jit
import time
import numpy as np

v = []
p = []
dic = {}
products = ['BTC-USD', 'ETH-USD']

for i in products:
    dic[i] = [[],[]]

def vwap(pid):
    v = dic[pid][0]
    p = dic[pid][1]
    tmp1 = np.zeros_like(v)
    tmp2 = np.zeros_like(v)

    for i in range(0,len(v)):
        tmp1[i] = tmp1[i-1] + v[i] * p[i]
        tmp2[i] = tmp2[i-1] + v[i]

    return tmp1[-1] / tmp2[-1]

class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = 'wss://ws-feed.pro.coinbase.com/'
        self.products = products
        self.channels = ['matches']

    def on_message(self, msg):
        if msg and msg['type'] == 'match':
            pid = msg['product_id']
            dic[pid][0].append(float(msg['size']))
            dic[pid][1].append(float(msg['price']))

            if len(dic[pid][0]) > 200:
                print('pop!')
                dic[pid][0].pop(0)
                dic[pid][1].pop(0)

            print(pid + ' VWAP:' ,vwap(pid), len(dic[pid][0]))

    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
