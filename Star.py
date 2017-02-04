from decimal import Decimal

__author__ = "Moskvin Vasilii (vasiliy.moscvin@yandex.ru)"


class KeyInputError(Exception):
    pass


class Star:
    def __init__(self, name, ra, dec):
        self.name = name
        self.ra = self.get_coord(ra, "h")
        self.dec = self.get_coord(dec, "g")

    @staticmethod
    def get_coord(x, key):
        """
        Переводит координаты из h(g):m:s в h(g), m, s
        :param x: координата вида h m s (g m s)
        :param key: в каком формате возвращать h, g, m, s
        :return: координаты в виде h, g, m, s. В случае неизвестного ключа, кидает ошибку KeyInputError
        """
        x_out = 0
        for i, src in enumerate(x.split()):
            if i == 0:
                x_out += int(src)
            elif i == 1:
                x_out += Decimal(src) / 60
            elif i == 2:
                x_out += Decimal(src) / 3600
        if key == "h" or key == "g":
            return x_out
        elif key == "m":
            return x_out * 60
        elif key == "s":
            return x_out * 3600
        else:
            raise KeyInputError

    def get_lmst(self, gmst, long, ra):
        """
        Возвращает часовой угол звезды по среднему звёздному вемени
        :param gmst: звёздное время
        :param long: долгота места наблюдения
        :param ra: прямое восхождение звезды
        :return: часовой угол звезды
        """
        lmst = self.get_coord(gmst, "h") - self.get_coord(long, "h") - ra
        if lmst < 0:
            return lmst + 360
        elif lmst > 360:
            return lmst - 360
        else:
            return lmst