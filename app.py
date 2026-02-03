#!/usr/bin/env python3
"""
app.py - Application Flask intégrant HTML (frontend), Python (backend) et C++ (calculs)

Ce fichier démontre l'intégration des trois langages:
- HTML: Interface utilisateur (templates)
- Python: Serveur web et logique applicative (Flask)
- C++: Bibliothèque de calculs haute performance (via ctypes)

Pour exécuter:
1. Compiler la bibliothèque C++:
   g++ -shared -fPIC -o libmath.so math_lib.cpp
2. Lancer l'application:
   python app.py
3. Ouvrir http://localhost:5000 dans un navigateur
"""

import ctypes
import os
import platform
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Charger la bibliothèque C++
def load_cpp_library():
    """Charge la bibliothèque C++ selon le système d'exploitation."""
    lib_dir = os.path.dirname(os.path.abspath(__file__))
    
    if platform.system() == "Windows":
        lib_path = os.path.join(lib_dir, "math_lib.dll")
    else:
        lib_path = os.path.join(lib_dir, "libmath.so")
    
    if not os.path.exists(lib_path):
        print(f"Bibliothèque C++ non trouvée: {lib_path}")
        print("Utilisation de l'implémentation Python de secours")
        return None
    
    try:
        lib = ctypes.CDLL(lib_path)
        
        # Définir les types de retour
        lib.add.restype = ctypes.c_double
        lib.subtract.restype = ctypes.c_double
        lib.multiply.restype = ctypes.c_double
        lib.divide.restype = ctypes.c_double
        lib.power_calc.restype = ctypes.c_double
        lib.sqrt_calc.restype = ctypes.c_double
        lib.factorial.restype = ctypes.c_ulonglong
        lib.fibonacci.restype = ctypes.c_ulonglong
        lib.is_prime.restype = ctypes.c_int
        lib.gcd.restype = ctypes.c_int
        lib.lcm.restype = ctypes.c_int
        
        print(f"Bibliothèque C++ chargée: {lib_path}")
        return lib
    except OSError as e:
        print(f"Erreur lors du chargement de la bibliothèque: {e}")
        return None

# Implémentation Python de secours
class PythonFallback:
    """Implémentation Python des fonctions si la bibliothèque C++ n'est pas disponible."""
    
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def subtract(a, b):
        return a - b
    
    @staticmethod
    def multiply(a, b):
        return a * b
    
    @staticmethod
    def divide(a, b):
        return a / b if b != 0 else 0
    
    @staticmethod
    def power_calc(base, exp):
        return base ** exp
    
    @staticmethod
    def sqrt_calc(n):
        return n ** 0.5 if n >= 0 else -1
    
    @staticmethod
    def factorial(n):
        if n < 0:
            return 0
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    @staticmethod
    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @staticmethod
    def is_prime(n):
        if n <= 1:
            return 0
        if n <= 3:
            return 1
        if n % 2 == 0 or n % 3 == 0:
            return 0
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return 0
            i += 6
        return 1
    
    @staticmethod
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)
    
    @staticmethod
    def lcm(a, b):
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // PythonFallback.gcd(a, b)

# Charger la bibliothèque au démarrage
cpp_lib = load_cpp_library()
fallback = PythonFallback()

def calculate(operation, *args):
    """Effectue un calcul en utilisant C++ si disponible, sinon Python."""
    if cpp_lib:
        func = getattr(cpp_lib, operation)
        return func(*args)
    else:
        func = getattr(fallback, operation)
        return func(*args)


@app.route('/')
def index():
    """Page d'accueil avec l'interface de calculatrice."""
    using_cpp = cpp_lib is not None
    return render_template('index.html', using_cpp=using_cpp)


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API pour effectuer des calculs."""
    data = request.get_json()
    operation = data.get('operation')
    
    try:
        if operation == 'add':
            result = calculate('add', 
                             ctypes.c_double(data['a']) if cpp_lib else data['a'],
                             ctypes.c_double(data['b']) if cpp_lib else data['b'])
        elif operation == 'subtract':
            result = calculate('subtract',
                             ctypes.c_double(data['a']) if cpp_lib else data['a'],
                             ctypes.c_double(data['b']) if cpp_lib else data['b'])
        elif operation == 'multiply':
            result = calculate('multiply',
                             ctypes.c_double(data['a']) if cpp_lib else data['a'],
                             ctypes.c_double(data['b']) if cpp_lib else data['b'])
        elif operation == 'divide':
            if data['b'] == 0:
                return jsonify({'error': 'Division par zéro'}), 400
            result = calculate('divide',
                             ctypes.c_double(data['a']) if cpp_lib else data['a'],
                             ctypes.c_double(data['b']) if cpp_lib else data['b'])
        elif operation == 'power':
            result = calculate('power_calc',
                             ctypes.c_double(data['base']) if cpp_lib else data['base'],
                             ctypes.c_double(data['exp']) if cpp_lib else data['exp'])
        elif operation == 'sqrt':
            if data['n'] < 0:
                return jsonify({'error': 'Racine carrée d\'un nombre négatif'}), 400
            result = calculate('sqrt_calc',
                             ctypes.c_double(data['n']) if cpp_lib else data['n'])
        elif operation == 'factorial':
            if data['n'] < 0:
                return jsonify({'error': 'Factorielle d\'un nombre négatif'}), 400
            result = calculate('factorial',
                             ctypes.c_int(int(data['n'])) if cpp_lib else int(data['n']))
        elif operation == 'fibonacci':
            result = calculate('fibonacci',
                             ctypes.c_int(int(data['n'])) if cpp_lib else int(data['n']))
        elif operation == 'is_prime':
            result = calculate('is_prime',
                             ctypes.c_int(int(data['n'])) if cpp_lib else int(data['n']))
            result = 'Oui' if result else 'Non'
        elif operation == 'gcd':
            result = calculate('gcd',
                             ctypes.c_int(int(data['a'])) if cpp_lib else int(data['a']),
                             ctypes.c_int(int(data['b'])) if cpp_lib else int(data['b']))
        elif operation == 'lcm':
            result = calculate('lcm',
                             ctypes.c_int(int(data['a'])) if cpp_lib else int(data['a']),
                             ctypes.c_int(int(data['b'])) if cpp_lib else int(data['b']))
        else:
            return jsonify({'error': 'Opération inconnue'}), 400
        
        return jsonify({
            'result': result,
            'using_cpp': cpp_lib is not None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  Application d'intégration HTML + Python + C++")
    print("=" * 50)
    print(f"\nBackend: {'C++' if cpp_lib else 'Python (fallback)'}")
    print("\nDémarrage du serveur sur http://localhost:5000")
    print("Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50 + "\n")
    
    # Note: debug=False for production security. Set to True only for development.
    app.run(debug=False, host='0.0.0.0', port=5000)
