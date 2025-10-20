"""
Configuration file for Can Conveyor Simulation

Modify these parameters to customize the simulation behavior.
"""

# Conveyor Belt Parameters
CONVEYOR_LENGTH = 5.0           # meters
CONVEYOR_WIDTH = 0.8            # meters (80 cm)
CONVEYOR_SPEED = 15.0           # m/min (meters per minute)

# Can Parameters (Standard 330ml beverage can)
CAN_DIAMETER = 0.066            # meters (66mm)
CAN_HEIGHT = 0.115              # meters (115mm - standard can height)
CAN_SPACING = 0.02              # meters (20mm spacing between cans)
CAN_MASS = 0.015                # kg (15 grams - empty aluminum can)
CAN_WALL_THICKNESS = 0.0001     # meters (0.1mm - typical aluminum can)

# Drive System Parameters
SPROCKET_RADIUS = 0.1           # meters (10cm)
MOTOR_RPM = 60.0                # RPM (revolutions per minute)
MOTOR_TORQUE = 50.0             # Nm (Newton-meters)

# Simulation Parameters
SIMULATION_TIME = 30.0          # seconds
TIME_STEP = 0.01                # seconds (10ms)
USE_VULKAN = True               # Try to use Vulkan renderer (falls back to Irrlicht)

# Initial Can Population
INITIAL_CANS = 20               # Number of cans to place initially (None = maximum)

# Physics Parameters
GRAVITY = -9.81                 # m/s^2
BELT_FRICTION = 0.6             # Coefficient of friction (belt to cans)
CAN_FRICTION = 0.4              # Coefficient of friction (can to can)
BELT_RESTITUTION = 0.1          # Bounciness of belt
CAN_RESTITUTION = 0.2           # Bounciness of cans

# Solver Parameters
SOLVER_MAX_ITERATIONS = 50
SOLVER_TOLERANCE = 1e-4

# Visualization Parameters
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CAMERA_POSITION = (2, 2, 2)     # (x, y, z)
CAMERA_TARGET = (0, 0, 0)       # (x, y, z)

# Material Colors (R, G, B) - values from 0 to 1
GROUND_COLOR = (0.3, 0.3, 0.3)       # Dark gray
BELT_COLOR = (0.2, 0.5, 0.8)         # Blue
CAN_COLOR = (0.9, 0.1, 0.1)          # Red (aluminum can)
SPROCKET_COLOR = (0.6, 0.6, 0.6)     # Silver/gray

# Material Properties
CAN_METALLIC = 0.7              # 0-1 (metallic appearance)
CAN_ROUGHNESS = 0.3             # 0-1 (surface roughness)
SPROCKET_METALLIC = 0.8


# Common Can Sizes (uncomment to use different sizes)
# ---------------------------------------------------

# Standard 330ml can
# CAN_DIAMETER = 0.066  # 66mm
# CAN_HEIGHT = 0.115    # 115mm

# Slim 250ml can
# CAN_DIAMETER = 0.053  # 53mm
# CAN_HEIGHT = 0.146    # 146mm

# Tall 500ml can
# CAN_DIAMETER = 0.066  # 66mm
# CAN_HEIGHT = 0.168    # 168mm

# Large 568ml (pint) can
# CAN_DIAMETER = 0.073  # 73mm
# CAN_HEIGHT = 0.161    # 161mm


# Conveyor Speed Presets (uncomment to use)
# ------------------------------------------

# Slow: 10 m/min
# CONVEYOR_SPEED = 10.0

# Medium: 15 m/min (default)
# CONVEYOR_SPEED = 15.0

# Fast: 25 m/min
# CONVEYOR_SPEED = 25.0

# Very Fast: 40 m/min
# CONVEYOR_SPEED = 40.0


def print_configuration():
    """Print the current configuration."""
    print("\n" + "="*60)
    print("CONVEYOR CONFIGURATION")
    print("="*60)
    print(f"Conveyor: {CONVEYOR_LENGTH}m x {CONVEYOR_WIDTH}m @ {CONVEYOR_SPEED} m/min")
    print(f"Can: D={CAN_DIAMETER*1000}mm H={CAN_HEIGHT*1000}mm (Mass={CAN_MASS*1000}g)")
    print(f"Spacing: {CAN_SPACING*1000}mm")
    print(f"Motor: {MOTOR_RPM} RPM, Torque={MOTOR_TORQUE} Nm")
    print(f"Sprocket: Radius={SPROCKET_RADIUS*100}cm")
    print(f"Simulation: {SIMULATION_TIME}s @ {TIME_STEP*1000}ms timestep")
    print(f"Renderer: {'Vulkan (preferred)' if USE_VULKAN else 'Irrlicht'}")
    print("="*60 + "\n")


if __name__ == "__main__":
    print_configuration()
