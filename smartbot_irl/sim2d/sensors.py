import math
import random
from ..data import SensorData



class SimSensors:
    """
    Generates synthetic sensor readings from the current SimState.
    Produces realistic-enough fields to populate a SensorData object.
    """

    def __init__(self, state: SensorData):
        self.state = state

    # ------------------------------------------------------------------
    def read_all(self) -> SensorData:
        """
        Return a freshly populated SensorData instance based on current state.
        """
        s = self.state
        data = SensorData()

        # Odometry-like pose
        data.pose_x = s.x
        data.pose_y = s.y
        data.pose_theta = s.theta

        # Wheel velocities
        data.wheel_vel_left = s.v_left
        data.wheel_vel_right = s.v_right

        # Arm state
        data.arm = s.arm

        # Simulated laser scan (flat environment with mild noise)
        num_rays = 360
        data.scan = [random.uniform(0.3, 3.0) for _ in range(num_rays)]

        # Simulated ArUco markers — deterministic positions with noise
        data.aruco_marker_poses = [
            {
                "id": i,
                "x": math.cos(s.theta + i) + random.uniform(-0.05, 0.05),
                "y": math.sin(s.theta + i) + random.uniform(-0.05, 0.05),
            }
            for i in range(3)
        ]

        return data
