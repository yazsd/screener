from datetime import datetime
import time
import sig

four_hrs_ms = 14400
req_sec = [0]
req_min = [0,30]

def log_data(fn, val):
	with open(fn, "a") as myfile:
		myfile.write(val+'\n')

# sig.process_positions()

while 1:
	ts = (time.time()+four_hrs_ms)
	mnt = int(datetime.utcfromtimestamp(ts).strftime('%M'))
	sec = int(datetime.utcfromtimestamp(ts).strftime('%S'))
	if((mnt in req_min) and (sec in req_sec)):
		start_ts = time.time()*1000
		s = sig.process_positions()
		print(s)
		end_ts = time.time()*1000
		print(end_ts-start_ts)
		ts = (time.time()+four_hrs_ms)
		tm = datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
		print(tm)
		print(f'min={mnt}\tsec={sec}')
		sig_log = f'{tm}--{s}'
		log_data('sig-log.txt', sig_log)
	time.sleep(0.1)
