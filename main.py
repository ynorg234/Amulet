import pydivert as p
from time import sleep
import random
import sys
from warnings import warn
# Amulet source, scuffed

sys.setrecursionlimit(2147483647)
def rnd(percent):
	if float(random.random()) < float(int(percent)/100):
		return True
	else:
		return False
def main():
	print("""
           ,ggg,                                                        
          dP""8I                                  ,dPYb,           I8   
         dP   88                                  IP'`Yb           I8   
        dP    88                                  I8  8I        88888888
       ,8'    88                                  I8  8'           I8   
       d88888888    ,ggg,,ggg,,ggg,   gg      gg  I8 dP   ,ggg,    I8   
 __   ,8"     88   ,8" "8P" "8P" "8,  I8      8I  I8dP   i8" "8i   I8   
dP"  ,8P      Y8   I8   8I   8I   8I  I8,    ,8I  I8P    I8, ,8I  ,I8,  
Yb,_,dP       `8b,,dP   8I   8I   Yb,,d8b,  ,d8b,,d8b,_  `YbadP' ,d88b, 
 "Y8P"         `Y88P'   8I   8I   `Y88P'"Y88P"`Y88P'"Y88888P"Y8888P""Y8 
              Update 0.2-rc3
              The Lagger made in Python!                                                          
                                                                                                                                                
""")
	print("""
		Options:
		Lag: L
		Drop: D
		Duplicate: X2
		Tamper: T?
		""")
	choice = input("Enter choice here: ")
	if choice == "L":
		delay = int(input("Enter delay (in milliseconds): "))
		chance = input("Enter chance here (in percentage): ")
		with p.WinDivert("((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))") as w:
			for packet in w:
				try:
					if rnd(chance):
						sleep(delay/1000)
						w.send(packet)
						print(f"Delayed packet by {delay} milliseconds")
					else:
						w.send(packet)
						print(f"Ignoring packet, {chance}% chance of lagging")
				except:
					print("Packet too large or other error.")
	if choice == "D":
		chance = input("Enter chance here (in percentage): ")
		with p.WinDivert("((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))") as w:
			for packet in w:
				try:
					if rnd(chance):
						print("Dropped packet")
						continue
					else:
						w.send(packet)
						print(f"Ignoring packet, {chance}% chance of packet loss")
				except:
					print("Packet too large or other error.")
	if choice == "X2":
		times = int(input("Enter amount of packet dupes to make: "))
		chance = input("Enter chance here (in percentage): ")
		with p.WinDivert("((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))") as w:
			for packet in w:
				try:
					if rnd(chance):
						for _ in range(times):
							w.send(packet)
						print(f"Sent packets {times} times.")
					else:
						w.send(packet)
						print(f"Ignoring packet, {chance}% chance of duping")
				except:
					print("Packet too large or other error.")
	if choice == "T?":
		chance = input("Enter chance here (in percentage): ")
		percent = int(input("Enter percent of packet to corrupt: "))
		with p.WinDivert("((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))") as w:
			for packet in w:
				try:
					if rnd(chance):
						if packet.payload == None:
							continue
						pStr = str(packet.payload)
						prevLen = len(pStr)
						cutOff = prevLen - (int((len(pStr) * percent)/100)+1)
						packet.payload = bytes(pStr[:cutOff]+''.join(random.choice(pStr) for _ in range(prevLen - cutOff)), 'utf-8') # confusing as heck but is a partial corruptor
						if prevLen != len(packet.payload):
							warn(f"Error! Data lost in corruption! {int((prevLen - len(packet.payload))/prevLen)}% lost!")
							warn("Sending fallback")
							w.send(bytes(pStr, 'utf-8'))
							continue
						print(f"Corrupted {percent}% of packet")
						w.send(packet)
					else:
						w.send(packet)
						print(f"Ignoring packet, {chance}% chance of corruption")
				except:
					warn("error idek")
					w.send(packet)
if __name__ == "__main__":
	main()
