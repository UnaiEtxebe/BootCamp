"""Discrete-event entities for the can line simulation."""
from __future__ import annotations

import simpy
from simpy.events import Event


class Sink:
    """Collects finished cans."""

    def __init__(self, env: simpy.Environment):
        self.env = env
        self.count = 0

    def put(self, item):
        self.count += 1


class Conveyor:
    """Simple conveyor that delays items based on length and speed."""

    def __init__(self, env: simpy.Environment, length: float, speed: float, downstream):
        self.env = env
        self.length = length
        self.speed = speed
        self.downstream = downstream
        self.store = simpy.Store(env)
        env.process(self.run())

    def put(self, item):
        return self.store.put(item)

    def run(self):
        while True:
            item = yield self.store.get()
            travel_time = self.length / self.speed
            yield self.env.timeout(travel_time)
            res = self.downstream.put(item)
            if isinstance(res, Event):
                yield res


class Machine:
    """Source machine emitting items at a given rate (CPM)."""

    def __init__(self, env: simpy.Environment, cpm: float, downstream):
        self.env = env
        self.cpm = cpm
        self.downstream = downstream
        env.process(self.run())

    def run(self):
        inter = 60.0 / self.cpm
        while True:
            yield self.env.timeout(inter)
            res = self.downstream.put(object())
            if isinstance(res, Event):
                yield res
