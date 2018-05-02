#class_configfile.py
###############################################################
# File utilities
#
# Author: Adam A. Koch (aakoch)
# Date: 2018-04-03
# Copyright (c) 2018 Adam A. Koch
# This work is licensed under the MIT license.
###############################################################

import uio, uos

class ConfigFile():
    def _file_exists(self, filename):
        for file in uos.ilistdir():
            if (file[0] == filename):
                return True

        return False

    def set_property(self, key, value):
        file = uio.open(key + ".config", "wt")
        file.write(str(value))
        file.close()

    def get_property(self, key):
        filename = key + ".config"
        if (self._file_exists(filename)):
            file = uio.open(filename, "rt")
            value = file.read()
            file.close()
        else:
            print("Could not find property with name " + key)
            return None
        return value

    def delete_property(self, key):
        filename = key + ".config"
        if (self._file_exists(filename)):
            file = uos.remove(filename)
