# PyCDP

[![PyPI](https://img.shields.io/pypi/v/chrome-devtools-protocol.svg)](https://pypi.org/project/chrome-devtools-protocol/)
![Python Versions](https://img.shields.io/pypi/pyversions/chrome-devtools-protocol)
![MIT License](https://img.shields.io/github/license/HyperionGray/python-chrome-devtools-protocol.svg)
[![Build Status](https://img.shields.io/travis/com/HyperionGray/python-chrome-devtools-protocol.svg?branch=master)](https://travis-ci.com/HyperionGray/python-chrome-devtools-protocol)
[![Read the Docs](https://img.shields.io/readthedocs/py-cdp.svg)](https://py-cdp.readthedocs.io)

Python Chrome DevTools Protocol (shortened to PyCDP) is a library that provides
Python wrappers for the types, commands, and events specified in the [Chrome
DevTools Protocol](https://github.com/ChromeDevTools/devtools-protocol/).

The Chrome DevTools Protocol provides for remote control of a web browser by
sending JSON messages over a WebSocket. That JSON format is described by a
machine-readable specification. This specification is used to automatically
generate the classes and methods found in this library.

You could write a CDP client by connecting a WebSocket and then sending JSON
objects, but this would be tedious and error-prone: the Python interpreter would
not catch any typos in your JSON objects, and you wouldn't get autocomplete for
any parts of the JSON data structure. By providing a set of native Python
wrappers, this project makes it easier and faster to write CDP client code.

**This library does not perform any I/O!** In order to maximize
flexibility, this library does not actually handle any network I/O, such as
opening a socket or negotiating a WebSocket protocol. Instead, that
responsibility is left to higher-level libraries, for example
[trio-chrome-devtools-protocol](https://github.com/hyperiongray/trio-chrome-devtools-protocol).

For more information, see the [complete documentation](https://py-cdp.readthedocs.io).

<a href="https://www.hyperiongray.com/?pk_campaign=github&pk_kwd=pycdp"><img alt="define hyperion gray" width="500px" src="https://hyperiongray.s3.amazonaws.com/define-hg.svg"></a>
