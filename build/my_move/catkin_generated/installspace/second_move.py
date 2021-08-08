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
rospy.init_node('second_move', anonymous=True)

robot = moveit_commander.RobotCommander()

scene = moveit_commander.PlanningSceneInterface()

group_name = "manipulator"
move_group = moveit_commander.MoveGroupCommander(group_name)

# We can get the name of the reference frame for this robot:
planning_frame = move_group.get_planning_frame()
print("============ Planning frame: %s" % planning_frame)

# We can also print the name of the end-effector link for this group:
eef_link = move_group.get_end_effector_link()
print("============ End effector link: %s" % eef_link)

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print("============ Available Planning Groups:", robot.get_group_names())

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print("============ Printing robot state")
print(robot.get_current_state())
print("")

joint_goal = move_group.get_current_joint_values()
joint_goal[0] = -tau/10
joint_goal[1] = -tau/10
joint_goal[2] = 0
joint_goal[3] = 0
joint_goal[4] = 0
joint_goal[5] = 0 

# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
move_group.go(joint_goal, wait=True)

# Calling ``stop()`` ensures that there is no residual movement
move_group.stop()

box_pose = geometry_msgs.msg.PoseStamped()
box_pose.header.frame_id = "base"
box_pose.pose.orientation.w = 1.0
box_pose.pose.position.z = 0 # above the panda_hand frame
box_name = "box"
scene.add_box(box_name, box_pose, size=(2, 2, 0.01))

# We get the joint values from the group and change some of the values:
joint_goal = move_group.get_current_joint_values()
joint_goal[0] = 0
joint_goal[1] = -tau/8
joint_goal[2] = 0
joint_goal[3] = -tau/4
joint_goal[4] = 0
joint_goal[5] = tau/6  # 1/6 of a turn

# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
move_group.go(joint_goal, wait=True)

# Calling ``stop()`` ensures that there is no residual movement
move_group.stop()
 
#move to Endefektor position
pose_goal = geometry_msgs.msg.Pose()
pose_goal.orientation.w = 1.0
pose_goal.position.x = 0.4
pose_goal.position.y = 0.1
pose_goal.position.z = 0.4

move_group.set_pose_target(pose_goal)

plan = move_group.go(wait=True)
# Calling `stop()` ensures that there is no residual movement
move_group.stop()
move_group.clear_pose_targets()

# We get the joint values from the group and change some of the values:
joint_goal = move_group.get_current_joint_values()
joint_goal[0] = 0
joint_goal[1] = -tau/6
joint_goal[2] = -tau/2
joint_goal[3] = -tau/4
joint_goal[4] = 0
joint_goal[5] = tau/6  # 1/6 of a turn

# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group
move_group.go(joint_goal, wait=True)

# Calling ``stop()`` ensures that there is no residual movement
move_group.stop()