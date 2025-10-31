from machine import Pin, PWM
from time import sleep, ticks_ms

EM_frequency = 18_000
EM_pwm_pct = 0.0
pwm_max = 65535


# Initialize the PWM signal pin
ledAndMagnet = Pin(10,Pin.OUT)
EM_pwm = PWM(ledAndMagnet)
EM_pwm.freq(EM_frequency)


pwm.duty_u16(int(pwm_pct*pwm_max))