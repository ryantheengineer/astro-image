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
        init_coord: Tuple coordinates (RA, DEC) of the initial position

        obj_coord: Tuple coordinates (RA, DEC) of the desired position

        RAcalR: Calibration value for pressing the right RA button (deg/sec)

        RAcalL: Calibration value for pressing the left RA button (deg/sec)

        DECcal: Calibration value for turning the DEC knob (unitless, deg/deg)

    Returns:
        A string describing the necessary RA and DEC adjustments.

    """
    # Set meridian_threshold, the angle at which a warning message will display
    meridian_threshold = 90.0

    # Get the required coordinate change in RA coordinate
    RAchange = obj_coord[0] - init_coord[0]

    # Get the required coordinate change in DEC coordinate. Change DECchange so
    # it requires 180 degrees rotation or less to achieve
    DECchange = obj_coord[1] - init_coord[0]

    if DECchange > 180.0:
        DECchange = 180.0 - DECchange

    # Print the RA and DEC change values in degrees for context and debugging
    print("\nRA change = {} deg".format(RAchange))
    print("DEC change = {} deg\n".format(DECchange))

    # Print a warning if the required RA change is greater than
    # meridian_threshold
    if np.abs(RAchange) > meridian_threshold:
        print("\n[WARNING]: REQUIRED RA CHANGE MAY REQUIRE MERIDIAN FLIP")

    # Convert the RA change from degrees to seconds of button press, using the
    # appropriate button calibration
    if RAchange < 0:
        RAchange = np.abs(RAchange)
        RApress = RAcalL * RAchange
        RAdirection = "LEFT"

    else:
        RApress = RAcalR * RAchange
        RAdirection = "RIGHT"

    # Convert the DEC change from celestial degrees to degrees of DEC knob turn
    DECknob = DECcal * DECchange

    # NOTE: HERE THE DECKNOB CALCULATION SHOULD BE RECALCULATED TO COUNT THE
    # FULL TURNS INHERENT IN THE MOVE, SO IT WOULD OUTPUT SOMETHING LIKE "3
    # TURNS CLOCKWISE AND 45 DEGREES"

    # Build the instruction strings and print them out
    RAinstruction = "\nPress the {} RA button for {} seconds".format(RAdirection, RApress)
    DECinstruction = "\nTurn the DEC knob by {} degrees".format(DECknob)
    print(RAinstruction)
    print(DECinstruction)


def main():
    # Maybe the calibration values should have defaults that are roughly correct
    # This function would be benefitted from implementation as a GUI program

    print("Running as a main function.")



if __name__ == "__main__":
    main()
