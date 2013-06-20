# global imports
import logging
import sys

# local imports
import arapi.bottle
import arapi.config
import arapi.plugins.bottle_augeas

main = arapi.bottle.Bottle()

class GetMainApp(object):
    _main_app = None
    def __new__(cls, *args, **kwargs):
        if cls._main_app is None:
            logging.basicConfig(format='%(levelname)s: %(message)s',
                level='DEBUG' if arapi.config.DebugMode() else 'INFO')

            config_dict = arapi.config.GetConfig()

            main.install(arapi.plugins.bottle_augeas.AugeasPlugin(
                root=config_dict['root'], loadpath=config_dict['loadpath']))
            cls._main_app = main
        return cls._main_app

def sanitizePath(p):
    if not p:
        arapi.bottle.redirect('/help')
    if p[0] != "/":
        return "/" + p
    else:
        return p


@main.route('/help')
def help():
    """List current scope and show docstrings of url-handling methods."""
    txt = ("API listing for arapi instance\n"
           "==============================\n\n")
    for symbol in sys.modules[__name__].__dict__:
        if symbol.startswith("handle_"):
            url_handling_method = sys.modules[__name__].__dict__[symbol]
            txt += url_handling_method.__doc__
            txt += "\n"
    arapi.bottle.response.content_type = "text/plain"
    return txt


@main.route('/<action>/<path:path>')
def handle_get_or_match(action, path, augeas_handle):
    """* GET to /get/<path expresison> or /match/<path expression>

         Will do augeas get or match for given path expression.
         E.g.:
           /get/files/etc/hosts/1/ipaddress
           /match/files/etc/hosts/*

         More about Augeas paths:
           https://github.com/hercules-team/augeas/wiki/Path-expressions
    """
    if action == 'get':
        result = augeas_handle.get(sanitizePath(path))
    elif action == 'match':
        result = augeas_handle.match(sanitizePath(path))
    else:
        arapi.bottle.abort(400,
            'Forbidden action for GET. See /help')
    arapi.bottle.response.content_type = "text/plain"
    return result

