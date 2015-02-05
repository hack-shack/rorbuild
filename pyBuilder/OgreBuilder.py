# OgreBuilder.py
# To build, Ogre requires Boost. Boost should be built before Ogre.

from pyBuilder import *
import hashlib

class OgreBuilder(BuildCMakeTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            rorbuild_root = str(globals()['ROOT'])
            print('    Extracting Ogre\n    ---------------')
            self.unzip('files/ogre_src_v*.bz2')
            if os.path.exists(rorbuild_root + '/build/Ogre'):
                print('Found Ogre build directory. Removing it...')
                shutil.rmtree(rorbuild_root + '/build/Ogre')
            if not os.path.exists(rorbuild_root + '/build/Ogre'):
                print('Couldn\'t find Ogre build directory. (This is normal.) Creating...')
            os.rename(rorbuild_root + '/build/ogre_src_v1-8-1', rorbuild_root + '/build/Ogre')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            res |= self.unzip('files/ogre_src_v*.zip')
            res |= self.unzip('files/OgreDependencies_MSVC_*.zip', self.path+'/ogre_*')
            return res
        else:
            print "    Build platform not supported. See \'def extract\' in OgreBuilder.py."
            return 1

    def configure(self):
        rorbuild_root = str(globals()['ROOT'])
        target = str(globals()['PLATFORMS']).strip('[]')
        build_configuration = 'RelWithDebInfo'

        if 'osx_10.9' in target:
            print('\n    Configuring Ogre\n    ----------------')
            print('    rorbuild_root: ' + rorbuild_root)
        # prepare build directory
            if os.path.exists(rorbuild_root + '/build/Ogre-build'):
                print('    Found Ogre-build directory. Removing it...')
                shutil.rmtree(rorbuild_root + '/build/Ogre-build')
            if not os.path.exists(rorbuild_root + '/build/Ogre-build'):
                print('    Could not find Ogre-build directory. This is normal. Creating it...')
                os.mkdir(rorbuild_root + '/build/Ogre-build')
        # apply patches
            shutil.copyfile(rorbuild_root + '/patches/Ogre/CMakeLists.txt', rorbuild_root + '/build/Ogre/CMakeLists.txt')
            def md5sum(filename, blocksize=65536):
                hash = hashlib.md5()
                with open(filename, "r+b") as f:
                    for block in iter(lambda: f.read(blocksize), ""):
                        hash.update(block)
                return hash.hexdigest()
            md5_sw_base = md5sum(rorbuild_root + '/build/Ogre/RenderSystems/GL/src/OSX/OgreOSXCocoaWindow.mm')
            print md5_sw_base
            if md5_sw_base == 'b614e602d78efda87e822f6258b6f400': # Ogre 1.8.1 OSXCocoaWindow.mm, patched for OS X
                print '    Looks like OgreOSXCocoaWindow.mm is already patched for OS X.'
            if md5_sw_base == '6acd49721f85a94e4b869590c93b7039': # Ogre 1.8.1 OSXCocoaWindow.mm, unpatched
                print '    Found unpatched OgreOSXCocoaWindow.mm. Patching...'
                os.chdir(rorbuild_root + '/build/Ogre/RenderSystems/GL/src/OSX')
                subprocess.Popen("patch < ../../../../../../patches/Ogre/OgreOSXCocoaWindow.mm.diff", shell=True)
                # TODO: Verify the file was patched.
            else:
                print '    Couldn\'t md5sum OgreOSXCocoaWindow.mm. Maybe it\'s missing?'
                return 1

        # cmake
            os.chdir(rorbuild_root + '/build/Ogre-build')
            print('    Starting CMake...')
            if os.path.exists('/Applications/CMake.app/Contents/bin'):
                print('Found CMake in /Applications/CMake.app/Contents/bin. Adding to PATH and running CMake...')
            if not os.path.exists('/Applications/CMake.app/Contents/bin'):
                print('Did not find CMake in /Applications/CMake.app/Contents/bin. Download it, and copy '
                      'the CMake application into your Applications folder.')

            # Begin Ogre config options
            # -----------------------------------------------------------------
            os.system('PATH=/Applications/CMake.app/Contents/bin:$PATH;export PATH;cmake \\' + # generate Xcode project
            #'-D CMAKE_OSX_ARCHITECTURES=i386 \\' +
            #'-D CMAKE_PREFIX_PATH=' + rorbuild_root + ' \\' +
            #'-D CMAKE_INCLUDE_PATH=' + rorbuild_root + '/include/%s \\' % target +
            #'-D CMAKE_LIBRARY_PATH=' + rorbuild_root + '/lib/%s \\' % target +

            '-D Ogre_DEPENDENCIES_DIR=' + rorbuild_root + '/include/%s/OgreDeps \\' % target +
            '-D OGRE_STATIC=1 \\ ' +
            '-D OGRE_BUILD_RENDERSYSTEM_GL=TRUE \\' +
            '-D OGRE_BUILD_PLUGIN_BSP=TRUE \\' +  # Build BSP SceneManager plugin
            '-D OGRE_BUILD_PLUGIN_OCTREE=TRUE \\' + # Build Octree SceneManager plugin
            '-D OGRE_BUILD_PLUGIN_PFX=TRUE \\' +  # Build ParticleFX plugin
            '-D OGRE_BUILD_SAMPLES=TRUE \\' +
            '-D OGRE_BUILD_TOOLS=0 \\' +

            '-D Boost_DEBUG=1 \\' +
            '-D BOOST_ROOT=' + rorbuild_root + '/Boost/boost \\' +
            '-D BOOST_INCLUDEDIR=' + rorbuild_root + '/Boost \\' +
            '-D BOOST_LIBRARYDIR=' + rorbuild_root + '/lib/%s/Boost \\' % target +
            '-D Boost_NO_SYSTEM_PATHS=ON \\' +  # force Boost to use our libs

            #'-D OIS_PREFIX_PATH=' + rorbuild_root + '/include/%s/OIS \\' % target +
            '-D OIS_INCLUDE_DIR=' + rorbuild_root + '/include/%s/OIS \\' % target +
            '-D OIS_LIBRARY_DBG=' + rorbuild_root + '/lib/' + target + '/OIS/%s \\' % build_configuration +
            '-D OIS_LIBRARY_REL=' + rorbuild_root + '/lib/' + target + '/OIS/%s/libOIS.a \\' % build_configuration +
            '-D CMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk \\' +
            '-G Xcode \\' +
            '../Ogre')  # path to existing build
            # End Ogre config options
            # -----------------------------------------------------------------

            # Patch OgreOSXCocoaWindow.mm to use default constructor
            #OgreOSXCocoaWindow.mm

            print('    Finished Ogre configure stage.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.execute(r"""
cd %(path)s\ogre_src*
call:checkReturnValue

msbuild Dependencies\src\OgreDependencies.VS2010.sln /t:rebuild /p:Configuration=%(configuration_restricted)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
call:checkReturnValue

mkdir build_%(arch)s
cd build_%(arch)s
call:checkReturnValue

cmake .. -G %(generator)s ^
 -DBOOST_LIBRARYDIR="%(depsdir_cmake)s/libs/%(arch)s/boost" ^
 -DBoost_INCLUDE_DIR="%(depsdir_cmake)s/includes/%(arch)s/boost" ^
 -DOgre_BUILD_RENDERSYSTEM_D3D10=ON ^
 -DOgre_BUILD_RENDERSYSTEM_D3D11=ON ^
 -DOgre_BUILD_SAMPLES=OFF ^
 -DOgre_CONFIG_ALLOCATOR=4 ^
 -DOgre_CONFIG_CONTAINERS_USE_CUSTOM_ALLOCATOR=ON ^
 -DOgre_CONFIG_DOUBLE=OFF
call:checkReturnValue
""")
        else:
            print "Build platform not supported. See \'def configure\' in OgreBuilder.py."
            return 1

    def build(self):
        rorbuild_root = str(globals()['ROOT'])
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('\n    Building Ogre')
            print('    -------------')
            os.chdir(rorbuild_root + '/build/Ogre-build')
            os.system('xcodebuild clean')
            os.system('xcodebuild')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.execute(r"""
cd %(path)s\ogre_src*
call:checkReturnValue
cd build_%(arch)s
call:checkReturnValue

msbuild ogre.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
call:checkReturnValue
""")
        else:
            print "Build platform not supported. See \'def build\' in OgreBuilder.py."
            return 1


    def install(self):
        rorbuild_root = str(globals()['ROOT'])
        target = str(globals()['PLATFORMS']).strip('[]').strip('\'')
        build_configuration = 'RelWithDebInfo'
        if 'osx_10.9' in globals()['PLATFORMS']:
            #headers_source_dir = rorbuild_root + '/build/Ogre-build/lib/Debug/Ogre.framework/Headers'
            headers_source_dir = rorbuild_root + '/build/Ogre/OgreMain/include'
            headers_target_dir = rorbuild_root + '/include/' + target + '/Ogre'
            library_source_dir = rorbuild_root + '/build/Ogre-build/lib/Debug'
            library_target_dir = rorbuild_root + '/lib/' + target + '/Ogre/' + build_configuration
            print('\n    Installing Ogre\n    ---------------')
            if os.path.exists(headers_target_dir):
                print('    Found existing Ogre headers target directory. Removing it...')
                shutil.rmtree(headers_target_dir)
            print('    Copying Ogre headers...')
            shutil.copytree(headers_source_dir, headers_target_dir)
            if os.path.exists(library_target_dir):
                print('    Found existing Ogre library target directory. Removing it...')
                shutil.rmtree(library_target_dir)
            BuildTarget.create_target_directory(library_target_dir)
            BuildTarget.install_built_files('*.a', library_source_dir, library_target_dir)
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            dir = self.getFirstFolder()
            res  = self.installIncludes(dir+'/build_%(arch)s/include/')
            res |= self.installIncludes(dir+'/OgreMain/include/*')
            res |= self.installIncludes(dir+'/Components/Paging/include/*', True, 'Paging')
            res |= self.installIncludes(dir+'/Components/Property/include/*', True, 'Property')
            res |= self.installIncludes(dir+'/Components/RTShaderSystem/include/*', True, 'RTShaderSystem')
            res |= self.installIncludes(dir+'/Components/Terrain/include/*', True, 'Terrain')
            res |= self.installLibs(dir+'/build_%(arch)s/lib/%(conf)s/Ogre*.lib')
            #res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/cg.dll')
            res |= self.installBinaries(dir+'/Dependencies/bin/Release/cg.dll')
            res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/Ogre*.dll')
            #res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/Ogre*.pdb', False) #optional
            res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/Plugin_*.dll')
            #res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/Plugin_*.pdb', False) #optional
            res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/RenderSystem_*.dll')
            #res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/RenderSystem_*.pdb', False) #optional
            res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/*.exe')
            res |= self.installBinaries(dir+'/build_%(arch)s/bin/%(conf)s/*.pdb', False) #optional
            return res
        else:
            print "Build platform not supported. See \'def install\' in OgreBuilder.py."
            return 1

