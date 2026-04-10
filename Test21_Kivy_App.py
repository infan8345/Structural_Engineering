import numpy as np

# Global constants
SAWN_E = 1.6e6  # psi, modulus of elasticity for sawn lumber
F = 1.0  # Adjustment factor (default)
ft_to_in = 12
kip_to_lb = 1000

# Global variables
L0 = [0, 5.00, 16.00, 5.00]  # Span lengths (ft)
N = [0, 1, 2, 1]  # Number of point loads
M = [0, 2, 3, 2]  # Number of uniform load segments
P = [[0]*8, [0]*8, [0]*8, [0]*8]  # Point loads (kips)
L = [[0]*8, [0]*8, [0]*8, [0]*8]  # Point load locations (ft)
W = [[0]*4, [0]*4, [0]*4, [0]*4]  # Uniform load magnitudes (k/ft)
L1 = [[0]*4, [0]*4, [0]*4, [0]*4]  # Uniform load segment lengths (ft)
R1 = [0, 0, 0, 0]  # Left reactions (kips)
R2 = [0, 0, 0, 0]  # Right reactions (kips)
M1 = [0, 0, 0, 0]  # Maximum moments (kip-ft)
D1 = [0, 0, 0, 0]  # Deflections (in)
I_req = [0, 0, 0, 0]  # Required moments of inertia (in^4)
MATERIAL = "SAWN"
B_real = 5.5  # Beam width (in), default to 8x14
D_real = 11.5  # Beam depth (in)

def input_loads():
    """Initialize load configuration based on provided input."""
    # Span 1 (Left Cantilever)
    P[1][2] = 0.64  # Point load at 3 ft
    L[1][2] = 3.00
    W[1][1] = 0.32  # Uniform load 0 to 3 ft
    L1[1][1] = 3.00
    W[1][2] = 0.60  # Uniform load 3 to 5 ft
    L1[1][2] = 2.00
    L[1][3] = 5.00  # End of span

    # Span 2 (Main Span)
    P[2][2] = 1.00  # Point load at 2 ft
    L[2][2] = 2.00
    P[2][3] = 0.50  # Point load at 5 ft
    L[2][3] = 5.00
    W[2][1] = 0.15  # Uniform load 0 to 2 ft
    L1[2][1] = 2.00
    W[2][2] = 0.70  # Uniform load 2 to 5 ft
    L1[2][2] = 3.00
    W[2][3] = 0.42  # Uniform load 5 to 16 ft
    L1[2][3] = 11.00
    L[2][4] = 16.00  # End of span

    # Span 3 (Right Cantilever)
    P[3][2] = 2.00  # Point load at 3 ft
    L[3][2] = 3.00
    W[3][1] = 0.20  # Uniform load 0 to 3 ft
    L1[3][1] = 3.00
    W[3][2] = 0.60  # Uniform load 3 to 5 ft
    L1[3][2] = 2.00
    L[3][3] = 5.00  # End of span

def calculate_reactions():
    """Calculate reaction forces for all spans."""
    global R1, R2
    if L0[1] > 0:
        R1[1] = sum(P[1][i] for i in range(2, M[1]+1)) + sum(W[1][i] * L1[1][i] for i in range(1, M[1]+1))
        print(f"Left Cantilever R1={R1[1]:.2f} kips")
    if L0[3] > 0:
        R2[3] = sum(P[3][i] for i in range(2, M[3]+1)) + sum(W[3][i] * L1[3][i] for i in range(1, M[3]+1))
        print(f"Right Cantilever R2={R2[3]:.2f} kips")
    if L0[2] > 0:
        sum_moments = sum(P[2][i] * (L0[2] - L[2][i]) for i in range(2, M[2]+1))
        sum_moments += sum(W[2][i] * L1[2][i] * (L0[2] - (sum(L1[2][j] for j in range(1, i)) + L1[2][i]/2)) for i in range(1, M[2]+1))
        sum_loads = sum(P[2][i] for i in range(2, M[2]+1)) + sum(W[2][i] * L1[2][i] for i in range(1, M[2]+1))
        R1[2] = sum_moments / L0[2]
        R2[2] = sum_loads - R1[2]
        print(f"Main Span R1={R1[2]:.2f}, R2={R2[2]:.2f}, Sum Moments={sum_moments:.2f}, Sum Loads={sum_loads:.2f}")

