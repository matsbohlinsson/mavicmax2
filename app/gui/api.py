import traceback

from remi import gui

import config


def grep_log(filename: str, reverse: str = 'True', grep: str = '', max_line_nbr: int = 0):
    #latest_file = config.test_settings.csv_dir_test.absolute().as_posix() + '/' + filename
    latest_file = 'fixme' + '/' + filename
    data = []
    if grep != '':
        with open(latest_file, "r") as myfile:
            while (line := myfile.readline()):
                if grep in line:
                    data.append(line)
    else:
        with open(latest_file, "r") as myfile:
            data = myfile.readlines()
    data.append(latest_file + '\n')
    if reverse == 'True':
        data.reverse()
    if max_line_nbr == 0:
        r = ''.join(data)
    else:
        try:
            r = ''.join(data[:max_line_nbr])
        except:
            r = ''.join(data)
    return r


class Api(gui.Label):
    def __init__(self, **kwargs):
        super(Api, self).__init__(**kwargs)

    # api function
    # http://127.0.0.1:8079/api/log?filename=python.txt&grep=AllText&max_line_nbr=70
    def log(self, filename, max_line_nbr, grep):
        if grep=="AllText": grep=""
        headers = {'Content-type': 'text/plain'}
        try:
            log = grep_log(filename=filename, grep=grep, max_line_nbr=int(max_line_nbr))
        except:
            log = traceback.format_exc()
        return [log, headers]
