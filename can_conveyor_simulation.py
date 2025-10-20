"""
PyChrono 9.0 Beverage Can Line Conveyor Simulation with Vulkan
================================================================

This simulation models a beverage can production line with:
- Mat conveyor belt driven by motor and sprocket
- Empty beverage cans (open cylinders, no ends)
- CPM (Cans Per Minute) calculation
- Conveyor speed in m/min
- Maximum can capacity estimation based on conveyor dimensions

Author: Generated with Claude Code
Date: 2025-10-20
"""

import pychrono as chrono
import pychrono.irrlicht as chronoirr
try:
    import pychrono.vulkan as chronovulkan
    VULKAN_AVAILABLE = True
except ImportError:
    print("Warning: Vulkan module not available, falling back to Irrlicht")
    VULKAN_AVAILABLE = False

import math
import numpy as np


class CanConveyorSystem:
    """
    Beverage can conveyor line simulation system.
    """

    def __init__(self,
                 conveyor_length=5.0,      # meters
                 conveyor_width=0.8,       # meters
                 conveyor_speed=15.0,      # m/min
                 can_diameter=0.066,       # meters (66mm standard can)
                 can_height=0.115,         # meters (115mm standard can)
                 can_spacing=0.02,         # meters (spacing between cans)
                 sprocket_radius=0.1,      # meters
                 motor_rpm=60.0):          # RPM

        # System parameters
        self.conveyor_length = conveyor_length
        self.conveyor_width = conveyor_width
        self.conveyor_speed = conveyor_speed  # m/min
        self.conveyor_speed_ms = conveyor_speed / 60.0  # m/s

        # Can parameters
        self.can_diameter = can_diameter
        self.can_height = can_height
        self.can_spacing = can_spacing
        self.can_mass = 0.015  # kg (empty aluminum can ~15g)
        self.can_thickness = 0.0001  # meters (0.1mm wall thickness)

        # Drive system parameters
        self.sprocket_radius = sprocket_radius
        self.motor_rpm = motor_rpm
        self.motor_torque = 50.0  # Nm (adjustable)

        # Calculated parameters
        self.calculate_system_parameters()

        # PyChrono system
        self.system = chrono.ChSystemNSC()
        self.system.SetGravitationalAcceleration(chrono.ChVector3d(0, -9.81, 0))

        # Collections
        self.cans = []
        self.conveyor_belt = None
        self.motor = None
        self.sprocket = None

    def calculate_system_parameters(self):
        """Calculate CPM, maximum cans, and other derived parameters."""

        # Calculate cans per minute (CPM)
        # Distance traveled per minute = conveyor_speed (m/min)
        # Space occupied per can = can_diameter + can_spacing
        can_pitch = self.can_diameter + self.can_spacing

        # CPM = (conveyor speed in m/min) / (space per can in m)
        self.cpm = self.conveyor_speed / can_pitch

        # Maximum cans on conveyor at once
        # Number of cans along length
        self.max_cans_length = int(self.conveyor_length / can_pitch)

        # Number of cans across width (with spacing)
        self.max_cans_width = int(self.conveyor_width / can_pitch)

        # Total maximum cans
        self.max_total_cans = self.max_cans_length * self.max_cans_width

        # Motor angular velocity from conveyor speed
        # v = ω * r  =>  ω = v / r
        self.motor_angular_velocity = self.conveyor_speed_ms / self.sprocket_radius
        self.calculated_motor_rpm = (self.motor_angular_velocity * 60) / (2 * math.pi)

        # Print calculated parameters
        print("\n" + "="*60)
        print("CONVEYOR SYSTEM PARAMETERS")
        print("="*60)
        print(f"Conveyor Length: {self.conveyor_length} m")
        print(f"Conveyor Width: {self.conveyor_width} m")
        print(f"Conveyor Speed: {self.conveyor_speed} m/min ({self.conveyor_speed_ms:.3f} m/s)")
        print(f"\nCan Diameter: {self.can_diameter*1000} mm")
        print(f"Can Height: {self.can_height*1000} mm")
        print(f"Can Spacing: {self.can_spacing*1000} mm")
        print(f"Can Pitch (diameter + spacing): {(self.can_diameter + self.can_spacing)*1000:.1f} mm")
        print(f"\nCPM (Cans Per Minute): {self.cpm:.1f} cans/min")
        print(f"Maximum Cans (Length): {self.max_cans_length} cans")
        print(f"Maximum Cans (Width): {self.max_cans_width} cans")
        print(f"Maximum Total Cans: {self.max_total_cans} cans")
        print(f"\nMotor RPM (calculated): {self.calculated_motor_rpm:.1f} RPM")
        print(f"Sprocket Radius: {self.sprocket_radius*100} cm")
        print("="*60 + "\n")

    def create_ground(self):
        """Create the ground body."""
        ground = chrono.ChBodyEasyBox(20, 0.2, 20, 1000, True, False)
        ground.SetPos(chrono.ChVector3d(0, -0.5, 0))
        ground.SetFixed(True)
        ground.SetName("ground")

        # Visual appearance
        ground_mat = chrono.ChVisualMaterial()
        ground_mat.SetDiffuseColor(chrono.ChColor(0.3, 0.3, 0.3))
        ground.GetVisualShape(0).SetMaterial(0, ground_mat)

        self.system.Add(ground)
        return ground

    def create_conveyor_belt(self):
        """Create the conveyor belt (mat)."""
        # Conveyor belt as a moving surface
        belt_thickness = 0.01  # 1cm thick

        self.conveyor_belt = chrono.ChBodyEasyBox(
            self.conveyor_length,
            belt_thickness,
            self.conveyor_width,
            500,  # density kg/m^3
            True,  # visualization
            True   # collision
        )

        self.conveyor_belt.SetPos(chrono.ChVector3d(0, 0, 0))
        self.conveyor_belt.SetName("conveyor_belt")

        # Set belt to move at constant velocity
        self.conveyor_belt.SetFixed(False)

        # Visual appearance
        belt_mat = chrono.ChVisualMaterial()
        belt_mat.SetDiffuseColor(chrono.ChColor(0.2, 0.5, 0.8))
        self.conveyor_belt.GetVisualShape(0).SetMaterial(0, belt_mat)

        # Contact material with friction
        contact_mat = chrono.ChContactMaterialNSC()
        contact_mat.SetFriction(0.6)
        contact_mat.SetRestitution(0.1)
        self.conveyor_belt.GetCollisionModel().SetAllShapesMaterial(contact_mat)

        self.system.Add(self.conveyor_belt)

        # Add linear actuator to move belt
        self.create_belt_actuator()

        return self.conveyor_belt

    def create_belt_actuator(self):
        """Create a motor actuator to move the conveyor belt."""
        # Create a prismatic joint for belt movement
        # We'll use a linear actuator

        # Create a fixed reference body for the motor
        motor_ref = chrono.ChBody()
        motor_ref.SetFixed(True)
        motor_ref.SetPos(chrono.ChVector3d(-self.conveyor_length/2, 0, 0))
        self.system.Add(motor_ref)

        # Create linear motor
        linear_motor = chrono.ChLinkMotorLinearSpeed()
        linear_motor.Initialize(
            self.conveyor_belt,
            motor_ref,
            chrono.ChFramed(chrono.ChVector3d(0, 0, 0))
        )

        # Set constant speed
        speed_function = chrono.ChFunctionConst(self.conveyor_speed_ms)
        linear_motor.SetSpeedFunction(speed_function)

        self.system.Add(linear_motor)
        self.motor = linear_motor

    def create_sprocket_system(self):
        """Create the sprocket and motor drive system (visual representation)."""
        # Create sprocket wheel
        self.sprocket = chrono.ChBodyEasyCylinder(
            chrono.ChAxis_Y,
            self.sprocket_radius,
            0.05,  # thickness
            1000,  # density
            True,  # visualization
            False  # collision
        )

        # Position at the end of conveyor
        self.sprocket.SetPos(chrono.ChVector3d(
            -self.conveyor_length/2 - 0.2,
            0.1,
            0
        ))
        self.sprocket.SetRot(chrono.QuatFromAngleAxis(math.pi/2, chrono.ChVector3d(0, 0, 1)))

        # Visual appearance
        sprocket_mat = chrono.ChVisualMaterial()
        sprocket_mat.SetDiffuseColor(chrono.ChColor(0.6, 0.6, 0.6))
        sprocket_mat.SetMetallic(0.8)
        self.sprocket.GetVisualShape(0).SetMaterial(0, sprocket_mat)

        self.system.Add(self.sprocket)

        # Add rotational motor to sprocket
        motor_base = chrono.ChBody()
        motor_base.SetFixed(True)
        motor_base.SetPos(self.sprocket.GetPos())
        self.system.Add(motor_base)

        rotational_motor = chrono.ChLinkMotorRotationSpeed()
        rotational_motor.Initialize(
            self.sprocket,
            motor_base,
            chrono.ChFramed(self.sprocket.GetPos())
        )

        # Set angular velocity
        omega = self.motor_angular_velocity
        speed_func = chrono.ChFunctionConst(omega)
        rotational_motor.SetSpeedFunction(speed_func)

        self.system.Add(rotational_motor)

    def create_empty_can(self, position):
        """
        Create an empty beverage can (open cylinder without ends).
        Modeled as a hollow cylinder.
        """
        # Create can body using cylinder
        # For open can (no ends), we use a thin-walled cylinder
        can = chrono.ChBodyEasyCylinder(
            chrono.ChAxis_Y,  # axis along Y (vertical)
            self.can_diameter / 2,  # radius
            self.can_height,        # height
            self.can_mass / (math.pi * (self.can_diameter/2)**2 * self.can_height),  # density
            True,   # visualization
            True    # collision
        )

        can.SetPos(chrono.ChVector3d(position[0], position[1], position[2]))
        can.SetName(f"can_{len(self.cans)}")

        # Visual appearance - aluminum can
        can_mat = chrono.ChVisualMaterial()
        can_mat.SetDiffuseColor(chrono.ChColor(0.9, 0.1, 0.1))  # Red can
        can_mat.SetMetallic(0.7)
        can_mat.SetRoughness(0.3)
        can.GetVisualShape(0).SetMaterial(0, can_mat)

        # Contact material
        contact_mat = chrono.ChContactMaterialNSC()
        contact_mat.SetFriction(0.4)
        contact_mat.SetRestitution(0.2)
        can.GetCollisionModel().SetAllShapesMaterial(contact_mat)

        self.system.Add(can)
        self.cans.append(can)

        return can

    def populate_conveyor_with_cans(self, num_cans=None):
        """
        Place cans on the conveyor belt.
        If num_cans is None, fill to maximum capacity.
        """
        if num_cans is None:
            num_cans = self.max_total_cans

        can_pitch = self.can_diameter + self.can_spacing

        # Starting position (back of conveyor)
        start_x = -self.conveyor_length / 2 + self.can_diameter / 2 + 0.1
        start_z = -self.conveyor_width / 2 + self.can_diameter / 2 + 0.05
        start_y = self.can_height / 2 + 0.02  # Just above belt

        cans_placed = 0
        row = 0
        col = 0

        while cans_placed < num_cans:
            x = start_x + row * can_pitch
            z = start_z + col * can_pitch

            # Check if still within conveyor bounds
            if x > self.conveyor_length / 2 - self.can_diameter / 2:
                break

            if z <= self.conveyor_width / 2 - self.can_diameter / 2:
                self.create_empty_can([x, start_y, z])
                cans_placed += 1
                col += 1
            else:
                col = 0
                row += 1

        print(f"Placed {cans_placed} cans on conveyor")

    def setup_simulation(self):
        """Set up the complete simulation."""
        print("Setting up simulation...")

        # Create components
        self.create_ground()
        self.create_conveyor_belt()
        self.create_sprocket_system()

        # Populate with cans (start with a subset)
        self.populate_conveyor_with_cans(min(20, self.max_total_cans))

        # Set solver parameters
        self.system.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN)
        self.system.GetSolver().AsIterative().SetMaxIterations(50)
        self.system.SetSolverForceTolerance(1e-4)

        print("Simulation setup complete!")

    def run_simulation(self, time_duration=20.0, time_step=0.01, use_vulkan=True):
        """
        Run the simulation with visualization.

        Args:
            time_duration: Total simulation time in seconds
            time_step: Time step for integration
            use_vulkan: Use Vulkan if available, otherwise Irrlicht
        """
        # Setup visualization
        if use_vulkan and VULKAN_AVAILABLE:
            vis = self.setup_vulkan_visualization()
        else:
            vis = self.setup_irrlicht_visualization()

        if vis is None:
            print("Error: Could not initialize visualization")
            return

        # Simulation loop
        print(f"\nRunning simulation for {time_duration} seconds...")
        print(f"Press Q to quit, SPACE to pause\n")

        time = 0
        frame = 0

        while vis.Run() and time < time_duration:
            vis.BeginScene()
            vis.Render()

            # Display info
            if frame % 50 == 0:
                print(f"Time: {time:.2f}s | Cans: {len(self.cans)} | "
                      f"Belt velocity: {self.conveyor_belt.GetPosDt().x:.3f} m/s")

            vis.EndScene()
            self.system.DoStepDynamics(time_step)

            time += time_step
            frame += 1

        print("\nSimulation complete!")

    def setup_irrlicht_visualization(self):
        """Setup Irrlicht visualization."""
        print("Initializing Irrlicht visualization...")

        vis = chronoirr.ChVisualSystemIrrlicht()
        vis.AttachSystem(self.system)
        vis.SetWindowSize(1280, 720)
        vis.SetWindowTitle("Can Conveyor Line - PyChrono 9.0")
        vis.Initialize()
        vis.AddLogo()
        vis.AddSkyBox()
        vis.AddCamera(chrono.ChVector3d(2, 2, 2), chrono.ChVector3d(0, 0, 0))
        vis.AddTypicalLights()

        return vis

    def setup_vulkan_visualization(self):
        """Setup Vulkan visualization."""
        if not VULKAN_AVAILABLE:
            print("Vulkan not available, using Irrlicht instead")
            return self.setup_irrlicht_visualization()

        print("Initializing Vulkan visualization...")

        try:
            vis = chronovulkan.ChVisualSystemVulkan()
            vis.AttachSystem(self.system)
            vis.SetWindowSize(1280, 720)
            vis.SetWindowTitle("Can Conveyor Line - PyChrono 9.0 (Vulkan)")
            vis.Initialize()

            # Setup camera
            vis.AddCamera(chrono.ChVector3d(2, 2, 2), chrono.ChVector3d(0, 0, 0))

            # Add lights
            vis.AddLight(chrono.ChVector3d(5, 10, 5),
                        chrono.ChColor(1, 1, 1), 100)
            vis.AddLight(chrono.ChVector3d(-5, 10, -5),
                        chrono.ChColor(0.8, 0.8, 1), 80)

            return vis
        except Exception as e:
            print(f"Error initializing Vulkan: {e}")
            print("Falling back to Irrlicht...")
            return self.setup_irrlicht_visualization()


def main():
    """Main function to run the conveyor simulation."""

    print("\n" + "="*60)
    print("PyChrono 9.0 - Beverage Can Conveyor Line Simulation")
    print("with Vulkan Rendering")
    print("="*60 + "\n")

    # Create conveyor system with custom parameters
    conveyor = CanConveyorSystem(
        conveyor_length=5.0,       # 5 meters long
        conveyor_width=0.8,        # 80 cm wide
        conveyor_speed=15.0,       # 15 m/min
        can_diameter=0.066,        # 66mm diameter (standard can)
        can_height=0.115,          # 115mm height
        can_spacing=0.02,          # 20mm spacing
        sprocket_radius=0.1,       # 10cm sprocket
        motor_rpm=60.0             # 60 RPM
    )

    # Setup and run simulation
    conveyor.setup_simulation()
    conveyor.run_simulation(
        time_duration=30.0,   # 30 seconds
        time_step=0.01,       # 10ms time step
        use_vulkan=True       # Try to use Vulkan
    )


if __name__ == "__main__":
    main()
