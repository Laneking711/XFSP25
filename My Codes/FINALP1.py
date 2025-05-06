import sys
import numpy as np
from scipy.integrate import quad
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QFormLayout)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class TakeoffModel:
    """Model class handling the takeoff distance calculations"""

    def __init__(self):
        # Constants (English units)
        self.rho = 0.002377  # air density (slug/ft^3)
        self.S = 1000  # wing area (ft^2)
        self.C_Lmax = 2.4  # maximum lift coefficient
        self.C_D = 0.0279  # drag coefficient
        self.gc = 32.2  # gravitational constant (lbm·ft/lbf·s^2)

    def calculate_sto(self, weight, thrust):
        """Calculate takeoff distance for given weight and thrust"""
        # Calculate stall speed
        V_stall = np.sqrt(2 * weight / (self.rho * self.S * self.C_Lmax))

        # Takeoff speed (1.2 × V_stall)
        V_TO = 1.2 * V_stall

        # Calculate A and B parameters
        A = self.gc * (thrust / weight)
        B = (self.gc / weight) * (0.5 * self.rho * self.S * self.C_D)

        # Integrate to find takeoff distance
        integrand = lambda V: V / (A - B * V ** 2)
        S_TO, _ = quad(integrand, 0, V_TO)

        return S_TO


class TakeoffView(QMainWindow):
    """View class handling the GUI presentation"""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Airplane Takeoff Distance Calculator")
        self.setGeometry(100, 100, 800, 600)

        # Create main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QHBoxLayout(self.main_widget)

        # Create input panel
        self.input_panel = QWidget()
        self.input_layout = QFormLayout(self.input_panel)

        # Weight input
        self.weight_label = QLabel("Weight (lb):")
        self.weight_input = QLineEdit("56000")
        self.input_layout.addRow(self.weight_label, self.weight_input)

        # Thrust input
        self.thrust_label = QLabel("Thrust (lb):")
        self.thrust_input = QLineEdit("13000")
        self.input_layout.addRow(self.thrust_label, self.thrust_input)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.input_layout.addRow(self.calculate_button)

        # Matplotlib figure
        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Add widgets to main layout
        self.layout.addWidget(self.input_panel, 1)
        self.layout.addWidget(self.canvas, 3)
        self.layout.addWidget(self.toolbar, 0)

        # Connect button to controller
        self.calculate_button.clicked.connect(self.controller.handle_calculate)

    def get_input_values(self):
        """Get input values from the GUI"""
        try:
            weight = float(self.weight_input.text())
            thrust = float(self.thrust_input.text())
            return weight, thrust
        except ValueError:
            return None, None

    def plot_results(self, thrust_values, sto_values, current_thrust, current_sto, weight):
        """Plot the takeoff distance results"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Plot the three lines
        for i, (w, label) in enumerate(zip(weight, ['Weight', 'Weight -10k', 'Weight +10k'])):
            ax.plot(thrust_values, sto_values[i], label=f"{label} ({w:.0f} lb)")

        # Mark the current point
        ax.plot(current_thrust, current_sto, 'ro', markersize=8,
                label=f'Current: {current_sto:.1f} ft')

        ax.set_xlabel('Thrust (lb)')
        ax.set_ylabel('Takeoff Distance (ft)')
        ax.set_title('Takeoff Distance vs. Thrust')
        ax.grid(True)
        ax.legend()

        self.canvas.draw()


class TakeoffController:
    """Controller class handling user input and model updates"""

    def __init__(self):
        self.model = TakeoffModel()
        self.view = TakeoffView(self)

    def handle_calculate(self):
        """Handle calculate button click"""
        weight, thrust = self.view.get_input_values()

        if weight is None or thrust is None:
            return  # Invalid input

        # Calculate for current weight and ±10,000 lb
        weights = [weight, weight - 10000, weight + 10000]

        # Generate thrust range (80% to 120% of current thrust)
        thrust_min = 0.8 * thrust
        thrust_max = 1.2 * thrust
        thrust_values = np.linspace(thrust_min, thrust_max, 20)

        # Calculate S_TO for all combinations
        sto_values = []
        for w in weights:
            sto_for_weight = [self.model.calculate_sto(w, t) for t in thrust_values]
            sto_values.append(sto_for_weight)

        # Calculate current S_TO
        current_sto = self.model.calculate_sto(weight, thrust)

        # Update the view
        self.view.plot_results(thrust_values, sto_values, thrust, current_sto, weights)

    def show(self):
        """Show the view"""
        self.view.show()


def main():
    app = QApplication(sys.argv)
    controller = TakeoffController()
    controller.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()