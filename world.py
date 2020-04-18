# world.py -- World class definition and related functions
#
# Copyright (c) 2020 Steve Simenic <orffen@orffenspace.com>
#
# This file is part of the Cepheus Engine Toolbox and is licensed
# under the MIT license - see LICENSE for details.

from dice import *
from pseudohex import *
from typing import List, Tuple
import sys


class World(object):
    """Holds the attributes of a world. Most keyword arguments that are None
    will be automatically generated.

    For example, if you only provide a name and travel_zone, a random world
    will be generated including UWP, bases, trade codes, the PBG values, with
    a default allegiance of "Na"

    remarks will accept a list of remarks, if None will automatically
    populate trade codes.
    """
    def __init__(self,
                 name: str = "Erehwemos",
                 uwp: str = None,
                 bases: str = None,
                 remarks: List[str] = None,
                 travel_zone: str = None,
                 pbg: str = None,
                 allegiance: str = "Na"):
        self.name = name
        if uwp is None:
            self.world_size = roll_dice() - 2
            self.atmosphere = self.generate_atmosphere()
            self.hydrographics = self.generate_hydrographics()
            self.population = self.generate_population()
            self.population_modifier = self.generate_population_modifier()
            self.starport = self.generate_starport()
            self.government = self.generate_government()
            self.law_level = self.generate_law_level()
            self.technology_level = self.generate_technology_level()
            self.uwp = generate_uwp(
                self.starport,
                self.world_size,
                self.atmosphere,
                self.hydrographics,
                self.population,
                self.government,
                self.law_level,
                self.technology_level
            )
        else:
            (self.starport, self.world_size, self.atmosphere,
             self.hydrographics, self.population, self.government,
             self.law_level, self.technology_level) = parse_uwp(self.uwp)
        if bases is None:
            self.naval_base = self.generate_naval_base()
            self.scout_base = self.generate_scout_base()
            self.pirate_base = self.generate_pirate_base()
            self.bases = generate_base_code(self.naval_base,
                                            self.scout_base,
                                            self.pirate_base)
        else:
            (self.naval_base,
             self.scout_base,
             self.pirate_base) = parse_bases(bases)
        self.remarks = \
            self.generate_trade_codes() \
            if remarks is None else remarks
        self.travel_zone = self.generate_travel_zone() if travel_zone is None \
            else travel_zone
        if pbg is None:
            self.population_modifier = self.generate_population_modifier()
            self.planetoid_belts = self.generate_planetoid_belts()
            self.gas_giants = self.generate_gas_giants()
            self.pbg  = generate_pbg(self.population_modifier,
                                     self.planetoid_belts,
                                     self.gas_giants)
        else:
            (self.population_modifier,
            self.planetoid_belts,
            self.gas_giants) = parse_pbg(pbg)
        self.allegiance = allegiance

    def __repr__(self):
        r = ["World("]
        r.append("name='{}', ".format(self.name))
        r.append("uwp='{}', ".format(self.uwp))
        r.append("bases='{}', ".format(self.bases))
        r.append("remarks={}, ".format(self.remarks))
        r.append("travel_zone='{}', ".format(self.travel_zone))
        r.append("pbg='{}', ".format(self.pbg))
        r.append("allegiance='{}')".format(self.allegiance))
        return "".join(r)

    def __str__(self):
        # Name, UWP, Bases, Remarks, Travel Zone, PBG, Allegiance
        # Width 80:
        # - Name:        15
        # - UWP:         9
        # - Bases:       1
        # - Remarks:     43
        # - Travel Zone: 1
        # - PBG:         3
        # - Allegiance:  2
        # - (spaces):    6
        return "{:<15} {} {} {:<43} {} {} {}".format(
            self.name,
            self.uwp,
            self.bases,
            " ".join(self.remarks),
            self.travel_zone,
            self.pbg,
            self.allegiance
        )

    def generate_atmosphere(self) -> int:
        if self.world_size == 0:
            return 0
        else:
            return max(0, min(roll_dice() - 7 + self.world_size, 15))

    def generate_hydrographics(self) -> int:
        if self.world_size <= 1:
            return 0
        else:
            r = roll_dice() - 7 + self.world_size
            # CT errata says atmosphere, but CE uses world_size
            if self.atmosphere in (0, 1, 10, 11, 12):
                r -= 4
            elif self.atmosphere == 14:
                r -= 2
            return max(0, min(r, 10))

    def generate_population(self) -> int:
        r = roll_dice() - 2
        if self.world_size <= 2:
            r -= 1
        if self.atmosphere >= 10:
            r -= 2
        elif self.atmosphere == 6:
            r += 3
        elif self.atmosphere in (5, 8):
            r += 1
        elif self.atmosphere < 3 and self.hydrographics == 0:
            r -= 2
        return max(0, min(r, 10))

    def generate_population_modifier(self) -> int:
        if self.population == 0:
            return 0
        else:
            # Note that while Cepheus Engine generates an exponent between
            # 1 and 10, an exponent of 10 effectively bumps the world
            # population up to the next value -- a population of 7 (10,000,000)
            # with an exponent of 10 becomes 7x10^10 = 100,000,000, or
            # population 8. If you want to use the "pure" Cepheus method,
            # change the below to -2 instead of -3.
            return max(1, roll_dice() - 3)

    def generate_starport(self) -> str:
        r = roll_dice() - 7 + self.population
        if r <= 2:
            return "X"
        elif r in (3, 4):
            return "E"
        elif r in (5, 6):
            return "D"
        elif r in (7, 8):
            return "C"
        elif r in (9, 10):
            return "B"
        else:
            return "A"

    def generate_government(self) -> int:
        if self.population == 0:
            return 0
        else:
            r = roll_dice() - 7 + self.population
            return max(0, min(r, 15))

    def generate_law_level(self) -> int:
        if self.government == 0:
            return 0
        else:
            r = roll_dice() - 7 + self.government
            return max(0, r)

    def generate_technology_level(self) -> int:
        r = roll_dice(1)
        if self.starport == "A":
            r += 6
        elif self.starport == "B":
            r += 4
        elif self.starport == "C":
            r += 2
        elif self.starport == "X":
            r -= 4
        if self.world_size <= 1:
            r += 2
        elif self.world_size <=4:
            r += 1
        if self.atmosphere <= 3 or self.atmosphere >= 10:
            r += 1
        if self.hydrographics in (0, 9):
            r += 1
        elif self.hydrographics == 10:
            r += 2
        if self.population in (1, 2, 3, 4, 5, 9):
            r += 1
        elif self.population <= 10 and self.population >= 12:
            r += self.population - 8
        if self.government in (0, 5):
            r += 1
        elif self.government == 7:
            r += 2
        elif self.government in (13, 14):
            r -= 2
        # tech level minimums
        if self.hydrographics in (0, 10) and self.population >= 6:
            return max(4, r)
        if self.atmosphere in (4, 7, 9):
            return max(5, r)
        elif self.atmosphere <= 3 and self.atmosphere in (10, 11, 12):
            return max(7, r)
        elif self.atmosphere in (13, 14) and self.hydrographics == 10:
            return max(7, r)
        else:
            return r

    def generate_trade_codes(self) -> List[str]:
        r = []
        if self.atmosphere in range(4, 10) \
            and self.hydrographics in range(4, 9) \
            and self.population in range(5, 8):
            r.append("Ag")
        elif self.atmosphere in range(4) \
            and self.hydrographics in range(4) \
            and self.population >= 6:
            r.append("Na")
        if self.world_size == 0 and self.atmosphere == 0 and self.hydrographics == 0:
            r.append("As")
        if self.population == 0 and self.government == 0 and self.law_level == 0:
            r.append("Ba")
        if self.atmosphere >= 2 and self.hydrographics == 0:
            r.append("De")
        if self.atmosphere >= 10 and self.hydrographics >= 1:
            r.append("Fl")
        if self.atmosphere in (5, 6, 8) \
            and self.hydrographics in range(4, 10) \
            and self.population in range(4, 9):
            r.append("Ga")
        if self.population >= 9:
            r.append("Hi")
        elif self.population in range(1, 4):
            r.append("Lo")
        if self.technology_level >= 12:
            r.append("Ht")
        elif self.technology_level <= 5:
            r.append("Lt")
        if self.atmosphere in (0, 1) and self.hydrographics >= 1:
            r.append("Ic")
        if self.atmosphere in (0, 1, 2, 4, 7, 9) and self.population >= 9:
            r.append("In")
        elif self.population in range(4, 7):
            r.append("Ni")
        if self.atmosphere in range(2, 6) and self.hydrographics in range(4):
            r.append("Po")
        elif self.atmosphere in (6, 8) and self.population in range(6, 9):
            r.append("Ri")
        if self.hydrographics == 10:
            r.append("Wa")
        if self.atmosphere == 0:
            r.append("Va")
        return r

    def generate_planetoid_belts(self):
        r = 0
        if roll_dice() >= 4:
            r = max(1, roll_dice(1) - 3)
        if self.world_size == 0:
            return max(1, r)
        else:
            return r

    def generate_gas_giants(self):
        r = 0
        if roll_dice() >= 5:
            r = max(1, roll_dice(1) - 2)
        return r

    def generate_naval_base(self) -> bool:
        if self.starport in ("A", "B") and roll_dice() >= 8:
            return True
        else:
            return False

    def generate_scout_base(self) -> bool:
        if self.starport not in ("E", "X"):
            dm = {"A": -3, "B": -2, "C": -1, "D": 0}
            r = roll_dice() + dm[self.starport]
            if r >= 7:
                return True
        return False

    def generate_pirate_base(self):
        if self.starport != "A" and not self.naval_base:
            if roll_dice() >= 12:
                return True
        return False

    def generate_travel_zone(self) -> str:
        if self.atmosphere >= 10 \
        or self.government in (0, 7, 10) \
        or self.law_level == 0 \
        or self.law_level >= 9:
            return "A"
        return " "


