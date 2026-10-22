# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .twist_with_covariance import TwistWithCovariance
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class VelocityWithCovarianceStamped:
    header: Header = field(default_factory=Header)
    body_frame_id: str = ""
    reference_frame_id: str = ""
    velocity: TwistWithCovariance = field(default_factory=TwistWithCovariance)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/VelocityWithCovarianceStamped"


__all__ = ["VelocityWithCovarianceStamped"]