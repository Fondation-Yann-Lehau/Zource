/**
 * math_lib.cpp - Bibliothèque C++ pour calculs haute performance
 * Compilée en bibliothèque partagée pour être utilisée par Python
 * 
 * Compilation:
 *   Linux/Mac: g++ -shared -fPIC -o libmath.so math_lib.cpp
 *   Windows:   g++ -shared -o math_lib.dll math_lib.cpp
 */

#include <cmath>

extern "C" {
    // Addition
    double add(double a, double b) {
        return a + b;
    }

    // Soustraction
    double subtract(double a, double b) {
        return a - b;
    }

    // Multiplication
    double multiply(double a, double b) {
        return a * b;
    }

    // Division
    double divide(double a, double b) {
        if (b == 0) return std::nan("");  // Return NaN for division by zero
        return a / b;
    }

    // Puissance
    double power_calc(double base, double exponent) {
        return std::pow(base, exponent);
    }

    // Racine carrée
    double sqrt_calc(double n) {
        if (n < 0) return std::nan("");  // Return NaN for negative input
        return std::sqrt(n);
    }

    // Factorielle (itérative pour la performance)
    unsigned long long factorial(int n) {
        if (n < 0) return 0;
        unsigned long long result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        return result;
    }

    // Calcul de Fibonacci (récursif avec mémoïsation serait mieux)
    unsigned long long fibonacci(int n) {
        if (n <= 0) return 0;
        if (n == 1) return 1;
        
        unsigned long long a = 0, b = 1, c;
        for (int i = 2; i <= n; ++i) {
            c = a + b;
            a = b;
            b = c;
        }
        return b;
    }

    // Vérification nombre premier
    int is_prime(int n) {
        if (n <= 1) return 0;
        if (n <= 3) return 1;
        if (n % 2 == 0 || n % 3 == 0) return 0;
        
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return 0;
        }
        return 1;
    }

    // PGCD (Plus Grand Commun Diviseur)
    int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a < 0 ? -a : a;
    }

    // PPCM (Plus Petit Commun Multiple)
    int lcm(int a, int b) {
        if (a == 0 || b == 0) return 0;
        return (a / gcd(a, b)) * b;
    }
}
