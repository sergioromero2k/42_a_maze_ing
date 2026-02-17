#!/usr/bin/env python3

from typing import Dict, Any
import sys

"""
This module provides functions to read and parse a configurate file.
The configuration file should have key=value pairs, optionally with comments
starting with '#' and empty lines.
"""


class ConfigError(Exception):
    # Custom exception for configuration errors
    pass


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
            if value.lower() == "true":
                value = True
            else:
                raise ValueError("PERFECT must be true")
        # Default: keep as string
        return value
    except ValueError as e:
        print(f"Error converting {key}=‘{value}’: {e}")
        # The program will end and close.
        sys.exit(1)


def format_config(raw_data: Dict[str, str]) -> Dict[str, Any]:
    # Receives the string dictionary and returns the correct types.
    return {
        key.lower(): format_value(key, value) for key, value in raw_data.items()
    }


def validate_logic(config: Dict[str, Any]) -> bool:
    # Validate the main configuration: ensures WIDTH, HEIGHT, ENTRY, and EXIT
    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit_ = config["exit"]

    # Basic sanity check: width and height must exist and not be empty/zero.
    if not width or not height:
        raise ConfigError("Config.txt is missing WIDTH or HEIGHT")

    # Validate that ENTRY coordinates are inside the map boundaries.
    # entry[0] is row (y), entry[1] is col (x)
    if not (0 <= entry[0] < height):
        raise ConfigError(f"Entry ROW out of map: {entry[0]} with height = {height}")
    if not (0 <= entry[1] < width):
        raise ConfigError(f"Entry COL out of map: {entry[1]} with width = {width}")

    # Validate that EXIT coordinates are inside the map boundaries.
    # exit_[0] is row (y), exit_[1] is col (x)
    if not (0 <= exit_[0] < height):
        raise ConfigError(f"Exit ROW out of map: {exit_[0]} with height = {height}")
    if not (0 <= exit_[1] < width):
        raise ConfigError(f"Exit COL out of map: {exit_[1]} with width = {width}")

    return True


def parse_config(file_path: str) -> Dict[str, Any]:
    # Main funciton that coordinates reading and formatting.
    raw = get_raw_config(file_path)
    raw_data = format_config(raw)
    try:
        validate_logic(raw_data)
    except ConfigError as e:
        print("Configuration error: ", e)
        sys.exit(1)
    return raw_data


# if __name__ == "__main__":
#     # Quick test to see if it works
#     config = parse_config("../config.txt")
#     print(config)
