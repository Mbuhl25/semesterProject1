#include <iostream>
#include <chrono>

int main() {
    const long iterations = 1000000000; // 1 milliard og 100 mio iterationer
    long sum = 0;

    auto start = std::chrono::high_resolution_clock::now();

    for (long i = 0; i < iterations; ++i) {
        sum += i;
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << "Elapsed time: " << elapsed.count() << " seconds\n";
    std::cout << "Sum: " << sum << std::endl;

    return 0;
}
