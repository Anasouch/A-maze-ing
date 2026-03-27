import sys


class TokenError(Exception):
    pass


class InvalidConf(Exception):
    pass


def parsing() -> dict:
    try:
        if len(sys.argv) != 2:
            raise TokenError("Invalid tokens <python3 a_maze_ing.py config.txt>")
        with open("config.txt", "r") as file:
            get_conf = file.read().split("\n")
            conf_lists = []
            conf_dict = {}
            for s in get_conf:
                if s.strip() != "" and s.strip()[0] != '#':
                    conf_lists.append(s.split("="))
            for a_list in conf_lists:
                # if '#' in a_list[1]:
                conf_dict[a_list[0].upper().strip()] = a_list[1].upper().strip()
            i = 0
            keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"]
            for k in conf_dict.keys():
                if  k not in keys:
                    raise InvalidConf(f"Invalid config '{k}'")
    except Exception as e:
        print(f"Error: {e}")
    if "SEED" not in conf_dict:
        conf_dict["SEED"] = 42
    return conf_dict


if __name__ == "__main__":
    print(parsing())