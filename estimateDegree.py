from pylsl import StreamInfo, StreamInlet, resolve_streams
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from sklearn.linear_model import LinearRegression
import csv
import pandas as pd
import os

#try:
#readData = pd.read_csv('/Users/yutauchimine/work/mywork/parameters.csv', header=None)
#arr_param = np.array(readData.values)

arr_param = np.loadtxt('/Users/yutauchimine/work/mywork/parameters.csv',
                  delimiter=",",    # ファイルの区切り文字
                  skiprows=0,       # 先頭の何行を無視するか（指定した行数までは読み込まない）
                  usecols=(0,1) # 読み込みたい列番号
                 )

print(arr_param)
#except:
    #print('problem with reading csv file occured')


class RealTimeReceive():
    def print_receiveRate(self, sw, uFrame, e_time, czero, cmore):
        if(sw):
            print('Unit frame / elapsed time : ', uFrame/e_time , ' , Num of missed data: ', czero, ' , Num of over data: ', cmore)

    def inlet_specific_stream(self, stream_name):
        import numpy as np
        streams = resolve_streams(wait_time=3.)
        stream_names = []
        for stream in streams:      #stream変数を宣言してにstreamsの要素を順に入れる
            inlet = StreamInlet(stream)   #streamのStreamInletをしてinletに入れる
            stream_names.append(inlet.info().name()) # inletのname()要素をstream_names配列に入れる

        print(':   ', stream_names)
        stream_names.append('Pupil Primitive Data - Eye 0')
        for aiueo in (stream_names):
            print('Data : ', aiueo)
        idx = stream_names.index(stream_name)   # stream_nameと同じstream_namesの要素があるときのインデックスを代入

        streams.append('Pupil Primitive Data - Eye 0')

        inlet = StreamInlet(streams[idx])
        print(type(inlet))
        return inlet

    def pick_ch_names(self, info):
        # channelに存在する内容を調べるためLabel名を返す
        ch_xml = info.desc().child('channels').child('channel')
        ch_names = []
        for _ in range(info.channel_count()):
            ch_names.append(ch_xml.child_value('label'))
            ch_xml = ch_xml.next_sibling()
        return ch_names

    def test(self):
        print('worked')

    def streamOpen(self):
        self.StreamInlet.open_stream()


class ZmqSend():
    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.diameter = [0]
        self.angle = [0]
        self.distance = [0]
    def sendData(self, degX, degY):
       # print('1')
        ctx = zmq.Context()
        sock = ctx.socket(zmq.REQ)
        sock.connect(self.conn_str)
       # print('2')
        self.diameter[0] = dia
        self.angle[0] = ang
        self.distance[0] = dist
        data = [ np.array(self.degX), np.array(self.degY)]
        sock.send_multipart(data)
     #   print('Sent : ', data)




# conver pupil position data into
def convert(pupilPosX, pupilPosY):
    paramA = arr_param[0]
    paramB = arr_param[1]
    # calculation below is only available for linear regression. Refer to calibration.py
    """
    y=ax+b
    posX = paramA * degX  + paramB
    """

    degX = (pupilPosX-paramB)/paramA

    degY = 0.
    return degX, degY


def sender(degX, degY):
    #print('This function passes converted degree data to MLA program')
    print('degX =  ', degX)








if __name__ == "__main__":

    unitFrame = 50
    printSwitch = 1

    realtimereceive = RealTimeReceive()
    #stream_name = 'pupil_capture'
    stream_name = 'Pupil Primitive Data - Eye 0'
    streams = resolve_streams(wait_time=3.)
    print("-----")
    print(len(streams))

    inlet = StreamInlet(streams[0]) # そもそもStream[]にはIndex0ひとつしかないのでinlet_specific_streamがいらなかった

    ch_names = realtimereceive.pick_ch_names(inlet.info())

    inlet.open_stream
#    time.sleep(.1)
    chunk, timestamps = inlet.pull_sample(timeout=3.)
    countdmore = 0
    countdzero = 0


    str = "tcp://127.0.0.1:5553"
    zmqSend = ZmqSend(str)

    confThr = 0.0 # confidence threshold. 0.6?
    print('set confidence threshold is: ', confThr)

    while True:
        """
        quit = input()
        if(quit == 'q'):
            print('out')
            break
        """
        time.sleep(0.1)
        d, _ = inlet.pull_chunk(max_samples=64)    # バッファにあるデータを全部取る
       # print(d)
       # time.sleep(0.5)
    #    diameter = np.array(d)[-1, 0]
    #    print('dia : ', np.array(d)[1])
     #   print('dia: ', dia)
        if(len(d) == 0):
            countdzero += 1
        else:
            if len(d) > 1:
                countdmore += 1



            #diameter = np.array(d)[-1, -2] # とってきたデータの最後の部分(list[-1, x])を使う
            pupilPosX = np.array(d)[-1, 1]
            pupilPosY = np.array(d)[-1, 2]
            print('PupilPosX: ', pupilPosX)

            degX, degY = convert(pupilPosX, pupilPosY)
            zmqSend.sendData(degX, degY)
