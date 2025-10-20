# Quick Reference Guide - Can Conveyor Simulation

## Quick Start

```bash
# Install dependencies
pip install pychrono[vulkan] numpy

# Run default simulation
python can_conveyor_simulation.py

# Run examples
python examples.py
```

## Key Formulas

### Cans Per Minute (CPM)
```
CPM = Conveyor Speed (m/min) / (Can Diameter + Can Spacing)
```

### Maximum Can Capacity
```
Max Cans = Floor(Length / Can Pitch) × Floor(Width / Can Pitch)
```

### Motor RPM from Belt Speed
```
Motor RPM = (Belt Speed / Sprocket Circumference) × 60
          = (Belt Speed / (2π × Sprocket Radius)) × 60
```

### Conveyor Speed from Target CPM
```
Required Speed (m/min) = Target CPM × (Can Diameter + Can Spacing)
```

## Common Can Sizes

| Type | Diameter | Height | Volume |
|------|----------|--------|--------|
| Slim | 53 mm | 146 mm | 250 ml |
| Standard | 66 mm | 115 mm | 330 ml |
| Tall | 66 mm | 168 mm | 500 ml |
| Pint | 73 mm | 161 mm | 568 ml |

## Typical Conveyor Speeds

| Speed Class | m/min | m/s | Application |
|-------------|-------|-----|-------------|
| Slow | 10 | 0.167 | Heavy/unstable loads |
| Medium | 15 | 0.250 | Standard production |
| Fast | 25 | 0.417 | High throughput |
| Very Fast | 40 | 0.667 | Maximum speed lines |

## Performance Examples

### Standard Setup (5m × 0.8m @ 15 m/min)
- Can: 66mm diameter, 115mm height
- Spacing: 20mm
- **CPM: 174 cans/min**
- **Max Capacity: 522 cans**

### High-Speed Setup (8m × 1.0m @ 30 m/min)
- Can: 66mm diameter, 115mm height
- Spacing: 15mm
- **CPM: 370 cans/min**
- **Max Capacity: 969 cans**

### Compact Setup (3m × 0.5m @ 10 m/min)
- Can: 66mm diameter, 115mm height
- Spacing: 20mm
- **CPM: 116 cans/min**
- **Max Capacity: 102 cans**

## Quick Configuration Changes

### Change Can Size
Edit `can_conveyor_simulation.py` line ~370:
```python
conveyor = CanConveyorSystem(
    can_diameter=0.053,    # 53mm for slim can
    can_height=0.146,      # 146mm for slim can
    ...
)
```

### Change Speed
Edit `can_conveyor_simulation.py` line ~370:
```python
conveyor = CanConveyorSystem(
    conveyor_speed=25.0,   # 25 m/min for fast line
    ...
)
```

### Change Conveyor Size
Edit `can_conveyor_simulation.py` line ~370:
```python
conveyor = CanConveyorSystem(
    conveyor_length=8.0,   # 8 meters
    conveyor_width=1.0,    # 1 meter
    ...
)
```

## Simulation Controls

| Key | Action |
|-----|--------|
| Q | Quit |
| SPACE | Pause/Resume |
| Mouse Drag | Rotate camera |
| Mouse Wheel | Zoom |

## Troubleshooting Quick Fixes

### Vulkan not available
```python
# Force Irrlicht
conveyor.run_simulation(use_vulkan=False)
```

### Too slow
```python
# Reduce cans
INITIAL_CANS = 10

# Increase timestep
TIME_STEP = 0.02

# Reduce iterations
SOLVER_MAX_ITERATIONS = 30
```

### Import error
```bash
pip install --upgrade pychrono[vulkan]
```

## File Quick Reference

| File | Purpose |
|------|---------|
| `can_conveyor_simulation.py` | Main simulation |
| `conveyor_config.py` | Configuration parameters |
| `examples.py` | Usage examples |
| `CONVEYOR_README.md` | Full documentation |
| `requirements.txt` | Dependencies |

## Calculation Examples

### Example 1: Find Required Speed for 200 CPM
```
Target: 200 cans/min
Can: 66mm + 20mm spacing = 86mm = 0.086m

Speed = 200 × 0.086 = 17.2 m/min
```

### Example 2: Find CPM for 25 m/min
```
Speed: 25 m/min
Can: 66mm + 15mm spacing = 81mm = 0.081m

CPM = 25 / 0.081 = 308.6 cans/min
```

### Example 3: Find Maximum Cans
```
Conveyor: 5m × 0.8m
Can pitch: 86mm = 0.086m

Length: 5.0 / 0.086 = 58.1 → 58 cans
Width: 0.8 / 0.086 = 9.3 → 9 cans
Total: 58 × 9 = 522 cans
```

### Example 4: Find Motor RPM
```
Belt speed: 15 m/min = 0.25 m/s
Sprocket radius: 0.1m

ω = v/r = 0.25/0.1 = 2.5 rad/s
RPM = (2.5 × 60) / (2π) = 23.9 RPM
```

## Performance Optimization Tips

1. **For Higher CPM**: Increase speed or reduce can spacing
2. **For More Capacity**: Increase length or width
3. **For Stability**: Reduce speed or increase friction
4. **For Different Cans**: Adjust diameter and height

## Common Modifications

### Add Can Spawning
```python
# In run loop
if time % 0.5 < time_step:  # Every 0.5s
    spawn_position = [-length/2 + 0.2, 0.3, 0]
    self.create_empty_can(spawn_position)
```

### Record Metrics
```python
# After simulation
with open('metrics.txt', 'w') as f:
    f.write(f"CPM: {conveyor.cpm}\n")
    f.write(f"Max: {conveyor.max_total_cans}\n")
```

### Change Visual Colors
```python
# In create_conveyor_belt()
belt_mat.SetDiffuseColor(chrono.ChColor(0.1, 0.8, 0.1))  # Green

# In create_empty_can()
can_mat.SetDiffuseColor(chrono.ChColor(0.2, 0.2, 0.9))  # Blue
```

---

**For detailed information, see CONVEYOR_README.md**