def parse_uwp(uwp: str) -> Tuple:
    r = list(uwp)
    r.remove('-')
    for i in range(1, len(r) + 1):
        r[i] = pseudohex(r[i])
    return tuple(r)

def generate_uwp(starport: str,
                 world_size: int,
                 atmosphere: int,
                 hydrographics: int,
                 population: int,
                 government: int,
                 law_level: int,
                 technology_level: int) -> str:
    """Returns the Universal World Profile in pseudo-hexadecimal code:

    A123456-7

    A -- Starport
    1 -- World Size
    2 -- Atmosphere
    3 -- Hydrographics
    4 -- Population
    5 -- Government
    6 -- Law Level
    7 -- Technology Level
    """
    r = []
    r.append(starport)
    r.append(pseudohex(world_size))
    r.append(pseudohex(atmosphere))
    r.append(pseudohex(hydrographics))
    r.append(pseudohex(population))
    r.append(pseudohex(government))
    r.append(pseudohex(law_level))
    r.append("-")
    r.append(pseudohex(technology_level))
    return "".join(r)

def parse_bases(bases: str) -> Tuple[bool, bool, bool]:
    if bases == "A":
        return (True, True, False)
    elif bases == "G":
        return (False, True, True)
    elif bases == "N":
        return (True, False, False)
    elif bases == "P":
        return (False, False, True)
    elif bases == "S":
        return (False, True, False)
    else:
        return (False, False, False)

def generate_base_code(naval_base: bool,
                   scout_base: bool,
                   pirate_base: bool) -> str:
    """Returns a base code, one of:

    A -- Naval Base and Scout Base/Outpost
    G -- Scout Base/Outpost and Pirate Base
    N -- Naval Base
    P -- Pirate Base
    S -- Scout Base/Outpost
    """
    if naval_base and scout_base:
        return "A"
    elif scout_base and pirate_base:
        return "G"
    elif naval_base:
        return "N"
    elif pirate_base:
        return "P"
    elif scout_base:
        return "S"
    else:
        return " "

def parse_pbg(pbg: str) -> Tuple[int, ...]:
    r = [pseudohex(i) for i in list(pbg)]
    return tuple(r)

def generate_pbg(population_modifier: int,
                 planetoid_belts: int,
                 gas_giants: int) -> str:
    r = [pseudohex(population_modifier),
         pseudohex(planetoid_belts),
         pseudohex(gas_giants)]
    return "".join(r)


if __name__ == "__main__":
    try:
        number = int(sys.argv[1])
    except:
        number = 1
    print("{:<15} {:<11} {}".format("Name", "Statistics", "Remarks"))
    for i in range(number):
        print(World())
