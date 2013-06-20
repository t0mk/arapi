__author__ = 'Tomas Karasek'
__version__ = '0.1'

import augeas
import inspect
import bottle
import logging

class AugeasPlugin(object):

    name = 'augeas'
    api = 2

    def __init__(self, root, loadpath, keyword='augeas_handle'):
        self.root = root
        self.loadpath = loadpath
        self.keyword = keyword
        self.augeas_handle = self.getAugeasHandle()

    def getAugeasHandle(self):
        logging.debug("Creating Augeas handle with root=%s, loadpath=%s" %
                      (self.root, self.loadpath))
        a = augeas.Augeas(root=self.root, loadpath=self.loadpath)
        return a

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, AugeasPlugin): continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another augeas plugin with "\
                        "conflicting settings (non-unique keyword).")

    def apply(self, callback, route):

        cb_args = inspect.getargspec(route.callback)[0]
        if self.keyword not in cb_args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = self.augeas_handle

            returned_value = callback(*args, **kwargs)
            return returned_value

        return wrapper

Plugin = AugeasPlugin
