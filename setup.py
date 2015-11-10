#NOTE: See the README file for a list of dependencies to install.

try:
    from setuptools import setup, Extension
except ImportError:
    print("No setuptools found, attempting to use distutils instead.")
    from distutils.core import setup, Extension
import sys

err = ""

try:
    import usb
except ImportError:
    err += "usb (apt-get install python-usb)\n"

try:
    import rflib
except ImportError:
    err += "rfcat and rflib (https://bitbucket.org/atlas0fd00m/rfcat)\n"


if err != "":
    print >>sys.stderr, """
Library requirements not met.  Install the following libraries, then re-run
the setup script.

""", err
    sys.exit(1)

setup  (name        = 'killerzee',
        version     = '0.1.0',
        description = 'Z-Wave Attack Framework and Tools',
        author = 'Joshua Wright',
        author_email = 'jwright@willhackforsushi.com',
        license   = 'LICENSE.txt',
        packages  = ['killerzee'],
        requires = ['rflib'],
        scripts = ['tools/zwdump', 'tools/zwreplay', 'tools/zwpoweroff',
            'tools/zwthermostatctrl', 'tools/zwthermostattemp' ]
        )

