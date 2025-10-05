import rclpy
from rclpy.node import Node
from mavros_msgs.srv import SetMode
fail_count = 0

class SetModeClient(Node):
    def __init__(self):
        super().__init__('set_mode_client')
        self.client = self.create_client(SetMode,'/mavros/set_mode')
        self.get_logger().info("Initializing Guiding Mode...")
        while not self.client.wait_for_service(timeout_sec=0.8):
            self.get_logger().info("Awaiting Service Availability...")
        self.request = SetMode.Request()
        self.request.custom_mode = "GUIDED"
        self.future = self.client.call_async(self.request)
        self.get_logger().info("Service Call Sent...")
def main():
    rclpy.init()
    node = SetModeClient()
    while rclpy.ok():
        rclpy.spin_once(node)
        if node.future.done():
            try:
                response = node.future.result()
                node.get_logger().info("Mode successfully changed to GUIDED, completing initialization...")
                break
            except:
                node.get_logger().error("Service call error!")
        else:
            fail_count += 1
            self.get_logger().info(f'No response yet ({fail_count})')
            if fail_count >= 6:
                self.get_logger().info("Response took too long, initialization FAILED")
                self.get_logger().info("Please relaunch and try again")
                self.get_logger().info("exiting...")
                break
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

            
            
    


