from pathlib import Path

def get_simulated_app_root():
    app_root = Path(__file__).parent.parent.absolute().as_posix()
    return app_root


if __name__ == "__main__":
    print(get_simulated_app_root())
