# PyChrono 9.0 Beverage Can Conveyor Line Simulation

A physics-based simulation of a beverage can production line conveyor system using PyChrono 9.0 with Vulkan rendering support.

## Overview

This simulation models a complete can conveyor line system with:

- **Mat Conveyor Belt**: Continuous belt driven by motor and sprocket
- **Empty Beverage Cans**: Realistic can models (open cylinders without ends)
- **Motor Drive System**: Sprocket-driven conveyor with adjustable speed
- **Performance Metrics**: Automatic calculation of CPM (Cans Per Minute) and throughput
- **Vulkan Rendering**: High-performance visualization using Vulkan (with Irrlicht fallback)

## Features

### Physics Simulation
- Accurate rigid body dynamics
- Contact and friction modeling
- Belt-driven motion with motor control
- Realistic can-to-can and can-to-belt interactions

### Performance Calculations
The system automatically calculates:

- **CPM (Cans Per Minute)**: Based on conveyor speed and can spacing
- **Maximum Can Capacity**: Total cans that fit on the conveyor
- **Conveyor Speed**: Configurable in m/min and m/s
- **Motor Parameters**: RPM and angular velocity matching conveyor speed

### Visualization
- Vulkan rendering for high performance (primary)
- Irrlicht rendering (automatic fallback)
- Real-time 3D visualization
- Adjustable camera views
- Material properties (metallic cans, textured belt)

## Installation

### Prerequisites

- Python 3.8 or higher
- PyChrono 9.0 or later
- Vulkan-capable GPU (recommended) or Irrlicht support

### Install Dependencies

```bash
# Full installation with Vulkan support
pip install pychrono[vulkan] numpy matplotlib pandas

# Or basic installation with Irrlicht
pip install pychrono[irrlicht] numpy

# Or use requirements file
pip install -r requirements.txt
```

### Platform-Specific Setup

**Linux:**
```bash
sudo apt-get install vulkan-tools libvulkan-dev
pip install pychrono[vulkan]
```

**Windows:**
- Ensure latest graphics drivers are installed
- Install PyChrono with Vulkan support

**macOS:**
```bash
brew install vulkan-headers vulkan-loader molten-vk
pip install pychrono[vulkan]
```

## Usage

### Quick Start

Run the simulation with default parameters:

```bash
python can_conveyor_simulation.py
```

### Custom Configuration

Edit `conveyor_config.py` to customize:

```python
# Conveyor dimensions
CONVEYOR_LENGTH = 5.0      # meters
CONVEYOR_WIDTH = 0.8       # meters
CONVEYOR_SPEED = 15.0      # m/min

# Can specifications
CAN_DIAMETER = 0.066       # meters (66mm)
CAN_HEIGHT = 0.115         # meters (115mm)
CAN_SPACING = 0.02         # meters (20mm)

# Motor parameters
SPROCKET_RADIUS = 0.1      # meters
MOTOR_RPM = 60.0           # RPM
```

### Running with Custom Parameters

```python
from can_conveyor_simulation import CanConveyorSystem

# Create custom conveyor
conveyor = CanConveyorSystem(
    conveyor_length=10.0,      # 10 meter long conveyor
    conveyor_width=1.0,        # 1 meter wide
    conveyor_speed=25.0,       # 25 m/min (fast)
    can_diameter=0.066,        # Standard 330ml can
    can_height=0.115,
    can_spacing=0.015,         # Tighter spacing
    sprocket_radius=0.15,      # Larger sprocket
    motor_rpm=80.0
)

conveyor.setup_simulation()
conveyor.run_simulation(time_duration=60.0)
```

## System Parameters

### Conveyor Specifications

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| Length | 5.0 m | Conveyor belt length |
| Width | 0.8 m | Conveyor belt width |
| Speed | 15.0 m/min | Belt velocity |
| Thickness | 0.01 m | Belt material thickness |

### Can Specifications (Standard 330ml)

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| Diameter | 66 mm | Can outer diameter |
| Height | 115 mm | Can height |
| Mass | 15 g | Empty can weight |
| Wall Thickness | 0.1 mm | Aluminum wall |
| Spacing | 20 mm | Gap between cans |

### Drive System

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| Sprocket Radius | 0.1 m | Drive wheel radius |
| Motor RPM | 60 RPM | Motor rotation speed |
| Motor Torque | 50 Nm | Drive torque |

## Performance Calculations

The simulation automatically calculates key performance metrics:

### Cans Per Minute (CPM)

```
CPM = Conveyor Speed (m/min) / Can Pitch (m)
Can Pitch = Can Diameter + Can Spacing
```

**Example:**
- Conveyor Speed: 15 m/min
- Can Diameter: 66 mm
- Can Spacing: 20 mm
- Can Pitch: 86 mm = 0.086 m
- **CPM = 15 / 0.086 = 174.4 cans/min**

### Maximum Capacity

```
Max Cans (Length) = Floor(Conveyor Length / Can Pitch)
Max Cans (Width) = Floor(Conveyor Width / Can Pitch)
Total Max Cans = Max Cans (Length) × Max Cans (Width)
```

**Example:**
- Conveyor: 5.0 m × 0.8 m
- Can Pitch: 0.086 m
- Length: Floor(5.0 / 0.086) = 58 cans
- Width: Floor(0.8 / 0.086) = 9 cans
- **Total: 58 × 9 = 522 cans**

