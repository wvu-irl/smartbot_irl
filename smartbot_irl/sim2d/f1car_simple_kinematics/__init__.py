"""Nicely export the set of components and systems associated with an f1car.

Lets have one package per entity model. Then we can just
```
from sim2d.f1car_simple_kinematics import components, systems
```

which are lists of type sim2d.Component and sim2d.System we can then register with the simulator.

Then we can use car1_id = SmartWorld.create_entity_with_components(components) as many times as we want
and just once register the systems from the package with
```
SmartWorld.add_system(systems)
```
Need to figure out how to send the queue and desired udpate rate to the special read and write systems. Maybe make
this a generic system? But the input/output is specific to the entity.
"""
