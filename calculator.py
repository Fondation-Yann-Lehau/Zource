#!/usr/bin/env python3
"""
Exemple de code Python: Calculatrice scientifique simple
Ce script démontre les concepts de base de Python.
"""

import math
from typing import Union


class Calculator:
    """Calculatrice scientifique avec opérations de base et avancées."""
    
    def __init__(self) -> None:
        """Initialise la calculatrice avec un historique vide."""
        self.history: list[str] = []
    
    def add(self, a: float, b: float) -> float:
        """Addition de deux nombres."""
        result = a + b
        self._record(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a: float, b: float) -> float:
        """Soustraction de deux nombres."""
        result = a - b
        self._record(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplication de deux nombres."""
        result = a * b
        self._record(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a: float, b: float) -> Union[float, str]:
        """Division de deux nombres."""
        if b == 0:
            return "Erreur: Division par zéro"
        result = a / b
        self._record(f"{a} ÷ {b} = {result}")
        return result
    
    def power(self, base: float, exponent: float) -> float:
        """Calcul de puissance."""
        result = math.pow(base, exponent)
        self._record(f"{base}^{exponent} = {result}")
        return result
    
    def square_root(self, n: float) -> Union[float, str]:
        """Racine carrée d'un nombre."""
        if n < 0:
            return "Erreur: Racine carrée d'un nombre négatif"
        result = math.sqrt(n)
        self._record(f"√{n} = {result}")
        return result
    
    def factorial(self, n: int) -> Union[int, str]:
        """Factorielle d'un entier positif."""
        if n < 0:
            return "Erreur: Factorielle d'un nombre négatif"
        result = math.factorial(int(n))
        self._record(f"{n}! = {result}")
        return result
    
    def sin(self, angle_degrees: float) -> float:
        """Sinus d'un angle en degrés."""
        result = math.sin(math.radians(angle_degrees))
        self._record(f"sin({angle_degrees}°) = {result:.6f}")
        return result
    
    def cos(self, angle_degrees: float) -> float:
        """Cosinus d'un angle en degrés."""
        result = math.cos(math.radians(angle_degrees))
        self._record(f"cos({angle_degrees}°) = {result:.6f}")
        return result
    
    def _record(self, operation: str) -> None:
        """Enregistre une opération dans l'historique."""
        self.history.append(operation)
    
    def show_history(self) -> None:
        """Affiche l'historique des opérations."""
        if not self.history:
            print("Historique vide")
            return
        print("\n--- Historique des opérations ---")
        for i, operation in enumerate(self.history, 1):
            print(f"{i}. {operation}")
        print("-" * 35)


def main() -> None:
    """Fonction principale démontrant l'utilisation de la calculatrice."""
    calc = Calculator()
    
    print("=" * 40)
    print("  Calculatrice Scientifique Python")
    print("=" * 40)
    
    # Démonstration des opérations de base
    print("\n--- Opérations de base ---")
    print(f"10 + 5 = {calc.add(10, 5)}")
    print(f"20 - 8 = {calc.subtract(20, 8)}")
    print(f"6 × 7 = {calc.multiply(6, 7)}")
    print(f"100 ÷ 4 = {calc.divide(100, 4)}")
    
    # Démonstration des opérations avancées
    print("\n--- Opérations avancées ---")
    print(f"2^10 = {calc.power(2, 10)}")
    print(f"√144 = {calc.square_root(144)}")
    print(f"5! = {calc.factorial(5)}")
    
    # Démonstration des fonctions trigonométriques
    print("\n--- Fonctions trigonométriques ---")
    print(f"sin(30°) = {calc.sin(30):.6f}")
    print(f"cos(60°) = {calc.cos(60):.6f}")
    
    # Affichage de l'historique
    calc.show_history()


if __name__ == "__main__":
    main()
