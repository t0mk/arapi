arapi
=====

Arapi is RESTful HTTP API to Augeas. It exposes the tree over HTTP. In future it will also allow modification.

Dependencies
------------
On Ubuntu, the only dependency is python-augeas. bottle.py is included as the version in Ubuntu is very old. You can install python-augeas with apt-get or pip. pip would be preferred but python-augeas in 12.04 seems to work alright.

  Didn't try on RHEL clones yet but if it works with the old versions in Ubuntu repos, it's gotta work in RHEL world too. I didn't (and will not) try with python2.4 so running it on RHEL5 clones will be non-trivial.

Instructions
------------
To run a devel instance, do ./arapi\_start\_devel in the top-level dir. see arapi/conf/arapi\_dev.cfg for configuration details.

  If arapi is listening on 127.0.0.1:8091, you can see nodes in /etc/hosts as:

```
curl 'http://127.0.0.1:8091/match/files/etc/hosts/*'
```

Or you can see the IP of the first node in /etc/hosts as
```
curl 'http://127.0.0.1:8091/get/files/etc/hosts/1/ipaddress'
```

You can see available API resources at:
```
curl http://127.0.0.1:8091/help
```
This is generated automatically from docstrings of handling functions.


  A devel instance will read configuration from arapi/conf/arapi_dev.cfg, normal instance will attempt to read it from /etc/arapi/arapi.cfg. The config file location is passed in environment variable ARAPI_CONFIG.

  You can also supply additional lens files in a directory. You must specify the directory in arapi.cfg then.

Packaging
---------
I try my best with setuptools so
```
python setup.py install
```
should install the package. I will improve this later.

References
----------
- http://augeas.net
- python bindings: https://github.com/hercules-team/python-augeas

