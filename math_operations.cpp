/**
 * Exemple de code C++: Bibliothèque de calculs mathématiques
 * Ce programme démontre les concepts de base de C++.
 */

#include <iostream>
#include <cmath>
#include <vector>
#include <string>
#include <stdexcept>

/**
 * Classe MathOperations - Opérations mathématiques de base et avancées
 */
class MathOperations {
private:
    std::vector<std::string> history;

    void record(const std::string& operation) {
        history.push_back(operation);
    }

public:
    MathOperations() = default;

    // Addition
    double add(double a, double b) {
        double result = a + b;
        record(std::to_string(a) + " + " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    // Soustraction
    double subtract(double a, double b) {
        double result = a - b;
        record(std::to_string(a) + " - " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    // Multiplication
    double multiply(double a, double b) {
        double result = a * b;
        record(std::to_string(a) + " * " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    // Division
    double divide(double a, double b) {
        if (b == 0) {
            throw std::invalid_argument("Erreur: Division par zero");
        }
        double result = a / b;
        record(std::to_string(a) + " / " + std::to_string(b) + " = " + std::to_string(result));
        return result;
    }

    // Puissance
    double power(double base, double exponent) {
        double result = std::pow(base, exponent);
        record(std::to_string(base) + "^" + std::to_string(exponent) + " = " + std::to_string(result));
        return result;
    }

    // Racine carrée
    double squareRoot(double n) {
        if (n < 0) {
            throw std::invalid_argument("Erreur: Racine carree d'un nombre negatif");
        }
        double result = std::sqrt(n);
        record("sqrt(" + std::to_string(n) + ") = " + std::to_string(result));
        return result;
    }

    // Factorielle
    unsigned long long factorial(int n) {
        if (n < 0) {
            throw std::invalid_argument("Erreur: Factorielle d'un nombre negatif");
        }
        unsigned long long result = 1;
        for (int i = 2; i <= n; ++i) {
            result *= i;
        }
        record(std::to_string(n) + "! = " + std::to_string(result));
        return result;
    }

    // Afficher l'historique
    void showHistory() const {
        if (history.empty()) {
            std::cout << "Historique vide" << std::endl;
            return;
        }
        std::cout << "\n--- Historique des operations ---" << std::endl;
        int count = 1;
        for (const auto& op : history) {
            std::cout << count++ << ". " << op << std::endl;
        }
        std::cout << "---------------------------------" << std::endl;
    }
};

/**
 * Fonction de démonstration du tri à bulles
 */
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

/**
 * Afficher un vecteur
 */
void printVector(const std::vector<int>& arr, const std::string& label) {
    std::cout << label << ": [";
    for (size_t i = 0; i < arr.size(); ++i) {
        std::cout << arr[i];
        if (i < arr.size() - 1) std::cout << ", ";
    }
    std::cout << "]" << std::endl;
}

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "  Bibliotheque Mathematique C++" << std::endl;
    std::cout << "========================================" << std::endl;

    MathOperations calc;

    // Opérations de base
    std::cout << "\n--- Operations de base ---" << std::endl;
    std::cout << "10 + 5 = " << calc.add(10, 5) << std::endl;
    std::cout << "20 - 8 = " << calc.subtract(20, 8) << std::endl;
    std::cout << "6 * 7 = " << calc.multiply(6, 7) << std::endl;
    std::cout << "100 / 4 = " << calc.divide(100, 4) << std::endl;

    // Opérations avancées
    std::cout << "\n--- Operations avancees ---" << std::endl;
    std::cout << "2^10 = " << calc.power(2, 10) << std::endl;
    std::cout << "sqrt(144) = " << calc.squareRoot(144) << std::endl;
    std::cout << "5! = " << calc.factorial(5) << std::endl;

    // Démonstration du tri
    std::cout << "\n--- Tri a bulles ---" << std::endl;
    std::vector<int> numbers = {64, 34, 25, 12, 22, 11, 90};
    printVector(numbers, "Avant tri");
    bubbleSort(numbers);
    printVector(numbers, "Apres tri");

    // Afficher l'historique
    calc.showHistory();

    return 0;
}
