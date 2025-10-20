"""
Example Usage Scripts for Can Conveyor Simulation

This file demonstrates different configurations and use cases
for the beverage can conveyor line simulation.
"""

from can_conveyor_simulation import CanConveyorSystem
import math


def example_1_standard_line():
    """
    Example 1: Standard production line
    Medium speed, standard 330ml cans
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Standard Production Line")
    print("="*60)

    conveyor = CanConveyorSystem(
        conveyor_length=5.0,
        conveyor_width=0.8,
        conveyor_speed=15.0,        # 15 m/min - medium speed
        can_diameter=0.066,         # 66mm - standard 330ml can
        can_height=0.115,
        can_spacing=0.02,
        sprocket_radius=0.1,
        motor_rpm=60.0
    )

    conveyor.setup_simulation()
    conveyor.run_simulation(time_duration=20.0, use_vulkan=True)


def example_2_high_speed_line():
    """
    Example 2: High-speed production line
    Fast conveyor with tight can spacing for maximum throughput
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: High-Speed Production Line")
    print("="*60)

    conveyor = CanConveyorSystem(
        conveyor_length=8.0,        # Longer conveyor
        conveyor_width=1.0,         # Wider for multi-lane
        conveyor_speed=30.0,        # 30 m/min - high speed
        can_diameter=0.066,
        can_height=0.115,
        can_spacing=0.015,          # Tighter spacing
        sprocket_radius=0.12,       # Larger sprocket
        motor_rpm=100.0
    )

    conveyor.setup_simulation()
    print(f"\nExpected throughput: {conveyor.cpm:.1f} cans/min")
    conveyor.run_simulation(time_duration=30.0, use_vulkan=True)


def example_3_slim_can_line():
    """
    Example 3: Slim can (250ml) production line
    Optimized for smaller diameter cans
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Slim Can (250ml) Line")
    print("="*60)

    conveyor = CanConveyorSystem(
        conveyor_length=5.0,
        conveyor_width=0.6,         # Narrower for slim cans
        conveyor_speed=20.0,
        can_diameter=0.053,         # 53mm - slim can
        can_height=0.146,           # Taller slim can
        can_spacing=0.015,
        sprocket_radius=0.1,
        motor_rpm=80.0
    )

    conveyor.setup_simulation()
    print(f"\nSlim can CPM: {conveyor.cpm:.1f} cans/min")
    print(f"Maximum capacity: {conveyor.max_total_cans} cans")
    conveyor.run_simulation(time_duration=25.0, use_vulkan=True)


def example_4_large_can_line():
    """
    Example 4: Large can (500ml) production line
    Slower speed for stability with larger cans
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Large Can (500ml) Line")
    print("="*60)

    conveyor = CanConveyorSystem(
        conveyor_length=6.0,
        conveyor_width=1.0,         # Wider for large cans
        conveyor_speed=12.0,        # Slower for stability
        can_diameter=0.066,
        can_height=0.168,           # Tall 500ml can
        can_spacing=0.025,          # More spacing
        sprocket_radius=0.1,
        motor_rpm=50.0
    )

    conveyor.setup_simulation()
    print(f"\nLarge can CPM: {conveyor.cpm:.1f} cans/min")
    conveyor.run_simulation(time_duration=25.0, use_vulkan=True)


def example_5_compact_line():
    """
    Example 5: Compact production line
    Short conveyor for limited space
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Compact Production Line")
    print("="*60)

    conveyor = CanConveyorSystem(
        conveyor_length=3.0,        # Short conveyor
        conveyor_width=0.5,         # Narrow
        conveyor_speed=10.0,        # Moderate speed
        can_diameter=0.066,
        can_height=0.115,
        can_spacing=0.02,
        sprocket_radius=0.08,       # Smaller sprocket
        motor_rpm=50.0
    )

    conveyor.setup_simulation()
    print(f"\nCompact line capacity: {conveyor.max_total_cans} cans")
    print(f"CPM: {conveyor.cpm:.1f} cans/min")
    conveyor.run_simulation(time_duration=15.0, use_vulkan=True)


def calculate_optimal_parameters():
    """
    Example 6: Calculate optimal conveyor parameters
    Demonstrates how to size a conveyor for target CPM
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: Optimal Parameter Calculator")
    print("="*60)

    # Target specifications
    target_cpm = 200.0              # Target: 200 cans per minute
    can_diameter = 0.066            # 66mm can
    can_spacing = 0.02              # 20mm spacing
    available_length = 5.0          # 5m space available

    # Calculate required conveyor speed
    can_pitch = can_diameter + can_spacing
    required_speed = target_cpm * can_pitch  # m/min

    print(f"\nTarget CPM: {target_cpm} cans/min")
    print(f"Can pitch: {can_pitch*1000:.1f} mm")
    print(f"Required conveyor speed: {required_speed:.2f} m/min")

    # Calculate sprocket parameters
    sprocket_radius = 0.1  # 10cm sprocket
    motor_rpm = (required_speed / 60) / (2 * math.pi * sprocket_radius) * 60
    print(f"Sprocket radius: {sprocket_radius*100} cm")
    print(f"Required motor RPM: {motor_rpm:.1f} RPM")

    # Calculate maximum capacity
    max_cans_length = int(available_length / can_pitch)
    print(f"\nMaximum cans on conveyor: {max_cans_length} cans")

    # Time to fill conveyor
    fill_time = max_cans_length / target_cpm  # minutes
    print(f"Time to fill conveyor: {fill_time:.2f} minutes")

    print("\n" + "="*60)
    print("Creating simulation with calculated parameters...")
    print("="*60)

    conveyor = CanConveyorSystem(
        conveyor_length=available_length,
        conveyor_width=0.8,
        conveyor_speed=required_speed,
        can_diameter=can_diameter,
        can_height=0.115,
        can_spacing=can_spacing,
        sprocket_radius=sprocket_radius,
        motor_rpm=motor_rpm
    )

    conveyor.setup_simulation()
    print(f"\nActual CPM achieved: {conveyor.cpm:.1f} cans/min")
    print(f"Difference from target: {abs(conveyor.cpm - target_cpm):.2f} cans/min")

    # Run simulation
    conveyor.run_simulation(time_duration=20.0, use_vulkan=True)


