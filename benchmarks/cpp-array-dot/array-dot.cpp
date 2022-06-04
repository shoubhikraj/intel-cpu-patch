// compile array-dot.cpp and dot-helper.cpp with
// icl -O3 -QaxCORE-AVX2 -arch:pentium -c (Windows)
// icc -O3 -axCORE-AVX2 -march=pentium -c (Linux)
// This will produce two object files, link them again with icl
// icl array-dot.obj dot-helper.obj (windows)
// icc array-dot.o dot-helper.o (Linux)

#include <vector>
#include <random>
#include <chrono>
#include <algorithm>
#include <iostream>

double dot_product(std::vector<double>& first, std::vector<double>& second);

constexpr long long LEN_OF_ARR = 100000000;// the size of array

void calculation() {
    std::vector<double> a;
    std::vector<double> b;
    double sum = 0.0;
    
    a.resize(LEN_OF_ARR,0.0); // fill the array with zeros
    b.resize(LEN_OF_ARR,0.0);

    std::random_device rnd_device;
    std::mt19937_64 random_engine {rnd_device()};
    std::uniform_real_distribution<double> doubleDist {-2.0,2.0};
    auto random_generator = [&doubleDist, &random_engine]() {return doubleDist(random_engine);};
    // fill a with random numbers    
    std::generate(a.begin(),a.end(),random_generator);
    // fill b with random numbers 
    std::generate(b.begin(),b.end(),random_generator);

    auto begin = std::chrono::steady_clock::now();
    
    for (int x=0; x< 100; x++) {
        sum = dot_product(a,b); // this is to trick the compiler so it does not optimize away whole loop
    }

    /*for (size_t i=0; i < LEN_OF_ARR; i++) {
        sum += a[i] * b[i]; // multiply then add => FMA instructions
    } */
    std::cout << "Result of final call of dot product is " << sum << "\n"; 
    auto end = std::chrono::steady_clock::now();
    double time = std::chrono::duration_cast<std::chrono::microseconds>(end-begin).count();
    std::cout<< "Time taken : " << float(time/1000000.0) << " s" << std::endl; 
}


int main() {

  calculation();

}