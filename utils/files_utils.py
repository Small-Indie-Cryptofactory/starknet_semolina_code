import csv
import json
import os
from typing import Optional, Union


def join_path(path: Union[str, tuple, list]) -> str:
    if isinstance(path, str):
        return path

    return os.path.join(*path)


def touch(path: Union[str, tuple, list], file: bool = False) -> bool:
    path = join_path(path)
    if file:
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write('')

            return True

        return False

    if not os.path.isdir(path):
        os.mkdir(path)
        return True

    return False


def write_json(path: Union[str, tuple, list], obj: Union[list, dict], indent: Optional[int] = None,
               encoding: Optional[str] = None) -> None:
    path = join_path(path)
    with open(path, mode='w', encoding=encoding) as f:
        json.dump(obj, f, indent=indent)


def read_json(path: Union[str, tuple, list], encoding: Optional[str] = None) -> Union[list, dict]:
    path = join_path(path)
    return json.load(open(path, encoding=encoding))


def read_lines(path: Union[str, tuple, list], skip_empty_rows: bool = False, encoding: Optional[str] = None) -> list:
    path = join_path(path)
    with open(path, encoding=encoding) as f:
        lines = f.readlines()

    lines = [line.rstrip() for line in lines]
    if skip_empty_rows:
        lines = list(filter(lambda a: a, lines))

    return lines


def write_row_to_csv_file(path: str, row: list):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(row)
