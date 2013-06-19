# global imports
import bottle
import augeas

import argparse
import logging
import os
import sys

# local imports
import config


class AugeasSingletonWrapper(object):
    _augeas = None

    def __new__(cls, *args, **kwargs):
        if not cls._augeas:
            cls._augeas = augeas.Augeas(*args, **kwargs)
        else:
            if args or kwargs:
                logging.warn("augeas handle already exists, the values you "
                             "pass to the constuctor are nto considered:"
                             "args: %s, kwargs: %s" % (args, kwargs))
        return cls._augeas


def sanitizePath(p):
    if not p:
        bottle.redirect('/help')
    if p[0] != "/":
        return "/" + p
    else:
        return p


@bottle.route('/help')
def help():
    """List current scope and show docstrings of url-handling methods."""
    txt = ("API listing for arapi instance\n"
           "==============================\n\n")
    for symbol in sys.modules[__name__].__dict__:
        if symbol.startswith("handle_"):
            url_handling_method = sys.modules[__name__].__dict__[symbol]
            txt += url_handling_method.__doc__
            txt += "\n"
    bottle.response.content_type = "text/plain"
    return txt


@bottle.route('/<action>/<path:path>')
def handle_get_or_match(action, path):
    """* GET to /get/<path expresison> or /match/<path expression>

         Will do augeas get or match for given path expression.
         E.g.:
           /get/files/etc/hosts/1/ipaddress
           /match/files/etc/hosts/*

         More about Augeas paths:
           https://github.com/hercules-team/augeas/wiki/Path-expressions
    """
    a = AugeasSingletonWrapper()
    if action == 'get':
        result = a.get(sanitizePath(path))
    elif action == 'match':
        result = a.match(sanitizePath(path))
    else:
        bottle.abort(400,
            'Forbidden action for GET. See /help')
    bottle.response.content_type = "text/plain"
    return result


DESC = """
REST API for augeas. Configuration values read from %s.
If you run a development instance (with -d), those are read from %s.
""" % (config.CONFIG_PATH, config.CONFIG_DEVEL)

DEVEL_HELP = 'run a development instance'


def run():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('-d', '--devel', help=DEVEL_HELP,
                        action='store_true')

    args = parser.parse_args()

    log_level = 'INFO'
    if args.devel:
        log_level = 'DEBUG'

    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    c = config.GetConfig(devel=args.devel)

    logging.debug("loaded config is %s" % c)

    if not c['loadpath']:
        logging.debug('No additioal load path for lenses specified.')
    elif not os.path.isdir(c['loadpath']):
        logging.debug("Directory %s passed in loadpath does not exist."
                      "This is not critical - augeas use the system-wide "
                      "lense storage anyway." % c['loadpath'])


    AugeasSingletonWrapper(root=c['root'], loadpath=c['loadpath'])

    bottle.run(host=c['address'], port=c['port'], debug=True)

if __name__ == '__main__':
    run()
