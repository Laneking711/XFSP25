# region imports
from Air import AirStandardCycle
import numpy as np
# endregion

class dualCycleController():
    def __init__(self):
        self.model = AirStandardCycle()
        self.widgets = []

    def setWidgets(self, w):
        self.widgets = w

    def calc(self):
        # Parse input widgets
        THigh = float(self.widgets[5].text())
        TLow = float(self.widgets[6].text())
        P0 = float(self.widgets[7].text())
        V0 = float(self.widgets[8].text())
        CR = float(self.widgets[9].text())

        # Example extra dual cycle params (you may want to expose in UI later)
        rc = 1.2               # cutoff ratio
        rp = 1.5               # pressure ratio (P3/P2)
        gamma = 1.4            # assume air

        # T1 and P1
        T1 = TLow
        P1 = P0 * 101.325      # convert atm to kPa if needed
        V1 = V0
        V2 = V1 / CR

        # Process 1-2: isentropic compression
        T2 = T1 * (CR)**(gamma - 1)
        P2 = P1 * (CR)**gamma

        # Process 2-3: constant volume heat addition
        T3 = T2 * rp
        V3 = V2
        P3 = P2 * (T3 / T2)

        # Process 3-4: constant pressure heat addition
        V4 = rc * V3
        T4 = T3 * (V4 / V3)
        P4 = P3

        # Process 4-5: isentropic expansion
        V5 = V1
        T5 = T4 * (V4 / V5)**(1 - gamma)
        P5 = P4 * (V4 / V5)**gamma

        # Process 5-1: constant volume heat rejection

        # Calculate work and efficiency
        cv = 0.718
        cp = 1.005
        q_in = cv * (T3 - T2) + cp * (T4 - T3)
        q_out = cv * (T5 - T1)
        w_net = q_in - q_out
        eta = w_net / q_in * 100  # %

        # Update output widgets
        self.widgets[10].setText(f"{T1:.2f}")
        self.widgets[11].setText(f"{T2:.2f}")
        self.widgets[12].setText(f"{T3:.2f}")
        self.widgets[13].setText(f"{T4:.2f}")
        self.widgets[18].setText(f"{w_net:.2f}")
        self.widgets[19].setText(f"{cv*(T2-T1):.2f}")  # Compression stroke
        self.widgets[20].setText(f"{q_in:.2f}")        # Heat added
        self.widgets[21].setText(f"{eta:.2f}")

        self.updateView()

    def updateView(self):
        # Get selected x/y variables from UI
        x_choice = self.widgets[24].currentText()
        y_choice = self.widgets[25].currentText()
        logx = self.widgets[26].isChecked()
        logy = self.widgets[27].isChecked()

        # Prepare dummy curve data
        states = [1, 2, 3, 4, 5]
        T = [float(self.widgets[10].text()), float(self.widgets[11].text()),
             float(self.widgets[12].text()), float(self.widgets[13].text()), float(self.widgets[10].text())]
        P = [100, 200, 300, 250, 100]
        v = [1.0, 0.1, 0.1, 0.15, 1.0]

        x = {'T': T, 'P': P, 'v': v, 'u': T, 'h': T, 's': T}[x_choice]
        y = {'T': T, 'P': P, 'v': v, 'u': T, 'h': T, 's': T}[y_choice]

        ax = self.widgets[28]
        ax.clear()
        ax.plot(x, y, marker='o')

        if logx: ax.set_xscale('log')
        if logy: ax.set_yscale('log')

        ax.set_xlabel(x_choice)
        ax.set_ylabel(y_choice)
        self.widgets[29].draw()
