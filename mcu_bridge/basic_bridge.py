import rclpy
from rclpy.node import Node

import serial
import struct
from geometry_msgs.msg import Twist, Vector3

mcu = serial.Serial('/dev/ttyMCU', 9600)


class BasicBridge(Node):

    def __init__(self):
        super().__init__('basic_bridge')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        ang_z = msg.angular.z
        lin_x = msg.linear.x
        
        mcu.write(struct.pack('>f', ang_z))
        mcu.write(struct.pack('>f', lin_x))
        


def main(args=None):
    rclpy.init(args=args)

    basic_bridge = BasicBridge()

    rclpy.spin(basic_bridge)
    
    mcu.close()

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    basic_bridge.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
