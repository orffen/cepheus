# pseudohex.py -- functions to convert to/from pseudohex
#
# Copyright (c) 2020 Steve Simenic <orffen@orffenspace.com>
#
# This file is part of the Cepheus Engine Toolbox and is licensed
# under the MIT license - see LICENSE for details.

def to_pseudohex(value: int) -> str:
    pseudohex = (
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D",
        "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z"
    )
    return pseudohex[value]

def from_pseudohex(value: str) -> int:
    pseudohex = (
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D",
        "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z"
    )
    return pseudohex.index(value.upper())

def pseudohex(value):
    if type(value) is int:
        return to_pseudohex(value)
    elif type(value) is str:
        return from_pseudohex(value)
    else:
        raise ValueError("Can only convert int and str types to pseudohex!")
