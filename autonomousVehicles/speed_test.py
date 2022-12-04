import time

speed = 0
prev = 0
cur = 0
while True:

    with open('/sys/module/op_encode/parameters/op_count', 'r') as fileread:
        cur = int(fileread.read())
    speed = cur - prev
    prev = cur
    
    print(speed)
    
    time.sleep(0.3)