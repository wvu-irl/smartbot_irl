def make_arena(
    width: float = 5.0, height: float = 5.0, thickness: float = 1.0
) -> list[list[float]]:
    """Make a set of point lists creating an empty box of obstacles.

    Returns
    -------
    _type_
        _description_
    """
    obstacles = [
        [-width - thickness, -height - thickness, -width, height],  # left wall
        [-width - thickness, -height - thickness, width, -height],  # bottom wall
        [width + thickness, -height - thickness, width, height],  # right wall
        [-width - thickness, height + thickness, width, height],  # top wall
    ]
    return obstacles
