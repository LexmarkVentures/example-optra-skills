import time
import gpiod
from gpiod.line import Direction, Value



def main():
    CHIP = "/dev/gpiochipUSR"
    LINES = [0, 1, 2, 3, 4, 5, 6]  # First 7 pins
    SLEEP_TIME = 0.5  # Delay between LED changes

    # Configure the GPIO lines
    config = {
        line: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE)
        for line in LINES
    }

    print("GPIO Loop Starting")

    with gpiod.request_lines(CHIP, consumer="HW-Test-Skil", config=config) as request:
        while True:
            try:
                # Move to the right
                for i in range(7):
                    # Set the current line to INACTIVE and the previous one to ACTIVE (inverted)
                    request.set_value(i, Value.INACTIVE)
                    if i > 0:
                        request.set_value(i - 1, Value.ACTIVE)
                    time.sleep(SLEEP_TIME)
                # Move to the left
                for i in range(5, -1, -1):
                    # Set the current line to INACTIVE and the next one to ACTIVE (inverted)
                    request.set_value(i, Value.INACTIVE)
                    if i < 6:
                        request.set_value(i + 1, Value.ACTIVE)
                    time.sleep(SLEEP_TIME)
            except gpiod.error as e:
                # Reset all pins to ACTIVE on exit (inverted)
                for line in LINES:
                    request.set_value(line, Value.ACTIVE)


if __name__ == '__main__':
    main()