import ConfigParser
import os
import logging

CONFIG_PATH = '/etc/arapi/arapi.cfg'
DEFAULTS = {'root': "/", 'loadpath': None}

class DebugMode(object):
    _debug_mode = None
    def __new__(cls, *args, **kwargs):
        if cls._debug_mode is None:
            if 'ARAPI_DEBUG' in os.environ:
                cls._debug_mode = True
            else:
                cls._debug_mode = False
        return cls._debug_mode


class GetConfig(object):
    _config = None

    def __new__(cls, *args, **kwargs):
        if not cls._config:
            path = CONFIG_PATH
            if 'ARAPI_CONFIG' in os.environ:
                path = os.environ['ARAPI_CONFIG']
            cls._config = loadConfig(path)
        return cls._config


def loadConfig(path):
    if (not os.path.isfile(path)) or (not os.access(path, os.R_OK)):
        raise IOError("%s is not a file or cant be read" % path)
    cfg_dict = {}
    c = ConfigParser.SafeConfigParser(DEFAULTS)
    c.read(path)
    cfg_dict['root'] = c.get('global','root')
    cfg_dict['loadpath'] = c.get('global', 'loadpath')

    logging.debug("loaded config is %s" % cfg_dict)

    if not cfg_dict['loadpath']:
        logging.debug('No additioal load path for lenses specified.')
    elif not os.path.isdir(cfg_dict['loadpath']):
        logging.debug("Directory %s passed in loadpath does not exist."
                      "This is not critical - augeas use the system-wide "
                      "lense storage anyway." % cfg_dict['loadpath'])


    return cfg_dict

