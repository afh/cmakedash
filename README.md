cmakedash
=========

A [CMake](http://cmake.org/) docset for [Dash](http://kapeli.com/dash/)
(inspired by [pgdash](https://github.com/datasaur/pgdash)).

Requirements
------------

* [Python](https://www.python.org)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)


Usage
-----

To generate a Dash compatible docset run the `cmakedash.py` script,
it will then create the following files in the `build` directory:

* `CMake.docset` - The CMake documentation as a Dash docset
* `CMake.xml` - File for use as a Dash docset feed
* `CMake.tgz` - A tar archive for use with a Dash docset feed


### Generating a Dash docset feed

When you would like to host a Dash docset feed add your feed URLs as
commandline arguments to `cmakedash.py` in order to generate the appropriate
feed URL entries into the XML feed file, e.g.:

    % ./cmakedash.py http://example.net/feed/CMake.tgz http://example.com/feed/CMake.tgz


Copyright
---------

See LICENSE for details.

CMake, the CMake logo, and the CMake documentation is copyrighted
by [Kitware](http://www.kitware.com/) under a [Creative Commons Attribution-NoDerivs 3.0 Unported License](http://creativecommons.org/licenses/by-nd/3.0/).

Dash is copyrighted by [Kapeli](http://kapeli.com/dash/).
