# sector.py -- Sector class definition and related functions
#
# Copyright (c) 2020 Steve Simenic <orffen@orffenspace.com>
#
# This file is part of the Cepheus Engine Toolbox and is licensed
# under the MIT license - see LICENSE for details.

from dice import *
from world import *
from typing import Dict
import sys


class Sector(object):
    """Holds worlds in a sector. If no 'hexes' provided, will generate a
    subsector instead.

    Keyword arguments:
    hexes -- a Dict[str, World] containing the sectors with worlds in them
    subsector -- by letter A-P, used to specify hexes when generating a sector
    """
    def __init__(self, hexes: Dict[str, World] = None, subsector: str = "A"):
        self.subsector = subsector if subsector <= "P" else "A"
        self.hexes = self.generate_sector() if hexes is None else hexes

    def __str__(self):
        # Hex, Name, UWP, Bases, Remarks, Travel Zone, PBG, Allegiance
        # Width 80:
        # - Hex:         4
        # - Name:        15
        # - UWP:         9
        # - Bases:       1
        # - Remarks:     38
        # - Travel Zone: 1
        # - PBG:         3
        # - Allegiance:  2
        # - (spaces):    7
        line1 = ("{:<4} {:<15} {:<11} {}".format("Hex",
                                                 "Name",
                                                 "Statistics",
                                                 "Remarks"))
        r = []
        for hx, world in self.hexes.items():
            r.append("{} {:<15} {} {} {:<38} {} {} {}".format(
                hx,
                world.name,
                world.uwp,
                world.bases,
                " ".join(world.remarks),
                world.travel_zone,
                world.pbg,
                world.allegiance
            ))
        return "{}\n{}".format(line1, "\n".join(r))

    def generate_sector(self) -> Dict[str, World]:
        start = {
            "A": (1, 1),  "B": (9, 1),  "C": (17, 1),  "D":(25, 1),
            "E": (1, 11), "F": (9, 11), "G": (17, 11), "H": (25, 11),
            "I": (1, 21), "J": (9, 21), "K": (17, 21), "L": (25, 21),
            "M": (1, 31), "N": (9, 31), "O": (17, 31), "P": (25, 31)}
        r = {}
        for i in range(start[self.subsector][0], start[self.subsector][0] + 8):
            for j in range(start[self.subsector][1],
                           start[self.subsector][1] + 10):
                if roll_dice(1) >= 4:
                    r["{:02d}{:02d}".format(i, j)] = World()
        return r


if __name__ == "__main__":
    print(Sector())
