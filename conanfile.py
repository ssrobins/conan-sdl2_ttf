from conans import ConanFile, CMake, tools
import os, shutil
from cmake_utils import cmake_init, cmake_build_debug_release

class Conan(ConanFile):
    name = "sdl2_ttf"
    version = os.getenv("package_version")
    description = "A sample library which allows you to use TrueType fonts in your SDL applications"
    homepage = "https://www.libsdl.org/projects/SDL_ttf/"
    license = "Zlib"
    url = "https://gitlab.com/ssrobins/conan-" + name 
    settings = "os", "compiler", "arch"
    generators = "cmake"
    exports = "cmake_utils.py"
    exports_sources = ["CMakeLists.txt", "CMakeLists-%s.txt" % name]
    zip_folder_name = "SDL2_ttf-%s" % version
    zip_name = "%s.tar.gz" % zip_folder_name
    build_subfolder = "build"
    source_subfolder = "source"
    
    def requirements(self):
        self.requires.add("freetype/2.9.1@stever/testing")
        self.requires.add("sdl2/2.0.8@stever/testing")

    def source(self):
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/global_settings.cmake", "global_settings.cmake")
        tools.download("https://gitlab.com/ssrobins/cmake-utils/raw/master/ios.toolchain.cmake", "ios.toolchain.cmake")
        tools.download("https://www.libsdl.org/projects/SDL_ttf/release/%s" % self.zip_name, self.zip_name)
        tools.unzip(self.zip_name)
        os.unlink(self.zip_name)
        os.rename(self.zip_folder_name, self.source_subfolder)
        shutil.move("CMakeLists-%s.txt" % self.name, os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = cmake_init(self.settings, CMake(self), self.build_folder)
        cmake_build_debug_release(cmake, self.build_subfolder)

    def package(self):
        self.copy("SDL_ttf.h", dst="include", src=self.source_subfolder)
        self.copy("*.lib", dst="lib", src=self.build_subfolder, keep_path=False)
        self.copy("*.a", dst="lib", src=self.build_subfolder, keep_path=False)
        if self.settings.compiler == "Visual Studio":
            self.copy(pattern="*.pdb", dst="lib", src="build/source/SDL2_ttf.dir/Release", keep_path=False)

    def package_info(self):
        self.cpp_info.debug.libs = ["SDL2_ttfd"]
        self.cpp_info.release.libs = ["SDL2_ttf"]