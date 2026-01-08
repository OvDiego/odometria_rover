import rclpy
import math
from rclpy.node import Node
from Rosmaster_Lib import Rosmaster

class MobileBaseNode(Node):
    def __init__(self):
        super().__init__('mobile_base')

        self.bot = Rosmaster('/dev/ttyUSB0')
        self.bot.create_receive_threading()

        self.dist = [0.0, 0.0, 0.0, 0.0]
        self.diameter = 0.107
        self.ppr = 3600
        self.perimeter = self.diameter * math.pi

        self.timer = self.create_timer(0.05, self.encoder_timer_callback)

        self.get_logger().info("Leyendo encoders")

    def encoder_timer_callback(self):
        enc = self.bot.get_motor_encoder()

        if enc is None:
            return

        for i in range(4):
            self.dist[i] = -enc[i] * (self.perimeter / self.ppr)

        self.get_logger().info(f"Encoders [m]: {self.dist}")

def main(args=None):
    rclpy.init(args=args)
    node = MobileBaseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


"""
INSTRUCCIONES
ros2 run mobile_base mobile_base.py
SALIDA: Encoders [m]: [0.000, 0.000, 0.000, 0.000]
"""