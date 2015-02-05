from pyBuilder import *

class OgreDepsBuilder(BuildCMakeTarget):
    def __init__(self):
        self.initPaths()


    def extract(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Extracting OgreDeps (dependencies)...')
            source_files_dir = rorbuild_root + '/files/ogredeps'
            ogredeps_build_dir = rorbuild_root + '/build/ogredeps'

            #if os.path.exists(source_code_dir):
            #    print('    Found an ogredeps source code directory. Removing it...')
            #   shutil.rmtree(source_files_dir)
            #print('    Cloning OgreDeps (dependencies)...')
            #os.chdir(globals()['ROOT'] + '/files')
            #os.system('hg clone https://bitbucket.org/cabalistic/ogredeps')

            if os.path.exists(ogredeps_build_dir):
                print('    Found OgreDeps build directory. Removing it...')
                shutil.rmtree(ogredeps_build_dir)
            if not os.path.exists(ogredeps_build_dir):
                print('    Couldn\'t find OgreDeps build directory. (This is normal.)')
                print('    Copying downloaded OgreDeps to build directory...')
                shutil.copytree(source_files_dir, ogredeps_build_dir)
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            # Windows build script didn't have this
            return 0
        else:
            print "Build platform not supported. See \'def extract\' in OgreDepsBuilder.py."
            return 1

    def configure(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            build_dir = rorbuild_root + '/build/ogredeps/build'
            if os.path.exists(build_dir):
                print('Found OgreDeps /build sub-directory. Removing it...')
                shutil.rmtree(build_dir)
            os.mkdir(rorbuild_root + '/build/ogredeps/build')
            os.chdir(rorbuild_root + '/build/ogredeps/build')
            os.system('cmake -D CMAKE_OSX_SYSROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk -D CMAKE_OSX_ARCHITECTURES=i386 ..')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            # Windows build script didn't have this
            return 0
        else:
            print "Build platform not supported. See \'def configure\' in BoostBuilder.py."
            return 1

    def build(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Building OgreDeps...')
            build_dir = rorbuild_root + '/build/ogredeps/build'
            os.chdir(build_dir)
            os.system('make')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            # Windows build script didn't have this
            return 0
        else:
            print "Build platform not supported. See \'def build\' in BoostBuilder.py."
            return 1

    def install(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            target = 'osx_10.9'
            print('    Installing OgreDeps...')
            deps_list = ['FreeImage', 'freetype', 'ois', 'zlib', 'zziplib']
            ogredeps_source_library_root_dir = rorbuild_root + '/build/ogredeps/build/src'
            ogredeps_target_dir = rorbuild_root + '/include/' + target + '/OgreDeps'

            def mkdir_p(path):
                try:
                    os.makedirs(path)
                except OSError as exc: # Python >2.5
                    if exc.errno == errno.EEXIST and os.path.isdir(path):
                        pass
                    else:
                        raise

            if os.path.exists(ogredeps_target_dir):
                print('    Found existing OgreDeps target directory. Removing it...')
                shutil.rmtree(ogredeps_target_dir)
            print('    Creating OgreDeps target directory...')
            mkdir_p(ogredeps_target_dir)
        # copy static libraries
            print('    Creating OgreDeps library directory...')
            os.mkdir(ogredeps_target_dir + '/lib')
            for item in deps_list:
                print('    Copying ' + item + ' library into OgreDeps target directory...')
                shutil.copy(ogredeps_source_library_root_dir + '/' + item + '/lib' + item + '.a', ogredeps_target_dir + '/lib')
        # copy headers
            print('    Creating OgreDeps header target directory...')
            mkdir_p(os.path.join(ogredeps_target_dir + '/include'))
            print('    Copying header files...')

            def installFiles(filename, source_dir, dest_dir):
                files = glob.iglob(os.path.join(source_dir, filename))
                # TODO: replace awkward exclusion filter with *.h-only filter. We just want *.h files to be copied.
                shutil.copytree(source_dir, dest_dir, ignore=shutil.ignore_patterns('ANNOUNCE', 'AUTHORS', 'CHANGES',
                    'configure', 'ChangeLog', 'COPYING', 'COPYRIGHT', 'FAQ', 'INDEX', 'INSTALL', 'LICENSE', 'LICENSE*',
                    'makefile*', 'Makefile', 'Makefile.*', 'NEWS', 'README', 'README*', 'SConstruct', 'THANKS', 'TODO',
                    '*.3', '*.5', '*.am', '*.asm', '*.c', '*.cpp', '*.hxx', '*.in', '*.log', '*.sed', '*.txt', '*vms'))

            installFiles('*.h', rorbuild_root + '/build/ogredeps/src/FreeImage/Source', ogredeps_target_dir + '/include/FreeImage')
            installFiles('*.h', rorbuild_root + '/build/ogredeps/src/freetype/include', ogredeps_target_dir + '/include/freetype')
            installFiles('*.h', rorbuild_root + '/build/ogredeps/src/ois/includes', ogredeps_target_dir + '/include/ois')
            installFiles('*.h', rorbuild_root + '/build/ogredeps/src/zlib', ogredeps_target_dir + '/include/zlib')
            installFiles('*.h', rorbuild_root + '/build/ogredeps/src/zziplib/zzip', ogredeps_target_dir + '/include/zziplib')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            # Windows build script didn't have this
            return 0
        else:
            print "Build platform not supported. See \'def install\' in BoostBuilder.py."
            return 1