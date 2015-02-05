from pyBuilder import *

class OpenALBuilder(BuildCMakeTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            rorbuild_root = globals()['ROOT']
            if not os.path.isdir(rorbuild_root + '/build'):
                os.mkdir(rorbuild_root + '/build')
            return_value = self.unzip('files/openal-soft-*.bz2')
            if os.path.isdir(rorbuild_root + '/build/OpenAL'):
                shutil.rmtree(rorbuild_root + '/build/OpenAL')
            os.rename(rorbuild_root + '/build/openal-soft-1.15.1', rorbuild_root + '/build/OpenAL')
            return return_value

        elif 'x86' in globals()['PLATFORMS']:
            return self.unzip('files/openal-soft-*.zip')
        else:
            print "Build platform not supported. See \'def extract\' in OpenALBuilder.py."
            return 1

    def configure(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Configuring OpenAL...')
            os.chdir(globals()['ROOT'] + '/build/OpenAL/build')
            os.system('cmake ..')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            dir = self.getFirstFolder()
            self.mkd(dir+'/build_'+self.arch)
            return self.execute(r"""
cd %(path)s\openal*
@call:checkReturnValue

cd build_%(arch)s
@call:checkReturnValue

cmake -G %(generator)s ..
@call:checkReturnValue
""")
        else:
            print "Build platform not supported. See \'def configure\' in OpenALBuilder.py."
            return 1

    def build(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('    Building OpenAL...')
            os.chdir(globals()['ROOT'] + '/build/OpenAL/build')
            os.system('make')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.execute(r"""
cd %(path)s\openal*
@call:checkReturnValue

cd build_%(arch)s
@call:checkReturnValue

msbuild OpenAL.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
        else:
            print "Build platform not supported. See \'def build\' in OpenALBuilder.py."
            return 1

    def install(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            target = 'osx_10.9'
            build_configuration = 'RelWithDebInfo'  # TODO: add list support for multiple build configs
            print '    Installing OpenAL...'
            header_source_dir = globals()['ROOT'] + '/build/OpenAL/include/AL'
            header_target_dir = os.path.abspath(ROOT + '/include/' + target + '/OpenAL/')
            library_source_dir = str(globals()['ROOT'] + '/build/OpenAL/build')
            library_target_dir = globals()['ROOT'] + '/lib/' + target + '/OpenAL/' + build_configuration
            print 'Header target directory: ' + header_target_dir
            print 'Library target directory: ' + library_target_dir
            BuildTarget.create_target_directory(header_target_dir)
            BuildTarget.create_target_directory(library_target_dir)
            BuildTarget.install_built_files('*.h', header_source_dir, header_target_dir)
            BuildTarget.install_built_files('libopenal.dylib', library_source_dir, library_target_dir)
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            dir = self.getFirstFolder()
            result_value  = self.installIncludes(dir + '/include/*')
            result_value |= self.installLibs(dir + '/build_%(arch)s/%(conf)s/OpenAL32.lib')
            result_value |= self.installBinaries(dir + '/build_%(arch)s/%(conf)s/OpenAL32.pdb', False)
            result_value |= self.installBinaries(dir + '/build_%(arch)s/%(conf)s/OpenAL32.dll')
            result_value |= self.installBinaries(dir + '/build_%(arch)s/%(conf)s/openal-info.exe')
            return result_value
        else:
            print "Build platform not supported. See -def install- in OpenALBuilder.py."
            return 1
