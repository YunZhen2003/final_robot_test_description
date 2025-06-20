#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math


class AvoidFilter:
    def __init__(self):
        rospy.init_node('avoid_filter')

        self.cmd_input = Twist()
        self.obstacle_near = False

        rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.pub = rospy.Publisher('/cmd_vel_filtered', Twist, queue_size=10)

        self.rate = rospy.Rate(10)
        self.run()

    def cmd_callback(self, msg):
        self.cmd_input = msg

    def scan_callback(self, msg):
        # 取得正前方 -15 到 +15 度的範圍
        total_len = len(msg.ranges)
        center = total_len // 2
        window = total_len // 12  # 約 30 度視角
        front_ranges = msg.ranges[center - window: center + window]

        # 過濾掉 inf 和 NaN
        valid_ranges = [r for r in front_ranges if not math.isinf(
            r) and not math.isnan(r)]

        if valid_ranges and min(valid_ranges) < 0.5:
            self.obstacle_near = True
        else:
            self.obstacle_near = False

    def run(self):
        while not rospy.is_shutdown():
            cmd = Twist()

            # 如果要前進，但前面有障礙，就停止
            if self.obstacle_near and self.cmd_input.linear.x > 0:
                cmd.linear.x = 0.0
                cmd.angular.z = self.cmd_input.angular.z  # 保留旋轉
            else:
                cmd = self.cmd_input

            self.pub.publish(cmd)
            self.rate.sleep()


if __name__ == '__main__':
    AvoidFilter()
