# pyBuilder.py
# Description			:	This script builds RoR dependencies. Each dependency has its
#                       :   own Python build script.

from distutils.dir_util import copy_tree
import sys
import os
import platform  #	Used for checking arch, etc. (Works on both OS X and Win, while os.uname() is POSIX-only.)
import time
import os.path
import gzip
import tarfile
import zipfile
import subprocess
import shutil
import glob
import datetime


# Detect platform and build tools (work in progress; hardcoded stuff)
if platform.uname()[0] == "Darwin":
    detectedPlatform = 'Darwin'
    if platform.mac_ver()[0] == "10.10":
        print('Detected OS X 10.10 Yosemite.')
    elif platform.mac_ver()[0] == "10.9":
        print('Detected OS X 10.9 Mavericks.')
    else:
        print('Cannot identify running version of OS X.')
    CMAKE_PATH = '/usr/local/bin'
    COMPILER_PATH = '/usr/bin/gcc'
elif platform.uname()[0] == "Windows":
    detectedPlatform = 'Windows'

# Detect CPU architecture.
ARCH = platform.uname()[4]  # This returns the CPU architecture.
# Specifically, return 4th item in os.platform() tuplet: os.platform(machine).
# See os.uname, section 15.1.1, "Process Parameters," at http://docs.python.org/2/library/os.html
print("ARCH           :   " + (platform.uname()[4]) + " (as reported by pyBuilder.py)")


# Set environment variables.
MAXCPU = 6
#CMAKE_PATH 			= 	os.environ['CMAKE_PATH']
#DEV_ENV_BATCH		=	os.environ['ProgramFiles(x86)']+"\\Microsoft Visual Studio 10.0\\VC\\vcvarsall.bat"
DEV_ENV_BATCH = COMPILER_PATH
print "COMPILER_PATH  :   " + COMPILER_PATH + " (as reported by pyBuilder.py)"
DEBUG = False
CONTINUE_ON_ERROR = False
CONFIGURATIONS = []

# Convention for return values: 0 : Success, != 0 : Failure
def run(root, deps, configurations, platforms):
    #	sys.stdout = WTCW(sys.stdout)
    if not check_requirements():
        return

    # store config in global
    globals()['ROOT'] = root
    globals()['DEPS'] = deps
    globals()['CONFIGURATIONS'] = configurations
    globals()['PLATFORMS'] = platforms

    builders = {}
    for b in glob.glob(os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), '*Builder.py')):
        name = os.path.basename(b).split('.')[0]
        builders[name] = __import__(name, globals(), locals(), [], -1)
        # copy globals
        builders[name].__dict__.update(globals())

    buildOrder = """
#  Disable a module from building by commenting it out.
#
#  First, build standalone libraries.
# /----------------------------------
#/
#WxWidgetsBuilder
#MoFileReaderBuilder
#SocketWBuilder
#AngelScriptBuilder
#OISBuilder
#PThreadBuilder
#CurlBuilder
#OpenALBuilder
#
#  Next, build Ogre libraries.
#  Use either (OgreDepsBuilder and OgreBuilder), or (OgreDynamicBuilder), but not both.
#  The former builds from source; the latter uses the pre-built Ogre SDK.
# /--------------------------------------------
#/
#BoostBuilder
#
#OgreDepsBuilder
OgreBuilder
#
#OgreDynamicBuilder
#
#  Build libraries which depend on OGRE.
# /-------------------------------------
#/
#PagedGeometryBuilder
#CaelumBuilder
#MyGUIBuilder
#
#  Build RoR itself.
# /------------------
#/
#RoRBuilder
""".split("\n")

    # build everything
    sw = StopWatch("Elapsed time: ")
    res = 0
    for b in buildOrder:
        b = b.strip()
        if len(b) == 0 or b[0] == '#':
            continue
        banner2(b.replace('Builder', ''), '    ')
        instance = getattr(builders[b], b)
        res = instance().buildAll()
        if res != 0:
            if CONTINUE_ON_ERROR:
                print ("=" * 80) + "\n" + "A builder failed. Continuing the RoR build.\n"
                res = 1
                continue
            else:
                print ("=" * 80) + "\n" + "A builder failed. Stopping the RoR build.\n"
                sw.report()
                return 1
    sw.report()
    return res


from pyBuilder import *
# from WTCW import *		# Not used on OS X


