import wx
import pydivert as p
import ctypes
import time
import random, threading

__import__("sys").setrecursionlimit(2147483647)
__import__("os").system("cls")
print("Amulet 0.4 RELEASE")
class App1(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,400))
        panel = wx.Panel(self)
        self.Entry = wx.StaticText(panel, label="Amulet 0.4 (Finally, some UI!)", pos=(125,20))
        self.Show(True)
        self.input = wx.TextCtrl(panel, pos=(100, 45), size=(200, -1))
        self.input.SetHint("WinDivert Preset")
        self.Button = wx.Button(panel, wx.ID_CLEAR, "Lag", pos=(100, 100))
        self.Button.Show(True)
        self.Button.Bind(wx.EVT_BUTTON, self.lag)
        self.Entry1 = wx.TextCtrl(panel, size=(50, 20), pos=(177, 101))
        self.Entry1.SetHint("Threads")
        self.Entry2 = wx.TextCtrl(panel, size=(50, 20), pos=(177+55, 101))
        self.Entry2.SetHint("Delay")
        self.Entry3 = wx.TextCtrl(panel, size=(50, 20), pos=(177+110, 101))
        self.Entry3.SetHint("Chance")
        self.Button2 = wx.Button(panel, wx.ID_CLEAR, "Drop", pos=(100, 125))
        self.Button2.Show(True)
        self.Button2.Bind(wx.EVT_BUTTON, self.drop)
        self.Entry4 = wx.TextCtrl(panel, size=(50, 20), pos=(177, 126))
        self.Entry4.SetHint("Chance")
        self.Button3 = wx.Button(panel, wx.ID_CLEAR, "Duplicate", pos=(100, 150))
        self.Button3.Show(True)
        self.Button3.Bind(wx.EVT_BUTTON, self.dupe)
        self.Entry5 = wx.TextCtrl(panel, size=(50, 20), pos=(177, 151))
        self.Entry5.SetHint("Copies")
        self.Entry6 = wx.TextCtrl(panel, size=(50, 20), pos=(177+55, 151))
        self.Entry6.SetHint("Chance")
        self.Button3 = wx.Button(panel, wx.ID_CLEAR, "Tamper", pos=(100, 175))
        self.Button3.Show(True)
        self.Button3.Bind(wx.EVT_BUTTON, self.corrupt)
        self.Entry7 = wx.TextCtrl(panel, size=(50, 20), pos=(177, 176))
        self.Entry7.SetHint("Leave%")
        self.Entry8 = wx.TextCtrl(panel, size=(50, 20), pos=(177+55, 176))
        self.Entry8.SetHint("Chance")
        self.Button4 = wx.Button(panel, wx.ID_CLEAR, "Out of Order", pos=(93, 200))
        self.Button4.Show(True)
        self.Button4.Bind(wx.EVT_BUTTON, self.shuffle)
        self.Entry9 = wx.TextCtrl(panel, size=(50, 20), pos=(183, 201))
        self.Entry9.SetHint("Chance")
        self.Button5 = wx.Button(panel, wx.ID_CLEAR, "Jitter", pos=(99, 225))
        self.Button5.Bind(wx.EVT_BUTTON, self.jitter)
        self.Entry10 = wx.TextCtrl(panel, size=(50, 20), pos=(177, 226))
        self.Entry10.SetHint("TimeF...")
        self.Entry11 = wx.TextCtrl(panel, size=(50, 20), pos=(177+55, 226))
        self.Entry11.SetHint("Chance")
    def rc(self, percent):
	    return True if percent == 100 else False if percent == 0 else True if float(random.random()) < float(int(percent)/100) else False
    def lag(self, e=None): #type: ignore
        pcs = []
        preset = self.input.GetValue()
        if preset == "":
            preset = "((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))"
        maxThreads = self.Entry1.GetValue()
        if maxThreads == "":
            maxThreads = 5
        maxThreads = int(maxThreads)
        chance = self.Entry3.GetValue()
        if chance == "":
            chance = 25
        chance = int(chance)
        delay = self.Entry2.GetValue()
        if delay == "":
            delay = 10
        delay = int(delay)
        with p.WinDivert(preset) as w:
            def sendlag():
                time.sleep(delay/1000)
                w.send(packet)
            for packet in w:
                if self.rc(chance):
                    pcs.append(threading.Thread(target=sendlag, args=()))
                    pcs[len(pcs) - 1].start()
                    print("Started thread to lag packet")
                    print(f"Lagged packet for {delay} milliseconds.")
                    if threading.active_count == maxThreads:
                        for t in pcs:
                            t.join()
                else:
                     
                    w.send(packet)
                    print(f"Ignoring packet, {chance}% chance of packet lag")
    def drop(self, e=None):
        preset = self.input.GetValue()
        if preset == "":
            preset = "((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))"
        chance = self.Entry4.GetValue()
        if chance == "":
            chance = 25
        chance = int(chance)
        with p.WinDivert(preset) as w:
            for packet in w:
                if self.rc(chance) and packet.payload != None:
                    packet.payload = b""
                    w.send(packet)
                    print("Dropped Packet")
                else:
                     
                    w.send(packet)
                    print(f"Ignoring packet, {chance}% chance of packet loss")
    def dupe(self, e=None):
        preset = self.input.GetValue()
        if preset == "":
            preset = "((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))"
        chance = self.Entry6.GetValue()
        if chance == "":
            chance = 25
        chance = int(chance)
        copies = self.Entry5.GetValue()
        if copies == "":
            copies = 2
        copies = int(copies)
        with p.WinDivert(preset) as w:
            for packet in w:
                if self.rc(chance):
                    for _ in range(copies):
                        w.send(packet)
                    print(f"Duplicated packet {copies} time(s).")
                else:
                     
                    w.send(packet)
                    print(f"Ignoring packet, {chance}% chance for packet duplication.")
    def corrupt(self, e=None):
        leave = self.Entry7.GetValue()
        if leave == "":
            leave = 75
        leave = int(leave)
        chance = self.Entry8.GetValue()
        if chance == "":
            chance = 10
        chance = int(chance)
        preset = self.input.GetValue()
        if preset == "":
            preset = "((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))"
        with p.WinDivert(preset) as w:
            for packet in w:
                if self.rc(chance):
                    og = packet.payload
                    l = len(og)
                    packet.payload = og[:round(l * leave/100)]+bytes(''.join(random.choice(str(og)) for _ in range(l - round(l * leave/100))), 'utf-8')
                    if len(packet.payload) == l:
                        w.send(packet)
                        print(f"Sucessfully left {leave}% of packet, and corrupted the rest.")
                    else:
                        print("Error! Data lost in corruption!")
                        print("Fallback init")
                        packet.payload = og
                        w.send(packet)
                else:
                     
                    w.send(packet)
                    print(f"Ignoring packet, {chance}% chance for corruption.")
    def shuffle(self, e=None):
        preset = self.input.GetValue()
        if preset == "":
            preset = "((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))"
        chance = self.Entry9.GetValue()
        if chance == "":
            chance = 25
        chance = int(chance)
        packetlist = []
        with p.WinDivert(preset) as w:
            for packet in w:
                if self.rc(chance):
                    packetlist.append(packet)
                    randnum = random.randint(0, len(packetlist) - 1)
                    w.send(packetlist[randnum])
                    if len(packetlist) == 500:
                        del packetlist[:250]
                    print(f"Sent packet #{randnum}")
                else:
                    packetlist.append(packet)
                    w.send(packet)
                    if len(packetlist) == 500:
                        del packetlist[:250]
                    print(f"Ignoring packet, {chance}% chance for packet shuffling.")
    def jitter(self, e=None):
        preset = self.input.GetValue()
        if preset == "":
            preset = "((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))"
        timeframe = self.Entry10.GetValue()
        if timeframe == "":
            timeframe = 50
        timeframe = int(timeframe)
        chance = self.Entry11.GetValue()
        if chance == "":
            chance = 10
        chance = int(chance)
        with p.WinDivert(preset) as w:
            for packet in w:
                if self.rc(chance):
                    delay = random.randint(0, timeframe)
                    time.sleep(delay/1000)
                    w.send(packet)
                    print(f"Delayed packet by {delay} seconds while being in a {timeframe} timeframe.")
                else:
                    w.send(packet)
                    print(f"Ignoring packet, {chance}% chance for jitter...")








if __name__ == "__main__": #and ctypes.windll.shell32.IsUserAnAdmin():
    app = wx.App(False)
    frame = App1(None, "Amulet 0.4 RELEASE")
    app.MainLoop()
