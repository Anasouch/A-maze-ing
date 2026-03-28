import sys


class TokenError(Exception):
    pass


class InvalidConf(Exception):
    pass


class InvalidKey(InvalidConf):
    pass


class InvalidValue(InvalidConf):
    pass


def comment_index(s: str) -> int:
    i = 0
    for c in s:
        if c == '#':
            return i
        i += 1
    return -1


def parsing() -> dict[str, str]:
    try:
        if len(sys.argv) != 2:
            raise TokenError(
                "Invalid tokens <python3 a_maze_ing.py config.txt>"
                )

        with open("config.txt", "r") as file:
            get_conf = file.read().split("\n")
            conf_lists = []
            conf_dict = {}

            for s in get_conf:
                if s.strip() != "" and s.strip()[0] != '#':
                    conf_lists.append(s.split("="))

            for a_list in conf_lists:
                if '#' in a_list[1]:
                    i = comment_index(a_list[1])
                    a_list[1] = a_list[1][:i]
                conf_dict[a_list[0].upper().strip()] = a_list[1].strip()

            keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                    "OUTPUT_FILE", "PERFECT", "SEED"]
            for k in conf_dict.keys():
                if k not in keys:
                    raise InvalidKey(f"Invalid config '{k}', is not a key")

            width = int(conf_dict["WIDTH"])
            height = int(conf_dict["HEIGHT"])
            entry = conf_dict["ENTRY"].split(",")
            en1 = int(entry[0])
            en2 = int(entry[1])
            exit = conf_dict["EXIT"].split(",")
            ex1 = int(exit[0])
            ex2 = int(exit[1])
            booleen = ["True", "False"]

            if conf_dict["PERFECT"] not in booleen:
                raise InvalidValue(
                    f"Invalid config '{conf_dict["PERFECT"]}', is not a value"
                    )

            if "SEED" in conf_dict:
                int(conf_dict["SEED"])
            else:
                conf_dict["SEED"] = "42"

            if width <= 0 or height <= 0:
                raise InvalidValue(
                    "Invalid config, width and height must be greater than '0'"
                    )

            if (
                ((en1 < 0) or (en2 < 0))
                or ((ex1 < 0) or (ex2 < 0))
            ):
                raise InvalidValue(
                    "Invalid config, cordinates must be positive"
                    )

            if (
                ((en1 >= width) or (en2 >= height))
                or ((ex1 >= width) or (ex2 >= height))
            ):
                raise InvalidValue(
                    "Invalid config, cordinate is out of range"
                    )

            if entry == exit:
                raise InvalidValue(
                    "Invalid config, Entry and Exit must be different"
                    )
    except Exception as e:
        print(f"Error: {e}")
        conf_dict = {}
    return conf_dict


if __name__ == "__main__":
    print(parsing())
