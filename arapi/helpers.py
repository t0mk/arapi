# code usable by more apps

def getAppHandlingMethods(var_app):
    methods = set()
    for route in var_app.routes:
        if route.callback.__name__.startswith('handle_'):
            methods.add(route.callback)
        elif route.callback.__name__ == 'mountpoint_wrapper':
            methods.update(
                getAppHandlingMethods(route.config.mountpoint['target']))
    return methods

def getHelpDoc(var_app):
    txt = ("API listing for arapi instance\n"
           "==============================\n\n")
    for method in getAppHandlingMethods(var_app):
        txt += method.__doc__
        txt += "\n"
    return txt