### Motor Speed Calculation

```
Angular Velocity (ω) = Linear Velocity / Sprocket Radius
Motor RPM = (ω × 60) / (2π)
```

## File Structure

```
BootCamp/
├── can_conveyor_simulation.py    # Main simulation script
├── conveyor_config.py             # Configuration parameters
├── requirements.txt               # Python dependencies
├── CONVEYOR_README.md            # This file
└── README.md                      # Project readme
```

## Simulation Controls

During simulation:
- **Q**: Quit simulation
- **SPACE**: Pause/Resume
- **Mouse**: Rotate camera view
- **Mouse Wheel**: Zoom in/out

## Output Information

The simulation displays:

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
Can Pitch (diameter + spacing): 86.0 mm

CPM (Cans Per Minute): 174.4 cans/min
Maximum Cans (Length): 58 cans
Maximum Cans (Width): 9 cans
Maximum Total Cans: 522 cans

Motor RPM (calculated): 23.9 RPM
Sprocket Radius: 10.0 cm
==============================================================
```

## Can Size Presets

The `conveyor_config.py` includes common can sizes:

### Standard 330ml Can (Default)
- Diameter: 66 mm
- Height: 115 mm

### Slim 250ml Can
- Diameter: 53 mm
- Height: 146 mm

### Tall 500ml Can
- Diameter: 66 mm
- Height: 168 mm

### Large 568ml (Pint) Can
- Diameter: 73 mm
- Height: 161 mm

## Conveyor Speed Presets

Predefined speed settings in `conveyor_config.py`:

- **Slow**: 10 m/min
- **Medium**: 15 m/min (default)
- **Fast**: 25 m/min
- **Very Fast**: 40 m/min

## Physics Parameters

### Contact Materials

| Material | Friction | Restitution |
|----------|----------|-------------|
| Belt | 0.6 | 0.1 |
| Can | 0.4 | 0.2 |

### Solver Settings

- Solver Type: Barzilai-Borwein
- Max Iterations: 50
- Tolerance: 1e-4
- Time Step: 0.01 s (10 ms)

## Troubleshooting

### Vulkan Not Available

If Vulkan is not available, the simulation automatically falls back to Irrlicht:

```
Warning: Vulkan module not available, falling back to Irrlicht
Initializing Irrlicht visualization...
```

**Solutions:**
1. Install Vulkan drivers for your GPU
2. Install PyChrono with Vulkan support: `pip install pychrono[vulkan]`
3. Use Irrlicht instead (automatic fallback)

### ImportError: No module named 'pychrono'

```bash
pip install pychrono[vulkan]
# or
pip install pychrono[irrlicht]
```

### Slow Performance

1. Reduce number of initial cans in `conveyor_config.py`:
   ```python
   INITIAL_CANS = 10  # Instead of 20
   ```

2. Increase time step (less accurate but faster):
   ```python
   TIME_STEP = 0.02  # 20ms instead of 10ms
   ```

3. Reduce solver iterations:
   ```python
   SOLVER_MAX_ITERATIONS = 30  # Instead of 50
   ```

## Advanced Usage

### Adding Can Spawning

To continuously spawn cans during simulation, add a spawner:

```python
def spawn_can_periodically(self, time, interval=0.5):
    """Spawn a new can every interval seconds."""
    if time % interval < self.time_step:
        position = [-self.conveyor_length/2 + 0.2, 0.3, 0]
        self.create_empty_can(position)
```

### Recording Data

To record can positions and velocities:

```python
def record_can_data(self):
    """Record can positions and velocities."""
    data = []
    for i, can in enumerate(self.cans):
        pos = can.GetPos()
        vel = can.GetPosDt()
        data.append({
            'can_id': i,
            'x': pos.x, 'y': pos.y, 'z': pos.z,
            'vx': vel.x, 'vy': vel.y, 'vz': vel.z
        })
    return data
```

### Export Metrics

```python
def export_metrics(self, filename='conveyor_metrics.txt'):
    """Export system metrics to file."""
    with open(filename, 'w') as f:
        f.write(f"CPM: {self.cpm}\n")
        f.write(f"Max Cans: {self.max_total_cans}\n")
        f.write(f"Conveyor Speed: {self.conveyor_speed} m/min\n")
```

## Technical Details

### Empty Can Modeling

Cans are modeled as hollow cylinders (open at both ends):
- Cylindrical collision shape
- Mass distributed as thin-walled cylinder
- No end caps (representing cans before seaming)

### Belt Motion

The conveyor belt uses a linear motor with:
- Constant velocity control
- Friction-based can transport
- Realistic belt-to-can contact

### Sprocket System

The sprocket provides:
- Visual representation of drive mechanism
- Rotational motion synchronized with belt speed
- Configurable radius affecting gear ratio

## References

- [PyChrono Documentation](https://projectchrono.org/pychrono/)
- [Vulkan Specification](https://www.khronos.org/vulkan/)
- Beverage can specifications: Standard aluminum beverage can dimensions

## License

This simulation code is provided as-is for educational and industrial simulation purposes.

## Author

Generated with Claude Code
Date: 2025-10-20

## Support

For issues with:
- **PyChrono**: Visit [ProjectChrono.org](https://projectchrono.org)
- **This simulation**: Check configuration parameters and troubleshooting section
- **Vulkan**: Ensure GPU drivers are up to date

---

**Happy Simulating!**
