import Variable
import JDN
import os.path

__author__ = "Moskvin Vasilii (vasiliy.moscvin@yandex.ru)"

def get_ephemerides_by_date(in_filename, out_filename):
    """
    Return file with ephemerides sorted by date
    :param key: data of stars
    :return: file filename with sorted ephemerides by date
    """
    stars = read_stars_from_file(in_filename)
    dct_raw_eph = get_ephemerides(stars, 100)
    dct_eph = sort_by_date(dct_raw_eph)
    write_eph_by_date(out_filename, dct_eph)


def get_ephemerides_bn_date(in_filename, out_filename, start_date, end_date):
    """
    Return file with ephemerides sorted by date
    :param key: data of stars
    :return: file filename with sorted ephemerides by date
    """
    stars = read_stars_from_file(in_filename)
    dct_raw_eph = get_eph_bn_date(stars, start_date, end_date)
    dct_eph = sort_by_date(dct_raw_eph)
    write_eph_by_date(out_filename, dct_eph)


def read_stars_from_file(filename):
    """
    It is reading file with a list of stars
    :param filename: name of file
    :return: Variable - objects
    """
    with open(filename, "r",  encoding='utf-8') as f:
        stars = []
        f.readline()
        for line in f:
            stars.append(Variable.Variable(*line.split(",")))
    return stars


def get_ephemerides(stars, n):
    """
    Возвращает список звёзд со временем начала, середины и конца процесса
    :param stars: списко звёзд
    :param n: количество эфемерид
    :return:
    """
    dct_ephemerides = dict(name=[], start=[], center=[], end=[])
    for i in stars:
        dct_temp = dict(**i.get_dct_ephemerids(n))
        {key: dct_ephemerides[key].extend(dct_temp[key]) for key in dct_ephemerides.keys()}

    return dct_ephemerides


def get_eph_bn_date(stars, date_start, date_end):
    """
    Returns the dictionary of some transit's property: name, satrt, center, end time transit
    :param stars: list of stars
    :param date_start: from date
    :param date_end: to date
    :return: the dictionary of some transit's property: name, satrt, center, end time transit
    """
    dct_ephemerides = dict(name=[], start=[], center=[], end=[])
    for i in stars:
        dct_temp = dict(**i.get_dct_eph_bn_dates(date_start, date_end))
        {key: dct_ephemerides[key].extend(dct_temp[key]) for key in dct_ephemerides.keys()}

    return dct_ephemerides



def sort_by_date(dct_input):
    """
    Returns sorted dictionary of transits by start transit time
    :param dct_input: don't sortered dictionary of transits
    :return:  sorted dictionary of transits
    """
    lst_zip = list(zip(dct_input['name'], dct_input['start'], dct_input['center'], dct_input['end']))
    lst_zip.sort(key=lambda x: x[1])
    rezip = list(zip(*lst_zip))
    dct_output = dict(name=rezip[0],
                      start=rezip[1],
                      center=rezip[2],
                      end=rezip[3])
    return dct_output


def write_eph_by_date(filename, dct):
    """
    It is writing ephemerides from lst to the file file name.
    Example format output:

    name,start,center,end

    19/1/2017
    HAT-P-16b,	19/1/2017 10:52:22,	19/1/2017 12:24:22,	19/1/2017 13:56:23
    Qatar-1b,	19/1/2017 21:0:9,	19/1/2017 21:48:30,	19/1/2017 22:36:51

    20/1/2017
    WASP-12b,	20/1/2017 22:45:37,	21/1/2017 0:15:38,	21/1/2017 1:45:40

    :param filename: the file name where you want to save ephemerides
    :param lst: ephemerides of Variable objects
    :return: file filename
    """
    with open(filename, "w", encoding="utf-8") as f:
         f.write("name,start,center,end\n")
         temp_start = ""
         for i in zip(dct['name'], dct['start'], dct['center'], dct['end']):
             jd_start = JDN.get_GD(str(i[1]))
             jd_ccenter = JDN.get_GD(str(i[2]))
             jd_end = JDN.get_GD(str(i[3]))
             if temp_start != jd_start[0]:
                 f.write("\n{}/{}/{}\n".format(*jd_start))
             temp_start = jd_start[0]
             f.write("{},"
                     "{}/{}/{} {}:{}:{},"
                     "{}/{}/{} {}:{}:{},"
                     "{}/{}/{} {}:{}:{}\n".format(i[0], *jd_start, *jd_ccenter, *jd_end))


def print_menu():
    """
    Return program's menu.
    :return: menu
    """
    print("\nMenu (q - to exit)")
    print("1 - Get the list ephemerides by date")
    print("2 - Get the list ephemerides between dates")
    print("3 - Get JD by GD")
    print("4 - Get JDN by GD")
    print("5 - Get GD by JD")


def main():
    """
    It is doing by default
    :return:
    """
    ans = ''
    while ans != 'q':
        print_menu()
        ans = input("Enter what is do?\n")
        if ans == "1":
            try:
                file_input, file_output = input('filename-input filename-output:\n').split()
            except ValueError as e:
                print('Check the input format\n{}'.format(e))
            else:
                try:
                    get_ephemerides_by_date(file_input, file_output)
                except TypeError as e:
                    print('Output file is not defined\n{}'.format(e))
                except FileNotFoundError as e:
                    print('File {} is not found\n{}'.format(file_input, e))
                else:
                    if os.path.exists(file_output):
                        print('File {} has created'.format(file_output))
                    else:
                        print('File {} has not created'.format(file_output))
        elif ans == "2":
            try:
                file_input, file_output = input('filename-input filename-output:\n').split()
            except ValueError as e:
                print('Check the input format\n{}'.format(e))
            else:

                try:
                    start_date = input('Enter the start date. Format date "year/month/day/h/m/s":\n').split('/')
                    end_date = input('Enter the start date. Format date "year/month/day/h/m/s":\n').split('/')
                except TypeError as e:
                    print('Check the input format\n{}'.format(e))
                except ValueError as e:
                    print('Check the type of input data\n{}'.format(e))
                else:
                    try:
                        start = JDN.get_JD(*start_date)
                        end = JDN.get_JD(*end_date)
                        get_ephemerides_bn_date(file_input, file_output, start, end)
                    except TypeError as e:
                        print('Output file is not defined\n{}'.format(e))
                    except FileNotFoundError as e:
                        print('File {} is not found\n{}'.format(file_input, e))
                    else:
                        if os.path.exists(file_output):
                            print('File {} has created'.format(file_output))
                        else:
                            print('File {} has not created'.format(file_output))

        elif ans == '3':
            arg = input('Input GD. Format GD "year/month/day/h/m/s":\n').split('/')
            try:
                print(JDN.get_JD(*arg))
            except TypeError as e:
                print('Check the input format\n{}'.format(e))
            except ValueError as e:
                print('Check the type of input data\n{}'.format(e))
        elif ans == '4':
            arg = input('Input GD. Format GD "year/month/day":\n').split('/')
            try:
                print(JDN.get_JDN(*arg))
            except TypeError as e:
                print('Check the input format\n{}'.format(e))
            except ValueError as e:
                print('Check the type of input data\n{}'.format(e))
        elif ans == '5':
            arg = input('Input JD:\n')
            try:
                print(JDN.get_GD(arg, '-f'))
            except TypeError as e:
                print('Check the input format\n{}'.format(e))
            except ValueError as e:
                print('Check the type of input data\n{}'.format(e))


if __name__ == '__main__':
    main()
