from collections import namedtuple
import csv
import os.path

import JDN

Ephemeris = namedtuple('Ephemeris', ('object_name', 'start', 'center', 'end'))


class VarStar:
    def __init__(self, name, ra, de, period, center_epoch, duration):
        self.name = name
        self.ra = ra
        self.de = de
        self.period = float(period)
        self.center_epoch = float(center_epoch)
        self.duration = float(duration)

    def start_epoch(self, epoch):
        return epoch - self.duration / 2

    def end_epoch(self, epoch):
        return epoch + self.duration / 2

    def next_ephemeris(self, epoch):
        return epoch + self.period

    def ephemerises_between_dates(self, first_date, second_date):
        first_date = float(first_date)
        second_date = float(second_date)
        lst_ephemerises = list()

        count_periods = (first_date - self.start_epoch(self.center_epoch)) // self.period
        temp_epoch = self.center_epoch + self.period * count_periods
        while self.next_ephemeris(self.end_epoch(temp_epoch)) <= second_date:
            lst_ephemerises.append(Ephemeris(self.object_name,
                                           self.start_epoch(temp_epoch),
                                           temp_epoch,
                                           self.end_epoch(temp_epoch)))
            temp_epoch = self.next_ephemeris(temp_epoch)

        return lst_ephemerises

    def __str__(self):
        return 'name = {} ra = {} de = {} period = {} center_epoch = {} duration = {}'.format(self.name, self.ra,
                                                                                               self.de, self.period,
                                                                                               self.center_epoch,
                                                                                               self.duration)


def stars_from_file(file_path):
    with open(file_path, 'r') as csv_file:
        csv_file = csv.DictReader(csv_file, delimiter=',')
        lst_stars = [VarStar(**row) for row in csv_file]

    return lst_stars


def ephemerises_for_stars(stars, first_date, second_date):
    lst_ephemerises = list()
    for star in stars:
        lst_ephemerises.extend(star.ephemerises_between_dates(first_date, second_date))

    return sorted(lst_ephemerises, key=lambda x: x.start)


def main():
    stars = stars_from_file(os.path.abspath(input('Enter path:\n')))
    first_date = JDN.get_JD(*input('Enter first date'
                                   ' (format: year/month/day/hour/minute/second):\n').strip().split('/'))
    second_date = JDN.get_JD(*input('Enter first date '
                                    '(format: year/month/day/hour/minute/second):\n').strip().split('/'))
    lst_ephemerises = ephemerises_for_stars(stars, str(first_date), str(second_date))
    for ephemeris in lst_ephemerises:
        print("{}\t"
              "{}/{}/{} {}:{}:{}\t"
              "{}/{}/{} {}:{}:{}\t"
              "{}/{}/{} {}:{}:{}".format(ephemeris.object_name,
                                         *JDN.get_GD(str(ephemeris.start)),
                                         *JDN.get_GD(str(ephemeris.center)),
                                         *JDN.get_GD(str(ephemeris.end))))


if __name__ == '__main__':
    main()
