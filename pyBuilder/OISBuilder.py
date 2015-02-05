from pyBuilder import *
import distutils
import hashlib
import sys

class OISBuilder(BuildTarget):
    def __init__(self):
        self.initPaths()

    def extract(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            self.unzip('files/ois*.gz')
            os.rename(rorbuild_root + '/build/ois-v1-3', rorbuild_root + '/build/OIS')
            return 0
        elif 'x86' in globals()['PLATFORMS']:
            return self.unzip('files/ois*.zip')
        else:
            print "Build platform not supported. See -def extract- in OISBuilder.py."
            return 1

    def configure(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in globals()['PLATFORMS']:
            build_target = str(globals()['PLATFORMS']).strip('[]').strip('\'')
            print '    Configuring OIS...'
            print '    ------------------'
            def md5sum(filename, blocksize=65536):
                hash = hashlib.md5()
                with open(filename, "r+b") as f:
                    for block in iter(lambda: f.read(blocksize), ""):
                        hash.update(block)
                return hash.hexdigest()
            md5_file_hash = md5sum(rorbuild_root + '/build/OIS/Mac/XCode-2.2/OIS.xcodeproj/project.pbxproj')
            print md5_file_hash
            if md5_file_hash == 'da1050e4f55abef93a341eefac470031': # OIS 1.3 (Xcode 2.4 project), patched for OS X
                print '    Looks like OIS is already patched for OS X.'
                return 0
            if md5_file_hash == '67cc905a253bd62b811fbe61a13757fd': # OIS 1.3 (Xcode 2.4 project), unpatched
                print '    Found unpatched OIS. Patching...'
                print("    cd " + rorbuild_root + "/build/OIS")
                print("    patch -p0 < " + rorbuild_root + "/patches/" + build_target + "/OIS/cocoa.diff")
                os.chdir(rorbuild_root + '/build/OIS')
                try:
                    return_code = subprocess.Popen("patch -p0 < ../../patches/" + build_target + "/OIS/cocoa.diff", shell=True)
                    cstderr = return_code.communicate()
                    print('    stderr: ' + str(cstderr))
                except:
                    pass
                    print('Exit code: ' + str(return_code))
                print('    Copying newer OIS.xcodeproj directory...')
                try:
                    return_code = distutils.dir_util.copy_tree(rorbuild_root + '/patches/' + build_target + '/OIS/OIS.xcodeproj', rorbuild_root + '/build/OIS/Mac/XCode-2.2/')
                    print return_code
                except:
                    print('Failed to copy OIS .xcodeproject tree.')
                print("    Patch stage complete.")
                return 0
                # TODO: Verify the file was patched.
            else:
                print '    Couldn\'t md5sum sw_base.cxx. Maybe it\'s missing?'
                return 1
        elif 'x86' in globals()['PLATFORMS']:
            return 0
        else:
            print "Build platform not supported. See -def configure- in OISBuilder.py."
            return 1

    def build(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in PLATFORMS:
            print('Building OIS...\n---------------')
            self.platform='osx_10.9'
            # TODO: Exception handler for failed make
            self.banner('Target: ' + self.target + ' / ' + 'Configuration: ' + self.configuration + ' / ' + 'Architecture: ' + self.arch + ' / ' + 'Platform: ' + self.platform)
            print('    Running make...')
            os.chdir(rorbuild_root + '/build/OIS/Mac/XCode-2.2')
            os.system('xcodebuild -target OIS -target OISdylib -target OISstatic')
            return 0
        elif 'x86' in PLATFORMS:
            self.platform='Win32'
            res |= self.execute(r"""
cd %(path)s\ois*
@call:checkReturnValue
cd Win32
@call:checkReturnValue
msbuild ois_vc9.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
            return res
        elif 'x64' in PLATFORMS:
            self.platform='x64'
            res |= self.execute(r"""
cd %(path)s\ois*
@call:checkReturnValue
cd Win32
@call:checkReturnValue
msbuild ois_vc9.sln /t:rebuild /p:Configuration=%(configuration)s /p:Platform=%(platform)s /verbosity:%(vsverbosity)s /nologo /maxcpucount:%(maxcpu)d
@call:checkReturnValue
""")
            return res
        else:
            print('Build platform not supported. See -def build- in OISBuilder.py.')

    def install(self):
        rorbuild_root = globals()['ROOT']
        if 'osx_10.9' in PLATFORMS:
            target = str(globals()['PLATFORMS']).strip('[]').strip('\'')
            build_configuration = 'RelWithDebInfo'  # TODO: add list support for multiple build configs
            print '    Installing OIS...\n    -----------------'
            header_source_dir =     rorbuild_root + '/build/OIS/includes'
            header_target_dir =     rorbuild_root + '/include/' + target + '/OIS'
            mac_header_source_dir = rorbuild_root + '/build/OIS/includes/mac'
            mac_header_target_dir = rorbuild_root + '/include/' + target + '/OIS'
            library_source_dir =    rorbuild_root + '/build/OIS/Mac/XCode-2.2/build/Release'
            library_target_dir =    rorbuild_root + '/lib/' + target + '/OIS/' + build_configuration
            print 'Header target directory: ' + header_target_dir
            print 'Library target directory: ' + library_target_dir
            BuildTarget.create_target_directory(header_target_dir)
            BuildTarget.create_target_directory(library_target_dir)
            BuildTarget.install_built_files('*.h', header_source_dir, header_target_dir)
            BuildTarget.install_built_files('*.h', mac_header_source_dir, mac_header_target_dir)
            BuildTarget.install_built_files('*.a', library_source_dir, library_target_dir)
            return 0
        dir = self.getFirstFolder()
        res = self.installIncludes(dir+'/includes/*')
        if 'x86' in PLATFORMS:
            self.arch = 'x86'
            if 'Release' in CONFIGURATIONS:
                self.configuration = 'Release'
                res |= self.installLibs(dir+'/lib/ois_static.lib')
            if 'Debug' in CONFIGURATIONS:
                self.configuration = 'Debug'
                res |= self.installLibs(dir+'/lib/ois_static_d.lib')
        if 'x64' in PLATFORMS:
            self.arch = 'x64'
            if 'Release' in CONFIGURATIONS:
                self.configuration = 'Release'
                res |= self.installLibs(dir+'/lib64/ois_static.lib')
            if 'Debug' in CONFIGURATIONS:
                self.configuration = 'Debug'
                res |= self.installLibs(dir+'/lib64/ois_static_d.lib')
        return res