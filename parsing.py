from typing import Dict, Any, Optional
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


def pars() -> Optional[Dict[str, Any]]:
    try:
        if len(sys.argv) != 2:
            raise TokenError(
                "Invalid tokens <python3 a_maze_ing.py config.txt>"
                )

        with open(sys.argv[1]) as file:
            get_conf = file.read().split("\n")
            conf_lists = []
            conf_dict: Dict[str, Any] = {}

            for s in get_conf:
                if s.strip() != "" and s.strip()[0] != '#':
                    conf_lists.append(s.split("=", 1))

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
            if "SEED" in keys:
                keys.remove("SEED")
            for k in keys:
                if k not in conf_dict.keys():
                    raise InvalidKey(f"Missing the '{k}' config")

            conf_dict["WIDTH"] = int(conf_dict["WIDTH"])
            width = conf_dict["WIDTH"]

            conf_dict["HEIGHT"] = int(conf_dict["HEIGHT"])
            height = conf_dict["HEIGHT"]

            entry = conf_dict["ENTRY"].split(",")
            en1 = int(entry[0])
            en2 = int(entry[1])
            conf_dict["ENTRY"] = (en1, en2)

            exit = conf_dict["EXIT"].split(",")
            ex1 = int(exit[0])
            ex2 = int(exit[1])
            conf_dict["EXIT"] = (ex1, ex2)

            if len(entry) != 2 or len(exit) != 2:
                raise InvalidValue(
                    "Invalid config, Entry and Exit must include 2 cordinates"
                    )

            if (
                '/' in conf_dict["OUTPUT_FILE"]
                or "\\" in conf_dict["OUTPUT_FILE"]
            ):
                raise InvalidValue(
                    f"Invalid config {conf_dict["OUTPUT_FILE"]}, "
                    "file name must not include '/' or double '\\'"
                    )
            if (
                conf_dict["OUTPUT_FILE"] == ".."
                or conf_dict["OUTPUT_FILE"] == "."
            ):
                raise InvalidValue(
                    f"Invalid config '{conf_dict["OUTPUT_FILE"]}', "
                    "it is a directory"
                    )

            booleen = ["True", "False"]
            if conf_dict["PERFECT"] not in booleen:
                raise InvalidValue(
                    f"Invalid config '{conf_dict["PERFECT"]}', is not a value"
                    )
            conf_dict["PERFECT"] = bool(conf_dict["PERFECT"])

            if "SEED" in conf_dict:
                conf_dict["SEED"] = int(conf_dict["SEED"])
            else:
                conf_dict["SEED"] = None

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
                    "Invalid config, a cordinate is out of range"
                    )

            if conf_dict["ENTRY"] == conf_dict["EXIT"]:
                raise InvalidValue(
                    "Invalid config, Entry and Exit must be different"
                    )
    except Exception as e:
        print(f"Error: {e}")
        return None
    return conf_dict
