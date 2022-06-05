# intel-cpu-patch
Provides a python script that can patch executables and libraries compiled with Intel compiler (or Intel MKL), for better performance on AMD processors.

**Before running the script, make backup copies of your binaries!** This is because the patching is irreversible and it might break softwares. Use it at your own risk. **Never patch any executable used by OS or any OS library (\*.dll).**

Run the script with Python:
```python
python find_intel_replace.py myfile.exe
```
This will only *check* for Intel CPUID dispatcher.

To do the modification:
```python
python find_intel_replace.py myfile.exe --force
```

### Background

Intel C/C++ and Fortran compilers have an option `/Qax` (Windows) or `-ax` (Linux) which introduces multiple dispatch versions of computationally heavy functions where SIMD (e.g. AVX, AVX2, FMA, AVX-512) can be used. Unfortunately, the dispatcher only works correctly for Intel processors. If you have a different processor e.g. AMD, the dispatcher will always use the slowest codepath, even if AVX or AVX2 is available.

The dispatcher first checks the CPU vendor string by using the instruction `cpuid`. If the vendor string is `GenuineIntel`, only then it checks whether the CPU has modern SIMD instruction sets like AVX2 are available. If the CPU vendor is not Intel, it selects the default codepath, which is SSE2 on Windows and x86 on Linux.

The python script opens the binary file and then looks for locations where a string is checked against `GenuineIntel` and then it replaces that with `AuthenticAMD`. This makes the software use the best available codepath on AMD processors.

My idea came from https://github.com/jimenezrick/patch-AuthenticAMD. However, I did not use any of their code and instead wrote everything from scratch with Python. This also makes the program cross platform as it can be used on both Linux and Windows, unline patch-AuthenticAMD which is written in C and works on Linux/Unix systems only. Please also note that my python script does not use as many checks as that code.


