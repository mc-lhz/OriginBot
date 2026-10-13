import rclpy,time
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import Bool 
class ViewLidar(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("LiDAR is OK")
        self.laser_sub= self.create_subscription(LaserScan, "/scan", self.laser_callback, rclpy.qos.qos_profile_sensor_data)        
        self.pub = self.create_publisher(Bool, '/has_obs', 10) 
        self.has_obs = Bool()    
        self.pub.publish(self.has_obs) 
    def laser_callback(self, scan_data):           
        self.has_obs.data = False
        #print(len(scan_data.ranges))
        for i in range(int(0.4*len(scan_data.ranges)),int(0.6*len(scan_data.ranges))):            
            if 0.05< scan_data.ranges[i] <0.40:                
                print("ranges["+str(i)+"] = ",scan_data.ranges[i])  
                print('2')
                self.has_obs.data = True  #有障碍物 
                
                
            else:
                  #无障碍物 
                  pass
            if self.has_obs.data == False:
              pass
            
            self.pub.publish(self.has_obs) 









def main(args=None):
    rclpy.init(args=args)        
    lidarview = ViewLidar("View_YDLidar")
    rclpy.spin(lidarview)
    lidarview.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()