class BuildTarget:
    path = ''
    target = ''
    arch = ARCH  # Or enter manually. Valid values: x86_32, x86_64
    platform = 'osx_10.9'  # Valid: osx_10.9, win
    generator = ''
    configuration = ''

    def initPaths(self):
        path = self.__class__.__name__.replace('Builder', '')
        self.target = path
        self.path = os.path.abspath(ROOT + '/build/' + path)

    def mkd(self, dirs):
        path = os.path.abspath(self.path + '/' + dirs)
        print 'mkdir ' + path
        return os.system('mkdir ' + path)

    def clean(self):
        print('    Cleaning:')
        print('        ' + self.path)
        if os.path.isdir(self.path):
            return self.rm_rf(self.path)
        elif os.path.isdir(self.path) == False:
            print '    No directory to clean.'
            return 0
        else:
            print 'Unhandled exception.'
            return 1

    def unzip(self, source, path=''):
        "Decompress a .bz2 or .zip file."
        if path == '':
            path = self.path
        else:
            path = glob.glob(path)[0]

        compressed_files = glob.glob(os.path.join(ROOT, source))
        if len(compressed_files) == 0:
            print '    No matching compressed files found in: ', source, os.path.join(ROOT, source)
            print '    Try downloading the source code first.'
            print '    Also, pyBuilder is case-sensitive.'
            return 1  # return exit code 0 to indicate success, 1 if failure
        for f in compressed_files:
            # TODO: unify bz2 and gz extraction functions
            if f[-3:] == 'bz2':
                print '    Found .bz2 file: ' + f
                try:
                    if tarfile.is_tarfile(f):
                        print('\n    Extracting:\n'
                            + '            ' + f + '\n'
                            + '        to:\n'
                            + '            ' + ROOT + '/build')
                        tarfile.open(f).extractall(ROOT + '/build')
                        return 0
                    if not tarfile.is_tarfile(f):
                        print "    That file doesn't look like a tarfile."
                        return 1
                except Exception as e:
                    print "Exception while extracting tarfile: ", e
                    return 1
            if f[-3:] == '.gz':
                print '    Found .gz file: ' + f
                try:
                    if tarfile.is_tarfile(f):
                        print('\n    Extracting:\n'
                            + '            ' + f + '\n'
                            + '        to:\n'
                            + '            ' + ROOT + '/build')
                        tarfile.open(f).extractall(ROOT + '/build')
                        return 0
                    if not tarfile.is_tarfile(f):
                        print "That file doesn't look like a tarfile."
                        return 1
                except Exception as e:
                    print "Exception while extracting tarfile: ", e
                    return 1
            # .zip file
            if f[-3:] == 'zip':
                print "    Extracting\n        " + f + "\n        to\n        " + path
                try:
                    zip_buffer = zipfile.ZipFile(f)
                    zip_buffer.extractall(path)
                    return 0
                except Exception as e:
                    print "    Exception while unzipping: ", e
                    return 1
            else:
                print('    Can\'t find a supported file to decompress.')
                return 1

    def rm_rf(self, d):
        if platform.uname()[0] == "Darwin":
            print "    Removing: " + d
            shutil.rmtree(d)
            return 0
        elif platform.uname()[0] == "Windows":
            print "    rd /s /q ", d
            return os.system('rd /s /q ' + d)
            return 0
        else:
            print "Build platform not supported. See -def rm_rf- in pyBuilder.py."
            return 1

    def _installBase(self, src, dst, type, required, dstDir):
        # first: fill possible arguments
        src = self._fillArgs(src)
        dst = self._fillArgs(dst)
        # then normalize the whole paths
        src_path = os.path.abspath(self.path + '/' + src)
        if type == 'includes':
            dst_path = os.path.abspath(DEPS + '/' + type + '/' + self.arch + '/' + dst + '/' + dstDir)
            print('Destination path: ' + dst_path)
        else:
            dst_path = os.path.abspath(
                DEPS + '/' + type + '/' + self.arch + '/' + dst + '/' + self.configuration + '/' + dstDir)
        # create the target directory if it is not existing
        if not os.path.isdir(dst_path):
            os.makedirs(dst_path)
        # invoke the system
        print src_path, ' --> ', dst_path
        # map xcopy result codes to ours, CHANGE: no files found to copy = no error
        #0 Files were copied without error.
        #1 No files were found to copy.
        #2 The user pressed CTRL+C to terminate xcopy.
        #4 Initialization error occurred. There is not enough memory or disk space, or you entered an invalid drive name or invalid syntax on the command line.
        #5 Disk write error occurred.

        no_files_found = False
        glob_files = glob.glob(src_path)
        if len(glob_files) == 0 and not os.path.isfile(src_path) and not os.path.isdir(src_path):
            print('Source files were not found. Tried looking here: ' + src_path)
            no_files_found = True
        if detectedPlatform == 'Darwin':
            # we have to emulate xcopy pretty faithfully, as this build script was originally written for it
            try:
                if os.path.isdir(src_path):
                    shutil.copytree(src_path,dst_path)
                elif not os.path.isdir(src_path):
                    shutil.copy(src_path, dst_path)
            except:
                pass
        elif detectedPlatform == 'Windows':
            xcmd = "xcopy /S /Y %s %s" % (src_path, dst_path)
            res = os.system(xcmd)
            if DEBUG:
                print "XCOPY CMD: ", xcmd
                if res == 0:
                    print "{G}XCOPY RESULT: ", res
                elif res != 0 and not required:
                    print "{RG}XCOPY RESULT: ", res
                else:
                    print "{R}XCOPY RESULT: ", res
            if not required:
                return 0
            if no_files_found:
                return 1
            return res
        else:
            print "Build platform not supported. See -def __installBase- in pyBuilder.py."

    @staticmethod
    def create_target_directory(directory_path):
        # install function for OS X
        if not os.path.exists(directory_path):
            print('    Target directory not found, creating: \n        ' + directory_path)
            os.makedirs(directory_path)
            return 0
        if os.path.exists(directory_path):
            print('    Target directory found: \n        ' + directory_path)
            return 0

    @staticmethod
    def install_built_files(file_extension, source_directory, target_directory):
        # install function for OS X
        files = glob.iglob(os.path.join(source_directory, file_extension))
        for file in files:
            if os.path.isfile(file):
                shutil.copy2(file, target_directory)
        return 0

    def installIncludes(self, src, required=True, dstDir=''):
        return self._installBase(src, self.target, 'includes', required, dstDir)

    def installLibs(self, src, required=True, dstDir=''):
        return self._installBase(src, self.target, 'libs', required, dstDir)

    def installBinaries(self, src, required=True, dstDir=''):
        return self._installBase(src, self.target, 'bin', required, dstDir)

    def banner(self, txt, indent="    "):
        print ""
        print indent + "=" * 80
        print indent + txt

    def getFirstFolder(self):
        for f in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, f)):
                return f
        return ''

    def _fillArgs(self, str):
        return str % self._getArgs()

    def _getArgs(self):
        args = {}
        args['path'] = self.path
        args['rootdir'] = ROOT
        args['depsdir'] = DEPS
        args['depsdir_cmake'] = DEPS.replace('\\', '/')
        args['arch'] = self.arch
        args['arch_bits'] = 32
        if self.arch == 'x86_x64':
            args['arch_bits'] = 64
        args['generator'] = self.generator
        args['platform'] = self.platform
        args['target'] = self.target
        # restricted configurations to Release and Debug
        cr = self.configuration
        if cr == 'RelWithDebInfo' or cr == 'MinSizeRel': cr = 'Release'
        args['configuration_restricted'] = cr
        args['configuration'] = self.configuration
        args['debug_d'] = ''
        if self.configuration == 'Debug':
            args['debug_d'] = '_d'

        args['conf'] = self.configuration
        args['maxcpu'] = MAXCPU
        args['cmakedir'] = CMAKE_PATH
        args['devenv_batch'] = DEV_ENV_BATCH
        args['vswarninglevel'] = 0  # no warnings
        if DEBUG:
            args['vsverbosity'] = 'm'  # q[uiet], m[inimal], n[ormal], d[etailed], dia[gnostic]
        else:
            args['vsverbosity'] = 'q'

        return args

    def execute(self, cmd):
        if detectedPlatform == 'Darwin':
            self.execute_osx(cmd)
        elif detectedPlatform == 'Windows':
            self.execute_windows(cmd)

    # =============================================================================
    # Execute on OS X.
    # =============================================================================

    def execute_osx(self, cmd):
        return 0
        # On Windows, PyBuilder generates an exec.cmd file in each directory to be built.
        # On OS X, we execute shell commands directly in each *Builder.py file.

    # =============================================================================
    # Execute on Windows.
    # =============================================================================

    def execute_windows(self, cmd):
        cmdFile = self.path + '/exec.cmd'

        args = self._getArgs()
        f = open(cmdFile, "w")
        if DEBUG:
            f.write("@echo on\n")
        else:
            f.write("@echo off\n")
        f.write(r"""
:: AUTO-GENERATED, do not modify\n")
:: setup PATH
SET PATH=%%PATH%%;%(rootdir)s;%(cmakedir)s\\bin;

:: Load compilation environment
call "%(devenv_batch)s"
""" % args)

        if DEBUG:
            f.write("@echo on\n")

        f.write(r"""
:: change the directory
cd %(path)s
:: the actual command we want to execute
""" % args)

        # replace magic in commands
        command = self._fillArgs(cmd)

        f.write(command + "\n")
        f.write(r"""
:: DONE
cd %(rootdir)s

GOTO PYTHONBUILDEREND
:::: FUNCTIONS BELOW
:checkReturnValue
@IF "%%ERRORLEVEL%%"=="0" (
    @echo ### everything looks good, continuing ...
    @GOTO:EOF
) ELSE (
    @echo ### error level is set to %%errorlevel%%
    @echo ### something failed, exiting
    @cd %(rootdir)s
    @exit %%ERRORLEVEL%%
)
@GOTO:EOF
:PYTHONBUILDEREND
:: END""" % args)
        f.close()

        proc = subprocess.Popen('cmd /s /c ' + cmdFile,
                                shell=True)
        #stdin=subprocess.PIPE,
        #stdout=subprocess.PIPE,
        #stderr=subprocess.STDOUT,
        #)
        res = proc.wait()
        """
        res = None
        while proc.poll():
            line = proc.stdout.readline()
            print '...'+line.rstrip()
            #print '{r}%s|{x}%s' % (self.target, line)
            res = proc.poll()
            if line == '' and res != None:
                break
        """

        #res = subprocess.call(cmdFile, shell=True)
        if DEBUG:
            if res == 0:
                print "{G}EXECUTE RESULT: ", res
            else:
                print "{R}EXECUTE RESULT: ", res

        #if res != 0:
        #	raise Exception("command execution failed with error code ", res)
        if not DEBUG:
            os.unlink(cmdFile)
        return res

    def configure(self):
        return False

    def extract(self):
        return False

    def build(self):
        return False

    def install(self):
        return False

    def buildAll(self):
        res = 0
        if self.clean() != 0:
            self.banner("CLEAN FAILED", '{ri}')
            print "    " + ("-" * 80) + "\n" + "    " + "Clean failed.\n"
            if CONTINUE_ON_ERROR:
                res = 1
            else:
                return 1

        if self.extract() != 0:
            self.banner("Failed to extract a compressed dependency. Ensure it's in the \"files\" directory.")
            if CONTINUE_ON_ERROR:
                res = 1
            else:
                return 1

        if self.configure() != 0:
            self.banner("CONFIGURE FAILED")
            if CONTINUE_ON_ERROR:
                res = 1
            else:
                return 1

        if self.build() != 0:
            self.banner("BUILD FAILED", '{ri}')
            if CONTINUE_ON_ERROR:
                res = 1
            else:
                return 1

        if self.install() != 0:
            self.banner("INSTALL FAILED", '{ri}')
            if CONTINUE_ON_ERROR:
                res = 1
            else:
                return 1

        return res


