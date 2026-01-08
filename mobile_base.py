import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from Rosmaster_Lib import Rosmaster

class MobileBaseNode(Node):
    def __init__(self):
        super().__init__('mobile_base')

        self.bot = Rosmaster('/dev/ttyUSB0')
        self.bot.create_receive_threading()

        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.linear = 0.0
        self.angular = 0.0
        self.max_pwm = 60

        self.get_logger().info("Mobile base lista. Esperando /cmd_vel")

    def cmd_vel_callback(self, msg):
        self.linear = msg.linear.x
        self.angular = msg.angular.z
        self.drive()

    def drive(self):
        pwm_linear = int(self.linear * self.max_pwm)
        pwm_angular = int(self.angular * self.max_pwm)

        left = pwm_linear - pwm_angular
        right = pwm_linear + pwm_angular

        left = max(min(left, 100), -100)
        right = max(min(right, 100), -100)

        self.bot.set_motor(left, left, right, right)

        self.get_logger().info(
            f"L:{left} R:{right} v={self.linear:.2f} w={self.angular:.2f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = MobileBaseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()