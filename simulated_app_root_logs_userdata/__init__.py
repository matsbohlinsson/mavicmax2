from pathlib import Path

def get_simulated_app_root():
    return Path(__file__).parent.absolute().as_posix()


if __name__ == "__main__":
    print(get_simulated_app_root())
