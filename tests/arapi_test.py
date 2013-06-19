import arapi

def test_help():
    assert len(arapi.help()) > 0

def test_get():
    c = arapi.config.GetConfig(devel=True)
    arapi.AugeasSingletonWrapper(root=c['root'], loadpath=c['loadpath'])
    r = arapi.handle_get_or_match('get', 'files/etc/hosts/1/ipaddr')
    assert r == '127.0.0.1'

def test_match():
    c = arapi.config.GetConfig(devel=True)
    arapi.AugeasSingletonWrapper(root=c['root'], loadpath=c['loadpath'])
    r = arapi.handle_get_or_match('match', 'files/etc/hosts/*')
    assert r == ['/files/etc/hosts/1']


