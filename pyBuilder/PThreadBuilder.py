from pyBuilder import *

class PThreadBuilder(BuildTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('PThreads library already built into OS X.')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.unzip('files/pthreads*.zip')
        else:
            print "Build platform not supported. See -def extract- in PThreadBuilder.py."
            return 1

    def configure(self):
        return 0

    def build(self):
        global PLATFORMS, CONFIGURATIONS
        res = 0
        self.configuration = 'Release'
        if 'osx_10.9' in globals()['PLATFORMS']:
            print('PThreads library already built into OS X.')
            return 0
        if 'x86' in PLATFORMS:
            self.platform='Win32'
            self.arch = 'x86'
            res |= self.execute(r"""
cd %(path)s\pthreads\
@call:checkReturnValue

msbuild %(target)s.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
            res |= self.installLibs('pthreads/pthreadVC2.lib')
            res |= self.installIncludes('pthreads/pthread.h')
            res |= self.installIncludes('pthreads/semaphore.h')
            res |= self.installIncludes('pthreads/sched.h')
            # ugly hack :-/
            self.configuration = 'Release'
            res |= self.installBinaries('pthreads/pthreadVC2.dll')
            self.configuration = 'RelWithDebInfo'
            res |= self.installBinaries('pthreads/pthreadVC2.dll')
            self.configuration = 'Debug'
            res |= self.installBinaries('pthreads/pthreadVC2.dll')

        if 'x64' in globals()['PLATFORMS']:
            self.platform='x64'
            self.arch = 'x64'
            res |= self.execute(r"""
cd %(path)s\pthreads\
@call:checkReturnValue

msbuild %(target)s.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
            res |= self.installLibs('pthreads/pthreadVC2.lib')
            res |= self.installIncludes('pthreads/pthread.h')
            res |= self.installIncludes('pthreads/semaphore.h')
            res |= self.installIncludes('pthreads/sched.h')
            self.configuration = 'Release'
            res |= self.installBinaries('pthreads/pthreadVC2.dll')
            self.configuration = 'RelWithDebInfo'
            res |= self.installBinaries('pthreads/pthreadVC2.dll')
            self.configuration = 'Debug'
            res |= self.installBinaries('pthreads/pthreadVC2.dll')
        return res

    def install(self):
        # since pthreads solution clears some targets, we have to install directly after building it
        return 0