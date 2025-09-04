import sys
sys.path.append('.')

import sim.apps.run_line as rl


def test_run_line_produces_cans():
    config = {
        'duration': 2.0,
        'machine': {'cpm': 120},
        'conveyor': {'length': 0.5, 'speed': 1.0},
    }
    result = rl.run_line(config)
    assert result['cans'] > 0
