"""
This module provides detailed step-by-step beam calculations, focusing on finding
the zero-shear points to determine maximum moments.
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_reactions(span_length, point_loads, point_load_positions, uniform_loads, uniform_load_regions):
    """
    Calculate reactions for a simply supported beam.
    
    Args:
        span_length: Length of beam span (ft)
        point_loads: List of point load magnitudes (kips)
        point_load_positions: List of point load positions from left support (ft)
        uniform_loads: List of uniform load magnitudes (k/ft)
        uniform_load_regions: List of tuples (start, end) for uniform load regions (ft)
        
    Returns:
        Tuple of (R1, R2) reactions at supports
    """
    print("1. CALCULATING REACTIONS:")
    print(f"   Span Length = {span_length} ft")
    
    # Step 1: Calculate moments about left support for R2
    print("\n   Step 1.1: Calculate moment equilibrium about left support (x=0) to find R2")
    sum_moments = 0
    
    # Point loads contribution to moment
    print("   Point load contributions to moment:")
    for i, (P, x) in enumerate(zip(point_loads, point_load_positions)):
        moment = P * x
        sum_moments += moment
        print(f"     P{i+1} = {P} kips at x = {x} ft -> M = {P} × {x} = {moment:.2f} kip-ft")
    
    # Uniform loads contribution to moment
    print("\n   Uniform load contributions to moment:")
    for i, (w, region) in enumerate(zip(uniform_loads, uniform_load_regions)):
        start, end = region
        length = end - start
        centroid = start + length/2
        load = w * length
        moment = load * centroid
        sum_moments += moment
        print(f"     w{i+1} = {w} k/ft from x = {start} to {end} ft")
        print(f"       Length = {length} ft, Centroid at x = {centroid} ft")
        print(f"       Total load = {w} × {length} = {load:.2f} kips")
        print(f"       Moment = {load:.2f} × {centroid} = {moment:.2f} kip-ft")
    
    # Calculate R2
    R2 = sum_moments / span_length if span_length > 0 else 0
    print(f"\n   Sum of moments = {sum_moments:.2f} kip-ft")
    print(f"   R2 = Sum of moments / Span Length = {sum_moments:.2f} / {span_length} = {R2:.2f} kips")
    
    # Step 2: Calculate vertical force equilibrium for R1
    print("\n   Step 1.2: Calculate vertical force equilibrium to find R1")
    sum_loads = 0
    
    # Point loads
    print("   Point load contributions:")
    for i, P in enumerate(point_loads):
        sum_loads += P
        print(f"     P{i+1} = {P} kips")
    
    # Uniform loads
    print("\n   Uniform load contributions:")
    for i, (w, region) in enumerate(zip(uniform_loads, uniform_load_regions)):
        start, end = region
        length = end - start
        load = w * length
        sum_loads += load
        print(f"     w{i+1} = {w} k/ft over {length} ft = {load:.2f} kips")
    
    # Calculate R1
    R1 = sum_loads - R2
    print(f"\n   Sum of loads = {sum_loads:.2f} kips")
    print(f"   R1 = Sum of loads - R2 = {sum_loads:.2f} - {R2:.2f} = {R1:.2f} kips")
    
    return R1, R2

def calculate_shear_diagram(span_length, R1, R2, point_loads, point_load_positions, uniform_loads, uniform_load_regions):
    """
    Calculate and plot the shear force diagram.
    
    Args:
        span_length: Length of beam span (ft)
        R1, R2: Reactions at supports (kips)
        point_loads: List of point load magnitudes (kips)
        point_load_positions: List of point load positions from left support (ft)
        uniform_loads: List of uniform load magnitudes (k/ft)
        uniform_load_regions: List of tuples (start, end) for uniform load regions (ft)
        
    Returns:
        Tuple of (x_values, shear_values, zero_shear_points)
    """
    print("\n2. CALCULATING SHEAR DIAGRAM:")
    
    # Create x-coordinates for the shear diagram
    # Add points of interest: supports, point loads, uniform load start/end
    x_points = [0, span_length]  # Add supports
    x_points.extend(point_load_positions)  # Add point load positions
    
    # Add uniform load boundaries
    for start, end in uniform_load_regions:
        x_points.extend([start, end])
    
    # Add intermediate points for a smoother diagram
    x_values = sorted(list(set(x_points)))  # Remove duplicates and sort
    x_dense = np.linspace(0, span_length, 200)  # Dense points for accurate zero-crossing
    
    # Initialize shear as R1 at x=0
    shear_values = []
    shear_dense = []
    
    print("\n   Step 2.1: Calculate shear at each point of interest")
    print(f"   Starting shear at x = 0: V(0) = R1 = {R1:.2f} kips")
    
    # Calculate shear at each x-value
    for x in x_dense:
        # Start with reaction at left support
        shear = R1
        
        # Subtract point loads to the left of x
        for P, pos in zip(point_loads, point_load_positions):
            if pos < x:
                shear -= P
        
        # Subtract uniform loads to the left of x
        for w, (start, end) in zip(uniform_loads, uniform_load_regions):
            if start < x:
                # If x is within the uniform load region
                if x <= end:
                    shear -= w * (x - start)
                # If x is beyond the uniform load region
                else:
                    shear -= w * (end - start)
        
        shear_dense.append(shear)
    
    # Calculate shear at points of interest for display
    for x in x_values:
        # Start with reaction at left support
        shear = R1
        
        # Subtract point loads to the left of x
        for P, pos in zip(point_loads, point_load_positions):
            if pos < x:
                shear -= P
                print(f"   At x = {x:.2f} ft: Subtract point load P = {P:.2f} kips at x = {pos:.2f} ft -> V = {shear:.2f} kips")
        
        # Subtract uniform loads to the left of x
        for i, (w, (start, end)) in enumerate(zip(uniform_loads, uniform_load_regions)):
            if start < x:
                # If x is within the uniform load region
                if x <= end:
                    uniform_load_effect = w * (x - start)
                    shear -= uniform_load_effect
                    print(f"   At x = {x:.2f} ft: Subtract uniform load w{i+1} = {w:.2f} k/ft from x = {start:.2f} to {x:.2f} ft")
                    print(f"     Effect = {w:.2f} × ({x:.2f} - {start:.2f}) = {uniform_load_effect:.2f} kips -> V = {shear:.2f} kips")
                # If x is beyond the uniform load region
                else:
                    uniform_load_effect = w * (end - start)
                    shear -= uniform_load_effect
                    print(f"   At x = {x:.2f} ft: Subtract uniform load w{i+1} = {w:.2f} k/ft from x = {start:.2f} to {end:.2f} ft")
                    print(f"     Effect = {w:.2f} × ({end:.2f} - {start:.2f}) = {uniform_load_effect:.2f} kips -> V = {shear:.2f} kips")
        
        shear_values.append(shear)
    
    # Find zero-shear points (where the shear changes sign)
    zero_shear_points = []
    print("\n   Step 2.2: Find points of zero shear (where shear diagram crosses x-axis)")
    
    for i in range(len(x_dense) - 1):
        if shear_dense[i] * shear_dense[i+1] <= 0 and abs(shear_dense[i]) + abs(shear_dense[i+1]) > 0:
            # Linear interpolation to find the exact zero-crossing
            x1, x2 = x_dense[i], x_dense[i+1]
            v1, v2 = shear_dense[i], shear_dense[i+1]
            
            # If both values are zero, take the midpoint
            if v1 == 0 and v2 == 0:
                zero_x = (x1 + x2) / 2
            else:
                # Linear interpolation
                zero_x = x1 - v1 * (x2 - x1) / (v2 - v1) if (v2 - v1) != 0 else x1
            
            zero_shear_points.append(zero_x)
            print(f"   Zero shear at x = {zero_x:.3f} ft (between x = {x1:.3f} and x = {x2:.3f} ft)")
    
    if not zero_shear_points:
        print("   No zero-shear points found in the span")
    
    return x_values, shear_values, zero_shear_points, x_dense, shear_dense

def calculate_moment_diagram(span_length, R1, zero_shear_points, point_loads, point_load_positions, uniform_loads, uniform_load_regions):
    """
    Calculate and plot the moment diagram. Find maximum moment.
    
    Args:
        span_length: Length of beam span (ft)
        R1: Reaction at left support (kips)
        zero_shear_points: List of x-coordinates where shear is zero
        point_loads: List of point load magnitudes (kips)
        point_load_positions: List of point load positions from left support (ft)
        uniform_loads: List of uniform load magnitudes (k/ft)
        uniform_load_regions: List of tuples (start, end) for uniform load regions (ft)
    
    Returns:
        Tuple of (x_values, moment_values, max_moment, max_moment_position)
    """
    print("\n3. CALCULATING MOMENT DIAGRAM:")
    
    # Create x-coordinates for the moment diagram
    x_points = [0, span_length]  # Add supports
    x_points.extend(point_load_positions)  # Add point load positions
    x_points.extend(zero_shear_points)  # Add zero-shear points
    
    # Add uniform load boundaries
    for start, end in uniform_load_regions:
        x_points.extend([start, end])
    
    # Add intermediate points for a smoother diagram
    x_values = sorted(list(set(x_points)))  # Remove duplicates and sort
    
    # Initialize moment values
    moment_values = []
    
    print("\n   Step 3.1: Calculate moment at each point of interest")
    
    # Calculate moment at each x-value
    for x in x_values:
        # Start with reaction at left support
        moment = R1 * x
        print(f"\n   At x = {x:.3f} ft:")
        print(f"     R1 contribution = {R1:.2f} × {x:.3f} = {R1 * x:.3f} kip-ft")
        
        # Subtract point loads to the left of x
        for P, pos in zip(point_loads, point_load_positions):
            if pos < x:
                point_moment = P * (x - pos)
                moment -= point_moment
                print(f"     P = {P:.2f} kips at x = {pos:.3f} ft, effect = -{P:.2f} × ({x:.3f} - {pos:.3f}) = -{point_moment:.3f} kip-ft")
        
        # Subtract uniform loads to the left of x
        for i, (w, (start, end)) in enumerate(zip(uniform_loads, uniform_load_regions)):
            if start < x:
                # If x is within the uniform load region
                if x <= end:
                    # The uniform load acts from start to x
                    length = x - start
                    centroid = start + length/2
                    load = w * length
                    uniform_moment = load * (x - centroid)
                    moment -= uniform_moment
                    print(f"     w{i+1} = {w:.2f} k/ft from x = {start:.3f} to {x:.3f} ft")
                    print(f"       Length = {length:.3f} ft, Centroid at x = {centroid:.3f} ft")
                    print(f"       Total load = {w:.2f} × {length:.3f} = {load:.3f} kips")
                    print(f"       Effect = -{load:.3f} × ({x:.3f} - {centroid:.3f}) = -{uniform_moment:.3f} kip-ft")
                
                # If x is beyond the uniform load region
                else:
                    # The uniform load acts from start to end
                    length = end - start
                    centroid = start + length/2
                    load = w * length
                    uniform_moment = load * (x - centroid)
                    moment -= uniform_moment
                    print(f"     w{i+1} = {w:.2f} k/ft from x = {start:.3f} to {end:.3f} ft")
                    print(f"       Length = {length:.3f} ft, Centroid at x = {centroid:.3f} ft")
                    print(f"       Total load = {w:.2f} × {length:.3f} = {load:.3f} kips")
                    print(f"       Effect = -{load:.3f} × ({x:.3f} - {centroid:.3f}) = -{uniform_moment:.3f} kip-ft")
        
        print(f"     Total moment at x = {x:.3f} ft: M = {moment:.3f} kip-ft")
        moment_values.append(moment)
    
    # Find maximum moment
    max_moment = max(moment_values)
    max_moment_index = moment_values.index(max_moment)
    max_moment_position = x_values[max_moment_index]
    
    # Check if maximum moment occurs at a zero-shear point
    at_zero_shear = False
    closest_zero_shear = None
    closest_distance = float('inf')
    
    for zero_x in zero_shear_points:
        if abs(zero_x - max_moment_position) < 0.001:  # Threshold for considering "at zero shear"
            at_zero_shear = True
            break
        # Find the closest zero-shear point
        if abs(zero_x - max_moment_position) < closest_distance:
            closest_distance = abs(zero_x - max_moment_position)
            closest_zero_shear = zero_x
    
    print("\n   Step 3.2: Locate maximum moment")
    print(f"   Maximum moment = {max_moment:.3f} kip-ft at x = {max_moment_position:.3f} ft")
    
    if at_zero_shear:
        print("   Maximum moment occurs at a zero-shear point, which confirms the theoretical expectation.")
    elif zero_shear_points:
        print(f"   Note: Closest zero-shear point is at x = {closest_zero_shear:.3f} ft, {closest_distance:.3f} ft away.")
        print("   Small difference may be due to calculation precision or load distribution.")
        # At ends or under point loads, maximum moment may not occur at zero shear
        if max_moment_position in point_load_positions or max_moment_position in (0, span_length):
            print("   Maximum moment occurs at a point load or support location, not at zero shear.")
    
    return x_values, moment_values, max_moment, max_moment_position

def plot_beam_diagrams(span_length, R1, R2, point_loads, point_load_positions, uniform_loads, uniform_load_regions,
                      x_shear, shear_values, x_dense, shear_dense, zero_shear_points,
                      x_moment, moment_values, max_moment_position):
    """Plot the beam, shear diagram, and moment diagram."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), gridspec_kw={'height_ratios': [1, 1, 1]})
    
    # Plot beam with loads
    ax1.plot([0, span_length], [0, 0], 'k-', linewidth=3)  # Beam
    ax1.plot([0, 0], [-0.1, 0.1], 'k-', linewidth=2)  # Left support
    ax1.plot([span_length, span_length], [-0.1, 0.1], 'k-', linewidth=2)  # Right support
    
    # Add reactions
    ax1.text(0, -0.2, f"R1={R1:.2f}k", ha='center', color='blue')
    ax1.text(span_length, -0.2, f"R2={R2:.2f}k", ha='center', color='blue')
    
    # Add point loads
    for P, pos in zip(point_loads, point_load_positions):
        ax1.arrow(pos, 0.5, 0, -0.4, head_width=0.1, head_length=0.05, fc='red', ec='red', linewidth=2)
        ax1.text(pos, 0.6, f"{P:.2f}k", ha='center', color='red')
    
    # Add uniform loads
    for w, (start, end) in zip(uniform_loads, uniform_load_regions):
        # Draw uniform load
        spacing = min(0.2, (end - start) / 5)
        positions = np.arange(start, end + spacing/2, spacing)
        for pos in positions:
            ax1.arrow(pos, 0.3, 0, -0.2, head_width=0.05, head_length=0.03, fc='green', ec='green', linewidth=1)
        # Draw horizontal line
        ax1.plot([start, end], [0.3, 0.3], 'g-', linewidth=2)
        # Add label
        ax1.text((start + end)/2, 0.4, f"{w:.2f}k/ft", ha='center', color='green')
    
    ax1.set_title("Beam with Loads and Reactions")
    ax1.set_xlim(-0.5, span_length + 0.5)
    ax1.set_ylim(-0.5, 1.0)
    ax1.set_ylabel("Load")
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_axisbelow(True)
    ax1.set_xticklabels([])
    
    # Plot shear diagram
    ax2.plot(x_dense, shear_dense, 'b-', linewidth=2)
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=1)
    
    # Mark zero-shear points
    for zero_x in zero_shear_points:
        ax2.plot(zero_x, 0, 'ro', markersize=6)
        ax2.text(zero_x, -0.5, f"Zero at\nx={zero_x:.2f}", ha='center', va='top', color='red',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax2.set_title("Shear Force Diagram")
    ax2.set_xlim(-0.5, span_length + 0.5)
    y_max = max(abs(min(shear_dense)), abs(max(shear_dense))) * 1.2
    ax2.set_ylim(-y_max, y_max)
    ax2.set_ylabel("Shear (kips)")
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_axisbelow(True)
    ax2.set_xticklabels([])
    
    # Plot moment diagram
    ax3.plot(x_moment, moment_values, 'g-', linewidth=2)
    ax3.axhline(y=0, color='k', linestyle='-', linewidth=1)
    
    # Mark maximum moment
    max_index = moment_values.index(max(moment_values))
    max_x = x_moment[max_index]
    max_M = moment_values[max_index]
    ax3.plot(max_x, max_M, 'ro', markersize=6)
    ax3.text(max_x, max_M * 0.9, f"Max = {max_M:.2f} kip-ft\nat x={max_x:.2f}", ha='center', va='top',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    ax3.set_title("Moment Diagram")
    ax3.set_xlim(-0.5, span_length + 0.5)
    ax3.set_xlabel("Position along beam (ft)")
    ax3.set_ylabel("Moment (kip-ft)")
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.set_axisbelow(True)
    ax3.invert_yaxis()  # Convention: positive moment plots downward
    
    plt.tight_layout()
    plt.savefig("beam_analysis_diagrams.png", dpi=150, bbox_inches='tight')
    print("\n   Beam diagrams saved to 'beam_analysis_diagrams.png'")
    plt.close()

def perform_detailed_beam_analysis(span_length, point_loads, point_load_positions, uniform_loads, uniform_load_regions):
    """
    Perform a detailed beam analysis including reactions, shear, and moment calculations.
    
    Args:
        span_length: Length of beam span (ft)
        point_loads: List of point load magnitudes (kips)
        point_load_positions: List of point load positions from left support (ft)
        uniform_loads: List of uniform load magnitudes (k/ft)
        uniform_load_regions: List of tuples (start, end) for uniform load regions (ft)
    """
    print("\n" + "="*80)
    print("DETAILED BEAM ANALYSIS")
    print("="*80)
    print(f"Span Length: {span_length} ft")
    
    if point_loads:
        print("\nPoint Loads:")
        for i, (P, pos) in enumerate(zip(point_loads, point_load_positions)):
            print(f"  P{i+1} = {P} kips at x = {pos} ft")
    
    if uniform_loads:
        print("\nUniform Loads:")
        for i, (w, (start, end)) in enumerate(zip(uniform_loads, uniform_load_regions)):
            print(f"  w{i+1} = {w} k/ft from x = {start} ft to x = {end} ft")
    
    print("\n" + "-"*80)
    
    # Step 1: Calculate reactions
    R1, R2 = calculate_reactions(span_length, point_loads, point_load_positions, uniform_loads, uniform_load_regions)
    
    # Step 2: Calculate shear diagram and find zero-shear points
    x_shear, shear_values, zero_shear_points, x_dense, shear_dense = calculate_shear_diagram(
        span_length, R1, R2, point_loads, point_load_positions, uniform_loads, uniform_load_regions
    )
    
    # Step 3: Calculate moment diagram and find maximum moment
    x_moment, moment_values, max_moment, max_moment_position = calculate_moment_diagram(
        span_length, R1, zero_shear_points, point_loads, point_load_positions, uniform_loads, uniform_load_regions
    )
    
    # Step 4: Plot the diagrams
    plot_beam_diagrams(
        span_length, R1, R2, point_loads, point_load_positions, uniform_loads, uniform_load_regions,
        x_shear, shear_values, x_dense, shear_dense, zero_shear_points,
        x_moment, moment_values, max_moment_position
    )
    
    print("\n" + "="*80)
    print("SUMMARY OF RESULTS:")
    print("="*80)
    print(f"Reactions: R1 = {R1:.2f} kips, R2 = {R2:.2f} kips")
    
    if zero_shear_points:
        print("\nZero-Shear Points:")
        for i, zero_x in enumerate(zero_shear_points):
            print(f"  Point {i+1}: x = {zero_x:.3f} ft")
    else:
        print("\nNo zero-shear points within the span")
    
    print(f"\nMaximum Moment: {max_moment:.3f} kip-ft at x = {max_moment_position:.3f} ft")
    
    print("\nTHEORETICAL VERIFICATION:")
    print("Maximum moment occurs where shear changes sign (crosses zero).")
    if any(abs(zero_x - max_moment_position) < 0.01 for zero_x in zero_shear_points):
        print("This is confirmed by our calculations.")
    else:
        print("Note: In this case, the maximum moment might not occur exactly at a zero-shear point due to:")
        print("  - The beam may have non-continuous loading")
        print("  - Maximum moment may occur at a point load or beam end")
        print("  - Numerical approximation in calculations")
    
    print("\n" + "="*80)

# Example usage
if __name__ == "__main__":
    # Simple beam example: 16-ft span with point load and uniform load
    span_length = 16.0  # feet
    
    # Point loads (kips) and their positions (ft from left support)
    point_loads = [1.0, 0.5]
    point_load_positions = [2.0, 5.0]
    
    # Uniform loads (k/ft) and their regions (start, end) in ft from left support
    uniform_loads = [0.15, 0.7, 0.42]
    uniform_load_regions = [(0, 2), (2, 5), (5, 16)]
    
    # Perform analysis
    perform_detailed_beam_analysis(span_length, point_loads, point_load_positions, 
                                 uniform_loads, uniform_load_regions) 