# OgreDynamicBuilder.py
# Adds the pre-built Ogre 1.8.0 SDK.
# Use in place of OgreDynamicBuilder.py.

from pyBuilder import *

class OgreDynamicBuilder(BuildCMakeTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        rorbuild_root = str(globals()['ROOT'])
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Mounting and extracting OgreSDK disk image...')
            os.system('hdiutil attach -mountpoint /Volumes/OgreSDK_1.8.0 %s' % rorbuild_root + '/files/OgreSDK_v1-8-0.dmg')
            ogresdk_build_dir = rorbuild_root + '/build/OgreSDK'
            if os.path.exists(ogresdk_build_dir):
                print('OgreSDK build directory exists. Removing...')
            if not os.path.exists(ogresdk_build_dir):
                shutil.copytree('/Volumes/OgreSDK_1.8.0/OgreSDK', ogresdk_build_dir)
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return 0
        else:
            print "    Build platform not supported. See \'def extract\' in OgreDynamicBuilder.py."
            return 1

    def configure(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    OgreDynamic doesn\'t have a configure stage. Skipping...')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return 0
        else:
            print "Build platform not supported. See \'def configure\' in OgreDynamicBuilder.py."
            return 1

    def build(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    OgreDynamic doesn\'t have a build stage. Skipping...')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return 0
        else:
            print "Build platform not supported. See \'def build\' in OgreDynamicBuilder.py."
            return 1


    def install(self):
        rorbuild_root = str(globals()['ROOT'])
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Installing OgreDynamic...')

            def mkdir_p(self, path):  # thanks to tzot at stackoverflow
                try:
                    os.makedirs(path)
                except OSError as exc: # Python >2.5
                    if exc.errno == errno.EEXIST and os.path.isdir(path):
                        pass
                    else:
                        raise

            source_dir = '/Volumes/OgreSDK'
            target = str(globals()['PLATFORMS']).strip('[]').strip('\'')
            header_source_dir = '/Volumes/OgreSDK_1.8.0/OgreSDK/include'
            header_target_dir = rorbuild_root + '/include/' + target + '/OgreDynamic'
            library_source_dir = '/Volumes/OgreSDK_1.8.0/OgreSDK/lib'
            library_target_dir = globals()['ROOT'] + '/lib/' + target + '/OgreDynamic'
            print 'Header target directory: ' + header_target_dir
            print 'Library target directory: ' + library_target_dir

            if os.path.exists(header_target_dir):
                print('    Found OgreDynamic header target directory: ' + header_target_dir)
                print('    Removing it...')
                shutil.rmtree(header_target_dir)
            if not os.path.exists(header_target_dir):
                print('    Couldn\'t find OgreDynamic header target directory. (This is normal.)')
                print('    Creating:\n        ' + header_target_dir)
                #os.mkdir(header_target_dir)
                #mkdir_p(header_target_dir)
            if os.path.exists(library_target_dir):
                print('    Found OgreDynamic library target directory: ' + library_target_dir)
                print('    Removing it...')
                shutil.rmtree(library_target_dir)
            if not os.path.exists(library_target_dir):
                print('    Couldn\'t find OgreDynamic library target directory. (This is normal.)')
                print('    Creating:\n        ' + library_target_dir)
                #os.mkdir(library_target_dir)
                #mkdir_p(library_target_dir)

            shutil.copytree(header_source_dir, header_target_dir)
            shutil.copytree(library_source_dir, library_target_dir)
            #BuildTarget.create_target_directory(header_target_dir)
            #BuildTarget.create_target_directory(library_target_dir)
            #BuildTarget.install_built_files('*.h', header_source_dir, header_target_dir)


            return 0
        elif 'x86' in globals()['PLATFORMS']:
           return 0
        else:
            print "Build platform not supported. See \'def install\' in OgreDynamicBuilder.py."
            return 1

