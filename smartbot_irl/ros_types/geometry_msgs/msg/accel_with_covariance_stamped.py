# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from .accel_with_covariance import AccelWithCovariance
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class AccelWithCovarianceStamped:
    header: Header = field(default_factory=Header)
    accel: AccelWithCovariance = field(default_factory=AccelWithCovariance)


    __msgtype__: ClassVar[str] = "geometry_msgs/msg/AccelWithCovarianceStamped"


__all__ = ["AccelWithCovarianceStamped"]