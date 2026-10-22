# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...sensor_msgs.msg.image import Image
from ...sensor_msgs.msg.region_of_interest import RegionOfInterest
from ...std_msgs.msg.header import Header


@dataclass(slots=True)
class DisparityImage:
    header: Header = field(default_factory=Header)
    image: Image = field(default_factory=Image)
    f: float = 0.0
    t: float = 0.0
    valid_window: RegionOfInterest = field(default_factory=RegionOfInterest)
    min_disparity: float = 0.0
    max_disparity: float = 0.0
    delta_d: float = 0.0


    __msgtype__: ClassVar[str] = "stereo_msgs/msg/DisparityImage"


__all__ = ["DisparityImage"]