import Star
from decimal import Decimal

__author__ = "Moskvin Vasilii (vasiliy.moscvin@yandex.ru)"


class Variable(Star.Star):
    def __init__(self, name, ra, dec, period, epoch_center, t_duration):
        super().__init__(name, ra, dec)
        epoch_center = Decimal(epoch_center)
        self.period = Decimal(period)
        self.t_duration = Decimal(t_duration)
        self.epoch = dict(start=epoch_center - self.t_duration / 2,
                          center=epoch_center,
                          end=epoch_center + self.t_duration / 2)

    def __str__(self):
        return 'name = {} ra = {:.7f} dec = {:.7f} period = {:.7f} ' \
               'epoch_center = {:.7f} transit duration = {:.7f}'.format(self.name,
                                                                        self.ra,
                                                                        self.dec,
                                                                        self.period,
                                                                        self.epoch['center'],
                                                                        self.t_duration)

    def next_ephemerid(self, epoch):
        """
        Возвращает следующую эфемериду, по указанной эпохе
        :param epoch: эпоха
        :return: следующая эфемерида
        """
        return epoch + self.period


    def get_dct_ephemerids(self, n, *key):
        """
        Возвращает список n следующих эфемерид, отсчитывая от: начала (s), центра (c) или конца (e) изменения блеска
        :param n: количество эфемерид
        :param key: ключ, указывающий начало отсчёта start, center, end, отсутствие ключа - возвращает
                    эфемериды для всех трёх точек
        :return: словарь эфемерид
        """
        dct_output, eph = self.prepare_to_dct(self.epoch, *key)

        for i in range(n):
            dct_output, eph = self.fill_dict_eph(dct_output, eph)

        return dct_output


    def get_dct_eph_bn_dates(self, date_start, date_end, *key):
        """
        Returs the list of ephemerides within interval date_start - date_end
        :param date_start: from date
        :param date_end: to date
        :param key: None, 'start', 'center', 'end'
        :return: the dictionary of ephemerides within interval date_start - date_end
        """
        dct_output, eph = self.prepare_to_dct(self.get_epoche(self.get_eph_before_date(date_start,
                                                                                        'start'),
                                                               'start'),
                                               *key)

        if not key:
            while eph['start'] < self.get_eph_after_date(date_end, 'start'):
                dct_output, eph = self.fill_dict_eph(dct_output, eph)

        return dct_output

    def prepare_to_dct(self, first_epoch, *key):
        """
        Prepare to output dictionary with ephemerides of transits
        :param first_epoch: first epoche for transit
        :param key: work with all or one part of transit
        :return: output dictionary with ephemerides of transits
        """
        if not key:
            eph = first_epoch
            dct_output = dict(name=[], start=[], center=[], end=[])
        elif key[0] in self.epoch:
            eph = {key[0]: first_epoch[key[0]]}
            dct_output = {'name': [], key[0]: []}
        else:
            raise Star.KeyInputError

        return dct_output, eph


    def fill_dict_eph(self, dct_output, eph):
        """
        Fill the output dictionary with ephemerides of transits
        :param dct_output: output dictionary
        :param eph: epehmerides
        :return: output dictionary and dictionary the last ephemerides
        """
        {dct_output[key].append(self.next_ephemerid(eph[key])) for key in eph.keys()}
        dct_output['name'].append(self.name)
        eph = {key: self.next_ephemerid(value) for key, value in eph.items()}

        return dct_output, eph


    def get_epoche(self, epoche, *key):
        """
        Returns the time of start, center and end transits by epoche. key - determinate what is part of transit epoch
        :param epoche: time
        :param key: 'start' - epoche==start_transition_time,
                    'center' - epoche==center_transition_time,
                    'end' - epoche==end_transition_time
                    '' - epoche==center_transition_time
        :return: dictionary of epoche
        """
        if not key:
            dct_epoche = dict(start=epoche - self.t_duration/2,
                              center=epoche,
                              end=epoche + self.t_duration/2)
        elif key[0] == 'start':
            dct_epoche = dict(start=epoche,
                              center=epoche + self.t_duration / 2,
                              end=epoche + self.t_duration)
        elif key[0] == 'center':
            dct_epoche = dict(start=epoche - self.t_duration / 2,
                              center=epoche,
                              end=epoche + self.t_duration / 2)
        elif key[0] == 'end':
            dct_epoche = dict(start=epoche - self.t_duration,
                              center=epoche - self.t_duration / 2,
                              end=epoche)
        else:
            raise Star.KeyInputError

        return dct_epoche


    def get_eph_before_date(self, my_date, *key):
        """
        Returns the first ephemeride before my_date
        :param my_date: your date
        :param key: None, 'start', 'center', 'end'
        :return: if no key, returns dictionary with ephemerides for start, center, end. Else returns one of these.
        """
        if not key:
            count_eph = (my_date - self.epoch['start']) // self.period
            return self.epoch['start'] + count_eph * self.period
        elif key[0] in self.epoch:
            count_eph = (Decimal(my_date) - self.epoch[key[0]]) // self.period
            return self.epoch[key[0]] + count_eph * self.period
        else:
            raise Star.KeyInputError


    def get_eph_after_date(self, my_date, *key):
        """
        Returns the first ephemeride after my_date
        :param my_date: your date
        :param key: None, 'start', 'center', 'end'
        :return: if no key, returns dictionary with ephemerides for start, center, end. Else returns one of these.
        """
        if not key:
            temp = self.get_eph_before_date(my_date, *key)
        elif key[0] in self.epoch:
            temp = self.get_eph_before_date(my_date, *key)
        else:
            raise Star.KeyInputError

        return self.next_ephemerid(temp)
