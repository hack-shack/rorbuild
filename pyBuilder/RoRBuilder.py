# RoRBuilder.py

from pyBuilder import *
import hashlib

class RoRBuilder(BuildCMakeTarget):

    def __init__(self):
        self.initPaths()

    def extract(self):
        print('\nExtracting RoR')
        print('--------------')

        def mkdir_p(self, path):
            try:
                os.makedirs(path)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise

        if 'osx_10.9' in globals()['PLATFORMS']:
            rorbuild_root = str(globals()['ROOT'])
            build_target = str(globals()['PLATFORMS']).strip('[]').strip('\'')
            source_dir = rorbuild_root + '/files/rigsofrods-codehg'
            build_dir = rorbuild_root + '/build/RoR'

            if os.path.exists(build_dir):
                print('    Found RoR build directory: ' + build_dir)
                print('    Removing it...')
                shutil.rmtree(build_dir)
            if not os.path.exists(build_dir):
                print('    Couldn\'t find RoR build directory. (This is normal.)')
                print('    build_dir: ' + build_dir)
            shutil.copytree(source_dir, build_dir)
            return 0
        elif 'x86' in build_target:
            return 0  # windows script needs writing
        else:
            print "    Build platform not supported. See \'def extract\' in RoRBuilder.py."
            return 1

    def configure(self):
        print('\nConfiguring RoR')
        print('---------------')
        if 'osx_10.9' in globals()['PLATFORMS']:
            cmake_path = '/opt/local/bin'
            rorbuild_root = str(globals()['ROOT'])
            build_configuration = str(globals()['CONFIGURATIONS']).strip('[]').strip('\'')
            build_target = str(globals()['PLATFORMS']).strip('[]').strip('\'')
            build_dir = os.path.join(rorbuild_root + '/build/RoR')
            include_dir = rorbuild_root + '/include/' + build_target
            library_dir = rorbuild_root + '/lib/' + build_target

            try:
                if os.path.exists(build_dir):
                    print('    Found a RoR build directory.')
                    #os.copyfile(rorbuild_root + '')
            except:
                if not os.path.exists(build_dir):
                    print('    Could not find a RoR build directory. See \'def configure\' in RorBuilder.py.')
                    print('    build_dir: ' + build_dir)

            print '    Replacing RoR CMakeLists.txt with updated version...'
            print '    ----------------------------------------------------'
            os.remove(build_dir + '/CMakeLists.txt')
            shutil.copyfile(rorbuild_root + '/patches/RoR/CMakeLists.txt', build_dir + '/CMakeLists.txt')
            os.remove(build_dir + '/CMakeDependenciesConfig.txt')
            shutil.copyfile(rorbuild_root + '/patches/RoR/CMakeDependenciesConfig.txt', build_dir + '/CMakeDependenciesConfig.txt')
            print '    Replacing RoR CMakeMacros.txt with updated version...'
            print '    -----------------------------------------------------------------'
            os.remove(build_dir + '/CMakeMacros.txt')
            shutil.copyfile(rorbuild_root + '/patches/RoR/CMakeMacros.txt', build_dir + '/CMakeMacros.txt')
            print '    Replacing RoR-Configurator CMakeLists.txt with updated version...'
            print '    -----------------------------------------------------------------'
            os.remove(build_dir + '/source/configurator/CMakeLists.txt')
            shutil.copyfile(rorbuild_root + '/patches/RoR/source/configurator/CMakeLists.txt', build_dir + '/source/configurator/CMakeLists.txt')
            os.remove(build_dir + '/CMakeDependenciesConfig.txt')
            shutil.copyfile(rorbuild_root + '/patches/RoR/CMakeDependenciesConfig.txt', build_dir + '/CMakeDependenciesConfig.txt')
            print '    Replacing RoR Main CMakeLists.txt with updated version...'
            print '    -----------------------------------------------------------------'
            os.remove(build_dir + '/source/main/CMakeLists.txt')
            shutil.copyfile(rorbuild_root + '/patches/RoR/source/main/CMakeLists.txt', build_dir + '/source/main/CMakeLists.txt')

            print('    Starting CMake...')
            # Begin RoR build options
            # -----------------------------------------------------------------
            os.chdir(build_dir)
            os.system(cmake_path + '/' + r'cmake -G Xcode \\' +  # generate Xcode project
            '-D CMAKE_INCLUDE_DIRS=' + include_dir + '/OgreStatic \\' +
            '-D rorbuild_root=' + rorbuild_root + ' \\' +
            '-D build_target=' + build_target + ' \\' +
            '-D build_configuration=' + build_configuration + ' \\' +
            '-D SOCKETW_INCLUDE_DIRS=' + include_dir + '/SocketW \\' +
            '-D CMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk \\' +
            '.')  # path to existing build
            # End RoR build options
            # -----------------------------------------------------------------
            print('\nFinished RoR configure stage.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return 0  # windows script needs writing

    def build(self):
        print('\nBuilding RoR')
        print('------------')
        if 'osx_10.9' in globals()['PLATFORMS']:
            rorbuild_root = str(globals()['ROOT'])
            os.chdir(rorbuild_root + '/build/RoR')
            #os.system('cmake ../.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return 0  # windows script needs writing
        else:
            print "Build platform not supported. See \'def build\' in RoRBuilder.py."
            return 1


    def install(self):
        print('\nInstalling RoR')
        print('--------------')
        if 'osx_10.9' in globals()['PLATFORMS']:
            return 0
        elif 'x86' in globals()['PLATFORMS']:
           return 0  # windows script needs writing
        else:
            print "Build platform not supported. See \'def install\' in RoRBuilder.py."
            return 1

