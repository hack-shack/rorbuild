# WxWidgetsBuilder.py


# Last modified by		:	terpsichorean, 2014-03-31
# RoR target version	:	0.4.0.7
# OS X target version	:	10.9.2
# Win32 target version	:	n/a
# Win64 target version  :	n/a


# Description			:	Builds WxWidgets.
# RoR					:
#	documentation		:	http://www.rigsofrods.com/wiki/pages/WxWidgets
#   documentation2		:	http://www.rigsofrods.com/wiki/pages/Compiling_3rd_party_libraries
# OS X					:
# 	documentation		:	http://wiki.wxwidgets.org/Compiling_wxWidgets_using_the_command-line_(Terminal)
#	dependencies		:	Xcode, Xcode Command Line Tools
#	source file 		:	http://sourceforge.net/projects/wxwindows/files/3.0.0/wxWidgets-3.0.0.tar.bz2/download


from pyBuilder import *
import errno
import os
from subprocess import call

class WxWidgetsBuilder(BuildTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        return self.unzip('files/wxWidgets-*.bz2')

    def configure(self):
        return 0

    def build(self):
        global PLATFORMS, CONFIGURATIONS
        result_code = 0
        for config in ['Release']: #'Debug',
            dstr = ''
            if config == 'Debug': dstr = 'd'

            if not config in CONFIGURATIONS:
                continue

            self.configuration = config

            # -----------------------------------------------------------------
            # Target	:	Windows 32-bit
            # -----------------------------------------------------------------
            if 'x86' in globals()['PLATFORMS']:
                self.platform='Win32'
                self.arch = 'x86'
                self.banner(self.target + ' / ' + self.configuration + ' / ' + self.arch + ' / ' + self.platform, '{gb}')
                result_code |= self.execute(r"""
cd %(path)s\build\wx291_msw_vc10
@call:checkReturnValue

msbuild wx_vc10.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
                result_code |= self.installIncludes('include/wx', True, 'wx')
                result_code |= self.installIncludes('lib/vc_lib/mswu/wx', True, 'wx')
                result_code |= self.installLibs('lib/vc_lib/*.lib')
                result_code |= self.installBinaries('lib/vc_lib/*.pdb', False)

            # -----------------------------------------------------------------
            # Target	:	Windows 64-bit
            # -----------------------------------------------------------------
            if 'x64' in globals()['PLATFORMS']:
                self.platform='x64'
                self.arch = 'x64'
                self.banner(self.target + ' / ' + self.configuration + ' / ' + self.arch + ' / ' + self.platform, '{gb}')
                result_code |= self.execute(r"""
cd %(path)s\build\wx291_msw_vc10
@call:checkReturnValue

msbuild wx_vc10.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
                result_code |= self.installIncludes('include/wx', True, 'wx')
                result_code |= self.installIncludes('lib/vc_lib/mswu/wx', True, 'wx')
                result_code |= self.installLibs('lib/vc_lib/*.lib')
                result_code |= self.installBinaries('lib/vc_lib/*.pdb', False)

            # -----------------------------------------------------------------
            # Target	:	OS X 10.9 64-bit
            # -----------------------------------------------------------------
            if 'osx_10.9' in globals()['PLATFORMS']:
                self.platform = 'osx_10.9'
                self.arch = 'x86_64'
                self.banner('Target: ' + self.target + ' / '+ 'Configuration: ' + self.configuration + ' / ' + 'Architecture: ' + self.arch + ' / ' + 'Platform: ' + self.platform)

                build_directory = globals()['ROOT'] + '/' + 'wxWidgets-release'

                def ensure_path_exists(path):
                    try:
                        os.makedirs(path)
                    except OSError as exception:
                        if exception.errno != errno.EEXIST:
                            raise

                ensure_path_exists(build_directory)

                try:
                    os.chdir(build_directory)
                    result_code |= os.system("../wxWidgets-3.0.0/configure")
                    result_code |= os.system("make")
                finally:
                    pass

                # result_code |= call(str('cd ' + globals()['ROOT'] + '/' + 'wxWidgets-3.0.0'),shell=True)
                #if not os.path.exists(globals()['ROOT'] + '/' + 'wxwidgets-release'):
                #    result_code |= os.makedirs(globals()['ROOT'] + '/' + 'wxwidgets-release')
                #else:
                #    print('wxwidgets directory already exists.')

        return result_code

    def install(self):
        # since angelscript solution clears some targets, we have to install directly after building it
        return 0