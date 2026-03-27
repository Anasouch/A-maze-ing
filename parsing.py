import sys


class TokenError(Exception):
    pass


def parsing() -> dict:
    try:
        if len(sys.argv) != 2:
            raise TokenError("Invalid tokens (python3 a_maze_ing.py config.txt)")
        with open("config.txt", "r") as file:
            conf_str = file.read()
            print(conf_str)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parsing()