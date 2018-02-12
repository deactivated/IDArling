import os

import idaapi

LOCAL_PATH = os.path.join(idaapi.get_user_idadir(), '.idaconnect')


def localResource(dirname, filename):
    """
    Get the absolute path of a local resource.

    :param dirname: the directory name
    :param filename: the file name
    :return: the path
    """
    resDir = os.path.join(LOCAL_PATH, dirname)
    if not os.path.exists(resDir):
        os.makedirs(resDir)
    return os.path.join(resDir, filename)


PLUGIN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def pluginResource(filename):
    """
    Get the absolute path of a plugin resource.

    :param filename: the fil ename
    :return: the path
    """
    return os.path.join(PLUGIN_PATH, 'resources', filename)


def refreshPseudocodeView(force=False):
    """
    Refresh the pseudocode view in IDA
    """
    names = ['Pseudocode-%c' % chr(ord('A') + i) for i in xrange(5)]
    for name in names:
        widget = idaapi.find_widget(name)
        if widget:
            vu = idaapi.get_widget_vdui(widget)
            vu.refresh_ctext()
            if force:
                vu.refresh_view(True)


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if
                   self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        return set(o for o in self.intersect if
                   self.past_dict[o] == self.current_dict[o])
