# AngelScriptBuilder.py
# Last modified by			:	terpsichorean, 2014-04-12
# Previous contributors		:	pricorde, tdev
# AngelScript version		:
#	osx_10.9				: 2.28.2, 2014-03-18
#							: http://www.angelcode.com/angelscript/sdk/files/angelscript_2.28.2.zip
#	win32					: 2.22.1 (RoR 0.4.0.7-win32)

from pyBuilder import *

class AngelScriptBuilder(BuildTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        return self.unzip('files/angelscript*.zip')

    def configure(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print '    Configuring AngelScript...'
            print '    --------------------------'
            os.makedirs(globals()['ROOT'] + '/build/AngelScript/sdk/angelscript/build')
            os.chdir(globals()['ROOT'] + '/build/AngelScript/sdk/angelscript/build')
            os.system('cmake ../projects/cmake/.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return 0
        else:
            print 'Build platform not supported. See \'def configure\' in AngelScriptBuilder.py.'
            return 1

    def build(self):
        res = 0

        if 'osx_10.9' in globals()['PLATFORMS']:
            print '    Building AngelScript...'
            print '    --------------------------'
            os.chdir(globals()['ROOT'] + '/build/AngelScript/sdk/angelscript/build')
            os.system('make')
            return 0

        if 'x86' in globals()['PLATFORMS']:
            self.platform='Win32'
            self.arch = 'x86'
            res |= self.execute(r"""
cd %(path)s\sdk\angelscript\projects\msvc10
@call:checkReturnValue

msbuild %(target)s.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
            res |= self.installLibs('sdk/angelscript/lib/angelscript'+dstr+'.lib')
            res |= self.installIncludes('sdk/angelscript/include/*')
            return res

        if 'x64' in globals()['PLATFORMS']:
            self.platform='x64'
            self.arch = 'x64'
            res |= self.execute(r"""
cd %(path)s\sdk\angelscript\projects\msvc10
@call:checkReturnValue

msbuild %(target)s.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
            res |= self.installLibs('sdk/angelscript/lib/angelscript64'+dstr+'.lib')
            res |= self.installIncludes('sdk/angelscript/include/*')
            return res

    def install(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            target = 'osx_10.9'
            build_configuration = 'RelWithDebInfo'
            print '    Installing AngelScript...'
            print '    -------------------------'
            header_source_dir = globals()['ROOT'] + '/build/AngelScript/sdk/angelscript/include'
            header_target_dir = globals()['ROOT'] + '/include/' + target + '/AngelScript'
            library_source_dir = globals()['ROOT'] + '/build/AngelScript/sdk/angelscript/lib'
            library_target_dir = globals()['ROOT'] + '/lib/' + target + '/AngelScript/' + build_configuration
            BuildTarget.create_target_directory(header_target_dir)
            BuildTarget.create_target_directory(library_target_dir)
            BuildTarget.install_built_files('*.h', header_source_dir, header_target_dir)
            BuildTarget.install_built_files('*.a', library_source_dir, library_target_dir)
            return 0
        if 'x86' in PLATFORMS:
            # since angelscript solution clears some targets, we have to install directly after building it
            return 0