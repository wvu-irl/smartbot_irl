from abc import ABC, abstractmethod
from typing import Any, Self


class BaseType(ABC):
    """Base class for custom Python types that support ROS conversion."""

    @classmethod
    @abstractmethod
    def from_ros(cls, msg: Any) -> Self:
        """Construct an instance from a ROS message."""
        ...

    @abstractmethod
    def to_ros(self) -> Any:
        """Convert this instance to its ROS representation."""
        ...
