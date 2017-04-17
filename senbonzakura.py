#!/usr/bin/env python3
import os
import fcntl
import time
import enum
import curses
#import pyaudio
#import math

senbonzakura = """
                    █████                                                      
                 ██████████                                                    
               ███████████                                                     
             ████████                            ███                           
         █████   ████                           █████                 ██       
                 ████       ███████              █████      ███       ███      
    █     ██████████████████████████             ████   █   █████    ██████    
   ████████████████████████████████              ████   ███  █████  ████████   
  ████████████   ████                            ████    ███ ████  ████████    
    █████        ████           ███          ███████████ ███  ██  █████        
                 ████            ███       ████  █████     ██    ████          
                 ████            ██             ███████      ██                
                 ████     ████████████████     █████ ███    ██   ███   ████    
                 ████    ██████████████████   ██ ███  █ ████████████████████   
                 ████         ███████        ██  ███     ██████████████████    
                 ████        ██  ██ ███     ██   ███    ███     ███            
                  ███      ███   ██   ███   █    ███  ███      ███             
                  ██     ███  ████████  ███      ███   ███████████             
                  ██   ███       ██       ███    ███      ███████████          
    █████          █             ██              ███  ██████    ████████       
       ██████████████████████████████████████████████████         ████████     
              ███████████████████████████████████████               █████      
"""

class Action(enum.Enum):
    music = 0
    clear = 1
    horizontal = 2
    vertical = 3
    senbonzakura = 4

class BeepPlayer():
    KIOCSOUND = 0x4B2F
    CLOCK_TICK_RATE = 1193180

    def init(self):
        os.system("modprobe pcspkr")
        self.fd = os.open("/dev/tty0", os.O_WRONLY)
    
    def play(self, frq, length):
        if frq == 0:
            time.sleep(length)
            return

        fcntl.ioctl(self.fd, BeepPlayer.KIOCSOUND, int(BeepPlayer.CLOCK_TICK_RATE/frq))
        try:
            time.sleep(length)
        finally:
            fcntl.ioctl(self.fd, BeepPlayer.KIOCSOUND, 0)

    def end(self):
        os.close(self.fd)

# for debug purpose
"""
class MutePlayer():
    def init(self):
        pass
    
    def play(self, frq, length):
        time.sleep(length)

    def end(self):
        pass

class AudioPlayer():
    sample_rate = 22050

    def init(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.p.get_format_from_width(1), 
                        channels = 1, 
                        rate = AudioPlayer.sample_rate, 
                        output = True)
    
    def play(self, frq, length):
        if frq == 0:
            time.sleep(length)
            return

        length = length/2

        n_samples = int(AudioPlayer.sample_rate * length)
        restframes = n_samples % AudioPlayer.sample_rate

        s = lambda t: math.sin(2 * math.pi * frq * t / AudioPlayer.sample_rate)
        samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples))
        self.stream.write(bytes(bytearray(samples)))
        self.stream.write(b'\x80' * restframes)

    def end(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
"""

def playMusic(sheet):
    scr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)

    player = BeepPlayer()
    player.init()

    try:
        for measure in sheet:
            for cmd in measure:
                if cmd[0] == Action.music:
                    frq, dur = cmd[1:]
                    player.play(frq, dur*60/tempo)
                elif cmd[0] == Action.clear:
                    scr.clear()
                elif cmd[0] == Action.horizontal:
                    x, y, string = cmd[1:]
                    scr.addstr(x, y, string)
                elif cmd[0] == Action.vertical:
                    x, y, string = cmd[1:]
                    for i in range(len(string)):
                        scr.addstr(x+i, y, string[i])
                elif cmd[0] == Action.senbonzakura:
                    scr.addstr(0, 0, senbonzakura)
                scr.refresh()
    finally:
        player.end()
        curses.endwin()



tempo = 150

