#!/usr/bin/env python
# take a set of joint positions from a yaml file and replay them,
# or take two sets of joint positions and interpolate between them
# 
# This is written specifically to make photoshoots of the PR2 easier.
#
# One pose:
#  pose.py [pose.yaml]
#
# Two poses:
#  pose.py <1.yaml> <2.yaml> <steps>


import roslib; roslib.load_manifest('pr2_pose')
import rospy
import yaml

# move the robot to the specified pose
def pose(position):
   print yaml.dump(position)


if __name__ == '__main__':
   rospy.init_node('pose')
   argv = rospy.myargv()

   fname1 = 'pose.yaml'
   if len(argv) > 1:
      fname1 = argv[1]

   p1 = yaml.load(file(fname1), 'r')

   if len(argv) == 4:
      fname2= argv[2]
      steps = int(argv[3])
   else if len(argv) < 2:
      pose(p1)
   else:
      print "Improper number of arguments"
      print "Usage"
      print "  pose.py [pose.yaml]"
      print "  pose.py <1.yaml> <2.yaml> <steps>"
