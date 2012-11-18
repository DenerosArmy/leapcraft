import sys
import time

import Leap
from autopy import mouse

MIN_X = -150
MAX_X = 150
XRANGE = MAX_X - MIN_X

MIN_Y = 220
MAX_Y = 360
YRANGE = MAX_Y - MIN_Y

screenx = 1440
screeny = 900

def x(val):
    if val < MIN_X:
        return 0
    if val > MAX_X:
        return 1439
    scale = screenx / XRANGE
    return int(scale * (val - MIN_X))

def y(val):
    if val < MIN_Y:
        return 899
    if val > MAX_Y:
        return 0
    scale = screeny / YRANGE
    return 899 - int(scale * (val - MIN_Y))

def low_pass_filter(vals):
    inc = 1/len(vals) * 2/len(vals)
    avg = 0
    for i in xrange(1, len(vals)+1):
        avg += vals[i-1] * i * inc
    return avg


class Listener(Leap.Listener):

    def onInit(self, controller):
        self.avgx = 0
        self.avgy = 0
        print "Initialized"

    def onConnect(self, controller):
        print "Connected"

    def onDisconnect(self, controller):
        print "Disconnected"

    def onFrame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands = frame.hands()
        numHands = len(hands)
        pos = Leap.Vector(self.avgx, self.avgy, 0)
        if len(hands) > 0:
            hand = hands[-1]

            move_x = x(self.avgx)
            move_y = y(self.avgy)
            mouse.move(move_x, move_y)
            print "Moving to %d, %d" % (move_x, move_y)

            fingers = hand.fingers()
            print "Frame id: %d, timestamp: %d, hands: %d" % (
                        frame.id(), frame.timestamp(), numHands)

            hand = hands[0]

            palmRay = hand.palm()
            if palmRay is not None:
                print "Hand has palm position (%f, %f" % (
                    pos.x, pos.y)
                palm = palmRay.position
                pos.x = palm.x
                pos.y = palm.y

            numFingers = len(fingers)
            if numFingers == 1:
                mouse.toggle(False, mouse.LEFT_BUTTON)
                mouse.toggle(True, mouse.RIGHT_BUTTON)
            elif numFingers == 2:
                mouse.toggle(True, mouse.LEFT_BUTTON)
                mouse.toggle(False, mouse.RIGHT_BUTTON)
            else:
                mouse.toggle(False, mouse.LEFT_BUTTON)
                mouse.toggle(False, mouse.RIGHT_BUTTON)
        else:
            mouse.toggle(False, mouse.LEFT_BUTTON)
            mouse.toggle(False, mouse.RIGHT_BUTTON)
        self.avgx = self.avgx*0.7 + pos.x*0.3
        self.avgy = self.avgy*0.7 + pos.y*0.3
        time.sleep(0.001)



def main():
# Create a sample listener and assign it to a controller to receive events
    listener = Listener()
    controller = Leap.Controller(listener)

# Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()

# The controller must be disposed of before the listener
    controller = None

if __name__ == "__main__":
    main()
