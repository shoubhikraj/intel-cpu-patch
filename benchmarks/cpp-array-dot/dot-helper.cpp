// In this case, I am putting the calculation in another file, so that the compiler does not optimize away
// the whole function call.

#include <vector>

double dot_product(std::vector<double>& first, std::vector<double>& second) {
    const auto len_vec = first.size();
    double sum;
    for (size_t i=0; i < len_vec; i++) {
        sum += first[i] * second[i]; // multiply then add => FMA instructions
    }
    return sum;
}