C0 = 16
C0sharp = 17
D0 = 18
D0sharp = 19
E0 = 20
F0 = 21
F0sharp = 23
G0 = 24
G0sharp = 25
A0 = 27
A0sharp = 29
B0 = 30
C1 = 32
C1sharp = 34
D1 = 36
D1sharp = 38
E1 = 41
F1 = 43
F1sharp = 46
G1 = 49
G1sharp = 51
A1 = 55
A1sharp = 58
B1 = 61
C2 = 65
C2sharp = 69
D2 = 73
D2sharp = 77
E2 = 82
F2 = 87
F2sharp = 92
G2 = 98
G2sharp = 103
A2 = 110
A2sharp = 116
B2 = 123
C3 = 130
C3sharp = 138
D3 = 146
D3sharp = 155
E3 = 164
F3 = 174
F3sharp = 185
G3 = 196
G3sharp = 207
A3 = 220
A3sharp = 233
B3 = 246
C4 = 261
C4sharp = 277
D4 = 293
D4sharp = 311
E4 = 329
F4 = 349
F4sharp = 369
G4 = 392
G4sharp = 415
A4 = 440
A4sharp = 466
B4 = 493
C5 = 523
C5sharp = 554
D5 = 587
D5sharp = 622
E5 = 659
F5 = 698
F5sharp = 739
G5 = 783
G5sharp = 830
A5 = 880
A5sharp = 932
B5 = 987
C6 = 1046
C6sharp = 1108
D6 = 1174
D6sharp = 1244
E6 = 1318
F6 = 1396
F6sharp = 1479
G6 = 1567
G6sharp = 1661
A6 = 1760
A6sharp = 1864
B6 = 1975
C7 = 2093
C7sharp = 2217
D7 = 2349
D7sharp = 2489
E7 = 2637
F7 = 2793
F7sharp = 2959
G7 = 3135
G7sharp = 3322
A7 = 3520
A7sharp = 3729
B7 = 3951
C8 = 4186
C8sharp = 4434
D8 = 4698
D8sharp = 4978
E8 = 5274
F8 = 5587
F8sharp = 5919
G8 = 6271
G8sharp = 6644
A8 = 7040
A8sharp = 7458
B8 = 7902
STOP = 0

music = [[]]
# 1
music.append([
    (Action.music, D4, 0.75),
    (Action.music, D4, 0.75),
    (Action.music, C4, 0.5),
    (Action.music, D4, 0.75),
    (Action.music, D4, 0.75),
    (Action.music, C4, 0.5),
])
music.append([
    (Action.music, D4, 0.75),
    (Action.music, D4, 0.75),
    (Action.music, C4, 0.5),
    (Action.music, D4, 1),
    (Action.music, F4, 1),
])
# 3
music.append([
    (Action.music, D4, 0.75),
    (Action.music, D4, 0.75),
    (Action.music, C4, 0.5),
    (Action.music, D4, 0.75),
    (Action.music, D4, 0.75),
    (Action.music, C4, 0.5),
])
music.append([
    (Action.music, D4, 1),
    (Action.music, F4, 1),
    (Action.music, G4, 1),
    (Action.music, A4, 1),
])
# 5
music.append([
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
])
music.append([
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, F4, 0.5),
    (Action.music, E4, 0.1666),
    (Action.music, F4, 0.1666),
    (Action.music, E4, 0.1666),
    (Action.music, D4, 0.5),
    (Action.music, C4, 0.5),
])
# 7
music.append([
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
])
music.append([
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.5),
    (Action.music, A4, 0.5),
])
# 9
music.append([
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
])
music.append([
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, F4, 0.5),
    (Action.music, E4, 0.1666),
    (Action.music, F4, 0.1666),
    (Action.music, E4, 0.1666),
    (Action.music, D4, 0.5),
    (Action.music, C4, 0.5),
])
# 11
music.append([
    (Action.music, D4, 0.5),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, F4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, G4, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, G4, 0.25),
    (Action.music, A4, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, A4, 0.25),
    (Action.music, C5, 0.25),
])
music.append([
    (Action.music, F5, 0.5),
    (Action.music, E5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 1),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 13
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, F5, 0.5),
    (Action.music, E5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
])
# 15
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, C6, 0.5),
    (Action.music, F6, 0.5),
    (Action.music, E6, 0.25),
    (Action.music, F6, 0.25),
    (Action.music, E6, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, C6, 0.5),
    (Action.music, A5, 0.5),
])
# 17
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, F5, 0.5),
    (Action.music, E5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
])
# 19
music.append([
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, C6, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, C6, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.senbonzakura,),
    (Action.music, D5, 0.75),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.5),
    (Action.music, D5, 1),
    (Action.music, STOP, 1),
])

