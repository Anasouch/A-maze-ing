from typing import Dict, Any, Optional
import sys


class TokenError(Exception):
    pass


class InvalidConf(Exception):
    pass


class MissingConf(Exception):
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

            for line in get_conf:
                if line.strip() != "" and line.strip()[0] != '#':
                    conf_lists.append(line.split("=", 1))

            for a_list in conf_lists:
                if len(a_list) == 1:
                    raise InvalidConf(
                        "Invalid config, it does not respect "
                        "the 'KEY=VALUE' format"
                        )
                if '#' in a_list[1]:
                    i = comment_index(a_list[1])
                    a_list[1] = a_list[1][:i]
                conf_dict[a_list[0].upper().strip()] = a_list[1].strip()

            keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                    "OUTPUT_FILE", "PERFECT", "SEED"]
            for k in conf_dict.keys():
                if k not in keys:
                    raise InvalidConf(f"Invalid config '{k}', is not a key")
            keys.remove("SEED")
            for k in keys:
                if k not in list(conf_dict.keys()):
                    raise MissingConf(f"Missing the '{k}' config")

            width = conf_dict["WIDTH"]
            height = conf_dict["HEIGHT"]
            entry = conf_dict["ENTRY"]
            exit = conf_dict["EXIT"]
            output_file = conf_dict["OUTPUT_FILE"]
            perfect = conf_dict["PERFECT"]
            if "SEED" in conf_dict:
                seed = conf_dict["SEED"]

            width = conf_dict["WIDTH"] = int(width)
            height = conf_dict["HEIGHT"] = int(height)
            if width < 9 or height < 7:
                raise InvalidConf(
                    "Invalid config, min dimensions is [WIDTH=9, HEIGHT=7]"
                    )

            entry = entry.split(",")
            en1 = int(entry[0])
            en2 = int(entry[1])
            entry = conf_dict["ENTRY"] = (en1, en2)

            exit = exit.split(",")
            ex1 = int(exit[0])
            ex2 = int(exit[1])
            exit = conf_dict["EXIT"] = (ex1, ex2)

            if len(entry) != 2 or len(exit) != 2:
                raise InvalidConf(
                    "Invalid config, Entry and Exit must include 2 coordinates"
                    )

            if ('/' in output_file) or ("\\" in output_file):
                raise InvalidConf(
                    f"Invalid config {output_file}, "
                    "file name must not include '/' or double '\\'"
                    )
            if (output_file == "..") or (output_file == "."):
                raise InvalidConf(
                    f"Invalid config '{output_file}', it is a directory"
                    )

            booleen = ["True", "False"]
            if perfect not in booleen:
                raise InvalidConf(
                    f"Invalid config '{perfect}', is not a value"
                    )
            if perfect == "True":
                conf_dict["PERFECT"] = True
            else:
                conf_dict["PERFECT"] = False

            if "SEED" in conf_dict:
                conf_dict["SEED"] = int(seed)
            else:
                conf_dict["SEED"] = None

            if width <= 0 or height <= 0:
                raise InvalidConf(
                    "Invalid config, width and height must be greater than '0'"
                    )

            if (
                ((en1 < 0) or (en2 < 0))
                or ((ex1 < 0) or (ex2 < 0))
            ):
                raise InvalidConf(
                    "Invalid config, coordinates must be positive"
                    )

            if (
                ((en1 >= width) or (en2 >= height))
                or ((ex1 >= width) or (ex2 >= height))
            ):
                raise InvalidConf(
                    "Invalid config, a coordinate is out of range"
                    )

            if entry == exit:
                raise InvalidConf(
                    "Invalid config, Entry and Exit must be different"
                    )
    except Exception as e:
        print(f"ERROR: {e}")
        return None
    return conf_dict
