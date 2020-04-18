# dice.py -- Dice class definition and related functions
#
# Copyright (c) 2020 Steve Simenic <orffen@orffenspace.com>
#
# This file is part of the Cepheus Engine Toolbox and is licensed
# under the MIT license - see LICENSE for details.

from typing import List
import math
import random
import sys


class Dice(object):
    def __init__(self):
        self.result: int = 0
        self.rolls: List[int] = []

    def __str__(self):
        return "Last roll: {} = {}".format(self.rolls, self.result)

    def roll(self, number: int = 2) -> int:
        """Roll a number of dice (2 by default) and return the result

        Also stores the result in self.result, and each individual die roll
        in self.rolls.

        Keyword arguments:
        number -- number of dice to roll (default 2)
        """
        self.rolls = []
        for _ in range(number):
            self.rolls.append(random.randint(1, 6))
        self.result = sum(self.rolls)
        return self.result

def roll_dice(number: int = 2):
    """Roll a number of dice (2 by default) and return the result"""
    d = Dice()
    return d.roll(number)


if __name__ == "__main__":
    try:
        number = int(sys.argv[1])
    except:
        number = 2
    d = Dice()
    d.roll(number)
    print(d)
