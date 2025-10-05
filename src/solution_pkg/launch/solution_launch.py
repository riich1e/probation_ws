from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    node1 = Node(
        package='solution_pkg',
        executable='set_mode_client',
        name='set_mode_client'
    )

    node2 = Node(
        package='solution_pkg',
        executable='depth_maintain_publisher',
        name='depth_maintain_publisher'
    )

    node3 = Node(
        package='solution_pkg',
        executable='nav_publisher',
        name='nav_publisher'
    )

    # Wrap node3 in a TimerAction to delay launch by 10 seconds
    delayed_node3 = TimerAction(
        period=10.0,
        actions=[node3]
    )

    return LaunchDescription([
        node1,
        node2,
        delayed_node3,
    ])
