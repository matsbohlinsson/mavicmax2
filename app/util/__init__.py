import math
import os
from pathlib import Path

from geographiclib.geodesic import Geodesic

class Location(object):
    def __init__(self, lat=None, lon=None, altitude=None):
        self.lat = lat
        self.lon = lon
        self.altitude = altitude

    def distance_to(self, location):
        return Geodesic.WGS84.Inverse(self.lat, self.lon, location.lat, location.lon)['s12']

    def course_to(self, location):
        return self.convert_angle_to_course(Geodesic.WGS84.Inverse(self.lat, self.lon, location.lat, location.lon)['azi1'])

    def incline_to(self, location) -> float:
        distance = self.distance_to(location)
        height_diff = self.altitude - location.altitude
        angle = -(90.0 - math.degrees(math.atan(distance / height_diff)))
        return angle


    def distance_course(self, location):
        d_c = Geodesic.WGS84.Inverse(self.lat, self.lon, location.lat, location.lon)
        return ( d_c['s12'], self.convert_angle_to_course(d_c['azi1']))

    @classmethod
    def convert_angle_to_course(cls, angle):
        if angle < 0:
            return angle+360
        return angle

class Course:
    @classmethod
    def diff(cls, desired, measured):
        diff = desired-measured
        if diff>180:
            diff=diff-180
        return diff

class _Platform:
    def is_running_on_android(self):
        try:
            machine = os.uname()[4]
        except:
            machine='x86'
        print(machine)
        if not 'x86' in machine:
            return True
        else:
            return False
platform=_Platform()


def grep_log(logfile_abs: str, grep: str = "", exclude: str = "", nbr_of_lines=20):
    lines = Path(logfile_abs).read_text().split('\n')
    grepped_lines = []
    reversed_lines = lines[::-1]
    index: int = 0
    for line in reversed_lines:
        if index > nbr_of_lines: break
        if grep in line and exclude != '' and not exclude in line:
            grepped_lines.append(line)
            index += 1
    return "\n".join(grepped_lines)


if __name__ == "__main__":
    l1 = Location(58,11.011,20)
    l2 = Location(58,11.01,10)
    course = l1.course_to(l2)
    distance = l1.distance_to(l2)
    incline = l1.incline_to(l2)
    print(course, distance, incline)
    print(platform.is_running_on_android())
