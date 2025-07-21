import time
import os

def main():
    while True:
        env_var = os.environ.get('EXAMPLE_ENV_VAR', 'Not Set')
        print(f"Environment Variable: {env_var}")
        time.sleep(10)

if __name__ == '__main__':
    main()