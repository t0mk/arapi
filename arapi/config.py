import ConfigParser
import pkg_resources
import os
import logging


CONFIG_PATH = '/etc/arapi/arapi.cfg'
CONFIG_DEVEL = pkg_resources.resource_filename('arapi', 'conf/arapi_dev.cfg')
DEFAULTS = {'port': 8091, 'address': '0.0.0.0', 'root': "/",
            'loadpath': None}


class GetConfig(object):
    _config = None

    def __new__(cls, *args, **kwargs):
        if not cls._config:
            path = CONFIG_PATH
            if 'devel' in kwargs and kwargs['devel']:
                path = CONFIG_DEVEL
            cls._config = loadConfig(path)
        else:
            if args or kwargs:
                logging.warn("config handle already exists, the values you "
                             "pass to the constuctor are not considered:"
                             "args: %s, kwargs: %s" % (args, kwargs))
        return cls._config


def loadConfig(path):
    if (not os.path.isfile(path)) or (not os.access(path, os.R_OK)):
        raise IOError("%s is not file or cant be read" % path)
    cfg_dir = {}
    c = ConfigParser.SafeConfigParser(DEFAULTS)
    c.read(path)
    cfg_dir['port'] = c.getint('global','port')
    cfg_dir['address'] = c.get('global','address')
    cfg_dir['root'] = c.get('global','root')
    cfg_dir['loadpath'] = c.get('global', 'loadpath')
    return cfg_dir

