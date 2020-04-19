import zbar
import sys
import multiprocessing
import time


def func():
	proc = zbar.Processor()
	proc.parse_config('enable')

	device = '/dev/video0'

	proc.init(device)
#	proc.visible = True
	proc.process_one()
	proc.visible = False

	for symbol in proc.results:
		print(symbol.data)

p = multiprocessing.Process(target=func, name="Func", args=())
p.start()

# Wait 10 seconds for foo
time.sleep(3)

# Terminate foo
p.terminate()

# Cleanup
p.join()