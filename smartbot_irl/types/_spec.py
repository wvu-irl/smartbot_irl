from typing import Any


class TopicSpec:
    def __int__(self) -> None:
        self.type: type[Any] | None = None
        self.ros_type: type[Any] | None = None
        self.ros_topic: str | None = None
        self.timeout: float | None = None
        self.pub: bool = False
