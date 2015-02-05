# build_osx.py
# Description           :
# This script sets build options (platform, target) and hands them off to pyBuilder.py.

import os.path
import sys

DEPDIR	        =	os.path.abspath(os.path.dirname(os.path.realpath(__file__ ))+'/../')
ROOTDIR	        =	os.path.abspath(os.path.dirname(os.path.realpath(__file__ )))

print 'DEPDIR         :   ' + DEPDIR + "   (as reported by build_osx.py)"
print 'ROOTDIR        :   ' + ROOTDIR + "   (as reported by build_osx.py)"


# Import pyBuilder, first trying pyBuilder.zip, then src/pyBuilder.py.
# In OS X port, pyBuilder.py is not compressed (no zipfile).

zipfn = os.path.join(ROOTDIR, 'pyBuilder.zip')
if os.path.isfile(zipfn):
    sys.path.append(zipfn)
else:
    sys.path.append(ROOTDIR)
from pyBuilder import *

# =============================================================================
# Pass build parameters to pyBuilder.py, then run it.


def main():
    # Desired configuration(s) to build. The more configurations, the longer the build takes.
    # Configurations        :	['Debug', 'Release', 'RelWithDebInfo']
    # Targets ("platforms")	:	['x86', 'x64', 'osx_10.9']
    #					    :	(These correspond to Win 32- and 64-bit, and OS X 10.9 64-bit.)

    #configurations = ['Release', 'RelWithDebInfo']
    configurations = ['RelWithDebInfo']
    platforms      = ['osx_10.9']

    print "Configurations :  " + str(configurations) + "(as reported by build_osx.py)"
    print "PLATFORMS      :  " + str(platforms) + "(as reported by build_osx.py)"
    # haven't changed variable name yet from PLATFORMS to TARGETS

    print '\n' + ('=' * 80)
    print 'Running pyBuilder.py (the main build script)...'
    print ""
    pyBuilder.run(ROOTDIR, DEPDIR, configurations, platforms)

if __name__ == '__main__':
    main()