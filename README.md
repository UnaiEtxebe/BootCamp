# PyChrono 9.0 Beverage Can Conveyor Line Simulation

Physics-based simulation of a beverage can production line conveyor system using PyChrono 9.0 with Vulkan rendering.

## Overview

This project provides a complete, production-ready simulation of a beverage can conveyor line with:

- Physics-accurate mat conveyor belt
- Empty beverage cans (open cylinders, no ends)
- Motor-driven sprocket system
- Automatic CPM (Cans Per Minute) calculations
- Maximum capacity estimation
- Vulkan high-performance rendering

## Quick Start

```bash
# Install dependencies
pip install pychrono[vulkan] numpy

# Run simulation
python can_conveyor_simulation.py

# Try examples
python examples.py
```

## Features

- **Complete Physics Simulation**: Rigid body dynamics with contact and friction
- **Automatic Calculations**: CPM, conveyor speed, motor parameters, maximum capacity
- **Flexible Configuration**: Easy parameter adjustment for different can sizes and speeds
- **High Performance**: Vulkan rendering with Irrlicht fallback
- **Production Ready**: Realistic industrial conveyor modeling

## Key Calculations

### Cans Per Minute (CPM)
```
CPM = Conveyor Speed (m/min) / (Can Diameter + Can Spacing)
```

Example: 15 m/min speed, 66mm can, 20mm spacing = **174 CPM**

### Maximum Capacity
```
Max Cans = Floor(Length / Can Pitch) × Floor(Width / Can Pitch)
```

Example: 5m × 0.8m conveyor, 86mm pitch = **522 cans**

## Documentation

- **[CONVEYOR_README.md](CONVEYOR_README.md)** - Complete documentation
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick formulas and examples
- **[examples.py](examples.py)** - Usage examples and configurations
- **[conveyor_config.py](conveyor_config.py)** - Configuration parameters

## Files

| File | Description |
|------|-------------|
| `can_conveyor_simulation.py` | Main simulation engine |
| `conveyor_config.py` | Configuration parameters |
| `examples.py` | Example configurations |
| `requirements.txt` | Python dependencies |
| `CONVEYOR_README.md` | Full documentation |
| `QUICK_REFERENCE.md` | Quick reference guide |

## Example Output

```
==============================================================
CONVEYOR SYSTEM PARAMETERS
==============================================================
Conveyor Length: 5.0 m
Conveyor Width: 0.8 m
Conveyor Speed: 15.0 m/min (0.250 m/s)

Can Diameter: 66.0 mm
Can Height: 115.0 mm
Can Spacing: 20.0 mm
Can Pitch: 86.0 mm

CPM (Cans Per Minute): 174.4 cans/min
Maximum Cans (Length): 58 cans
Maximum Cans (Width): 9 cans
Maximum Total Cans: 522 cans

Motor RPM (calculated): 23.9 RPM
Sprocket Radius: 10.0 cm
==============================================================
```

## Requirements

- Python 3.8+
- PyChrono 9.0+
- NumPy
- Vulkan-capable GPU (recommended) or Irrlicht support

## License

Educational and industrial simulation purposes.

## Author

Generated with Claude Code - 2025-10-20
