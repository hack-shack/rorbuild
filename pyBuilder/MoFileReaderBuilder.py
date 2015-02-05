# MoFileReaderBuilder.py


# Last modified by		:	terpsichorean, 2014-03-31
# RoR target version	:	0.4.0.7
# OS X target version	:	10.9.2
# Win32 target version	:	n/a
# Win64 target version  :	n/a


# Description			:	Builds MoFileReader.
# RoR					:
#	documentation		:	none on RoR site.
#   documentation req.	:	http://www.rigsofrods.com/wiki/pages/Compiling_3rd_party_libraries
# OS X					:
# 	documentation		:	http://wiki.wxwidgets.org/Compiling_wxWidgets_using_the_command-line_(Terminal)
#	dependencies		:	Xcode, Xcode Command Line Tools

from pyBuilder import *

class MoFileReaderBuilder(BuildCMakeTarget):
    def __init__(self):
        self.initPaths()


    def extract(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('Root directory: ' + rorbuild_root + '/build/mofilereader')
        # Git clone from code.google.com
            if not os.path.isdir(rorbuild_root + '/build'):
                print('    Could not find build directory. Creating...')
                os.mkdir(rorbuild_root + '/build')
            if os.path.isdir(rorbuild_root + '/build/mofilereader'):
                print("    Source directory found. Looks like it's been cloned already.")
                return 0
            elif not os.path.isdir(rorbuild_root + '/build/mofilereader'):
                print("    Source directory not found. '")
                print("    Running 'git clone'...")
                os.chdir(rorbuild_root + '/build')
                os.system('git clone https://code.google.com/p/mofilereader')
                return 0
        elif 'x86' in globals()['PLATFORMS']:
        # Unzip the v26-dependencies-win source code
            result_code = 1
            result_code |= self.unzip('files/moFileReader.0.1.2.zip')
            result_code |= self.unzip('files/moFileReader-headerfix.0.1.2.zip', self.path+'/include/')
            return result_code
        else:
            print "Build platform not supported. See -def extract- in MoFileReaderBuilder.py."
            return 1


    def configure(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
        # check for GitHub clone; run CMake
            if os.path.isdir(rorbuild_root + '/build/mofilereader'):
                print('Found source directory: ' + rorbuild_root + '/build/mofilereader')
                print('Starting CMake...')
                os.chdir(rorbuild_root + '/build/mofilereader/build')
                os.system('cmake .')
                return 0
            elif not os.path.isdir(rorbuild_root + '/build/mofilereader'):
                print 'No source directory found. Cloning...'
                os.chdir(rorbuild_root + '/build')
                self.extract()
                return 0
        elif 'x86' in globals()['PLATFORMS']:
        # Windows
            self.mkd('build/build_'+self.arch)
            return self.execute(r"""
cd %(path)s\build\build_%(arch)s
@call:checkReturnValue
cmake -G %(generator)s ..
@call:checkReturnValue
""")


    def build(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            # TODO: Exception handler for failed make
            self.banner('Target: ' + self.target + ' / '+ 'Configuration: ' + self.configuration + ' / ' + 'Architecture: ' + self.arch + ' / ' + 'Platform: ' + self.platform)
            print('    Running make...')
            os.chdir(rorbuild_root + '/build/mofilereader/build')
            os.system('make')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            self.platform = 'Win32'
            self.arch = 'x86'
            self.banner('Target: ' + self.target + ' / '+ 'Configuration: ' + self.configuration + ' / ' + 'Architecture: ' + self.arch + ' / ' + 'Platform: ' + self.platform)
            return self.execute(r"""
cd %(path)s\build\build_%(arch)s
@call:checkReturnValue
msbuild %(target)s.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")

    def install(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            target = 'osx_10.9'
            build_configuration = 'RelWithDebInfo'  # TODO: add list support for multiple build configs
            
            print '    Installing MoFileReader...'
            print '    --------------------------'
            header_source_dir = rorbuild_root + '/build/mofilereader/include/'
            header_target_dir = rorbuild_root + '/include/' + target + '/MoFileReader/'
            library_source_dir = rorbuild_root + '/build/mofilereader/lib/'
            library_target_dir = rorbuild_root + '/lib/' + target + '/MoFileReader/' + build_configuration
            BuildTarget.create_target_directory(header_target_dir)
            BuildTarget.create_target_directory(library_target_dir)
            BuildTarget.install_built_files('*.h', header_source_dir, header_target_dir)
            BuildTarget.install_built_files('*.a', library_source_dir, library_target_dir)
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            self.installIncludes('include/')
            self.installLibs('build/lib/%(conf)s/%(target)s*.lib')
            self.installBinaries('build/lib/%(conf)s/%(target)s*.pdb', False) #optional
            return 0
