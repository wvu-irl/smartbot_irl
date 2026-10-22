from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from smartbot_irl.types import TopicSpec


@dataclass
class BaseType:
    stamp_sec: int = 0
    stamp_nanosec: int = 0

    # # Adjustable thingies:
    # mapping_spec: TopicSpec = TopicSpec()
