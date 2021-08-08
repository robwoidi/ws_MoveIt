#!/usr/bin/env python3
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
try:
  from math import pi, tau, dist, fabs, cos
except: # For Python 2 compatibility
  from math import pi, fabs, cos, sqrt
  tau = 2.0*pi
  def dist(p, q):
    return sqrt(sum((p_i - q_i)**2.0 for p_i, q_i in zip(p,q)))
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('arm_move', anonymous=True)

robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

group_arm = "panda_arm"
move_group_arm = moveit_commander.MoveGroupCommander(group_arm)


# We get the joint values from the group and change some of the values:
#joint_goal = move_group_arm.get_current_joint_values()

move_group_arm.set_named_target('ready')
plan = move_group_arm.go(wait=True)
# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
#move_group.go(joint_goal, wait=True)

# Calling ``stop()`` ensures that there is no residual movement
move_group_arm.stop()
move_group_arm.clear_pose_targets()

rospy.sleep(5)

group_hand = "hand"
move_group_hand = moveit_commander.MoveGroupCommander(group_hand)


# We get the joint values from the group and change some of the values:
#joint_goal = move_group_hand.get_current_joint_values()

move_group_hand.set_named_target('open')
plan = move_group_hand.go(wait=True)
# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
#move_group.go(joint_goal, wait=True)

# Calling ``stop()`` ensures that there is no residual movement
move_group_hand.stop()
move_group_hand.clear_pose_targets()

rospy.sleep(3)

move_group_hand.set_named_target('close')
plan = move_group_hand.go(wait=True)
# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
#move_group.go(joint_goal, wait=True)

# Calling ``stop()`` ensures that there is no residual movement
move_group_hand.stop()
move_group_hand.clear_pose_targets()