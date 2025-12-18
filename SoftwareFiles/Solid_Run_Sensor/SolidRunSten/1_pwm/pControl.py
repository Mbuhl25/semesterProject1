# pController.py
# Optimized P-controller for MicroPython

import micropython
import array

# --------------------------------------------------
# Native-optimized weighted sum function
# --------------------------------------------------
@micropython.native
def _weighted_sum(adc, positions, weights):
    weight_sum = 0.0
    adc_sum = 0

    length = len(adc)
    for i in range(length):
        v = adc[i]
        adc_sum += v
        weight_sum += v * positions[i] * weights[i]

    if adc_sum != 0:
        weight_sum /= adc_sum

    return weight_sum


# --------------------------------------------------
# P-Controller class
# --------------------------------------------------
class pController:
    def __init__(self, kp=1.0):
        # Sensor positions (signed)
        self.positions = array.array('b', [-4, -3, -2, -1, 1, 2, 3, 4])

        # Sensor weights
        self.weights = array.array(
            'f',
            [3.2, 3.5, 2.0, 1.0, 1.0, 2.0, 3.5, 3.2]
        )

        # Proportional gain
        self.kp = kp

        self.control = 0.0

    def findError(self, current_adc_list):
        sensor_sum = _weighted_sum(
            current_adc_list,
            self.positions,
            self.weights
        )
        # Setpoint = 0
        return -sensor_sum

    def findControl(self, current_adc_list):
        return self.kp * self.findError(current_adc_list)

    @micropython.native
    def adjustStep(self, base_step, current_adc_list):
        control = self.findControl(current_adc_list)

        new_step_left = base_step + control
        new_step_right = base_step - control

        # Clamp values
        if new_step_left < 0.0:
            new_step_left = 0.0
        elif new_step_left > base_step:
            new_step_left = base_step

        if new_step_right < 0.0:
            new_step_right = 0.0
        elif new_step_right > base_step:
            new_step_right = base_step

        return new_step_left, new_step_right
