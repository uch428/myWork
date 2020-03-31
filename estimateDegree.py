from pylsl import StreamInfo, StreamInlet, resolve_streams
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from sklearn.linear_model import LinearRegression
import csv

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
    time.sleep(.1)
    chunk, timestamps = inlet.pull_sample(timeout=3.)
    countdmore = 0
    countdzero = 0
    frame = 0
    counter2 = 0

    confThr = 0.0 # confidence threshold. 0.6?
