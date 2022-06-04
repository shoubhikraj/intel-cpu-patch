Compile array-dot.cpp and dot-helper.cpp with

`icl -O3 -QaxCORE-AVX2 -arch:pentium -c` (Windows) <br>
`icc -O3 -axCORE-AVX2 -march=pentium -c` (Linux)

This will produce two object files, link them again with Intel C++ compiler

`icl array-dot.obj dot-helper.obj` (windows) <br>
`icc array-dot.o dot-helper.o` (Linux)
