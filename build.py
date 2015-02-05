import os.path
import sys

DEPDIR=os.path.abspath(os.path.dirname(os.path.realpath(__file__ ))+'/../');
ROOTDIR=os.path.abspath(os.path.dirname(os.path.realpath(__file__ )));

# load our code from the zip or the directory
zipfn = os.path.join(ROOTDIR, 'pyBuilder.zip')
if os.path.isfile(zipfn):
	sys.path.append(zipfn)
else:
	sys.path.append(ROOTDIR)
from pyBuilder import *

def main():
	# This is the configuration you want to build. The more you add here, the longer it will take.
	# configurations = ['Debug', 'Release', 'RelWithDebInfo']
	# platforms      = ['x86', 'x64', 'x86_osx'] These correspond to Win 32- and 64-bit, and OS X 32-bit.
	
	configurations = ['Release', 'RelWithDebInfo']
	platforms      = ['x86']
	pyBuilder.run(ROOTDIR, DEPDIR, configurations, platforms)
	
if __name__ == '__main__':
	main()