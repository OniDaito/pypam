""" Time related support functions """

__all__ = ["epoch"]
__version__ = "0.1"
__author__ = "Benjamin Blundell <bjb8@st-andrews.ac.uk>"


import datetime
import pytz


def epoch(zone="UTC"):
    epoch_str = "1970-01-01 00:00:00"
    epoch_format = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime(epoch_str, epoch_format)
    tz = pytz.timezone(zone)
    epoch = tz.localize(epoch)
    return epoch

