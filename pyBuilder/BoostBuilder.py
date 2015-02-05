from pyBuilder import *

class BoostBuilder(BuildTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            return_value = self.unzip('files/boost_*.bz2')
            if os.path.isdir(globals()['ROOT'] + '/Boost'):
                shutil.rmtree(globals()['ROOT'] + '/Boost')
            os.rename(globals()['ROOT'] + '/Boost_1_55_0', globals()['ROOT'] + '/Boost') # for compatibility with build script
            return return_value
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.unzip('files/Boost_*.zip')
        else:
            print "Build platform not supported. See \'def extract\' in BoostBuilder.py."
            return 1


    def configure(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Configuring Boost...')
            if os.path.exists(str(globals()['ROOT'] + '/Boost-build')):
                print('Found an existing Boost build directory. Removing it.')
                shutil.rmtree(globals()['ROOT'] + '/Boost-build')
            os.mkdir(globals()['ROOT'] + '/Boost-build')
            os.chdir(globals()['ROOT'] + '/Boost/tools/build/v2')
            os.system('./bootstrap.sh')
            os.system('./b2 install --prefix=' + globals()['ROOT'] + '/Boost-build')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.execute(r"""
cd boost_*
echo "bootstrapping boost ..."
call bootstrap.bat
call:checkReturnValue
""")
        else:
            print "Build platform not supported. See \'def configure\' in BoostBuilder.py."
            return 1


    def build(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Building Boost...')
            os.chdir(globals()['ROOT'] + '/Boost')
            os.system(globals()['ROOT'] + '/Boost-build/bin/b2 \\'
                      '--layout=versioned \\'
                      '--build-type=minimal \\'
                      'toolset=darwin \\'
                      'link=static architecture=x86 \\'
                      'address-model=32 \\'
                      'stage')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            global PLATFORMS, CONFIGURATIONS
            cmd = r"""
    cd boost_*
    """
            if 'x86' in PLATFORMS:
                if 'Release' in CONFIGURATIONS:
                    cmd += r"""
    echo "building boost 32 bits RELEASE ..."
    bjam -j%(maxcpu)d --toolset=msvc-10.0 address-model=32 variant=release link=static threading=multi runtime-link=shared --build-type=minimal --stagedir=x86
    call:checkReturnValue
    """
                    return self.execute(cmd)
                if 'Debug' in CONFIGURATIONS:
                    cmd += r"""
    echo "building boost 32 bits DEBUG ..."
    bjam -j%(maxcpu)d --toolset=msvc-10.0 address-model=32 variant=debug inlining=off debug-symbols=on link=static threading=multi runtime-link=shared --build-type=minimal --stagedir=x86
    call:checkReturnValue
    """
                    return self.execute(cmd)
            if 'x64' in PLATFORMS:
                if 'Release' in CONFIGURATIONS:
                    cmd += r"""
    echo "building boost 64 bits RELEASE ..."
    bjam -j%(maxcpu)d --toolset=msvc-10.0 address-model=64 variant=release link=static threading=multi runtime-link=shared --build-type=minimal --stagedir=x64
    call:checkReturnValue
    """
                    return self.execute(cmd)
                if 'Debug' in CONFIGURATIONS:
                    cmd += r"""
    echo "building boost 64 bits DEBUG ..."
    bjam -j%(maxcpu)d --toolset=msvc-10.0 address-model=64 variant=debug inlining=off debug-symbols=on link=static threading=multi runtime-link=shared --build-type=minimal --stagedir=x64
    call:checkReturnValue
    """
                    return self.execute(cmd)

    def install(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            target = 'osx_10.9'
            print('    Installing Boost...')
            header_source_dir = globals()['ROOT'] + '/Boost/boost'
            header_target_dir = globals()['ROOT'] + '/include/' + str(target) + '/Boost'
            library_source_dir = globals()['ROOT'] + '/Boost/stage/lib'
            library_target_dir = globals()['ROOT'] + '/lib/' + str(target) + '/Boost'
            if os.path.exists(header_target_dir):
                print('    Found existing header target directory. Removing it.')
                shutil.rmtree(header_target_dir)
            if os.path.exists(library_target_dir):
                print('    Found existing library target directory. Removing it.')
                shutil.rmtree(library_target_dir)
            print('    Copying Boost headers to:\n' + (' '*8) + header_target_dir)
            shutil.copytree(header_source_dir, header_target_dir)
            print('    Copying Boost libraries to:\n' + (' '*8) + library_target_dir)
            shutil.copytree(library_source_dir, library_target_dir)
            return 0
        elif 'x86' in PLATFORMS:
            global PLATFORMS, CONFIGURATIONS
            dir = self.getFirstFolder()
            return_code = 0
            self.arch = 'x86'
            if 'x86' in PLATFORMS:
                return_code |= self.installIncludes(dir+'/Boost', True, 'boost')
                return_code |= self.installLibs(dir+'/%(arch)s/lib/*.lib')
            if 'x64' in PLATFORMS:
                self.arch = 'x64'
                return_code |= self.installIncludes(dir+'/Boost', True, 'boost')
                return_code |= self.installLibs(dir+'/%(arch)s/lib/*.lib')
            return return_code
        else:
            print "Build platform not supported. See \'def install\' in BoostBuilder.py."
            return 1