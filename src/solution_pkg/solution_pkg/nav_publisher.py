import rclpy
from time import sleep
from rclpy.node import Node
from geometry_msgs.msg import Twist
from vision_msgs.msg import BoundingBoxArray
from rclpy.qos import QoSProfile, DurabilityPolicy


class NavPublisher(Node):
    def __init__(self):
        super().__init__('nav_publisher')
        qos = QoSProfile(depth=10)
        qos.durability = DurabilityPolicy.VOLATILE
        self.get_logger().info("Initializing Nav & Obstacle Avoidance")
        self.cmd_publisher = self.create_publisher(Twist, '/mavros/setpoint_velocity/cmd_vel_unstamped', 10)
        timer_period = 0.5
        self.index = 10000000000
        self.no_gate_counter = 0
        self.no_gate_once = 0
        self.throttlecounter_09 = 0
        self.throttlecounter_06 = 0
        self.boxes = []
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subscriber = self.create_subscription(BoundingBoxArray, '/main_camera/detection/bounding_boxes', self.BB_callback, 10)
        self.subscriber
    def BB_callback(self,msg):
        self.boxes = msg.bounding_boxes
        if self.boxes == []:
            self.no_gate_once = 1
        else:   
            for i, box in enumerate(self.boxes):
                if box.label_name not in ["gate", "red_flare"]:
                    continue
                elif box.label_name == "gate":   #Counts no. of times gate is not seen, to prevent misjudgment
                    self.index = i
                    self.no_gate_counter = 0
                    self.no_gate_once = 0
                else: 
                    self.no_gate_once = 1 
        if self.no_gate_once == 1:
            self.no_gate_counter += 1
            self.no_gate_once = 0
            self.index = 1000000000


    def timer_callback(self):
        if self.no_gate_counter > 10:
            self.throttlecounter_09 = 0
            self.throttlecounter_06 = 0
            self.get_logger().info("Gate not found, rotating to find Gate")
            msg = Twist()
            msg.angular.z = 0.85
            self.cmd_publisher.publish(msg)
        else:
            if (len(self.boxes)-1) < self.index:
                return
            else:
                msg = Twist()       
                if self.boxes[self.index].x > 0.54:     #Rotates ROV when gate is not centered in x-axis
                    self.throttlecounter_09 = 0
                    self.throttlecounter_06 = 0
                    msg = Twist()
                    msg.angular.z = -0.2
                    self.cmd_publisher.publish(msg)
                    self.get_logger().info("Adjusting Angle")
                elif self.boxes[self.index].x < 0.46:
                    self.throttlecounter_09 = 0
                    self.throttlecounter_06 = 0
                    msg = Twist()
                    msg.angular.z = 0.2
                    self.cmd_publisher.publish(msg)
                    self.get_logger().info("Adjusting Angle")
                else:
                    ratio = self.boxes[self.index].w/self.boxes[self.index].h
                    if self.boxes[self.index].h < 0.4:
                        self.throttlecounter_09 = 0
                        self.throttlecounter_06 = 0
                        msg = Twist()
                        msg.linear.x = 2.0
                        self.cmd_publisher.publish(msg)
                        self.get_logger().info("Approaching Gate")
                    elif self.boxes[self.index].h < 0.75:
                        self.throttlecounter_09 = 0
                        self.throttlecounter_06 = 0
                        msg = Twist()
                        msg.linear.x = 1.0
                        self.cmd_publisher.publish(msg)
                    elif self.boxes[self.index].h > 0.9 and self.boxes[self.index].w > 0.45:
                        if self.throttlecounter_09 < 1:
                            self.throttlecounter_09 += 1
                        elif self.throttlecounter_09 >= 1:
                            self.throttlecounter_09 = 0
                            msg = Twist()
                            msg.linear.x = 1.4
                            self.cmd_publisher.publish(msg)
                            sleep(1.0)
                            self.cmd_publisher.publish(msg)
                            sleep(1.0)
                            self.cmd_publisher.publish(msg)
                            sleep(1.0)
                            self.cmd_publisher.publish(msg)
                            self.get_logger().info("Gate centered, going full throttle!")

                    elif self.boxes[self.index].h > 0.75 and self.boxes[self.index].w > 0.32:
                        if self.throttlecounter_06 < 1:
                            self.throttlecounter_06 += 1
                        elif self.throttlecounter_06 >= 1:
                            self.throttlecounter_06 = 0
                            msg = Twist()
                            msg.linear.x = 1.4
                            self.cmd_publisher.publish(msg)
                            sleep(1.0)
                            self.cmd_publisher.publish(msg)
                            sleep(1.0)
                            self.cmd_publisher.publish(msg)
                            sleep(1.0)
                            self.cmd_publisher.publish(msg)
                            self.get_logger().info("Gate centered, going full throttle!")
                    elif ratio < 0.4267:
                        self.throttlecounter_09 = 0
                        self.throttlecounter_06 = 0
                        msg = Twist()
                        msg.linear.y = -1.4
                        self.cmd_publisher.publish(msg)
                        sleep(0.7)
                        self.cmd_publisher.publish(msg)
                        sleep(0.7)
                        self.cmd_publisher.publish(msg)
                        sleep(0.5)
                        self.cmd_publisher.publish(msg)
                        self.get_logger().info("Weird angle detected! Distancing to get a better approach!")


                
        
        



def main():
    rclpy.init()
    node = NavPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
