import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from rclpy.qos import QoSProfile, DurabilityPolicy


class DepthMaintainPublisher(Node):
    def __init__(self):
        super().__init__('depth_maintain_publisher')
        qos = QoSProfile(depth=10)
        qos.durability = DurabilityPolicy.VOLATILE
        self.get_logger().info("Initializing Depth Maintain Publisher")
        self.cmd_publisher = self.create_publisher(Twist, '/mavros/setpoint_velocity/cmd_vel_unstamped', 10)
        timer_period = 0.9
        self.depth = 0.0
        self.satisfactory_count = 0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subscriber = self.create_subscription(Float64, '/mavros/global_position/rel_alt', self.depth_callback, 10)
        self.subscriber
    def depth_callback(self,msg):
        self.depth = float(msg.data)
    def timer_callback(self):
        if self.depth > -1.6:
            msg = Twist()
            msg.linear.z = -0.35
            self.cmd_publisher.publish(msg)
            self.get_logger().info(f'Adjusting depth by {msg.linear.z}')
            self.get_logger().info(f'Current depth: {self.depth}')
            self.satisfactory_count = 0
        elif self.depth < -1.85:
            msg = Twist()
            msg.linear.z = 0.35
            self.cmd_publisher.publish(msg)
            self.get_logger().info(f'Adjusting depth by {msg.linear.z}')
            self.get_logger().info(f'Current depth: {self.depth}')
            self.satisfactory_count = 0
        else:
            self.satisfactory_count += 1
            if self.satisfactory_count == 5:
                self.get_logger().info(f'Current depth is satisfactory!')

        
        



def main():
    rclpy.init()
    node = DepthMaintainPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
