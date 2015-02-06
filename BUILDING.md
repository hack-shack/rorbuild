Building Rigs of Rods on OS X "Mavericks"
=========================================
Author				:	hack-shack
RoR target version		:	0.4.0.7
OS X target version		:	10.9.2

Overview
========
Rigs of Rods is a somewhat complex beast. It has a 3D engine, physics simulator, water and sky plug-ins, input device system, networking, localization plug-in module... and so on.

Some of these components are required to build RoR; some are optional.

Rigs of Rods is built in 4 steps:
  * Download source code for RoR and supporting libraries (dependencies)
  * Compile libraries
  * Using CMake, create a Makefile for RoR
  * Use make to build the RoR app (xcodebuild on Mac)
  
Required tools
==============
(YAML table below. If you don't see two columns, switch your Markdown reader to raw text mode.)
Xcode				:
	version			:	5.1 (5B130a)
	notes			:	Requires Xcode Command Line Tools to be installed.
	sourcefile		:	Mac App Store


Python				:
	version			:	2.7.5 (OS X built-in)
	notes			:	Required to run RoR build scripts.
	sourcefile		:	Built into OS X 10.9


CMake				:	
	version			: 	2.8.12.2 (installed via homebrew)
	notes			:	see below
	sourcefile		:	see below

Installing CMake
----------------	
Install Homebrew. http://brew.sh

Open a terminal window and run 'brew install cmake' to install CMake into a Homebrew bottle. If you already have an older version of CMake installed, Homebrew should warn you.

Run 'cmake --version' and verify it's at least 2.8.12.2 (used in this guide). If it's showing up as a different version, you may need to unlink and reinstall CMake (see above) or you have a conflicting version installed elsewhere (MacPorts, perhaps?)


Libraries (dependencies)
========================
Rigs of Rods needs these libraries to compile.
pyBuilder.py builds the libraries in the following order.
Libraries were selected to mirror those in RoR-Dependencies-v26 for Windows.
Certain library versions from the v26 package didn't work on OS X 10.9, so these have been annotated below.


First, build the simpler libraries
---------------------------------------
WxWidgets			:
	version			:	3.0.0
	notes			:	WxWidgets 3.0 required to build for OS X 10.9;
					:	Carbon is deprecated, which WxWidgets 2.9 used.
					:	(As of Mar 2014, RoR for Windows 0.4.0.7 uses WxWidgets 2.9.1.)
	sourcefile		:
		https://sourceforge.net/projects/wxwindows/files/3.0.0/wxWidgets-3.0.0.tar.bz2

  Build steps		:
  * cd to tmp directory, then:
  * wget https://sourceforge.net/projects/wxwindows/files/3.0.0/wxWidgets-3.0.0.tar.bz2
  * tar -xvf wxWidgets-3.0.0.tar.bz2; cd wxWidgets-3.0.0
  * mkdir wxwidgets-release; cd wxwidgets-release
  * ../configure; make
  * copytree wxwidgets-release/lib
  * copytree wxwidgets-release/
  * copytree include/wx



MoFileReader		:
	description		:	Reads .mo files; these are language localizations.
	version 		:	0.1.3: released 2012-05-20
	sourcefile		:	git; see "build process" below
	
  Build steps		:
  * cd to tmp directory, then:
  * git clone https://code.google.com/p/mofilereader/
  * cd mofilereader/build
  * cmake .
  * make

  Build products	:
	static lib		:	tmp/mofilereader/lib/libmoFileReader.static.a
	executable		:	tmp/mofilereader/bin/moReader



SocketW				:
	description		:	Streaming socket C++ library. (Networking and inter-process
					:	communication)
	url				:	http://www.digitalfanatics.org/cal/socketw/
	version			:	r031026 (2003-10-26)
	last_checked	:	2014-03-24
	sourcefile		:	http://www.digitalfanatics.org/cal/socketw/files/SocketW031026.tar.gz
	
	Build steps		:
	* from RoR dependencies src/ directory:
	* extract SocketW031026.tar.gz; rename created dir to "SocketW" exactly
	* cd SocketW/src
	* md5 sw_base.cxx
						...result should be (pre-patch):
			Version	:	SocketW_031026
				MD5	:	f13e583bb828b75c2cc388d044c9593f
	* patch < ../../files/SocketW.diff
	  (this changes "exit" to "_exit" in sw_base.cxx so it builds on OS X)
	* md5 sw_base.cxx
	  					...result should be (post-patch):
			Version	:	SocketW_031026
				MD5	:	0eee61a0b51f261734194e33d9b83f24
	* make
	
	Build products	:
	headers			:	SocketW.h, sw_base.h, sw_config.h, sw_inet.h, sw_internal.h,
						sw_ssl.h, sw_unix.h
	static lib		:	libSocketW.a
	executable		:		


	
AngelScript			:
	description		:	Provides in-game scripting.


	
OIS					:	
	description		:	Object-oriented Input System
	url				:	http://sourceforge.net/projects/wgois/
	version			:	1.3
	last_update		:	2013-04-29



PThreads
	description		:	POSIX Threads
	notes			:	Built into OS X.
	header_path		:	/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/pthread.h
	library_path	:	/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/lib/libpthread.dylib



curl
	description		:	"curl groks URLs"
	url				:	http://curl.haxx.se
	version
	notes			:	Built into OS X. (.dylib only)
	header_path		:	/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/include/curl/curl.h
	library_path	:	/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr/lib/libcurl.dylib

Read "Important note for curl users on OS X Mavericks 10.9, here:
http://curl.haxx.se/mail/archive-2013-10/0036.html


	
OpenALSoftBuilder
	description		:	Audio
	version			:	1.15.1 (win32 version is 1.13)
	source_code		:	http://kcat.strangesoft.net/openal-releases/openal-soft-1.15.1.tar.bz2
	
Note: Downloadable code may crash. Use nightly builds instead:
http://www.rigsofrods.com/threads/109854-Rigs-of-Rods-supports-HRTF-(Headphone-3D-Audio)!?p=1312516#post1312516



Build libraries which depend on Boost
---------------------------------------

Boost
	description		:	Cross-platform C++ framework, used for RoR-specific code


Ogre
----
	description		:	3D engine
	version			:	1.8.1
	notes			:	1.8.1 is the latest stable release of the Ogre v1.8 tree.
					:	Ogre changes with each .x release. Currently RoR builds against
					:	the Ogre 1.8 tree.
	sourcefile		: http://downloads.sourceforge.net/project/ogre/ogre/1.8/1.8.1/ogre_src_v1-8-1.tar.bz2

	sourcefile on mercurial (optional):
  	* cd ~/Developer (or wherever you're building the RoR project)
  	* hg clone http://bitbucket.org/sinbad/ogre/ -u -v1-8
  	* Mercurial downloads 265MB of data to ogre directory.

	build steps		:
	* mkdir Ogre/build; cd Ogre/build
	* 

	
		
Building Ogre with RoRBuilder.py
================================
Ogre is the trickiest library to get working. The codebase currently uses Ogre version 1.8.1 (2014-05). This is an explanation of how RoRBuilder.py does it.

Patch Ogre
----------

	Patch description for Mavericks: https://github.com/osrf/homebrew-simulation/issues/2
	Patch itself (for Ogre 1.7.4): https://gist.github.com/hgaiser/7346167
	
	Build CppUnit: https://code.google.com/p/tonatiuh/wiki/InstallingCppUnitForMac
	Doxygen
	GLSLOptimizer
	HLSL2GLSL


Configure Ogre CMakeLists.txt
-----------------------------
	Ogre 1.8.1		:
		Change
		OgreOSXCocoaWindow.mm, line 235:
		NameValuePairList::const_iterator param_useNSView_pair(NULL);
	to:
		NameValuePairList::const_iterator param_useNSView_pair;
	
	Change
		OgreOSXCocoaWindow.mm, line 121:
		NameValuePairList::const_iterator opt(NULL);
	to:
		NameValuePairList::const_iterator opt;


Build libraries which depend on Ogre
---------------------------------------

PagedGeometryBuilder
	description		:	Paged geometry (large landscape) library for Ogre

CaelumBuilder
	description		:	Sky, sun, weather library for Ogre
	version			:	0.6.1 (zip file, not gz)
	sourcefile		:	https://caelum.googlecode.com/files/caelum-0.6.1.zip

MyGUIBuilder
------------
	description		:	GUI library for Ogre
	version			:	3.2.0
	sourcefile		:	http://downloads.sourceforge.net/project/my-gui/MyGUI/MyGUI_3.2.0/MyGUI_3.2.0.zip
	
	Build steps		:
	* unzip MyGUI_3.2.0.zip
	* mv MyGUI_3.2.0 MyGUI
	* mkdir MyGUI/build
	* cd MyGUI/build
	* cmake ../. -DOgre_INCLUDE_DIR=/Users/asa/Developer/rigs_of_rods/dependencies_0.4.0.7_osx_10.9/include/osx_10.9/Ogre -DOgre_LIBRARIES="debug;OgreMain_d;optimized;OgreMain" -DOgre_LIB_DIR=/Users/asa/Developer/rigs_of_rods/dependencies_0.4.0.7_osx_10.9/lib/osx_10.9/Ogre/Release






Dependencies must be in <source-directory>/dependencies. (In same directory as CMakeDependenciesConfig.txt.)


Copying Ogre and using the dynamic library
------------------------------------------
Download Ogre 1.8.0 SDK for OS X.
cp /Volumes/OgreSDK/OgreSDK/include/Ogre <ror_dependencies_dir>/include/osx_10.9/Ogre
cp /Volumes/OgreSDK/OgreSDK/include/OIS <ror_dependencies_dir>/include/osx_10.9/OIS
cp /Volumes/OgreSDK/OgreSDK/lib/*.dylib <ror_dependencies_dir>/lib/osx_10.9/Ogre/Release/
cp -R /Volumes/OgreSDK/OgreSDK/lib/pkgconfig <ror_dependencies_dir>/lib/osx_10.9/Ogre/Release/
cp -R /Volumes/OgreSDK/OgreSDK/lib/release <ror_dependencies_dir>/lib/osx_10.9/Ogre/Release/
cp /Volumes/OgreSDK/OgreSDK/lib/release/libOIS.a <ror_dependencies_dir>/lib/osx_10.9/OIS/Release/
cp -R /Volumes/OgreSDK/OgreSDK/boost/boost <ror_dependencies_dir>/include/osx_10.9/
mv <ror_dependencies_dir>/include/osx_10.9/boost <ror_dependencies_dir>/include/osx_10.9/Boost/
cp -R /Volumes/OgreSDK/OgreSDK/boost/lib/*.a <ror_dependencies_dir>/lib/osx_10.9/Boost/Release/


Step 3: Build RoR
===============================================================================

Gather up compiled libraries into a directory structure for CMake
-----------------------------------------------------------------


Download RoR source

Configure CMake
---------------
Packages not found so far:

OGRE
OGRE-Terrain
OGRE-Paging	
OGRE-RTShaderSystem
OIS... finds version 1.3, presumably in system?



============================== end of tutorial ==============================

Future Ideas
============
See:  http://www.rigsofrods.com/wiki/pages/Planned_Features

I think the following stuff would make RoR rock.

SkyX				:
  * moon phase support
  * thunderstorm systems
  * interesting development model: new features crowdfunded
  url	:	http://www.paradise-sandbox.com/#hydraxskyx.php
  As of 2014-03-23	:	Hydrax 0.5.1 / SkyX 0.4

Ogre volume component
  * allows overhangs in terrain
  * site: www.volume-gfx.com
  * example: http://www.youtube.com/watch?v=3DNLkKKKDX8

SWIG				:
	description		:	interfaces to C++ code; use with python for motion platforms
	homepage		:	http://www.swig.org/Doc1.3/Introduction.html

Arbaro			:
	description		:	tree generation for povray
	homepage		:	arbaro.sourceforge.net
	notes			:	java library.
	
The same tree algorithm is used in a Python script, Sapling Tree: http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Curve/Sapling_Tree

Libraries for the following things
  * Flora	:	quadruped skeleton generator and animal behavior AI,
  			:	coupled to SkyX (wind sim)
  * Fauna	:	fast, pretty hardware plant generation and rendering
  * Mecha	:	AI framework for simulated traffic, using collision-avoidance
  				strategy: http://www.traffic-simulation.de/
  * Fractal terrain : http://complexity.massey.ac.nz/posters/pdf/A0-Fractal-Terrain-Poster.pdf
  * MyGUI replacement: libRocket, HTML/CSS game interface middleware (C++)
  					 :	http://librocket.com

"Shroud cloth sim goes free," http://www.ogre3d.org/forums/viewtopic.php?f=1&t=65004
...not libre, but worth a look

Fonts
==================================================
Below fonts are from Open Font Library.

MIT (X11) licensed
http://openfontlibrary.org/en/font/couture
http://openfontlibrary.org/en/font/estrangelo-edessa

OFL (SIL Open Font License)
http://openfontlibrary.org/en/font/acknowledgement
http://openfontlibrary.org/en/font/logisoso
http://openfontlibrary.org/en/font/h-h-samuel
http://openfontlibrary.org/en/font/k-o-activista
http://openfontlibrary.org/en/font/m-f-plexus-italic

http://openfontlibrary.org/en/font/j-m-nexus-grotesque
http://openfontlibrary.org/en/font/news-cycle
http://openfontlibrary.org/en/font/bananal-brick



Build notes
===========
Make a directory named "tmp" in the root path of the RoR build directory. (Alongside this file.)
Build in sequential order:

WxWidgets
-------------------------------------------------------------------------------

  
  

	

Ogre dependencies
-------------------------------------------------------------------------------
  * Go here: http://www.ogre3d.org/download/source
  * Download Ogre 1.8.1 Source for Linux/OSX (88.6MB)
  * cd to RoR master directory, then "hg clone https://bitbucket.org/cabalistic/ogredeps"
  * Download Dependencies Source Repo... (26.4MB)
  * cd ogredeps
  * cmake .
  * make
  * sudo make install
  
         
            
Ogre Xcode templates
--------------------
  Get Xcode 4 templates:
  http://downloads.sourceforge.net/project/ogre/ogre-dependencies-mac/1.8/Ogre_Xcode4_Templates_20130325.pkg.zip

Ogre
-------------------------------------------------------------------------------
Install Command Line Tools (Mavericks) for Xcode
	https://developer.apple.com/downloads/index.action

Download Cg (v3.1, Cg is legacy, last checked 2014-04):
http://developer.download.nvidia.com/cg/Cg_3.1/Cg-3.1_April2012.dmg

cmake -D BOOST_ROOT=/Users/asa/Developer/rigs_of_rods/ror_dependencies_v26/src/Boost/boost -D BOOST_LIBRARYDIR=/Users/asa/Developer/rigs_of_rods/ror_dependencies_v26/libs/x86/Boost -D Boost_DEBUG=1 -D OGRE_DEPENDENCIES_DIR=/Users/asa/Developer/rigs_of_rods/ror_dependencies_v26/src/files/ogredeps/build/src -D OGRE_STATIC=1 -D CMAKE_OSX_ARCHITECTURES=i386 -D OGRE_BUILD_SAMPLES=0 -G Xcode ../Ogre

open OGRE.xcodeproj




OpenALSoft
-------------------------------------------------------------------------------
May need pthreads to be built first. This error occurs during make:
	clang: warning: argument unused during compilation: '-pthread'

cd to tmp directory, then:
  * wget http://kcat.strangesoft.net/openal-releases/openal-soft-1.15.1.tar.bz2
  * tar -xvf openal-soft-1.15.1.tar.bz2
  * cd openal-soft-1.15.1/build
  * cmake ..
  * make


OIS
-------------------------------------------------------------------------------
OIS 1.3 needs to be patched to compile on OS X 10.9. It references Carbon, which
is deprecated. The following patch makes it work (no joystick/gamepad support):
http://sourceforge.net/p/wgois/patches/35/

Diff file itself: http://sourceforge.net/p/wgois/patches/_discuss/thread/3aad1ad2/6d46/attachment/cocoa.diff

There seem to be two versions of the ois-v1-3.tar.gz file. One has a reference to Xcode 2.4; the other has a reference to Xcode 3.0. If the wrong version is used, cocoa.diff will fail to patch chunk #1. This does not stop it from compiling, but we should distribute a copy of the OIS source (zlib license; OK as long as it isn't modified) with the appropriate cocoa.diff file.

cd to tmp directory, then:
  * wget http://sourceforge.net/p/wgois/patches/_discuss/thread/3aad1ad2/6d46/attachment/cocoa.diff
  * wget http://downloads.sourceforge.net/project/wgois/Source%20Release/1.3/ois_v1-3.tar.gz
  * tar -xvf ois-v1-3.tar.gz
  * cp cocoa.diff ois-v1-3/
  * cd ois-v1-3/
  * patch -p0 < cocoa.diff
  
  Copy over the new Xcode project; this is setup for OS X 10.9's compiler.
  
  * xcodebuild -target OIS -target OISdylib -target OISstatic

MD5 hashes
----------
Mac/XCode-2.2/OIS.xcodeproj/project.pbxproj
	unpatched v2.4	:		67cc905a253bd62b811fbe61a13757fd
	patched	v2.4	:		da1050e4f55abef93a341eefac470031
includes/mac/MacMouse.h
	unpatched		:		ba394be60522be0396d496012a7106da
	patched			:		ba394be60522be0396d496012a7106da
includes/mac/CocoaMouse.h
	unpatched		:	
	patched			:		9a9e52d0b7fd667383175ee30482be41
includes/mac/CocoaInputManager.h
	unpatched		:	
	patched			:		9c5dabefcd0aeb8d9c3311c7f10c15fb
includes/mac/MacHIDManager.h
	unpatched		:	
	patched			:		0e457b701a4588a8cf64d1621b5115ea
includes/mac/MacKeyboard.h
	unpatched		:	
	patched			:		768fa8613a08378e27a2179609ba8591
includes/mac/MacHelpers.h
	unpatched		:	
	patched			:		afc98e9bebcbf474d9a0ad5788df32c1
includes/mac/CocoaJoyStick.h
	unpatched		:	
	patched			:		458db382d99a281d530daed1706eb541
includes/mac/CocoaKeyboard.h
	unpatched		:	
	patched			:		6c17cee71a85f22442938a849ed786ee
includes/mac/CocoaHelpers.h
	unpatched		:	
	patched			:		a8a5839d28332779c605164b7951f105
demos/OISConsole.cpp
	unpatched		:	
	patched			:		5f43a6c8dc2eba201f94b4e9f0782a32
src/mac/MacHIDManager.cpp
	unpatched		:	
	patched			:		e28b6e083279db6752ff7e4e5ae48e29
src/mac/MacKeyboard.cpp
	unpatched		:	
	patched			:		ee0e37c2c86751a5f7e932c7bf86790e
src/mac/MacHelpers.cpp
	unpatched		:	
	patched			:		dd7e4f453366a5c9dfdac3d8fff02a62
src/mac/CocoaMouse.mm
	unpatched		:	
	patched			:		afd3b71a1649d4ca3935564eaea214c0
src/mac/CocoaInputManager.mm
	unpatched		:	
	patched			:		1ad299cc3fc93d54c7adfd485ebf9706
src/mac/MacMouse.cpp
	unpatched		:	
	patched			:		e36622c5e8dc65233cd3ae239b0e49f6
src/mac/MacInputManager.cpp
	unpatched		:	
	patched			:		f5ec147d80e3d8860e237fb820d98aba
src/mac/CocoaJoyStick.mm
	unpatched		:	
	patched			:		a9284c05588f978e66326f5c38ad5b11
src/mac/CocoaKeyboard.mm
	unpatched		:	
	patched			:		f1db13e65a6705a07c12a868664ca43c
src/OISInputManager.cpp
	unpatched		:	
	patched			:		78d78b751aa14873e8659696b9728fac


AngelScript
-------------------------------------------------------------------------------
cd to tmp directory, then:
  * wget http://www.angelcode.com/angelscript/sdk/files/angelscript_2.28.2.zip
  * unzip angelscript_2.28.2.zip;mv sdk angelscript
  * mkdir angelscript-release;cd angelscript-release
  * cmake ../angelscript/angelscript/projects/cmake/.
  * make

Build products	:
	static lib	:	tmp/angelscript/angelscript/lib/libAngelscript.a
	executable	:	tmp/angelscript/angelscript/samples/game/bin/game
				:	(this is a test game; avoid the zombies)



CMake (RoR makefile)
====================

Use CMake to create a Makefile for RoR.





Notes on Ogre
=============

Command to run Ogre build over and over:
  * mkdir build in decompressed Ogre directory
  * cd Ogre/build
  * cd ..;rm -rf ./build;mkdir build;cd build;cmake ../.

-- The following external packages were located on your system.
-- This installation will have the extra features provided by these packages.
+ zlib
+ zziplib
+ freeimage
+ freetype
+ OpenGL
+ OpenGL ES 1.x
+ OpenGL ES 2.x
+ cg
+ boost
+ boost-thread
+ boost-date_time
+ boost-system
+ boost-chrono
+ OIS
+ Doxygen
+ iOS SDK
+ Carbon
+ Cocoa
+ IOKit
+ CoreVideo



Automated testing
=================

Test on clean OS X 10.9.2 install with re-imageable home directory built from a template. Push completed builds to remote Jenkins host.
Home directory rebuilt every time a build is pushed to the machine.
Re-imaged nightly, weekly, etc. depending on needs.

rorbuild automated build workflow:

  * ssh in, login via GUI, and scp the files 30 seconds later (hackish, but works) and then trigger them to launch with ssh ("open") command.
  
  * Modified master OS X home profile, with Xcode and Python "all set up."

  * Upon login, auto-create cached home directory from modified master profile directory template.

  * Slipstreamed copy of latest rorbuild snapshot, for auto-run upon login

  * Python "check-in" script to feed resulting build to Jenkins (running on a VPS)

  * Cleanup code to log out. Home directory is wiped after account logs out. 

This runs whenever we push the latest build to the machine.



Jenkins
=======

Create Standard user named "rorbuild."

Grant permissions:
  * Locate rorbuild directory somewhere logical, where you and Jenkins can access it.
    I use /Users/Shared/rorbuild.
  * Open Get Info for the rorbuild directory.
  * Click the plus button below the folder list at the bottom. A user list pops up.
    Click the "rorbuild" user in the list, then click the Select button.
  * Under Sharing & Permissions at the bottom of the Get Info window for rorbuild:
    ** Click the padlock icon at the bottom and authenticate.
    ** Change the "rorbuild" user's privilege level from No Access to Read & Write
    ** Click the gear button > Apply to enclosed items...

Jenkins > New Project > Rigs of Rods
Rigs of Rods > Configure
Build schedule: "H * * * *" (no quotes)
Execute shell: see script below
Change the path to point to the build_osx.sh script on your system.

echo RoRBuild | su rorbuild -S cd /Users/Shared/rorbuild/;python build_osx.py

Hit Save.

