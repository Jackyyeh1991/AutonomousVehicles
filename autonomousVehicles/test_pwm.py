duty_cycle = 7.4
duty_to_write = 200000 * duty_cycle
duty_to_write = int(duty_to_write)
with open('/dev/bone/pwm/1/a/duty_cycle', 'w') as filetowrite:
	filetowrite.write(str(duty_to_write))
