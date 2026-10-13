#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data

class ViewLidar(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("LiDAR is OK")
        self.laser_sub= self.create_subscription(LaserScan, "/scan", self.laser_callback, rclpy.qos.qos_profile_sensor_data)        
    
    def laser_callback(self, scan_data):           
        for i in range (0, len(scan_data.ranges)):
            if 0.12 < scan_data.ranges[i] <0.3:
                print("ranges["+str(i)+"] = ",scan_data.ranges[i])  

def main(args=None):
    rclpy.init(args=args)        
    lidarview = ViewLidar("View_YDLidar")
    rclpy.spin(lidarview)
    lidarview.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()