class BuildCMakeTarget(BuildTarget):
    def buildAll(self):
        archs = {}

        if 'x86' in PLATFORMS:
            archs['x86'] = ['x86', 'win32', '"Visual Studio 10"']
        if 'x64' in PLATFORMS:
            archs['x64'] = ['x64', 'x64', '"Visual Studio 10 Win64"']
        if 'osx_10.9' in PLATFORMS:
            archs['x64'] = ['x64', 'osx', '"Xcode 5"']

        if self.clean() != 0:
            self.banner("Clean failed: " + self.target)
            return 1

        if self.extract() != 0:
            self.banner("Extraction failed: " + self.target)
            return 1

        res = 0
        stopwatch_arch_all = StopWatch(self.target)

        for arch in archs:
            self.arch = archs[arch][0]
            self.platform = archs[arch][1]
            self.generator = archs[arch][2]

            for configuration in CONFIGURATIONS:
                self.configuration = configuration
                self.banner(
                    self.target + ' / ' + configuration + ' / ' + self.arch + ' / ' + self.platform + ' / ' + self.generator)

                if self.configure() != 0:
                    self.banner("Configure failed.")
                    if CONTINUE_ON_ERROR:
                        res = 1
                        continue
                    else:
                        return 1

                if self.build() != 0:
                    self.banner("Build failed.")
                    if CONTINUE_ON_ERROR:
                        res = 1
                        continue
                    else:
                        return 1

                if self.install() != 0:
                    self.banner("Install failed.")
                    if CONTINUE_ON_ERROR:
                        res = 1
                        continue
                    else:
                        return 1

        stopwatch_arch_all.report()
        return res


class StopWatch():
    def __init__(self, txt):
        self.start = time.clock()
        self.txt = txt

    def report(self):
        self.end = time.clock()
        print '%s %s' % (self.txt, str(datetime.timedelta(seconds=self.end - self.start)))


def check_requirements():
    if sys.version_info[0] != 2:
        print "This script will only work with Python 2."
        return False
    if not os.path.isdir(CMAKE_PATH):
        print "CMake not found in: " + CMAKE_PATH
        print "Please install CMake 2.8 in: " + CMAKE_PATH
        return False
    if not os.path.isfile(DEV_ENV_BATCH):
        print "Visual Studio 2010 not found. Please install it."
        return False
    return True


def banner2(txt, col=''):
    print "    " + txt + ":"
    print "    " + ("-" * (len(txt) + 1))