import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from ..data import Command, SensorData
from std_msgs.msg import String, Bool
from sensor_msgs.msg import LaserScan, JointState
from geometry_msgs.msg import PoseArray, Twist, TwistStamped
from nav_msgs.msg import Odometry


class SmartbotNode(Node):
    """
    This node acts as the intermediary between the wrapper SmartBot and the ros2 system.
    """

    def __init__(self, smartbot_num) -> None:
        """
        TODO: Add arg to namespace topics. Or use yaml?
        """
        super().__init__(node_name="SmartBotNode")
        # This is kept up to date by subscriber callbacks.
        self.sensor_data = SensorData()

        prefix = f"/smartbot{str(smartbot_num)}"

        self.cmd_vel_publisher_ = self.create_publisher(
            msg_type=Twist, topic=prefix + "/cmd_vel", qos_profile=10
        )
        self.arm_position_control_publisher = self.create_publisher(
            msg_type=Bool, topic=prefix + "/arm_position_control", qos_profile=10
        )

        # Example subscriber to pull in data.
        self.odom_sub = self.create_subscription(
            Odometry, topic=prefix + "/odom", callback=self.odom_cb, qos_profile=10
        )
        self.joint_state_sub = self.create_subscription(
            JointState,
            topic=prefix + "/joint_state",
            callback=self.joint_state_cb,
            qos_profile=10,
        )
        self.scan_sub = self.create_subscription(
            LaserScan, topic=prefix + "/scan", callback=self.scan_cb, qos_profile=10
        )
        self.aruco_poses_sub = self.create_subscription(
            PoseArray,
            topic=prefix + "/aruco_poses",
            callback=self.aruco_poses_cb,
            qos_profile=10,
        )
        print(prefix + "/joint_state")

    def odom_cb(self, msg: Odometry) -> None:
        self.sensor_data.pose_x = msg.pose.pose.position.x
        self.sensor_data.pose_y = msg.pose.pose.position.y
        self.sensor_data.pose_theta = msg.pose.pose.orientation.z

    def joint_state_cb(self, msg: JointState) -> None:
        self.sensor_data.arm = msg.position

    def scan_cb(self, msg: LaserScan) -> None:
        self.sensor_data.scan = msg.ranges

    def aruco_poses_cb(self, msg: PoseArray):
        self.sensor_data.aruco_marker_poses = msg.poses
        ...

    def pubber(self) -> None:
        msg = String()
        msg.data = "Hello World: %d" % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


class SmartBot:
    def __init__(self, smartbot_num=0):
        print("Creating smartbot")
        rclpy.init()
        self.node = SmartbotNode(smartbot_num=smartbot_num)
        print("node created")
        # rclpy.spin_once(self.node)  # Do I need to spin at least once?
        # print("done spinning")

    def init(self):
        print("Initialized!")
        # What goes here?

    def read(self) -> SensorData:
        # Fetch the most recent SensorData from the node.
        return (
            self.node.sensor_data
        )  # Make this owned by SmartBot and sent to SmartBotNode thread?

    def write(self, command: Command):
        print("Moving left motor {command.wheel_left_vel}")
        print("Moving right motor {command.wheel_right_vel}")

    def spin(self):
        """
        Invoked by user every dt. Print warning if not real time enough?
        """
        print("Spinning!")
        rclpy.spin_once(self.node, timeout_sec=0.0)