def benchmark_different_speeds():
    """
    Example 7: Benchmark different conveyor speeds
    Compare performance at various speeds without visualization
    """
    print("\n" + "="*60)
    print("EXAMPLE 7: Speed Benchmark Comparison")
    print("="*60)

    speeds = [10.0, 15.0, 20.0, 25.0, 30.0, 40.0]  # m/min

    print("\n{:<15} {:<15} {:<20} {:<15}".format(
        "Speed (m/min)", "CPM", "Max Capacity", "Motor RPM"
    ))
    print("-" * 65)

    for speed in speeds:
        conveyor = CanConveyorSystem(
            conveyor_length=5.0,
            conveyor_width=0.8,
            conveyor_speed=speed,
            can_diameter=0.066,
            can_height=0.115,
            can_spacing=0.02,
            sprocket_radius=0.1,
            motor_rpm=60.0
        )

        print("{:<15.1f} {:<15.1f} {:<20} {:<15.1f}".format(
            speed,
            conveyor.cpm,
            conveyor.max_total_cans,
            conveyor.calculated_motor_rpm
        ))

    print("\nNote: Run individual simulations to visualize specific speeds")


def compare_can_sizes():
    """
    Example 8: Compare different can sizes
    Show how can size affects throughput
    """
    print("\n" + "="*60)
    print("EXAMPLE 8: Can Size Comparison")
    print("="*60)

    can_types = {
        "Slim 250ml": {"diameter": 0.053, "height": 0.146},
        "Standard 330ml": {"diameter": 0.066, "height": 0.115},
        "Tall 500ml": {"diameter": 0.066, "height": 0.168},
        "Pint 568ml": {"diameter": 0.073, "height": 0.161}
    }

    conveyor_speed = 15.0  # m/min
    conveyor_length = 5.0
    conveyor_width = 0.8
    can_spacing = 0.02

    print(f"\nConveyor: {conveyor_length}m x {conveyor_width}m @ {conveyor_speed} m/min")
    print("\n{:<20} {:<15} {:<15} {:<15}".format(
        "Can Type", "Diameter (mm)", "CPM", "Max Capacity"
    ))
    print("-" * 65)

    for can_name, dimensions in can_types.items():
        conveyor = CanConveyorSystem(
            conveyor_length=conveyor_length,
            conveyor_width=conveyor_width,
            conveyor_speed=conveyor_speed,
            can_diameter=dimensions["diameter"],
            can_height=dimensions["height"],
            can_spacing=can_spacing,
            sprocket_radius=0.1,
            motor_rpm=60.0
        )

        print("{:<20} {:<15.1f} {:<15.1f} {:<15}".format(
            can_name,
            dimensions["diameter"] * 1000,
            conveyor.cpm,
            conveyor.max_total_cans
        ))


def main_menu():
    """Interactive menu to select examples."""
    print("\n" + "="*60)
    print("CAN CONVEYOR SIMULATION - EXAMPLES")
    print("="*60)
    print("\nAvailable Examples:")
    print("  1. Standard Production Line")
    print("  2. High-Speed Production Line")
    print("  3. Slim Can (250ml) Line")
    print("  4. Large Can (500ml) Line")
    print("  5. Compact Production Line")
    print("  6. Optimal Parameter Calculator")
    print("  7. Speed Benchmark Comparison")
    print("  8. Can Size Comparison")
    print("  0. Run All Examples (sequential)")
    print("\nEnter example number (or 'q' to quit): ", end='')

    choice = input().strip()

    examples = {
        '1': example_1_standard_line,
        '2': example_2_high_speed_line,
        '3': example_3_slim_can_line,
        '4': example_4_large_can_line,
        '5': example_5_compact_line,
        '6': calculate_optimal_parameters,
        '7': benchmark_different_speeds,
        '8': compare_can_sizes
    }

    if choice == 'q':
        print("Exiting...")
        return
    elif choice == '0':
        print("\nRunning all examples...")
        for func in examples.values():
            func()
            print("\n" + "="*60)
            print("Press Enter to continue to next example...")
            input()
    elif choice in examples:
        examples[choice]()
    else:
        print("Invalid choice. Please try again.")
        main_menu()


if __name__ == "__main__":
    # Run interactive menu
    main_menu()

    # Or uncomment to run specific example:
    # example_1_standard_line()
    # example_6_calculate_optimal_parameters()
    # benchmark_different_speeds()
    # compare_can_sizes()
