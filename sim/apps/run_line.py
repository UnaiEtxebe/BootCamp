"""CLI entry point to run a simple line scenario."""
from __future__ import annotations

import argparse
import yaml
import simpy

from sim.core.line_des import Machine, Conveyor, Sink


def run_line(config: dict) -> dict:
    env = simpy.Environment()
    sink = Sink(env)
    conv_cfg = config["conveyor"]
    conveyor = Conveyor(env, conv_cfg["length"], conv_cfg["speed"], sink)
    mach_cfg = config["machine"]
    Machine(env, mach_cfg["cpm"], conveyor)
    env.run(until=config.get("duration", 1.0))
    return {"cans": sink.count}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    args = parser.parse_args()
    with open(args.scenario) as fh:
        config = yaml.safe_load(fh)
    result = run_line(config)
    print(result)


if __name__ == "__main__":
    main()
