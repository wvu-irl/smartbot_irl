import time


from dataclasses import dataclass, field
import numpy as np
import matplotlib.pyplot as plt
import pygame
import time
import multiprocessing as mp
from queue import Empty
from ._systems import GetInput, DiffDriveKinematics, EncoderSystem, Integrate, Read
from ._utils import robot_components
from smartbot_irl.utils import SmartLogger, check_realtime, logging, get_log_dir, save_data

logger = SmartLogger(level=logging.DEBUG)  # Print statements, but better!


def run_sim(cmd_queue, out_queue, sim_rate=100, publish_rate_hz=10.0):
    from queue import Empty

    world = SmartWorld()
    robot = world.create_entity_with_components(*robot_components())

    world.add_system(GetInput(cmd_queue))
    world.add_system(DiffDriveKinematics())
    world.add_system(EncoderSystem())
    world.add_system(Integrate())
    world.add_system(Read(world, out_queue, publish_rate_hz))

    target_dt = 1 / sim_rate  # Hz

    # Loop forever until killed.
    while True:
        world.step_realtime(target_dt)


class SmartWorld:
    def __init__(self) -> None:
        self.time = 0.0
        self.next_id = 0
        self.components = {}  # comp_type :{ent : comp_instance}
        self.entities = {}  # ent : frozenset(component types)
        self.systems = []

    def add_system(self, sys) -> None:
        self.systems.append(sys)

    def add_component(self, ent, comp) -> None:
        t = type(comp)
        if t not in self.components:
            self.components[t] = {}
        self.components[t][ent] = comp
        self.entities[ent] = self.entities[ent] | {t}

    def step_realtime(self, target_dt):
        real_t0 = time.perf_counter()

        # physics step
        self.step(target_dt)

        elapsed = time.perf_counter() - real_t0
        if elapsed < target_dt:
            time.sleep(target_dt - elapsed)

    def create_entity_with_components(self, *comps) -> int:
        ent = self.next_id
        self.next_id += 1
        self.entities[ent] = frozenset()
        for c in comps:
            self.add_component(ent, c)
        return ent

    # TODO make an archetype/metatype system for speed.
    # TODO use big numpy array to hold components. Make nice accessors.
    def step(self, dt=0.01) -> None:
        self.time += dt
        for sys in self.systems:
            logger.debug('running a system', rate=5)
            required = sys.components
            for ent, signature in self.entities.items():
                if not set(required).issubset(signature):
                    continue
                args = [self.components[t][ent] for t in required]
                sys.update(*args, dt)