# 21
music.append([
    (Action.clear,),
    (Action.vertical, 5, 60, "大 胆 不 敵 に"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
])
music.append([
    (Action.vertical, 7, 55, "ハ イ カ ラ 革 命"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
])
# 23
music.append([
    (Action.clear,),
    (Action.vertical, 4, 57, "磊  々  落  々"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.vertical, 4, 57, "反  戦  国  家"),
    (Action.music, A5, 1),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, F5, 1),
    (Action.music, D5, 1),
])
# 25
music.append([
    (Action.clear,),
    (Action.vertical, 5, 62, "日 の 丸 印 の"),
    (Action.vertical, 6, 58, "二 輪 車 転 が し"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
])
music.append([
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
])
# 27
music.append([
    (Action.clear,),
    (Action.horizontal, 10, 50, "悪 霊 退 散"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.horizontal, 12, 51, "I"),
    (Action.music, A5, 1),
    (Action.horizontal, 12, 53, "C"),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.horizontal, 12, 55, "B"),
    (Action.music, F5, 1),
    (Action.horizontal, 12, 57, "M"),
    (Action.music, D5, 1),
])
# 29
music.append([
    (Action.clear,),
    (Action.horizontal, 14, 10, "環状線を走り抜けて"),
    (Action.music, F5, 1),
    (Action.music, E5, 1),
    (Action.music, D5, 1),
    (Action.music, C5, 1),
])
music.append([
    (Action.music, C5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, G4, 0.5),
    (Action.music, A4, 2),
])
# 31
music.append([
    (Action.horizontal, 16, 14, "東奔西走なんのその"),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 1),
    (Action.music, G5, 1),
    (Action.music, E5, 1),
])
music.append([
    (Action.music, F5, 1),
    (Action.music, E5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 2),
])
# 33
music.append([
    (Action.clear,),
    (Action.vertical, 8, 18, "少 年"),
    (Action.music, F5, 1),
    (Action.music, E5, 1),
    (Action.horizontal, 13, 20, "少  女"),
    (Action.music, D5, 1),
    (Action.music, C5, 1),
])
music.append([
    (Action.vertical, 9, 26, "戦 国"),
    (Action.vertical, 9, 22, "無 双"),
    (Action.music, C5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, G4, 0.5),
    (Action.music, A4, 1),
    (Action.clear,),
    (Action.horizontal, 11, 32, "浮 世 の 随 に"),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
])
# 35
music.append([
    (Action.music, D5, 0.5),
    (Action.music, D5, 1),
    (Action.music, D5, 0.5),
    (Action.music, F5, 1),
    (Action.music, G5, 1),
])
music.append([
    (Action.music, E5, 2),
    (Action.music, STOP, 1),
    (Action.clear,),
    (Action.vertical, 7, 62, "千 本 桜"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])

# 37
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.vertical, 8, 58, "夜 ニ 紛 レ"),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.vertical, 7, 62, "君 ノ 声 モ"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 39
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.horizontal, 13, 46, "届 カ ナ イ ヨ"),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, A5sharp, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 1),
    (Action.clear,),
    (Action.vertical, 6, 65, "此 処 は 宴"),
    (Action.vertical, 7, 15, "鋼 の 檻"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 41
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 11, 25, "そ の 断 頭 台 で 見 下 ろ し て"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 43
music.append([
    (Action.music, A5sharp, 1),
    (Action.music, A5, 1),
    (Action.music, G5, 1),
    (Action.music, F5, 1),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, E5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 1),
    (Action.clear,),
    (Action.vertical, 6, 65, "三 千 世 界"),
    (Action.vertical, 6, 15, "常 世 之 闇"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 45 
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.vertical, 6, 65, "嘆 ク 唄 モ"),
    (Action.vertical, 6, 15, "聞 コ エ ナ イ ヨ"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 47
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, A5sharp, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 1),
    (Action.clear,),
    (Action.horizontal, 8, 12, "青 藍"),
    (Action.horizontal, 10, 12, "の 空"),
    (Action.horizontal, 11, 20, "遥 か 彼 方"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 49
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 11, 14, "その"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 51
music.append([
    (Action.horizontal, 11, 20, "光"),
    (Action.music, A5sharp, 1),
    (Action.horizontal, 11, 24, "線"),
    (Action.music, A5, 1),
    (Action.horizontal, 11, 28, "銃"),
    (Action.music, G5, 1),
    (Action.horizontal, 11, 32, "で"),
    (Action.music, F5, 1),
])
music.append([
    (Action.horizontal, 13, 18, "打"),
    (Action.music, G5, 0.5),
    (Action.horizontal, 13, 21, "ち"),
    (Action.music, F5, 0.5),
    (Action.horizontal, 13, 24, "抜"),
    (Action.music, A5, 0.5),
    (Action.horizontal, 13, 27, "い"),
    (Action.music, C6, 0.5),
    (Action.horizontal, 13, 30, "で"),
    (Action.music, D6, 2),
])

# 53
music.append([
    (Action.clear,),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, F5, 0.5),
    (Action.music, E5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
])
music.append([
# 55
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, C6, 0.5),
    (Action.music, F6, 0.5),
    (Action.music, E6, 0.25),
    (Action.music, F6, 0.25),
    (Action.music, E6, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, C6, 0.5),
    (Action.music, A5, 0.5),
])
# 57
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, F5, 0.5),
    (Action.music, E5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
])
# 59
music.append([
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, C6, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, C6, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, D5, 0.75),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.5),
    (Action.music, D5, 1),
    (Action.music, STOP, 1),
])

