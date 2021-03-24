import cbpro
import numpy as np

dic = {}
products = ['BTC-USD', 'ETH-USD', 'ETH-BTC']

#create array of volume/price/vwap for each pair
for i in products:
    dic[i] = [[],[], [0,0]]

def vwap(pid):
    v = dic[pid][0]
    p = dic[pid][1]

    #last vwap calculation
    last = dic[pid][2]

    #add new datapoint to vwap
    last[0] += v[-1] * p[-1]
    last[1] += v[-1]

    dic[pid][2] = last   

    return last[0] / last[1]

class myWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = 'wss://ws-feed.pro.coinbase.com/'
        self.products = products
        self.channels = ['matches']

    def on_message(self, msg):
        if msg and msg['type'] == 'match':
            pid = msg['product_id']
            coin = dic[pid]

            # add new datapoint
            coin[0].append(float(msg['size']))
            coin[1].append(float(msg['price']))

            # remove oldest datapoint if more than 200
            if len(coin[0]) > 200:
                # get oldest datapoint
                v = coin[0][0]
                p = coin[1][0]

                # subtract vw and volume from running vwap calculation
                coin[2][0] -= v*p
                coin[2][1] -= v

                # remove oldest datapoint
                coin[0].pop(0)
                coin[1].pop(0)

            dic[pid] = coin
            print(pid + ' VWAP:', vwap(pid))

    def on_close(self):
        print("-- Goodbye! --")

wsClient = myWebsocketClient()
wsClient.start()
