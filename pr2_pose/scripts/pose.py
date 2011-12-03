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
import actionlib
import yaml

from pr2_controllers_msgs.msg import JointTrajectoryGoal, JointTrajectoryAction
from trajectory_msgs.msg import JointTrajectoryPoint

def pose_(position, joints, client):
   goal = JointTrajectoryGoal()
   goal.trajectory.joint_names = joints

   goal.trajectory.points = [ JointTrajectoryPoint() ]

   goal.trajectory.points[0].velocities = [0.0] * len(joints);
   goal.trajectory.points[0].positions = [0.0] * len(joints);
   for i, j in enumerate(joints):
      goal.trajectory.points[0].positions[i] = position[j]

   goal.trajectory.points[0].time_from_start = rospy.Duration.from_sec(1.0)
   client.send_goal(goal)

def pose_r(position):
   joints = ["r_shoulder_pan_joint", "r_shoulder_lift_joint", "r_upper_arm_roll_joint", "r_elbow_flex_joint", "r_forearm_roll_joint", "r_wrist_flex_joint", "r_wrist_roll_joint"]
   pose_(position, joints, traj_client_r)

def pose_l(position):
   joints = ["l_shoulder_pan_joint", "l_shoulder_lift_joint", "l_upper_arm_roll_joint", "l_elbow_flex_joint", "l_forearm_roll_joint", "l_wrist_flex_joint", "l_wrist_roll_joint"]
   pose_(position, joints, traj_client_l)

def pose_head(position):
   joints = [ 'head_pan_joint', 'head_tilt_joint' ]
   pose_(position, joints, traj_client_head)

def pose_torso(position):
   joints = [ 'torso_lift_joint' ]
   pose_(position, joints, traj_client_torso)

# move the robot to the specified pose
def pose(position):
   pose_l(position)
   pose_r(position)
   pose_head(position)
   pose_torso(position)

def TrajClient(t):
   c = actionlib.SimpleActionClient(t, JointTrajectoryAction)
   c.wait_for_server()
   return c

if __name__ == '__main__':
   rospy.init_node('pose')
   argv = rospy.myargv()

   traj_client_r = TrajClient("r_arm_controller/joint_trajectory_action")
   traj_client_l = TrajClient("l_arm_controller/joint_trajectory_action")
   traj_client_head = TrajClient('head_traj_controller/joint_trajectory_action')
   traj_client_torso = TrajClient('torso_controller/joint_trajectory_action')

   fname1 = 'pose.yaml'
   if len(argv) > 1:
      fname1 = argv[1]

   p1 = yaml.load(file(fname1, 'r'))

   if len(argv) == 4:
      fname2= argv[2]
      steps = int(argv[3])

      p2 = yaml.load(file(fname2, 'r'))
      p = dict(p1)
      for i in range(steps):
         for j in p1:
            p[j] = ((steps - i)*p1[j] + i*p2[j]) / steps
         pose(p)
         print yaml.dump(p)
         raw_input("%d > "%i)
      print steps
      pose(p2)
      print yaml.dump(p2)
   elif len(argv) < 3:
      pose(p1)
   else:
      print "Improper number of arguments"
      print "Usage"
      print "  pose.py [pose.yaml]"
      print "  pose.py <1.yaml> <2.yaml> <steps>"
