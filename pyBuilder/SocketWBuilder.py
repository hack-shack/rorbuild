from pyBuilder import *
import errno
import hashlib

class SocketWBuilder(BuildCMakeTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        print '\n    Extracting SocketW'
        print '    ------------------'
        rorbuild_root = str(globals()['ROOT'])
        target = str(globals()['PLATFORMS']).strip('[]')
        if 'osx_10.9' in globals()['PLATFORMS']:
            self.unzip('files/SocketW*.gz')
            os.rename(rorbuild_root + '/build/SocketW031026', rorbuild_root + '/build/SocketW')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.unzip('files/socketw.zip')
        else:
            print "Build platform not supported. See -def extract- in SocketWBuilder.py."
            return 1

    def configure(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print '\n    Configuring SocketW'
            print '    -------------------'
            rorbuild_root = str(globals()['ROOT'])
            def md5sum(filename, blocksize=65536):
                hash = hashlib.md5()
                with open(filename, "r+b") as f:
                    for block in iter(lambda: f.read(blocksize), ""):
                        hash.update(block)
                return hash.hexdigest()
            md5_sw_base = md5sum(rorbuild_root + '/build/SocketW/src/sw_base.cxx')
            print md5_sw_base
            if md5_sw_base == '0eee61a0b51f261734194e33d9b83f24': # SocketW version 031026, patched for OS X
                print '    Looks like sw_base.cxx is already patched for OS X.'
                return 0
            if md5_sw_base == 'f13e583bb828b75c2cc388d044c9593f': # SocketW version 031026, unpatched
                print '    Found unpatched sw_base.cxx. Patching...'
                os.chdir(rorbuild_root + '/build/SocketW/src')
                subprocess.Popen("patch < ../../../patches/SocketW.diff", shell=True)
                return 0
                # TODO: Verify the file was patched.
            else:
                print '    Couldn\'t md5sum sw_base.cxx. Maybe it\'s missing?'
                return 1
        elif 'x86' in globals()['PLATFORMS']:
            self.mkd('socketw/build_'+self.arch)
            return self.execute(r"""
cd %(path)s\socketw\build_%(arch)s
@call:checkReturnValue
cmake -G %(generator)s ..
@call:checkReturnValue
""")
        else:
            print "Build platform not supported. See -def configure- in SocketWBuilder.py."
            return 1

    def build(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            print '\n    Building SocketW'
            print '    ----------------'
            os.chdir(globals()['ROOT'] + '/build/SocketW/src')
            os.system('make')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.execute(r"""
cd %(path)s\socketw\build_%(arch)s
@call:checkReturnValue
msbuild %(target)s.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
        else:
            print "Build platform not supported. See -def build- in SocketWBuilder.py."
            return 1

    def install(self):
        if 'osx_10.9' in globals()['PLATFORMS']:
            rorbuild_root = str(globals()['ROOT'])
            target = 'osx_10.9'
            build_configuration = 'RelWithDebInfo'

            print '\n    Installing SocketW'
            print '    ------------------'
            header_source_dir = rorbuild_root + '/build/SocketW/src'
            header_target_dir = rorbuild_root + '/include/' + target + '/SocketW'
            library_source_dir = rorbuild_root + '/build/SocketW/src'
            library_target_dir = rorbuild_root + '/lib/' + target + '/SocketW/' + build_configuration
            print 'Header target directory: ' + header_target_dir
            print 'Library target directory: ' + library_target_dir
            BuildTarget.create_target_directory(header_target_dir)
            BuildTarget.create_target_directory(library_target_dir)
            BuildTarget.install_built_files('*.h', header_source_dir, header_target_dir)
            BuildTarget.install_built_files('*.a', library_source_dir, library_target_dir)
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            res  = self.installIncludes('socketw/src/*.h')
            res |= self.installLibs('socketw/build_%(arch)s/%(conf)s/*%(target)s*.lib')
            res |= self.installBinaries('socketw/build_%(arch)s/%(conf)s/*%(target)s*.pdb', False) #optional
            return res
        else:
            print "Build platform not supported. See -def install- in SocketWBuilder.py."
            return 1