"""Enable manual slewing of SkyWatcher Star Adventurer mount and locating of
faint DSOs.

Usage:

    python3 find_object.py <URL>
"""

import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import Angle


def calibrate_RA(RA1, RA2, presstime):
    """Using two images and a known time that one of the RA buttons was pressed,
    calculates how many degrees per second the RA button moves the mount.

    Args:
        RA1: Right ascension coordinate of the first plate-solved image

        RA2: Right ascension coordinate of the second plate-solved image

        presstime: The number of seconds the slew button was pressed
            on the mount

    Returns:
        RAcal: A float value representing the number of degrees per second that
        the button is pressed. Use for each button individually, as these
        calibrations might be unique for each direction.

    """

    RAcal = (RA2 - RA1) / presstime

    return RAcal


def calibrate_DEC_knob(DEC1, DEC2, knobdegrees):
    """Using two images and a known degree of turn on the DEC knob, calculates
    how many degrees per turn the DEC knob moves the telescope.

    Args:
        DEC1: Declination coordinate of the first plate-solved image

        DEC2: Declination coordinate of the second plate-solved image

        knobdegrees: The number of degrees the declination knob was turned, with
            positive being clockwise

    Returns:
        DECcal: A float value representing the number of degrees in celestial
        coordinates per degree turned by the declination knob.

    """

    DECcal = (DEC2 - DEC1) / knobdegrees

    return DECcal


def findDSO(init_coord, obj_coord, RAcalR, RAcalL, DECcal):
    """Takes input coordinates of a desired DSO and the center coordinates of
    the mount's current position. Calculates the necessary DEC knob turns and RA
    inputs to get the desired DSO in frame.

    Args:
        init_coord:

        obj_coord:

        RAcalR:

        RAcalL:

        DECcal:

    Returns:
        A string describing the necessary RA and DEC adjustments.

    """





def main():
    # Maybe the calibration values should have defaults that are roughly correct
    # This function would be benefitted from implementation as a GUI program

    print("Running as a main function.")



if __name__ == "__main__":
    main()