# 61
music.append([
    (Action.horizontal, 6, 64, "百 戦"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.horizontal, 8, 61, "錬 磨 の"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
])
music.append([
    (Action.vertical, 8, 56, "見た目は"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.horizontal, 11, 61, "将 校"),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
])
# 63
music.append([
    (Action.clear,),
    (Action.vertical, 5, 20, "いったりきたりの"),
    (Action.vertical, 6, 16, "花 魁 道 中"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, A5, 1),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, F5, 1),
    (Action.music, D5, 1),
])
# 65
music.append([
    (Action.clear,),
    (Action.horizontal, 13, 56, "アイツもコイツも"),
    (Action.horizontal, 15, 62, "皆で集まれ"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
])
music.append([
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
])
# 67
music.append([
    (Action.clear,),
    (Action.horizontal, 14, 56, "聖 者 の 行 進"),
    (Action.music, D5, 1),
    (Action.music, D5, 0.75),
    (Action.music, C5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.clear,),
    (Action.horizontal, 15, 16, "わんっ"),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 15, 16, "つー"),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.clear,),
    (Action.horizontal, 15, 16, "さん"),
    (Action.music, F5, 1),
    (Action.clear,),
    (Action.horizontal, 15, 16, "しっ"),
    (Action.music, D5, 1),
])
# 69
music.append([
    (Action.clear,),
    (Action.vertical, 8, 68, "禅 定 門 を"),
    (Action.horizontal, 14, 53, "て け 抜 り 潜"),
    (Action.music, F5, 1),
    (Action.music, E5, 1),
    (Action.music, D5, 1),
    (Action.music, C5, 1),
])
music.append([
    (Action.music, C5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, G4, 0.5),
    (Action.music, A4, 2),
])
# 71
music.append([
    (Action.vertical, 10, 64, "安"),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
    (Action.vertical, 12, 64, "楽"),
    (Action.music, D5, 1),
    (Action.vertical, 10, 60, "浄"),
    (Action.music, G5, 1),
    (Action.vertical, 12, 60, "土"),
    (Action.music, E5, 1),
])
music.append([
    (Action.horizontal, 8, 58, "厄 払 い"),
    (Action.music, F5, 1),
    (Action.music, E5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 2),
])
# 73
music.append([
    (Action.clear,),
    (Action.vertical, 9, 60, "きっと終幕"),
    (Action.music, F5, 1),
    (Action.music, E5, 1),
    (Action.music, D5, 1),
    (Action.music, C5, 1),
])
music.append([
    (Action.vertical, 9, 54, "大"),
    (Action.music, C5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.vertical, 11, 54, "団"),
    (Action.music, A4, 0.5),
    (Action.music, G4, 0.5),
    (Action.vertical, 13, 54, "円"),
    (Action.music, A4, 1),
    (Action.clear,),
    (Action.horizontal, 11, 31, "拍 手 の 合 間 に"),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
])
# 75
music.append([
    (Action.music, D5, 0.5),
    (Action.music, D5, 1),
    (Action.music, D5, 0.5),
    (Action.music, F5, 1),
    (Action.music, G5, 1),
])
music.append([
    (Action.music, E5, 2),
    (Action.music, STOP, 1),
    (Action.clear,),
    (Action.vertical, 8, 16, "千  本  桜"),
    (Action.horizontal, 14, 20, "夜 ニ 紛 レ"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])

# 77
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 10, 28, "君 ノ 声 モ 届 カ ナ イ ヨ"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 79
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, A5sharp, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 1),
    (Action.clear,),
    (Action.vertical, 6, 65, "此 処 は 宴"),
    (Action.vertical, 7, 15, "鋼 の 檻"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 81
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 11, 25, "そ の 断 頭 台 で 見 下 ろ し て"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 83
music.append([
    (Action.music, A5sharp, 1),
    (Action.music, A5, 1),
    (Action.music, G5, 1),
    (Action.music, F5, 1),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, E5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 1),
    (Action.clear,),
    (Action.vertical, 6, 65, "三 千 世 界"),
    (Action.vertical, 6, 15, "常 世 之 闇"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 85 
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.vertical, 6, 65, "嘆 ク 唄 モ"),
    (Action.vertical, 6, 15, "聞 コ エ ナ イ ヨ"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 87
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, A5sharp, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 1),
    (Action.clear,),
    (Action.horizontal, 8, 12, "希 望"),
    (Action.horizontal, 10, 12, "の 空"),
    (Action.horizontal, 11, 20, "遥 か 彼 方"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 89
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 11, 14, "その"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 91
music.append([
    (Action.horizontal, 11, 20, "閃"),
    (Action.music, A5sharp, 1),
    (Action.horizontal, 11, 24, "光"),
    (Action.music, A5, 1),
    (Action.horizontal, 11, 28, "弾"),
    (Action.music, G5, 1),
    (Action.horizontal, 11, 32, "を"),
    (Action.music, F5, 1),
])
music.append([
    (Action.horizontal, 13, 18, "打"),
    (Action.music, G5, 0.5),
    (Action.horizontal, 13, 21, "ち"),
    (Action.music, F5, 0.5),
    (Action.horizontal, 13, 24, "上"),
    (Action.music, A5, 0.5),
    (Action.horizontal, 13, 27, "げ"),
    (Action.music, C6, 0.5),
    (Action.horizontal, 13, 30, "ろ"),
    (Action.music, D6, 2),
])

# 93
music.append([
    (Action.clear,),
    (Action.music, D6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, D6, 0.25),
    (Action.music, C6, 0.25),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, G5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.5),
])
# 95    
music.append([
    (Action.music, D5, 0.5),
    (Action.music, D5, 0.5),
    (Action.music, D5, 0.5),
    (Action.music, D5, 0.5),
    (Action.music, D5, 0.5),
    (Action.music, D5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, A4, 0.5),
])
music.append([
    (Action.music, G4, 0.5),
    (Action.music, A4, 0.25),
    (Action.music, G4, 0.25),
    (Action.music, A4, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, C5sharp, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, A5, 0.1666),
    (Action.music, D6, 0.25),
    (Action.music, F6, 0.25),
    (Action.music, E6, 0.5),
    (Action.music, D6, 0.25),
    (Action.music, E6, 0.25),
])
# 97
music.append([
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.5),
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.5),
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
])
music.append([
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5sharp, 0.25),
    (Action.music, A5sharp, 0.5),
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5sharp, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5sharp, 0.25),
    (Action.music, A5sharp, 0.5),
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5sharp, 0.25),
])
# 99
music.append([
    (Action.music, A5sharp, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5sharp, 0.5),
    (Action.music, A5sharp, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5sharp, 0.5),
    (Action.music, A5sharp, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
])
music.append([
    (Action.music, G5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, G5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, C5sharp, 0.25),
    (Action.music, A5, 0.5),
    (Action.music, A5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, C5sharp, 0.25),
])
# 101
music.append([
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, F6, 0.1666),
    (Action.music, E6, 0.1666),
    (Action.music, D6, 0.1666),
    (Action.music, A5, 0.25),
    (Action.music, F5, 0.25),
])
music.append([
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5sharp, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, D6sharp, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5sharp, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, D5sharp, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, G6, 0.1666),
    (Action.music, F6, 0.1666),
    (Action.music, D6sharp, 0.1666),
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
])
# 103
music.append([
    (Action.music, D6, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, F6, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, F6, 0.25),
    (Action.music, A6sharp, 0.25),
    (Action.music, F6, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, A5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
])
music.append([
    (Action.music, C5, 0.25),
    (Action.music, G4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, C4, 0.25),

    (Action.music, G3, 0.25),
    (Action.music, A3, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, D4, 0.25),

    (Action.music, E4, 0.25),
    (Action.music, G4, 0.25),
    (Action.music, A4, 0.25),
    (Action.music, C5sharp, 0.25),

    (Action.music, A4, 0.0833),
    (Action.music, A4sharp, 0.0833),
    (Action.music, B4, 0.0833),
    (Action.music, C5, 0.0833),
    (Action.music, C5sharp, 0.0833),
    (Action.music, D5, 0.0833),
    (Action.music, D5sharp, 0.0833),
    (Action.music, E5, 0.0833),
    (Action.music, F5, 0.0833),
    (Action.music, F5sharp, 0.0833),
    (Action.music, G5, 0.0833),
    (Action.music, G5sharp, 0.0833),
    (Action.music, A5, 0.0833),
])
# 105
music.append([
    (Action.music, A5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, A5, 0.1666),
    
    (Action.music, F5, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, A5, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, E5, 0.1666),
    
    (Action.music, G5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, F5, 0.1666),
    (Action.music, E5, 0.1666),
    
    (Action.music, D5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, D5, 0.1666),
    (Action.music, E5, 0.1666),
    (Action.music, D5, 0.1666),
    (Action.music, C5, 0.1666),
])
music.append([
    (Action.music, A4, 0.1666),
    (Action.music, G4, 0.1666),
    (Action.music, A4, 0.1666),
    (Action.music, G4, 0.1666),
    (Action.music, F4, 0.1666),
    (Action.music, E4, 0.1666),

    (Action.music, F4, 0.1666),
    (Action.music, G4, 0.1666),
    (Action.music, F4, 0.1666),
    (Action.music, G4, 0.1666),
    (Action.music, F4, 0.1666),
    (Action.music, G4, 0.1666),
    (Action.music, D4, 2)
])
# 107
music.append([
    (Action.music, D3, 0.25),
    (Action.music, D3, 0.25),
    (Action.music, E3, 0.25),
    (Action.music, E3, 0.25),
    (Action.music, F3, 0.25),
    (Action.music, F3, 0.25),
    (Action.music, A3, 0.25),
    (Action.music, A3, 0.25),
    
    (Action.music, G3, 0.25),
    (Action.music, A3, 0.25),
    (Action.music, G3, 0.25),
    (Action.music, G3, 0.25),

    (Action.music, E4, 0.1666),
    (Action.music, F4, 0.1666),
    (Action.music, E4, 0.1666),
    (Action.music, D4, 0.1666),
    (Action.music, E4, 0.1666),
    (Action.music, F4, 0.1666),
])
music.append([
    (Action.music, A4, 1),
    (Action.music, C5, 0.5),
    (Action.music, A4, 0.5),
    (Action.music, A4, 2),
])
# 109
music.append([
    (Action.music, D3, 0.25),
    (Action.music, D3, 0.25),
    (Action.music, C3, 0.25),
    (Action.music, C3, 0.25),
    (Action.music, F3, 0.25),
    (Action.music, F3, 0.25),
    (Action.music, E3, 0.25),
    (Action.music, E3, 0.25),
    
    (Action.music, A3, 0.25),
    (Action.music, A3, 0.25),
    (Action.music, G3, 0.25),
    (Action.music, G3, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, C4, 0.25),
    (Action.music, C4, 0.25),
])
music.append([
    (Action.music, G4, 0.25),
    (Action.music, G4, 0.25),
    (Action.music, F4, 0.25),
    (Action.music, F4, 0.25),
    (Action.music, C5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, C5, 2),
])
# 111
music.append([
    (Action.music, F5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A4sharp, 0.25),
    (Action.music, F4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, F4, 0.25),
    (Action.music, A4sharp, 0.25),
    (Action.music, D5, 0.25),
    
    (Action.music, G5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, G4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, G4, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, E5, 0.25),
])
music.append([
    (Action.music, A5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, A5, 2),
])
# 113
music.append([
    (Action.clear,),
    (Action.horizontal, 14, 10, "環状線を走り抜けて"),
    (Action.music, F5, 1),
    (Action.music, E5, 1),
    (Action.music, D5, 1),
    (Action.music, C5, 1),
])
music.append([
    (Action.music, C5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, G4, 0.5),
    (Action.music, A4, 2),
])
# 115
music.append([
    (Action.horizontal, 16, 14, "東奔西走なんのその"),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 1),
    (Action.music, G5, 1),
    (Action.music, E5, 1),
])
music.append([
    (Action.music, F5, 1),
    (Action.music, E5, 0.5),
    (Action.music, C5, 0.5),
    (Action.music, D5, 2),
])
# 117
music.append([
    (Action.clear,),
    (Action.vertical, 8, 18, "少 年"),
    (Action.music, F5, 1),
    (Action.music, E5, 1),
    (Action.horizontal, 13, 20, "少  女"),
    (Action.music, D5, 1),
    (Action.music, C5, 1),
])
music.append([
    (Action.vertical, 9, 26, "戦 国"),
    (Action.vertical, 9, 22, "無 双"),
    (Action.music, C5, 0.5),
    (Action.music, D5, 0.25),
    (Action.music, C5, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, G4, 0.5),
    (Action.music, A4, 1),
    (Action.clear,),
    (Action.horizontal, 11, 32, "浮 世 の 随 に"),
    (Action.music, A4, 0.5),
    (Action.music, C5, 0.5),
])
# 119
music.append([
    (Action.music, D5, 0.5),
    (Action.music, D5, 1),
    (Action.music, D5, 0.5),
    (Action.music, F5, 1),
    (Action.music, G5, 1),
])
music.append([
    (Action.music, E5, 2),
    (Action.music, STOP, 1),
    (Action.clear,),
    (Action.vertical, 5, 62, "千 本 桜"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])

# 121
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.vertical, 8, 58, "夜 ニ 紛 レ"),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.vertical, 6, 22, "君 ノ 声 モ"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 123
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.vertical, 9, 18, "届 カ ナ イ ヨ"),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, A5sharp, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, F5, 1),
    (Action.clear,),
    (Action.horizontal, 11, 34, "此 処 は 宴"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 125
music.append([
    (Action.music, G5, 0.75),
    (Action.music, G5, 0.75),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.music, STOP, 0.5),
    (Action.clear,),
    (Action.horizontal, 11, 35, "鋼 の 檻"),
    (Action.music, A5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 11, 25, "そ の 断 頭 台 を 飛 び 降 り て"),
    (Action.music, D5, 0.5),
    (Action.music, F5, 0.5),
])
# 127
music.append([
    (Action.music, A5sharp, 1),
    (Action.music, A5, 1),
    (Action.music, G5, 1),
    (Action.music, F5, 1),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, A5, 1),
    (Action.clear,),
    (Action.horizontal, 14, 14, "千  本  桜"),
    (Action.vertical, 5, 14, "夜 ニ 紛 レ"),
    (Action.music, E5, 0.5),
    (Action.music, G5, 0.5),
])
# 129 
music.append([
    (Action.music, A5, 0.75),
    (Action.music, A5, 0.75),
    (Action.music, B5, 0.5),
    (Action.music, B5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, B5, 0.5),
])
music.append([
    (Action.music, D6, 0.5),
    (Action.music, E6, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, B5, 1),
    (Action.clear,),
    (Action.horizontal, 12, 14, "君 が 歌 い"),
    (Action.horizontal, 15, 14, "僕 は 踊 る"),
    (Action.music, E5, 0.5),
    (Action.music, G5, 0.5),
])
# 131
music.append([
    (Action.music, A5, 0.75),
    (Action.music, A5, 0.75),
    (Action.music, B5, 0.5),
    (Action.music, B5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, B5, 0.5),
])
music.append([
    (Action.music, C6, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, G5, 1),
    (Action.clear,),
    (Action.horizontal, 8, 12, "此 処"),
    (Action.horizontal, 10, 12, "は 宴"),
    (Action.horizontal, 11, 20, "鋼 の 檻"),
    (Action.music, E5, 0.5),
    (Action.music, G5, 0.5),
])
# 133
music.append([
    (Action.music, A5, 0.75),
    (Action.music, A5, 0.75),
    (Action.music, B5, 0.5),
    (Action.music, B5, 1),
    (Action.music, STOP, 0.5),
    (Action.music, B5, 0.5),
])
music.append([
    (Action.music, D6, 0.5),
    (Action.music, E6, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, B5, 1),
    (Action.clear,),
    (Action.horizontal, 11, 14, "さあ"),
    (Action.music, E5, 0.5),
    (Action.music, G5, 0.5),
])
# 135
music.append([
    (Action.horizontal, 11, 20, "光"),
    (Action.music, C6, 1),
    (Action.horizontal, 11, 24, "線"),
    (Action.music, B5, 1),
    (Action.horizontal, 11, 28, "銃"),
    (Action.music, A5, 1),
    (Action.horizontal, 11, 32, "を"),
    (Action.music, G5, 1),
])
music.append([
    (Action.horizontal, 13, 18, "打"),
    (Action.music, A5, 0.5),
    (Action.horizontal, 13, 21, "ち"),
    (Action.music, G5, 0.5),
    (Action.horizontal, 13, 24, "ま"),
    (Action.music, B5, 0.5),
    (Action.horizontal, 13, 27, "く"),
    (Action.music, D6, 0.5),
    (Action.horizontal, 13, 30, "れ"),
    (Action.music, E6, 2),
])

