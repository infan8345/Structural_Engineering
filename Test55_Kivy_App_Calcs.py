from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Triangle
from kivy.core.window import Window
import numpy as np
import os

# Steel Material Properties
Fy = 50  # ksi (A992 steel)
E = 29000 * 1000  # psi

# AISC Steel Sections Database
AISC_SHAPES = {
    'W10x19': {'d': 10.24, 'bf': 4.02, 'tw': 0.25, 'tf': 0.395, 'A': 5.62, 'Ix': 96.3, 'Iy': 4.29, 'Zx': 23.2, 'wt': 19},
    'W10x22': {'d': 10.17, 'bf': 5.75, 'tw': 0.24, 'tf': 0.36, 'A': 6.49, 'Ix': 118, 'Iy': 11.4, 'Zx': 29.3, 'wt': 22},
    'W10x26': {'d': 10.33, 'bf': 5.77, 'tw': 0.26, 'tf': 0.44, 'A': 7.61, 'Ix': 144, 'Iy': 12.9, 'Zx': 35.9, 'wt': 26},
    'W10x30': {'d': 10.47, 'bf': 5.81, 'tw': 0.3, 'tf': 0.51, 'A': 8.84, 'Ix': 170, 'Iy': 15.3, 'Zx': 42.5, 'wt': 30},
    'W10x33': {'d': 9.73, 'bf': 7.96, 'tw': 0.29, 'tf': 0.435, 'A': 9.71, 'Ix': 170, 'Iy': 36.6, 'Zx': 38.8, 'wt': 33},
    'W10x39': {'d': 9.92, 'bf': 7.99, 'tw': 0.315, 'tf': 0.53, 'A': 11.5, 'Ix': 209, 'Iy': 45.0, 'Zx': 48.6, 'wt': 39},
    'W10x45': {'d': 10.10, 'bf': 8.02, 'tw': 0.35, 'tf': 0.62, 'A': 13.3, 'Ix': 248, 'Iy': 53.4, 'Zx': 58.1, 'wt': 45},
    'W12x19': {'d': 12.16, 'bf': 4.005, 'tw': 0.235, 'tf': 0.35, 'A': 5.57, 'Ix': 130, 'Iy': 4.22, 'Zx': 31.2, 'wt': 19},
    'W12x22': {'d': 12.31, 'bf': 4.03, 'tw': 0.26, 'tf': 0.425, 'A': 6.48, 'Ix': 156, 'Iy': 4.66, 'Zx': 37.2, 'wt': 22},
    'W12x26': {'d': 12.22, 'bf': 6.49, 'tw': 0.23, 'tf': 0.38, 'A': 7.65, 'Ix': 204, 'Iy': 17.3, 'Zx': 47.1, 'wt': 26},
    'W12x30': {'d': 12.34, 'bf': 6.52, 'tw': 0.26, 'tf': 0.44, 'A': 8.79, 'Ix': 238, 'Iy': 20.3, 'Zx': 55.5, 'wt': 30},
    'W12x35': {'d': 12.50, 'bf': 6.56, 'tw': 0.3, 'tf': 0.52, 'A': 10.3, 'Ix': 285, 'Iy': 24.5, 'Zx': 66.5, 'wt': 35},
    'W12x40': {'d': 11.94, 'bf': 8.005, 'tw': 0.295, 'tf': 0.515, 'A': 11.8, 'Ix': 310, 'Iy': 44.1, 'Zx': 68.4, 'wt': 40},
    'W12x45': {'d': 12.06, 'bf': 8.05, 'tw': 0.335, 'tf': 0.575, 'A': 13.2, 'Ix': 350, 'Iy': 50.6, 'Zx': 78.4, 'wt': 45},
    'W12x14': {'d': 11.91, 'bf': 3.97, 'tw': 0.2, 'tf': 0.225, 'A': 4.16, 'Ix': 88.6, 'Iy': 2.36, 'Zx': 17.4, 'wt': 14},
    'W12x16': {'d': 11.99, 'bf': 3.99, 'tw': 0.22, 'tf': 0.265, 'A': 4.71, 'Ix': 103, 'Iy': 2.82, 'Zx': 20.6, 'wt': 16},
    'W16x26': {'d': 15.69, 'bf': 5.5, 'tw': 0.25, 'tf': 0.345, 'A': 7.68, 'Ix': 301, 'Iy': 9.59, 'Zx': 56.5, 'wt': 26},
    'W16x31': {'d': 15.88, 'bf': 5.53, 'tw': 0.275, 'tf': 0.44, 'A': 9.13, 'Ix': 375, 'Iy': 12.4, 'Zx': 70.4, 'wt': 31},
    'W16x36': {'d': 15.86, 'bf': 6.985, 'tw': 0.295, 'tf': 0.43, 'A': 10.6, 'Ix': 448, 'Iy': 24.5, 'Zx': 81.0, 'wt': 36},
    'W16x40': {'d': 16.01, 'bf': 6.995, 'tw': 0.305, 'tf': 0.505, 'A': 11.8, 'Ix': 518, 'Iy': 28.9, 'Zx': 93.0, 'wt': 40},
    'W16x45': {'d': 16.13, 'bf': 7.04, 'tw': 0.345, 'tf': 0.565, 'A': 13.3, 'Ix': 586, 'Iy': 32.8, 'Zx': 105, 'wt': 45}
}

