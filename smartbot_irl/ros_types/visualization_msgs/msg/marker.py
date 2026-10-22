# Generated file. Do not edit.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar


from ...builtin_interfaces.msg.duration import Duration
from ...geometry_msgs.msg.point import Point
from ...geometry_msgs.msg.pose import Pose
from ...geometry_msgs.msg.vector3 import Vector3
from ...sensor_msgs.msg.compressed_image import CompressedImage
from ...std_msgs.msg.color_rgba import ColorRGBA
from ...std_msgs.msg.header import Header
from .mesh_file import MeshFile
from .uv_coordinate import UVCoordinate


@dataclass(slots=True)
class Marker:
    header: Header = field(default_factory=Header)
    ns: str = ""
    id: int = 0
    type: int = 0
    action: int = 0
    pose: Pose = field(default_factory=Pose)
    scale: Vector3 = field(default_factory=Vector3)
    color: ColorRGBA = field(default_factory=ColorRGBA)
    lifetime: Duration = field(default_factory=Duration)
    frame_locked: bool = False
    points: list[Point] = field(default_factory=list)
    colors: list[ColorRGBA] = field(default_factory=list)
    texture_resource: str = ""
    texture: CompressedImage = field(default_factory=CompressedImage)
    uv_coordinates: list[UVCoordinate] = field(default_factory=list)
    text: str = ""
    mesh_resource: str = ""
    mesh_file: MeshFile = field(default_factory=MeshFile)
    mesh_use_embedded_materials: bool = False

    ARROW: ClassVar[int] = 0
    CUBE: ClassVar[int] = 1
    SPHERE: ClassVar[int] = 2
    CYLINDER: ClassVar[int] = 3
    LINE_STRIP: ClassVar[int] = 4
    LINE_LIST: ClassVar[int] = 5
    CUBE_LIST: ClassVar[int] = 6
    SPHERE_LIST: ClassVar[int] = 7
    POINTS: ClassVar[int] = 8
    TEXT_VIEW_FACING: ClassVar[int] = 9
    MESH_RESOURCE: ClassVar[int] = 10
    TRIANGLE_LIST: ClassVar[int] = 11
    ARROW_STRIP: ClassVar[int] = 12
    ADD: ClassVar[int] = 0
    MODIFY: ClassVar[int] = 0
    DELETE: ClassVar[int] = 2
    DELETEALL: ClassVar[int] = 3

    __msgtype__: ClassVar[str] = "visualization_msgs/msg/Marker"


__all__ = ["Marker"]