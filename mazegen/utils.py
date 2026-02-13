#!/usr/bin/env python3

from typing import Dict, Any

"""
This module provides functions to read and parse a configurate file.
The configuration file should have key=value pairs, optionally with comments
starting with '#' and empty lines.
"""


def get_raw_config(file_path: str) -> Dict[str, str]:
    # Reads the configuration file and returns a dictionary of strings.
    raw_data = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for i, line in enumerate(file, start=1):
                line = line.strip()
                # Ignore empty lines or comments
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    # Split only once at the first '='
                    key, value = line.split("=", 1)
                    value = value.strip()
                    key = key.strip()
                    if not key:
                        raise Exception(
                            f"ignored (empty key): {line}")
                    raw_data[key] = value
    except FileNotFoundError:
        print(f"Error: the file {file_path} does not exist.")
        return {}
    except Exception as e:
        print(f"[Error] Line {i} not processed: {line}\nDetail:{e}")
        return {}
    return raw_data


def format_value(key: str, value: str) -> Any:
    # Converts a string value to the appropriate Python type based on the key.
    try:
        if key in ("WIDTH", "HEIGHT"):
            n = int(value)
            if n <= 0:
                raise ValueError(f"{key} must be a positive number")
            if key == "WIDTH" and n < 7:
                raise ValueError(
                    "WIDTH is too small for the stencil (minimum 7).")
            if key == "HEIGHT" and n < 5:
                raise ValueError(
                    "HEIGHT is too small for the stencil (minimum 5).")
            return n
        elif key in ("ENTRY", "EXIT"):
            parts = value.split(",")
            if len(parts) != 2:
                raise ValueError(f"Invalid value for {key}: {value}")
            value = (int(parts[0]), int(parts[1]))
            return value
        elif key == "PERFECT":
            value = (value.lower() == "true")
        # Default: keep as string
        return value
    except ValueError as e:
        print(f"Error converting {key}=‘{value}’: {e}")
        # Returns None if it can't convert
        return None


def format_config(raw_data: Dict[str, str]) -> Dict[str, Any]:
    # Receives the string dictionary and returns the correct types.
    return {
        key: format_value(key, value) for key, value in raw_data.items()
    }


def parse_config(file_path: str) -> Dict[str, Any]:
    # Main funciton that coordinates reading and formatting.
    raw = get_raw_config(file_path)
    return format_config(raw)


# if __name__ == "__main__":
#     # Quick test to see if it works
#     config = parse_config("../config.txt")
#     print(config)
