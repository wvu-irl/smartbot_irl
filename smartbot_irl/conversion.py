from __future__ import annotations

import base64
from collections.abc import Mapping
from dataclasses import MISSING, Field, fields, is_dataclass
from functools import cache
from typing import Any, TypeVar, get_args, get_origin, get_type_hints

import numpy as np

T = TypeVar('T')


@cache
def _type_hints(cls: type) -> dict[str, Any]:
    return get_type_hints(cls)


def _default_value(field: Field) -> Any:
    if field.default_factory is not MISSING:
        return field.default_factory()

    if field.default is not MISSING:
        return field.default

    return None


def _convert_value(
    annotation: Any,
    default: Any,
    value: Any,
) -> Any:
    """Convert to the data type"""
    # Nested generated ROS message.
    if is_dataclass(default):
        if not isinstance(value, Mapping):
            raise TypeError(
                f'Expected mapping for {type(default).__name__}, got {type(value).__name__}'
            )

        return from_dict(type(default), value)

    # Numeric ROS array/sequence.
    if isinstance(default, np.ndarray):
        if isinstance(value, str) and default.dtype == np.uint8:
            result = np.frombuffer(base64.b64decode(value), dtype=np.uint8)
        else:
            result = np.asarray(value, dtype=default.dtype)

        # Nonempty defaults represent fixed-size arrays.
        if default.size and result.shape != default.shape:
            raise ValueError(f'Expected array shape {default.shape}, got {result.shape}')

        return result

    # For any list-like object.
    if get_origin(annotation) is list:
        # Figure out the contained element type from first element.
        element_type = get_args(annotation)[0]

        # Sequence of nested ROS messages.
        if isinstance(element_type, type) and is_dataclass(element_type):
            return [from_dict(element_type, item) for item in value]

        return list(value)

    return value


def from_dict(
    cls: type[T],
    data: Mapping[str, Any],
) -> T:
    """Map a dict (from roslibp sub) into a class with correspondingly named attributes."""
    class_fields = {field.name: field for field in fields(cls)}

    unknown = data.keys() - class_fields.keys()

    if unknown:
        raise ValueError(f'Unknown fields for {cls.__name__}: {sorted(unknown)}')

    hints = _type_hints(cls)
    values = {}

    for name, value in data.items():
        field = class_fields[name]

        values[name] = _convert_value(
            hints[name],
            _default_value(field),
            value,
        )

    return cls(**values)
