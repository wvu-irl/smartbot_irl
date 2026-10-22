# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .pose_with_covariance import PoseWithCovariance
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class PoseWithCovarianceStamped:
    header: Header = field(default_factory=Header)
    pose: PoseWithCovariance = field(default_factory=PoseWithCovariance)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/PoseWithCovarianceStamped"


__all__ = ["PoseWithCovarianceStamped"]