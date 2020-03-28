from pylsl import StreamInfo, StreamInlet, resolve_streams
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

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


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchUnix()
        except ImportError:
            print('_GetchUnix ImportError')

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


#def waitInput:

def outputData(listLeft, listCenter, listRight): #worked on March 28th
    print("data will be output to csv file here ?")

    print('listLeft::', listLeft)
    print('listCenter:: ', listCenter)
    print('listRight:: ', listRight)
    npaLeft = np.array(listLeft)
    npaCenter = np.array(listCenter)
    npaRight = np.array(listRight)

#    dataArray = np.array(listLeft)
    dataArray = np.concatenate([npaLeft, npaCenter, npaRight])

    print('----dataArray----')
    print(dataArray)

def calcParameters():
    print("parameters to convert pos data will be calculated here")



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

    # やりたいこと：
    # 特定キーを押すとその後１秒間のPosXの平均を保存 ×3種類。中央，左右。
    # その値を使って角度に変換
    # 変換した値をC++に送信したい


    print('-Started-')
    t1 = time.time()
    time_chunk = 0

    posLeftList = [[]]
    posCenterList = [[]]
    posRightList = [[]]
    posLeftList.clear()
    posCenterList.clear()
    posRightList.clear()

    confThr = 0.0 # confidence threshold. 0.6?

    edgeDegree = 25.0 # the degree of left/right edge of the used display

    while True:
        # 操作説明
        # a,s,d: 各キーを押したときのPosデータを取得，それぞれ左端，中央，右端用．押した数だけデータを保持できる(後に平均計算)
        # q,w,e: データ取得キーa,s,dそれぞれに対するデータリセット用
        # x: Breakして，各データの平均値出力
        getch = _Getch()
        x = getch()
        print(x)

        if x == 'x':
            print('break')
            break

        time.sleep(0.1)
        d, _ = inlet.pull_chunk(max_samples=64)    # バッファにあるデータを全部取る

        if(len(d) == 0):
            countdzero += 1
        else:
            if len(d) > 1:
                countdmore += 1

            print('shape : ', np.array(d).shape) # (8,22)
            #for counter2 in range (len(d)):  # counter2 いくつ分のデータが溜まってるか counter2 of len(d)
                #print(counter2, '---------------------------')
                #for counter in range(len(chunk)): # counter ひとつのデータ郡のうち何番目のデータを指定するか(種類)
                #    print(ch_names[counter], ':    ', np.array(d)[counter2, counter])
                #time.sleep(0.2)
            diameter = np.array(d)[-1, -2] # とってきたデータの最後の部分(list[-1])を使う
            confidence = np.array(d)[-1,0]
            nPosX = np.array(d)[-1, 1]
            nPosY = np.array(d)[-1, 2]
            print('confi: ', confidence)
            print('nPosX: ', nPosX)
            print('nPosY: ', nPosY)
            print('diameter: ', diameter)
            print('--------------------------')

            if x == 'a':
                if confidence >= confThr:
                    a = [edgeDegree*(-1), nPosX]
                    posLeftList.append(a)

            elif x == 's':
                if confidence >= confThr:
                    a = [0., nPosX]
                    posCenterList.append(a)

            elif x == 'd':
                if confidence >= confThr:
                    a = [edgeDegree, nPosX]
                    posRightList.append(a)

            elif x == 'q':
                posLeftList.clear()
            elif x == 'w':
                posCenterList.clear()
            elif x == 'e':
                posRightList.clear()

            print(posLeftList)
            print(posCenterList)
            print(posRightList)
        #    time.sleep(0.5)

            frame = frame + 1
            if frame == unitFrame:
                frame = 0
                #t10 = time.time()
                #elapsed_time = t10-t1
               # realtimereceive.print_receiveRate(printSwitch, unitFrame, elapsed_time, countdzero, countdmore)
                #t1=time.time()


    #後々print出力部分をMLAに送信するメソッドにする
    print('==average data==')
    print('len(posLeftList): ',len(posLeftList))

    dataCheck = 0
    if len(posLeftList) < 1 :
        print("Average PosLeft: No valid data")
        dataCheck = 1
    else:
        b = []
        for i in posLeftList: # リストの各要素の二番目のデータだけをSum up
            b.append(i[1])
        #avePosLeft = sum(posLeftList) / len(posLeftList)
        print('Average PosLeft: ', sum(b)/len(b))

    if len(posCenterList) < 1 :
        print("Average PosCenter: No valid data")
        dataCheck = 1
    else:
        #avePosCenter = sum(posCenterList) / len(posCenterList)
        b = []
        for i in posCenterList:
            b.append(i[1])
        print('Average PosCenter: ', sum(b)/len(b))

    if len(posRightList) < 1 :
        print("Average PosRight: No valid data")
        dataCheck = 1
    else:
        #avePosRight = sum(posRightList) / len(posRightList)
        b = []
        for i in posRightList:
            b.append(i[1])
        print('Average PosRight: ', sum(b)/len(b))

    if dataCheck == 0:
        outputData(posLeftList, posCenterList, posRightList)
    else:
        print("Data not completed")
