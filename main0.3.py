from warnings import warn
import ctypes
import time
import pydivert as p
import random
import threading
# Amulet 0.3 source, much less scuffed.

# Admin Check
if not ctypes.windll.shell32.IsUserAnAdmin():
	warn("Program will not run if not admin.")
else:
	pcs = []
	print("Opening main program.")
	__import__("time").sleep(1)
	__import__("os").system("cls")
	opreset = "((ip and ip.Length<=1500) or (ipv6 and ipv6.Length<=1500))"
	# Random Chance
	def rc(percent):
		if percent == 100:
			return True
		if percent == 0:
			return False
		if float(random.random()) < float(int(percent)/100):
			return True
		else:
			return False
	def clear():
		__import__("os").system("cls") #inefficient, i know, but its alright
	def main():
			clear()
			print("Amulet 0.3")
			preset = input("Enter preset... (will go to default otherwise) ")
			if preset == "":
				preset = opreset
			clear()
			print("Options:")
			print("Lag: L")
			print("Drop: D")
			print("Duplicate: X2")
			print("Tamper: T?")
			choice = input("Enter choice here: ")
			if choice == "L" or choice == "l":
				clear()
				chance = input("Enter chance here... (will default to 50) ")
				if chance == "":
					chance = 50
				delay = input("Enter delay... (in milliseconds) ")
				maxThreads = input("Enter maximum threads for lag (will default to 5)... ")
				if maxThreads == "":
					maxThreads = 5
				with p.WinDivert(preset) as w:
					def sendlag():
						time.sleep(int(delay)/1000)
						w.send(packet)
					for packet in w:
						if rc(chance):
							pcs.append(threading.Thread(target=sendlag, args=()))
							pcs[len(pcs) - 1].start()
							print("Started thread to lag packet")
							print(f"Lagged packet for {delay} milliseconds.")
							if threading.active_count() == int(maxThreads):
								for t in pcs:
									t.join()
							else:
								w.send(packet)
								print(f"Ignoring packet, {chance}% chance of packet lag")

			if choice == "D" or choice == "d":
				chance = input("Enter chance for dropping... (will default to 50) ")
				if chance == "":
					chance = 50
				with p.WinDivert(preset) as w:
					for packet in w:
						if rc(chance):
							packet.payload = b""
							w.send(packet)
							print("Dropped packet")
						else:
							print(f"Ignoring packet, {chance}% chance of dropping")
			if choice == "X2" or choice == "x2":
				chance = input("Enter chance for duping... (will default to 50) ")
				if chance == "":
					chance = 50
				num = input("Enter number of packets to make... (will default to 2) ")
				if num == "":
					num = 2
				with p.WinDivert(preset) as w:
					for packet in w:
						if rc(chance):
							for _ in range(int(num)):
								w.send(packet)
							print(f"Duped packets {num} times")
						else:
							print(f"Ignoring packet, {chance}% chance for duping...")
							w.send(packet)
			if choice == "T?" or choice == "t?":
				chance = input("Enter chance for corruption... (will default to 10) ")
				if chance == "":
					chance = 10
				cpercent = int(input("Enter amount of packet to corrupt (will default to 5)..."))
				if cpercent == "":
					cpercent = 5
				with p.WinDivert(preset) as w:
					for packet in w:
						if rc(chance):
							og = packet.payload
							l = len(og)
							packet.payload = og[:round(l * cpercent/100)]+bytes(''.join(random.choice(str(og)) for _ in  range(l - round(l * cpercent/100))), 'utf-8')
							if len(packet.payload) == l:
								w.send(packet)
								print(f"Sucessfully corrupted {cpercent}% of packet.")
							else:
								print("Failed!")
								w.send(og)
						else:
							print(f"Ignoring packet, {chance}% chance for corrupting...")
							w.send(packet)





	if __name__ == "__main__":
		main()
