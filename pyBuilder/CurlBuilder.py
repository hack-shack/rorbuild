from pyBuilder import *

class CurlBuilder(BuildCMakeTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('Extract phase: cURL library already built into OS X.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.unzip('files/curl-*.zip')
        else:
            print "Build platform not supported. See -def extract- in CurlBuilder.py."
            return 1


    def configure(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('Configure phase: cURL library already built into OS X.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            dir = self.getFirstFolder()
            self.mkd(dir+'/build_'+self.arch)
            return self.execute(r"""
cd %(path)s\curl*
@call:checkReturnValue

cd build_%(arch)s
@call:checkReturnValue

cmake -G %(generator)s ..
@call:checkReturnValue
""")
        else:
            print "Build platform not supported. See -def configure- in CurlBuilder.py."
            return 1


    def build(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('Build phase: cURL library already built into OS X.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.execute(r"""
cd %(path)s\curl*
@call:checkReturnValue

cd build_%(arch)s
@call:checkReturnValue

msbuild %(target)s.sln /t:libcurl /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
        else:
            print "Build platform not supported. See -def build- in PThreadBuilder.py."
            return 1


    def install(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('Install phase: cURL library already built into OS X.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            dir = self.getFirstFolder()
            res  = self.installIncludes(dir+'/include/curl/*.h', True, 'curl')
            res |= self.installIncludes(dir+'/build_%(arch)s/lib/curl_config.h')
            res |= self.installBinaries(dir+'/build_%(arch)s/lib/%(conf)s/libcurl.dll')
            res |= self.installBinaries(dir+'/build_%(arch)s/lib/%(conf)s/libcurl.pdb', False)
            res |= self.installLibs(dir+'/build_%(arch)s/lib/libcurl_imp.lib')
            return res
        else:
            print "Build platform not supported. See -def install- in CurlBuilder.py."
            return 1
