#!/usr/bin/env python3

import argparse
import serial
import otomo_pb2
import time
import signal

ser = None

def handler(_signum, _frame):
    if ser is not None:
        ser.close()
    exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="serial port being used", default="/dev/ttyUSB0")
    parser.add_argument("-b", "--baud", help="serial port baudrate", default=38400)

    args = parser.parse_args()

    port = args.port
    baud = args.baud

    signal.signal(signal.SIGINT, handler)

    ser = serial.Serial(port, baud)
    
    js_move = otomo_pb2.Joystick()
    js_move.heading = 0.0
    js_move.speed = 50.0

    js_stop = otomo_pb2.Joystick()
    js_stop.heading = 0.0
    js_stop.speed = 0.0

    msg = otomo_pb2.TopMsg()

    while True:
        msg.joystick.CopyFrom(js_move)
        ser.write(msg.SerializeToString())
        ser.write(b"\xff")
        time.sleep(3)
        msg.joystick.CopyFrom(js_stop)
        ser.write(msg.SerializeToString())
        ser.write(b"\xff")
        time.sleep(3)