def calculate_moments():
    """Calculate maximum moments for all spans."""
    global M1
    if L0[1] > 0:
        M1[1] = sum(P[1][i] * L[1][i] for i in range(2, M[1]+1)) + \
                sum(W[1][i] * L1[1][i] * (sum(L1[1][j] for j in range(1, i)) + L1[1][i]/2) for i in range(1, M[1]+1))
        print(f"Left Cantilever M1={M1[1]:.2f} kip-ft")
    if L0[3] > 0:
        M1[3] = sum(P[3][i] * L[3][i] for i in range(2, M[3]+1)) + \
                sum(W[3][i] * L1[3][i] * (sum(L1[3][j] for j in range(1, i)) + L1[3][i]/2) for i in range(1, M[3]+1))
        print(f"Right Cantilever M1={M1[3]:.2f} kip-ft")
    if L0[2] > 0:
        max_moment = 0
        shear = R1[2]
        x_zero = 0
        for j in range(1, M[2]+1):
            seg_start = sum(L1[2][k] for k in range(1, j)) if j > 1 else 0
            seg_end = seg_start + L1[2][j]
            for i in range(2, M[2]+1):
                if L[2][i] <= seg_end:
                    shear -= P[2][i]
            if shear > 0 and W[2][j] > 0:
                x_zero = seg_start + shear / W[2][j]
                if seg_start <= x_zero <= seg_end:
                    break
            shear -= W[2][j] * L1[2][j]
        x_values = [0] + [L[2][i] for i in range(2, M[2]+1) if L[2][i] > 0] + [x_zero, L0[2]]
        x_values = sorted(list(set([x for x in x_values if 0 <= x <= L0[2]])))
        try:
            x_values += list(np.arange(0, L0[2] + 0.1, 0.1))
        except NameError:
            x_values += [i/10 for i in range(int(L0[2]*10) + 1)]
        x_values = sorted(list(set(x_values)))
        for x in x_values:
            moment = R1[2] * x
            for j in range(2, M[2]+1):
                if L[2][j] <= x:
                    moment -= P[2][j] * (x - L[2][j])
            for j in range(1, M[2]+1):
                seg_start = sum(L1[2][k] for k in range(1, j)) if j > 1 else 0
                seg_end = seg_start + L1[2][j]
                if seg_end <= x:
                    moment -= W[2][j] * L1[2][j] * (x - (seg_start + L1[2][j]/2))
                elif seg_start < x < seg_end:
                    partial_length = x - seg_start
                    moment -= W[2][j] * partial_length * (x - (seg_start + partial_length/2))
            max_moment = max(max_moment, moment)
        M1[2] = max_moment
        print(f"Main Span M1={M1[2]:.2f} kip-ft")

def validate_size(B, D, material):
    """Validate beam size and return properties using actual dimensions."""
    if material == "SAWN":
        valid_B = [2, 4, 6, 8]
        valid_D = [8, 10, 12, 14]
        actual_B = {2: 1.5, 4: 3.5, 6: 5.5, 8: 7.5}  # Nominal to actual width (in)
        actual_D = {8: 7.5, 10: 9.5, 12: 11.5, 14: 13.5}  # Nominal to actual depth (in)
        if B in valid_B and D in valid_D:
            B_act = actual_B[B]
            D_act = actual_D[D]
            I = (B_act * D_act**3) / 12
            S = (B_act * D_act**2) / 6
            M_capacity = (1200 * S) / 12000  # kip-ft, Fb = 1200 psi
            print(f"validate_size: B={B} ({B_act}), D={D} ({D_act}), I={I:.1f}, S={S:.1f}, M_capacity={M_capacity:.2f}")
            return {'I': I, 'S': S, 'M_capacity': M_capacity}
        else:
            print(f"Warning: Invalid B={B} or D={D} for sawn lumber")
    return {'I': 0, 'S': 0, 'M_capacity': 0}


def select_beam():
    """Select the smallest beam satisfying moment and inertia requirements."""
    global B_real, D_real
    max_moment = max(M1)
    max_I_req = max(I_req)
    valid_B = [2, 4, 6, 8]
    valid_D = [8, 10, 12, 14]
    selected_B = 0
    selected_D = 0
    best_I = float('inf')
    
    for B in valid_B:
        for D in valid_D:
            size_data = validate_size(B, D, MATERIAL)
            if size_data['M_capacity'] >= max_moment and size_data['I'] >= max_I_req:
                if size_data['I'] < best_I:
                    selected_B = B
                    selected_D = D
                    best_I = size_data['I']
    
    # If no beam meets criteria, use default 8x14 and warn user
    if selected_B == 0:
        print("Warning: No beam meets moment and inertia requirements. Defaulting to 8x14.")
        selected_B, selected_D = 8, 14
    
    size_data = validate_size(selected_B, selected_D, MATERIAL)
    print(f"Selected Beam: Sawn {selected_B}x{selected_D}, Capacity={size_data['M_capacity']:.2f} kip-ft, I={size_data['I']:.1f}")
    B_real, D_real = selected_B, selected_D
    return selected_B, selected_D

def main():
    """Main execution function."""
    print("Starting beam analysis...")
    input_loads()
    calculate_reactions()
    calculate_moments()
    calculate_required_inertia()
    global B_real, D_real
    B_real, D_real = select_beam()
    print("\nFinal Results:")
    print(f"Left Cantilever: R1={R1[1]:.2f} kips, M1={M1[1]:.2f} kip-ft")
    print(f"Main Span: R1={R1[2]:.2f}, R2={R2[2]:.2f}, M1={M1[2]:.2f} kip-ft")
    print(f"Right Cantilever: R2={R2[3]:.2f} kips, M1={M1[3]:.2f} kip-ft")
    print(f"Span 1: Deflection={D1[1]:.2f} in, I_req={I_req[1]:.2f}")
    print(f"Span 2: Deflection={D1[2]:.2f} in, I_req={I_req[2]:.2f}")
    print(f"Span 3: Deflection={D1[3]:.2f} in, I_req={I_req[3]:.2f}")
    size_data = validate_size(B_real, D_real, MATERIAL)
    print(f"Beam Sizing: Sawn {B_real}x{D_real}, Capacity={size_data['M_capacity']:.2f} kip-ft, I={size_data['I']:.1f}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Exception: {str(e)}")
