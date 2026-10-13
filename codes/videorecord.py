#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rclpy, cv2, cv_bridge
from rclpy.node import Node
from sensor_msgs.msg import  CompressedImage
import time 
import numpy as np
from cv_bridge import CvBridge

W = 1920
H = 1080
class VideoRecord(Node):
    def __init__(self):
        super().__init__('video_recorder')
        self.get_logger().info("Video Recording.")
        self.bridge = CvBridge()        
        self.out = cv2.VideoWriter('/userdata/videos/record_' + str(time.time()) + '.avi', 
            cv2.VideoWriter_fourcc('X','V','I','D'), 5, (W, H))        
        self.image_sub = self.create_subscription(CompressedImage, '/image', self.image_callback, 10) 
        
    def image_callback(self, msg):       
        self.image = CvBridge().compressed_imgmsg_to_cv2(msg)
        self.out.write(self.image)
        
def main(args=None):
    rclpy.init(args=args)    
    videorecord = VideoRecord()
    rclpy.spin(videorecord)
    videorecord.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
