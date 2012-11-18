################################################################################
# Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                    #
# NOTICE: This developer release of Leap Motion, Inc. software is confidential #
# and intended for very limited distribution. Parties using this software must #
# accept the SDK Agreement prior to obtaining this software and related tools. #
# This software is subject to copyright.                                       #
################################################################################

import Leap, sys, math

class SampleListener(Leap.Listener):

  def onInit(self, controller):
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
    print "Frame id: %d, timestamp: %d, hands: %d" % (
          frame.id(), frame.timestamp(), numHands)

    if numHands >= 1:
      # Get the first hand
      hand = hands[0]

      # Check if the hand has any fingers
      fingers = hand.fingers()
      numFingers = len(fingers)
      if numFingers >= 1:
        # Calculate the hand's average finger tip position
        pos = Leap.Vector(0, 0, 0)
        for finger in fingers:
          tip = finger.tip()
          pos.x += tip.position.x
          pos.y += tip.position.y
          pos.z += tip.position.z
        pos = Leap.Vector(pos.x/numFingers, pos.y/numFingers, pos.z/numFingers)
        print "Hand has %d fingers with average tip position (%f, %f, %f)" % (
              numFingers, pos.x, pos.y, pos.z)

      # Check if the hand has a palm
      palmRay = hand.palm()
      if palmRay is not None:
        # Get the palm position and wrist direction
        palm = palmRay.position
        wrist = palmRay.direction
        print "Palm position (%f, %f, %f)" % (palm.x, palm.y, palm.z)

        # Check if the hand has a normal vector
        normal = hand.normal()
        if normal is not None:
          # Calculate the hand's pitch, roll, and yaw angles
          pitchAngle = math.atan2(normal.z, normal.y) * 180/math.pi + 180
          rollAngle = math.atan2(normal.x, normal.y) * 180/math.pi + 180
          yawAngle = math.atan2(wrist.z, wrist.x) * 180/math.pi - 90
          # Ensure the angles are between -180 and +180 degrees
          if pitchAngle > 180: pitchAngle -= 360
          if rollAngle > 180: rollAngle -= 360
          if yawAngle > 180: yawAngle -= 360
          print "Pitch: %f degrees,  roll: %f degrees,  yaw: %f degrees" % (
                pitchAngle, rollAngle, yawAngle);

      # Check if the hand has a ball
      ball = hand.ball();
      if ball is not None:
        print "Hand curvature radius: %f mm" % ball.radius


def main():
  # Create a sample listener and assign it to a controller to receive events
  listener = SampleListener()
  controller = Leap.Controller(listener)

  # Keep this process running until Enter is pressed
  print "Press Enter to quit..."
  sys.stdin.readline()

  # The controller must be disposed of before the listener
  controller = None


if __name__ == "__main__":
  main()
