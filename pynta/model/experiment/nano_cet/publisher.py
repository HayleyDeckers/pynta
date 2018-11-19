"""
    publisher.py
    ============
    General script that shows how to use ZMQ to publish frames without a time limitation. It uses sockets. To stop it,
    pressing Ctrl+C will do the work cleanly. The data generated by the publisher should be consumed by a subscriber.
    Check ``subscriber.py`` to see how to achieve it.
"""

import zmq
import numpy as np
from time import time, sleep

image = np.random.random((1200, 120))

port = 5555
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
sleep(1)

i = 1
total_time = 0
while i <= 500:
    t0 = time()
    try:
        # md = dict(dtype=str(image.dtype),
        #           shape=image.shape)
        # socket.send_json(md, 0 | zmq.SNDMORE)
        # socket.send(image, flags=0, copy=True, track=False)
        # sleep(.1)
        socket.send_pyobj(image)
        this_time = time() - t0
        total_time += this_time
        # print("Sending time: {:3.4f}ms".format(1000*this_time), end='\r')
        i += 1
    except KeyboardInterrupt:
        break

    # sleep(0.01)


print("\nAverage time to send: {:3.4}ms".format(1000*total_time/i))
socket.send_json({'stop': True})
socket.send(image)
# print('Finishing')