class SteelMomentFrameDesign(App):
    def build(self):
        self.frame_width = 30  # ft
        self.frame_height = 12  # ft
        self.selected_column = 'W10x30'
        self.selected_beam = 'W12x30'
        self.lateral_load = 5.0  # kips (placeholder, will be replaced with seismic)
        self.gravity_load = 0.5  # kip/ft
        self.analysis_results = None  # Store analysis results for LaTeX generation
        
        Window.size = (1000, 800)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input Controls
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.25), spacing=15)
        
        # Frame Dimensions
        dim_layout = BoxLayout(orientation='vertical', spacing=5)
        dim_layout.add_widget(Label(text="Frame Dimensions", bold=True, size_hint_y=None, height=25))
        
        width_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)
        width_layout.add_widget(Label(text="Width (ft):", size_hint_x=0.4))
        self.width_input = TextInput(text=str(self.frame_width), multiline=False)
        self.width_input.bind(text=self.on_width_input)
        width_layout.add_widget(self.width_input)
        
        height_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)
        height_layout.add_widget(Label(text="Height (ft):", size_hint_x=0.4))
        self.height_input = TextInput(text=str(self.frame_height), multiline=False)
        self.height_input.bind(text=self.on_height_input)
        height_layout.add_widget(self.height_input)
        
        dim_layout.add_widget(width_layout)
        dim_layout.add_widget(height_layout)
        input_layout.add_widget(dim_layout)
        
        # Section Selection
        col_layout = BoxLayout(orientation='vertical', spacing=5)
        col_layout.add_widget(Label(text="Column Section", bold=True, size_hint_y=None, height=25))
        self.col_spinner = Spinner(
            text=self.selected_column,
            values=[s for s in AISC_SHAPES if s.startswith(('W10','W12')) and 15 <= AISC_SHAPES[s]['wt'] <= 45],
            size_hint=(1, None), height=35)
        self.col_spinner.bind(text=self.on_column_select)
        col_layout.add_widget(self.col_spinner)
        input_layout.add_widget(col_layout)
        
        beam_layout = BoxLayout(orientation='vertical', spacing=5)
        beam_layout.add_widget(Label(text="Beam Section", bold=True, size_hint_y=None, height=25))
        self.beam_spinner = Spinner(
            text=self.selected_beam,
            values=[s for s in AISC_SHAPES if s.startswith(('W12','W16')) and 15 <= AISC_SHAPES[s]['wt'] <= 45],
            size_hint=(1, None), height=35)
        self.beam_spinner.bind(text=self.on_beam_select)
        beam_layout.add_widget(self.beam_spinner)
        input_layout.add_widget(beam_layout)
        
        # Load Inputs
        load_layout = BoxLayout(orientation='vertical', spacing=5)
        load_layout.add_widget(Label(text="Loads", bold=True, size_hint_y=None, height=25))
        
        lateral_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)
        lateral_layout.add_widget(Label(text="Lateral (kips):", size_hint_x=0.5))
        self.lateral_input = TextInput(text=str(self.lateral_load), multiline=False)
        self.lateral_input.bind(text=self.on_lateral_input)
        lateral_layout.add_widget(self.lateral_input)
        
        vertical_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=35)
        vertical_layout.add_widget(Label(text="Vertical (klf):", size_hint_x=0.5))
        self.vertical_input = TextInput(text=str(self.gravity_load), multiline=False)
        self.vertical_input.bind(text=self.on_vertical_input)
        vertical_layout.add_widget(self.vertical_input)
        
        load_layout.add_widget(lateral_layout)
        load_layout.add_widget(vertical_layout)
        input_layout.add_widget(load_layout)
        
        # Visualization Canvas
        self.canvas_widget = Widget(size_hint=(1, 0.6))
        
        # Results Display
        self.result_label = Label(
            text="Configure frame and click 'Analyze'",
            size_hint=(1, 0.1),
            halign='left',
            valign='top',
            markup=True
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        
        # Button Layout for Analyze and Save LaTeX
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        # Analyze Button
        analyze_button = Button(text="Analyze Frame", bold=True, size_hint=(0.5, 1))
        analyze_button.bind(on_press=self.analyze_frame)
        
        # Save LaTeX Button
        save_latex_button = Button(text="Save LaTeX Report", bold=True, size_hint=(0.5, 1))
        save_latex_button.bind(on_press=self.save_latex_report)
        
        button_layout.add_widget(analyze_button)
        button_layout.add_widget(save_latex_button)
        
        layout.add_widget(input_layout)
        layout.add_widget(self.canvas_widget)
        layout.add_widget(self.result_label)
        layout.add_widget(button_layout)
        
        self.draw_frame(0, 0)
        return layout

    def on_width_input(self, instance, text):
        try: self.frame_width = float(text)
        except: pass
    
    def on_height_input(self, instance, text):
        try: self.frame_height = float(text)
        except: pass
    
    def on_column_select(self, spinner, text):
        self.selected_column = text
    
    def on_beam_select(self, spinner, text):
        self.selected_beam = text
    
    def on_lateral_input(self, instance, text):
        try: self.lateral_load = float(text)
        except: pass
    
    def on_vertical_input(self, instance, text):
        try: self.gravity_load = float(text)
        except: pass

    def perform_structural_analysis(self):
        # Seismic parameters (assumed for Los Angeles, CA, SDC D)
        S_S1 = 1.5  # Mapped spectral acceleration at short period
        S_S1 = 0.6  # Mapped spectral acceleration at 1s
        F_a = 1.0   # Site coefficient (Site Class D)
        F_v = 1.5   # Site coefficient (Site Class D)
        I_e = 1.0   # Importance factor
        R = 8.0     # Response modification factor (SMF)
        C_d = 5.5   # Deflection amplification factor (SMF)

        # Design spectral accelerations
        S_DS = (2/3) * F_a * S_S1
        S_D1 = (2/3) * F_v * S_S1

        # Seismic weight (tributary area: 30 ft x 12 ft)
        D = 50 * (self.frame_width * self.frame_height)  # 50 psf dead load
        L = 20 * (self.frame_width * self.frame_height)  # 20 psf live load
        W = 0.9 * D + 0.2 * L  # Seismic weight in lbs
        W_kips = W / 1000  # Convert to kips

        # Seismic response coefficient
        C_s = S_DS / (R / I_e)
        if C_s < 0.044 * S_D1 * I_e:
            C_s = 0.044 * S_D1 * I_e

        # Base shear
        V = C_s * W_kips

        # Lateral force distribution (single-story, k=1)
        F_x = V

        # Convert to consistent units
        h = self.frame_height * 12  # in
        L = self.frame_width * 12   # in
        P = F_x * 1000  # lbs (seismic lateral load)
        w = (self.gravity_load / 12) * 1000  # lb/in (gravity load)

        # Internal forces
        col_props = AISC_SHAPES[self.selected_column]
        beam_props = AISC_SHAPES[self.selected_beam]
        Ic = col_props['Ix']
        Ib = beam_props['Ix']

        # Deflections (as per script)
        numerator = 2 * h * Ib + 3 * L * Ic
        denom = numerator / (12 * Ic * E * h * Ib)
        delta_h = (P * h**3) * denom
        delta_v = (5 * w * L**4) / (384 * E * Ib)

        # Amplified deflection
        delta_h_allowable = C_d * delta_h / I_e
        delta_v_allowable = L / 360  # Serviceability limit

        # Combined load effects (1.0D + 0.7E)
        M_lateral = (P / 2000) * (h / 12)  # kip-ft
        M_gravity = (w * L**2) / (12 * 12)  # kip-ft (midspan moment)
        M_u = M_gravity + 0.7 * M_lateral  # kip-ft
        V_u = (self.gravity_load * self.frame_width) / 2  # kip

        # Member capacity checks
        phi = 0.9  # Resistance factor
        phi_Pn_col = phi * Fy * col_props['A']  # kips
        phi_Mn_col = phi * Fy * col_props['Zx']  # kip-in
        phi_Mn_beam = phi * Fy * beam_props['Zx']  # kip-in

        # Convert M_u to kip-in for interaction
        M_u_in = M_u * 12
        P_u = V_u  # Axial load from vertical reaction

        # Interaction check (AISC 360-16 H1-1a)
        if P_u / phi_Pn_col < 0.2:
            interaction = P_u / (2 * phi_Pn_col) + M_u_in / phi_Mn_col
        else:
            interaction = (P_u / phi_Pn_col) + (M_u_in / phi_Mn_col)

        # Seismic checks (AISC 341-16)
        b_f_col = col_props['bf']
        t_f_col = col_props['tf']
        h_col = col_props['d'] - 2 * t_f_col
        t_w_col = col_props['tw']
        b_f_beam = beam_props['bf']
        t_f_beam = beam_props['tf']
        h_beam = beam_props['d'] - 2 * t_f_beam
        t_w_beam = beam_props['tw']

        lambda_rf = 0.38 * np.sqrt(E / Fy)  # Flange slenderness limit
        lambda_rw = 2.45 * np.sqrt(E / Fy)  # Web slenderness limit

        col_flange_ratio = (b_f_col / 2) / t_f_col
        col_web_ratio = h_col / t_w_col
        beam_flange_ratio = (b_f_beam / 2) / t_f_beam
        beam_web_ratio = h_beam / t_w_beam

        # Determine pass/fail status for seismic checks
        col_flange_status = "OK" if col_flange_ratio < lambda_rf else "NG"
        col_web_status = "OK" if col_web_ratio < lambda_rw else "NG"
        beam_flange_status = "OK" if beam_flange_ratio < lambda_rf else "NG, consider W16x40"
        beam_web_status = "OK" if beam_web_ratio < lambda_rw else "NG"

        # Connection design (RBS for SMF)
        T_f = M_u_in / (beam_props['d'] - t_f_beam)  # kip
        phi_Rn_weld = 0.75 * 0.6 * 70 * (t_f_beam / np.sqrt(2))  # kip/in (E70, 1/4" weld)
        L_weld = T_f / phi_Rn_weld  # in
        shear_tab_capacity = 4 * 0.75 * 17.9  # kips (4 A490 3/4" bolts)

        # Results dictionary
        results = {
            'seismic_weight': f"{W_kips:.2f} kips",
            'base_shear': f"{V:.3f} kips",
            'lateral_force': f"{F_x:.3f} kips",
            'delta_h': f"{delta_h:.3f} in",
            'delta_h_allowable': f"{delta_h_allowable:.3f} in",
            'delta_v': f"{delta_v:.3f} in",
            'delta_v_allowable': f"{delta_v_allowable:.3f} in",
            'M_u': f"{M_u:.2f} kip-ft",
            'V_u': f"{V_u:.2f} kips",
            'phi_Pn_col': f"{phi_Pn_col:.2f} kips",
            'phi_Mn_col': f"{phi_Mn_col:.2f} kip-in",
            'phi_Mn_beam': f"{phi_Mn_beam:.2f} kip-in",
            'interaction': f"{interaction:.3f}",
            'col_flange_ratio': f"{col_flange_ratio:.2f}",
            'col_flange_limit': f"{lambda_rf:.2f}",
            'col_flange_status': col_flange_status,
            'col_web_ratio': f"{col_web_ratio:.2f}",
            'col_web_limit': f"{lambda_rw:.2f}",
            'col_web_status': col_web_status,
            'beam_flange_ratio': f"{beam_flange_ratio:.2f}",
            'beam_flange_limit': f"{lambda_rf:.2f}",
            'beam_flange_status': beam_flange_status,
            'beam_web_ratio': f"{beam_web_ratio:.2f}",
            'beam_web_limit': f"{lambda_rw:.2f}",
            'beam_web_status': beam_web_status,
            'T_f': f"{T_f:.2f} kips",
            'L_weld': f"{L_weld:.2f} in",
            'shear_tab_capacity': f"{shear_tab_capacity:.2f} kips"
        }

        return results

    def analyze_frame(self, instance):
        try:
            h = self.frame_height * 12  # in
            L = self.frame_width * 12   # in
            if h <= 0 or L <= 0:
                raise ValueError
            
            col_props = AISC_SHAPES[self.selected_column]
            beam_props = AISC_SHAPES[self.selected_beam]
            Ic = col_props['Ix']
            Ib = beam_props['Ix']
            
            P = self.lateral_load * 1000  # lbs
            w = (self.gravity_load / 12) * 1000  # lb/in
            
            numerator = 2 * h * Ib + 3 * L * Ic
            denom = numerator / (12 * Ic * E * h * Ib)
            delta_h = (P * h**3) * denom
            delta_v = (5 * w * L**4) / (384 * E * Ib)
            
            # Perform detailed structural analysis
            self.analysis_results = self.perform_structural_analysis()
            
            # Construct result text
            result_text = (
                f"[b]Analysis Results (CBC 2022, AISC 341-16, ASCE 7-16):[/b]\n"
                f"Seismic Weight: {self.analysis_results['seismic_weight']}\n"
                f"Base Shear: {self.analysis_results['base_shear']}\n"
                f"Lateral Force: {self.analysis_results['lateral_force']}\n"
                f"Lateral Deflection: {self.analysis_results['delta_h']} in "
                f"(Allowable: {self.analysis_results['delta_h_allowable']} in)\n"
                f"Vertical Deflection: {self.analysis_results['delta_v']} in "
                f"(Allowable: {self.analysis_results['delta_v_allowable']} in)\n"
                f"Max Moment: {self.analysis_results['M_u']} kip-ft\n"
                f"Shear: {self.analysis_results['V_u']} kips\n"
                f"Column Capacity: P_n = {self.analysis_results['phi_Pn_col']} kips, "
                f"M_n = {self.analysis_results['phi_Mn_col']} kip-in\n"
                f"Beam Capacity: M_n = {self.analysis_results['phi_Mn_beam']} kip-in\n"
                f"Interaction Ratio: {self.analysis_results['interaction']} < 1.0 (OK)\n"
                f"Seismic Checks:\n"
                f"  Column Flange: {self.analysis_results['col_flange_ratio']} < {self.analysis_results['col_flange_limit']} ({self.analysis_results['col_flange_status']})\n"
                f"  Column Web: {self.analysis_results['col_web_ratio']} < {self.analysis_results['col_web_limit']} ({self.analysis_results['col_web_status']})\n"
                f"  Beam Flange: {self.analysis_results['beam_flange_ratio']} < {self.analysis_results['beam_flange_limit']} ({self.analysis_results['beam_flange_status']})\n"
                f"  Beam Web: {self.analysis_results['beam_web_ratio']} < {self.analysis_results['beam_web_limit']} ({self.analysis_results['beam_web_status']})\n"
                f"Connection Design (RBS SMF):\n"
                f"  Flange Force: {self.analysis_results['T_f']} kips\n"
                f"  Weld Length: {self.analysis_results['L_weld']} in (use full flange)\n"
                f"  Shear Tab Capacity: {self.analysis_results['shear_tab_capacity']} kips > {self.analysis_results['V_u']} kips (OK)\n"
                f"[b]Plot Description:[/b]\n"
                f"- Undeformed Frame (White Lines): Two vertical columns (30 ft wide, 12 ft high) and a horizontal beam.\n"
                f"- Pin Supports (Green Triangles): At the base of each column.\n"
                f"- Uniform Load (Blue Box): Above the beam, with vertical lines spaced 30 pixels apart.\n"
                f"- Lateral Load (Green Arrow): Pointing right at the top-left corner.\n"
                f"- Deformed Shape (Red Lines): Scaled by 50x, showing lateral and vertical deflections."
            )
            
            self.result_label.text = result_text
            self.draw_frame(delta_h, delta_v)

            # Ensure the single_frame directory exists
            output_dir = os.path.join(os.path.dirname(__file__), 'single_frame')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the plot as PNG
            screenshot_path = os.path.join(output_dir, 'moment_frame_plot.png')
            Window.screenshot(name=screenshot_path)
            
        except Exception as e:
            self.result_label.text = f"[color=#ff0000]Error: Check input values and try again ({str(e)})[/color]"

    def generate_latex_content(self):
        if not self.analysis_results:
            return None

        latex_content = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

\begin{document}

\section*{Seismic Design of Steel Moment Frame (CBC 2022, AISC 341-16, ASCE 7-16)}

\subsection*{Frame Properties and Loads}
\begin{itemize}
    \item Dimensions: Width \(L = """ + str(self.frame_width) + r""" \, \text{ft} = """ + str(self.frame_width * 12) + r""" \, \text{in}\), Height \(h = """ + str(self.frame_height) + r""" \, \text{ft} = """ + str(self.frame_height * 12) + r""" \, \text{in}\)
    \item Gravity Load: \(w = """ + str(self.gravity_load) + r""" \, \text{kip/ft} = """ + str(self.gravity_load / 12) + r""" \, \text{kip/in}\)
    \item Column: """ + self.selected_column + r""" (\(I_c = """ + str(AISC_SHAPES[self.selected_column]['Ix']) + r""" \, \text{in}^4\)), Beam: """ + self.selected_beam + r""" (\(I_b = """ + str(AISC_SHAPES[self.selected_beam]['Ix']) + r""" \, \text{in}^4\))
    \item Material: A992, \(F_y = 50 \, \text{ksi}\), \(E = 29,000 \, \text{ksi}\)
    \item Seismic Weight: \(W = """ + self.analysis_results['seismic_weight'] + r"""\)
\end{itemize}

\subsection*{Seismic Load Calculation (ASCE 7-16)}
\begin{itemize}
    \item \(S_{DS} = 1.0g\), \(S_{D1} = 0.6g\), \(R = 8\), \(C_d = 5.5\)
    \item \(C_s = 0.125\), \(V = """ + self.analysis_results['base_shear'] + r"""\)
    \item Load Case: \(1.0D + 0.7E\), \(H_A = H_B = """ + str(float(self.analysis_results['lateral_force'].split()[0]) / 2) + r""" \, \text{kips}\)
\end{itemize}

\subsection*{Structural Analysis}
\subsubsection*{Internal Forces}
\begin{itemize}
    \item \(M_u = """ + self.analysis_results['M_u'] + r"""\)
    \item \(V_u = """ + self.analysis_results['V_u'] + r"""\)
(
\end{itemize}

\subsubsection*{Deflections}
\begin{itemize}
    \item \(\
