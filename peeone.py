import serial
import datetime

print('peeone agent running on smartmeter')

ser = serial.Serial('/dev/ttyUSB0', 115200)
runstate = 0
counter = 0
max_entries = 38

#initiale empty list
stream = []

while True:
	line = ser.readline()
	data = line.decode('latin-1')
	if runstate == 1: #stream synced - read / analyze data
		#print(str(counter) + " -> " + data)
		stream.append(data)
		counter += 1
		if data == '/XMX5LGF0010444195104\r\n':
			#print('end detected')
			runstate = 2
			break #once this is done: break and end script	 
			
	if runstate == 0: #First Run to find last line and sync stream
		#print('>' + data)
		if data == '/XMX5LGF0010444195104\r\n':
			runstate = 1
			#print('stream synched')

raw_tarif1kwh = stream[4]
raw_tarif2kwh = stream[5] 
raw_gasm3 = stream[35]

decimal_tarif1kwh = raw_tarif1kwh[10:16]
decimal_tarif2kwh = raw_tarif2kwh[10:16]
decimal_gasm3 = raw_gasm3[26:31]

small_tarif1kwh = raw_tarif1kwh[17:20]
small_tarif2kwh = raw_tarif2kwh[17:20]
small_gasm3 = raw_gasm3[32:35]

#tarif1kwh = int(decimal_tarif1kwh) + (int(small_tarif1kwh)/1000)
#tarif2kwh = int(decimal_tarif2kwh) + (int(small_tarif2kwh)/1000)
#gasm3 = int(decimal_gasm3) + (int(small_gasm3)/1000)

tarif1kwh = int(decimal_tarif1kwh)
tarif2kwh = int(decimal_tarif2kwh)
gasm3 = int(decimal_gasm3)



timenow = datetime.datetime.now().time()
datenow = datetime.datetime.now().date()

output = str(datenow) + ';' + str(timenow) + ';'+  str(tarif1kwh) + ';' + str(tarif2kwh) + ';' + str(gasm3) + '\n'

print(output)

f= open('/home/pi/peeone/data.txt' , 'a')
f.write(output)
f.close

print("Success")


