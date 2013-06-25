# global imports
import logging
import pkgutil
import sys

# local imports
import arapi.bottle
import arapi.config
import arapi.plugins.bottle_augeas

# list of Arapi plugins which are inherited from the main application to
# sub-applications
# (there are some plugins which are mounted by default by Bottle framework
#  to each application [JSON, hooks, template]. I suppose that list changes
#  with Bottle development and it should be safe to ignore it.)
INHERIT_PLUGINS = [ arapi.plugins.bottle_augeas.AugeasPlugin ]

#subapplications import
import arapi.subapps


app = arapi.bottle.Bottle()
url_base = "/"

class ArapiException(bottle.BottleException):
    pass


def getAppHandlers(var_app):
    handlers = {}
    for route in var_app.routes:
        if route.callback.__name__.startswith('handle_'):
            handlers[route.callback] = (route.method, route.rule)
        elif route.callback.__name__ == 'mountpoint_wrapper':
            prefix = '/' + route.rule.split('/')[1]
            sub_handlers = getAppHandlers(route.config.mountpoint['target'])
            for h in sub_handlers:
                m, rule = sub_handlers[h]
                sub_handlers[h] = (m, prefix + rule)
            handlers.update(sub_handlers)
    return handlers


def getHelpDoc(var_app, url_base):
    txt = "API listing for app on %s\n" % url_base
    txt += '=' * (len(txt) - 1) + '\n'
    logging.info("Generating help for %s" % var_app)

    for handler, tup in getAppHandlers(var_app).items():
        if not handler.__doc__:
            logging.error("You forgot to document %s" % handler)
            raise ArapiException("%s not documented" % handler)
        http_method, rule = tup
        txt += "* " + http_method + " to " + rule + '\n'
        txt += handler.__doc__
        txt += "\n"
    return txt


def loadAllSubApps(main_app):
    for l, name, _ in pkgutil.iter_modules(arapi.subapps.__path__):
        loadSubApp(main_app, name)


def loadSubApp(main_app, subapp_modname):
    logging.info("Loading python module for sub-application: %s" %
        subapp_modname)

    # this is lame but until I find a nicer way to load a module..
    loader = pkgutil.find_loader('arapi.subapps.' + subapp_modname)
    subapp_mod = loader.load_module(subapp_modname)

    # mount sub-application
    logging.info("Mounting sub-application: %s to %s" %
        (subapp_modname, subapp_mod.url_base))
    main_app.mount(subapp_mod.url_base, subapp_mod.app, skip=None)

    # create a doc resource for a sub-app, and update doc of mother app
    subapp_mod.app.config.doc = getHelpDoc(subapp_mod.app,
                                           subapp_mod.url_base)
    main_app.config.doc = getHelpDoc(main_app, "/")

    # inherit plugins from the main app
    # (Is this cool? maybe each sub-app should have it's own plugin instance)
    for plugin in main_app.plugins:
        if type(plugin) in INHERIT_PLUGINS:
            logging.info("Mounting plugin %s to %s" %
                (plugin, subapp_modname))
            subapp_mod.app.install(plugin)


class GetMainApp(object):
    _main_app = None
    def __new__(cls, *args, **kwargs):
        if cls._main_app is None:
            logging.basicConfig(format='%(levelname)s: %(message)s',
                level='DEBUG' if arapi.config.DebugMode() else 'INFO')

            config_dict = arapi.config.GetConfig()

            aug_plugin = arapi.plugins.bottle_augeas.AugeasPlugin(
                root=config_dict['root'], loadpath=config_dict['loadpath'])
            app.install(aug_plugin)

            app.doc = getHelpDoc(app, "/")

            cls._main_app = app
        return cls._main_app



def sanitizePath(p):
    if not p:
        arapi.bottle.redirect('/help')
    if p[0] != "/":
        return "/" + p
    else:
        return p


@app.get('/help')
def help():
    arapi.bottle.response.content_type = "text/plain"
    return app.config.doc


@app.get('/get/<path:path>')
@app.get('/match/<path:path>')
def handle_get_or_match(path, augeas_handle):
    """  Will do augeas get or match for given path expression.
         E.g.:
           /get/files/etc/hosts/1/ipaddress
           /match/files/etc/hosts/*

         More about Augeas paths:
           https://github.com/hercules-team/augeas/wiki/Path-expressions
    """
    # is this lame? Any better way to find out whether it was "get" or "match"?
    action = bottle.request.path.split('/')[1]
    if action == 'get':
        result = augeas_handle.get(sanitizePath(path))
    elif action == 'match':
        result = augeas_handle.match(sanitizePath(path))
    arapi.bottle.response.content_type = "text/plain"
    return result

