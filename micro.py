import sys
import time

import Leap
from autopy import mouse

MIN_X = -180
MAX_X = 180
XRANGE = MAX_X - MIN_X

MIN_Y = 200
MAX_Y = 360
YRANGE = MAX_Y - MIN_Y

screenx = 1440
screeny = 900

def x(val):
    if val < -180:
        return 0
    if val > 180:
        return 1439
    scale = screenx / XRANGE
    return int(scale * (val + 180))

def y(val):
    if val < 200:
        return 899
    if val > 360:
        return 0
    scale = screeny / YRANGE
    return 900 - int(scale * (val - 200))

def low_pass_filter(vals):
    inc = 1/len(vals) * 2/len(vals)
    avg = 0
    for i in xrange(1, len(vals)+1):
        avg += vals[i-1] * i * inc
    return avg


class Listener(Leap.Listener):

    def onInit(self, controller):
        self.avgx = [0 for i in xrange(10)]
        self.avgy = [0 for i in xrange(10)]
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
        if len(hands) > 0:
            hand = hands[-1]
            fingers = hand.fingers()
            print "Frame id: %d, timestamp: %d, hands: %d" % (
                        frame.id(), frame.timestamp(), numHands)

            hand = hands[0]

            numFingers = len(fingers)
            if numFingers >= 1:
                if numFingers == 1:
                    mouse.toggle(False, mouse.LEFT_BUTTON)
                else:
                    mouse.toggle(True, mouse.LEFT_BUTTON)
                # Calculate the hand's average finger tip position
                pos = Leap.Vector(0, 0, 0)
                for finger in fingers:
                    tip = finger.tip()
                    pos.x += tip.position.x
                    pos.y += tip.position.y
                    pos.z += tip.position.z
                pos = Leap.Vector(pos.x/numFingers, pos.y/numFingers, pos.z/numFingers)
                print "Hand has %d fingers with average tip position (%f, %f" % (
                        numFingers, pos.x, pos.y)
                self.avgx.pop(0)
                self.avgy.pop(0)
                self.avgx.append(pos.x)
                self.avgy.append(pos.y)
                move_x = x(low_pass_filter(self.avgx))
                move_y = y(low_pass_filter(self.avgy))
                print "Moving to %d, %d" % (move_x, move_y)
                mouse.move(move_x, move_y)
                mouse.move(x(low_pass_filter(self.avgx)), y(low_pass_filter(self.avgy)))
            else:
                mouse.toggle(False, mouse.LEFT_BUTTON)
                self.avgx.pop(0)
                self.avgy.pop(0)
                self.avgx.append(self.avgx[-1])
                self.avgy.append(self.avgy[-1])
        else:
            mouse.toggle(False, mouse.LEFT_BUTTON)
            self.avgx.pop(0)
            self.avgy.pop(0)
            self.avgx.append(self.avgx[-1])
            self.avgy.append(self.avgy[-1])
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