# 137
music.append([
    (Action.clear,),
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
])
music.append([
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, G4, 0.5),
    (Action.music, F4sharp, 0.1666),
    (Action.music, G4, 0.1666),
    (Action.music, F4sharp, 0.1666),
    (Action.music, E4, 0.5),
    (Action.music, D4, 0.5),
])
# 139
music.append([
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
])
music.append([
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, D5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, F5sharp, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, F5sharp, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.5),
    (Action.music, B4, 0.5),
])
# 141
music.append([
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
])
music.append([
    (Action.music, A4, 0.5),
    (Action.music, B4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, D4, 0.25),
    (Action.music, G4, 0.5),
    (Action.music, F4sharp, 0.1666),
    (Action.music, G4, 0.1666),
    (Action.music, F4sharp, 0.1666),
    (Action.music, E4, 0.5),
    (Action.music, D4, 0.5),
])
# 143
music.append([
    (Action.music, E4, 0.5),
    (Action.music, D4, 0.25),
    (Action.music, E4, 0.25),
    (Action.music, G4, 0.5),
    (Action.music, E4, 0.25),
    (Action.music, A4, 0.25),
    (Action.music, B4, 0.5),
    (Action.music, A4, 0.25),
    (Action.music, B4, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, G5, 0.25),
    (Action.music, B4, 0.25),
    (Action.music, D5, 0.25),
])
music.append([
    (Action.music, G5, 0.5),
    (Action.music, F5sharp, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, F5sharp, 0.1666),
    (Action.music, E5, 0.5),
    (Action.music, D5, 0.5),
    (Action.music, E5, 1),
    (Action.music, E5, 0.5),
    (Action.music, G5, 0.5),
])
# 145
music.append([
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
])
music.append([
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, F5sharp, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, F5sharp, 0.1666),
    (Action.music, E5, 0.5),
    (Action.music, D5, 0.5),
])
# 147
music.append([
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
])
music.append([
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, D6, 0.5),
    (Action.music, G6, 0.5),
    (Action.music, F6sharp, 0.25),
    (Action.music, G6, 0.25),
    (Action.music, F6sharp, 0.25),
    (Action.music, E6, 0.25),
    (Action.music, D6, 0.5),
    (Action.music, B5, 0.5),
])
# 149
music.append([
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
])
music.append([
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, E5, 0.25),
    (Action.music, D5, 0.25),
    (Action.music, G5, 0.5),
    (Action.music, F5sharp, 0.1666),
    (Action.music, G5, 0.1666),
    (Action.music, F5sharp, 0.1666),
    (Action.music, E5, 0.5),
    (Action.music, D5, 0.5),
])
# 151
music.append([
    (Action.music, B5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, B5, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, E6, 0.25),
    (Action.music, D6, 0.25),
    (Action.music, B5, 0.25),
    (Action.music, A5, 0.25),
    (Action.music, E5, 0.5),
    (Action.music, G5, 0.5),
    (Action.music, A5, 0.5),
    (Action.music, B5, 0.5),
])
music.append([
    (Action.senbonzakura,),
    (Action.music, E6, 0.75),
    (Action.music, E6, 0.75),
    (Action.music, D6, 0.5),
    (Action.music, E6, 1),
    (Action.music, STOP, 0.5),
    (Action.music, D6, 0.25),
    (Action.music, D6sharp, 0.25),
])
# 153
music.append([
    (Action.music, E6, 0.75),
    (Action.music, E6, 0.75),
    (Action.music, D6, 0.5),
    (Action.music, E6, 1),
    (Action.music, STOP, 1),
])



def main():
    playMusic(music)

main()