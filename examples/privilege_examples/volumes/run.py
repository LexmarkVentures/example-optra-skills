import time

VOLUME_PATH = "/app/volume_ex_skill"

def read_counter_value_from_file():
    try:
        with open(f"{VOLUME_PATH}/counter.txt", "r") as file:
            counter = int(file.read().strip())
            print(f"Read counter value from volume: {counter}")
            return counter
    except FileNotFoundError:
        print(f"Counter file not found, initializing counter to 0.")
        return 0
    except ValueError:
        print(f"Invalid counter value found, initializing counter to 0.")
        return 0

def write_counter_value_to_file(counter):
    with open(f"{VOLUME_PATH}/counter.txt", "w") as file:
        file.write(str(counter))

def main():
    counter = read_counter_value_from_file()

    while True:
        print(f"Printing counter value: {counter}")
        counter += 1

        write_counter_value_to_file(counter)
        time.sleep(10)

if __name__ == '__main__':
    main()