==========
tlswrapper
==========

Wrap an existing socket connection to make it a secure connection.
This is meant to be used with other tools, such as a simple http-only
server that you want to be accessible from http. Can also be used to
wrap an insecure socket connection and connect to a secure endpoint.


Installation
------------

To install tlswrapper, run the command::

  $ python3.6 -m pip install --user git+https://github.com/player1537/tlswrapper.git

If you get an error about ``-m pip``, first run::

  $ python3.6 -m ensurepip


Usage
-----

First, run a server that listens on some host/port combination, for
instance::

  $ python3 -m http.server --bind 127.0.0.1 8080

Then in another terminal, run the tlswrapper program::

  $ tlswrapper -u 127.0.0.1:8080 -b 127.0.0.2:4443

Which says: the upstream server (that we forward our requests to) is
``127.0.0.2`` on port ``8080``, and we bind ourselves to ``127.0.0.3``
on port ``4443``.

It can also be used in the other way, using the ``-r`` ("reverse")
flag::

  $ tlswrapper -r -u 127.0.0.2:4443 -b 127.0.0.3:8080

By connecting to ``127.0.0.3:8080``, you should see the same thing as
if you connected to ``127.0.0.1:8080``, but a little slower because
extra TLS work has been done in the middle.
