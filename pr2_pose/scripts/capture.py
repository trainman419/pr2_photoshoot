#!/usr/bin/env python

import roslib; roslib.load_manifest('pr2_pose')
import rospy
import yaml
from sensor_msgs.msg import JointState

if __name__ == '__main__':
   rospy.init_node('capture')
   argv = rospy.myargv()

   joints = [
      'torso_lift_joint', 'torso_lift_motor_screw_joint', 
      'head_pan_joint', 'head_tilt_joint',

      'r_upper_arm_roll_joint', 'r_shoulder_pan_joint', 'r_shoulder_lift_joint',
      'r_forearm_roll_joint', 'r_elbow_flex_joint', 'r_wrist_flex_joint',
      'r_wrist_roll_joint', 

      'l_upper_arm_roll_joint', 'l_shoulder_pan_joint', 'l_shoulder_lift_joint',
      'l_forearm_roll_joint', 'l_elbow_flex_joint', 'l_wrist_flex_joint',
      'l_wrist_roll_joint'
   ]

   pose = rospy.wait_for_message('joint_states', JointState)

   output = {}

   for joint in joints:
      index = pose.name.index(joint)
      output[joint] = pose.position[index]


   fname = 'pose.yaml'
   if len(argv) > 1:
      fname = argv[1]

   print "Writing pose to %s"%fname

   stream = file(fname, 'w')

   yaml.dump(output, stream)
