# Langages informatiques: Python, HTML, C++ et Quantum

Ce dépôt contient des exemples de code en HTML, Python et C++, ainsi qu'une démonstration d'intégration de ces trois langages.

## 📁 Structure du projet

```
.
├── html/                    # Exemples HTML
│   └── index.html          # Page web interactive
├── python/                  # Exemples Python
│   └── calculator.py       # Calculatrice scientifique
├── cpp/                     # Exemples C++
│   └── math_operations.cpp # Opérations mathématiques
├── integration/             # Intégration des 3 langages
│   ├── app.py              # Serveur Flask (Python)
│   ├── math_lib.cpp        # Bibliothèque de calculs (C++)
│   └── templates/
│       └── index.html      # Interface web (HTML)
└── README.md
```

## 🌐 HTML

Le fichier `html/index.html` démontre:
- Structure HTML5 sémantique
- CSS intégré avec design moderne
- JavaScript interactif
- Formulaires et tableaux

**Pour visualiser:** Ouvrez `html/index.html` dans un navigateur web.

## 🐍 Python

Le fichier `python/calculator.py` démontre:
- Classes et programmation orientée objet
- Typage avec `typing`
- Opérations mathématiques (math library)
- Documentation avec docstrings

**Pour exécuter:**
```bash
python python/calculator.py
```

## ⚡ C++

Le fichier `cpp/math_operations.cpp` démontre:
- Classes et méthodes
- Templates STL (vector, string)
- Gestion d'exceptions
- Algorithmes (tri à bulles)

**Pour compiler et exécuter:**
```bash
g++ -o math_operations cpp/math_operations.cpp
./math_operations
```

## 🔗 Intégration HTML + Python + C++

Le dossier `integration/` contient une application web complète qui démontre comment les trois langages peuvent travailler ensemble:

- **HTML/CSS/JavaScript**: Interface utilisateur moderne et responsive
- **Python (Flask)**: Serveur web et API REST
- **C++**: Bibliothèque de calculs haute performance

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Navigateur Web                                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │  HTML/CSS/JavaScript (Frontend)                      ││
│  │  - Interface utilisateur                             ││
│  │  - Formulaires interactifs                           ││
│  │  - Appels API REST                                   ││
│  └────────────────────────┬────────────────────────────┘│
└───────────────────────────┼─────────────────────────────┘
                            │ HTTP/JSON
┌───────────────────────────▼─────────────────────────────┐
│  Serveur Python (Flask)                                  │
│  ┌─────────────────────────────────────────────────────┐│
│  │  app.py                                              ││
│  │  - Routes HTTP                                       ││
│  │  - Logique métier                                    ││
│  │  - Interface ctypes                                  ││
│  └────────────────────────┬────────────────────────────┘│
└───────────────────────────┼─────────────────────────────┘
                            │ ctypes (FFI)
┌───────────────────────────▼─────────────────────────────┐
│  Bibliothèque C++ (libmath.so)                          │
│  ┌─────────────────────────────────────────────────────┐│
│  │  math_lib.cpp                                        ││
│  │  - Calculs haute performance                         ││
│  │  - Opérations mathématiques                          ││
│  │  - Fonctions sur les nombres                         ││
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### Installation et exécution

1. **Compiler la bibliothèque C++:**
   ```bash
   cd integration
   g++ -shared -fPIC -o libmath.so math_lib.cpp
   ```

2. **Installer les dépendances Python:**
   ```bash
   pip install flask
   ```

3. **Lancer l'application:**
   ```bash
   python integration/app.py
   ```

4. **Ouvrir dans le navigateur:**
   ```
   http://localhost:5000
   ```

> **Note:** Si la bibliothèque C++ n'est pas compilée, l'application utilisera automatiquement une implémentation Python de secours.

## 📝 Fonctionnalités

### Opérations de base
- Addition
- Soustraction
- Multiplication
- Division

### Opérations avancées
- Puissance
- Racine carrée
- PGCD (Plus Grand Commun Diviseur)
- PPCM (Plus Petit Commun Multiple)

### Fonctions sur les nombres
- Factorielle
- Suite de Fibonacci
- Test de primalité

## 🎯 Objectifs pédagogiques

Ce projet vise à illustrer:

1. **Les différences entre les langages:**
   - HTML: langage de balisage pour structurer le contenu
   - Python: langage interprété, facile à lire
   - C++: langage compilé, haute performance

2. **L'interopérabilité:**
   - Comment les langages peuvent communiquer
   - API REST pour la communication web
   - ctypes pour appeler du code C++ depuis Python

3. **Les bonnes pratiques:**
   - Documentation du code
   - Gestion des erreurs
   - Architecture modulaire

## 📜 Licence

Ce projet est à but éducatif.

---

*Fondation Yann LEHAU et ADO - Langages informatiques*
