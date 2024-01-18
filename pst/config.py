from __future__ import annotations
import typing as t

import json
import os

class Config:
    
    data: dict[t.Any, t.Any]
    name: str
    fp: str
    
    def __init__(self, filepath: str, name: str = None) -> None:
        
        self.fp = filepath
        self.name = name or filepath.rstrip(".json")
        self.reload()
    
    
    def reload(self) -> None:
        """Re-updates the config from its save file"""
        with open(self.fp, "r") as f:
            self.data = dict(json.load(f))
        

    def get(self, key: str, default: t.Any = None) -> t.Any:
        """Retrieves a value from a target key

        Args:
            key (str): Key to get value from
            default (Any, optional): Default value. Defaults to None.

        Returns:
            Any: Config value from key
        """
        try:
            return self.data[key]
        except:
            return default
    
    def set(self, key: str, value: t.Any, save: bool = True) -> t.Any:
        """Sets a configuration object at a key to a value

        Args:
            key (str): Target key
            value (Any): Value to set
            save (bool, optional): Weather to save to object file after update. Defaults to True.

        Returns:
            t.Any: The value that was set
        """
        self.data[key] = value
        if save:
            self.save()
        return value
    
    def update_dict(self, new_dict: dict, save: bool = True) -> None:
        """Merges config dict with a new dict, useful for updating values en mass

        Args:
            new_dict (dict): Dict containing all new keys and values
            save (bool, optional): Weather to save to object file after update. Defaults to True.
        """
        self.data = self.data | new_dict
        if save:
            self.save()

    def save(self) -> None:
        """Saves the current dict to the source file"""
        with open(self.fp, "w+") as f:
            json.dump(self.data, f, indent=4)
    
    @property
    def length(self) -> int:
        """Returns the number of keys in the config

        Returns:
            int: The number of keys
        """
        return len(self.data.keys())

    @property
    def keys(self) -> list[str]:
        """Returns all keys as a list

        Returns:
            list[str]: All config keys
        """
        return list(self.data.keys())


# PST Terminal base config
CONFIG = Config("pst/base_config.json")
CONFIG.fp = "current_config.json"
if not os.path.exists("current_config.json"):
    CONFIG.save()
else:
    CONFIG.reload()