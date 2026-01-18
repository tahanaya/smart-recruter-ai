# Smart Recruiter AI - Module Odoo de Recrutement Intelligent

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Odoo](https://img.shields.io/badge/Odoo-14%20|%2015%20|%2016-green.svg)
![License](https://img.shields.io/badge/license-LGPL--3-orange.svg)

## 📋 Table des Matières

1. [Contexte du Projet](#contexte)
2. [Fonctionnalités](#fonctionnalités)
3. [Architecture Technique](#architecture)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [Algorithme de Scoring](#algorithme)
7. [Configuration](#configuration)
8. [Captures d'écran](#captures)
9. [Auteur](#auteur)

---

## 🎯 Contexte

Dans le module de Recrutement standard d'Odoo, les responsables RH doivent lire manuellement chaque fiche candidat pour évaluer sa pertinence. Avec l'augmentation du volume de candidatures, ce processus devient chronophage et sujet à l'erreur humaine.

**Smart Recruiter AI** automatise ce processus en fournissant une analyse instantanée et objective de chaque profil candidat.

---

## ✨ Fonctionnalités

### 🔍 Analyse Automatique des Profils

- **Scoring sur 100** : Calcul automatique d'un score de pertinence
- **Détection d'expérience** : Classification automatique (Junior/Intermédiaire/Senior/Expert)
- **Badges visuels** : Identification rapide des profils (🔴 Faible / 🟠 Intéressant / 🟢 Top)

### 📊 Analyse Détaillée

- Liste des compétences détectées avec pondération
- Identification des compétences critiques manquantes
- Horodatage de chaque analyse
- Bouton d'analyse manuelle pour recalcul instantané

### 🎨 Interface Enrichie

- Onglet dédié "Analyse IA Smart Recruiter"
- Visualisation en temps réel du score (widget percentpie)
- Filtres intelligents dans la vue liste
- Colorisation automatique des candidats selon leur score
- Groupage par verdict ou niveau d'expérience

### ⚙️ Configuration Avancée

- Création de profils de postes personnalisés
- Définition de compétences avec pondération
- Marquage de compétences critiques
- Seuils de score personnalisables

---

## 🏗️ Architecture Technique

### Stack Technique

- **Backend** : Python 3.7+
- **Framework** : Odoo 14/15/16
- **Base de données** : PostgreSQL
- **Frontend** : XML (Odoo Views)

### Structure du Module

```
smart_recruiter_ai/
│
├── __init__.py
├── __manifest__.py
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── res_partner_ai.py      # Extension du modèle res.partner
│   └── job_profile.py          # Modèle de profils de postes
│
├── views/
│   ├── partner_view.xml        # Vues enrichies pour les contacts
│   └── job_profile_views.xml   # Vues pour la configuration
│
├── security/
│   └── ir.model.access.csv     # Droits d'accès
│
└── static/
    └── description/
        ├── icon.png
        └── banner.png
```

### Modèles de Données

#### 1. Extension `res.partner` (Contacts/Candidats)

**Nouveaux champs ajoutés :**

| Champ | Type | Description |
|-------|------|-------------|
| `ai_score` | Integer | Score de pertinence (0-100%) |
| `ai_verdict` | Selection | Badge verdict (low/medium/high) |
| `ai_experience_level` | Selection | Niveau d'expérience détecté |
| `ai_detected_skills` | Text | Liste des compétences trouvées |
| `ai_missing_skills` | Text | Compétences critiques manquantes |
| `ai_analysis_date` | Datetime | Date de la dernière analyse |

#### 2. Nouveau modèle `smart.recruiter.job.profile`

Permet de créer des profils de postes personnalisés avec :
- Nom du profil
- Description
- Liste de compétences requises
- Seuil de score minimum
- Priorité

#### 3. Nouveau modèle `smart.recruiter.skill`

Définition des compétences pour chaque profil :
- Nom de la compétence
- Pondération (0-20 points)
- Type (technique/soft skill/langue/certification)
- Marqueur de compétence critique

---

## 📥 Installation

### Prérequis

- Odoo 14, 15 ou 16 installé
- PostgreSQL configuré
- Python 3.7+

### Étapes d'installation

1. **Télécharger le module**

```bash
cd /path/to/odoo/addons/
git clone https://github.com/tahanaya/smart_recruiter_ai.git
```

2. **Redémarrer le serveur Odoo**

```bash
sudo systemctl restart odoo
# ou
./odoo-bin -c /path/to/odoo.conf
```

3. **Activer le mode développeur**

Dans Odoo : `Paramètres > Activer le mode développeur`

4. **Mettre à jour la liste des applications**

`Applications > Mettre à jour la liste des applications`

5. **Installer le module**

Rechercher "Smart Recruiter AI" et cliquer sur "Installer"

---

## 🚀 Utilisation

### Analyse d'un Candidat

1. **Créer ou ouvrir un contact** (Menu : Contacts)

2. **Ajouter des informations dans "Notes Internes"**

   Exemple :
   ```
   Développeur Python avec 5 ans d'expérience.
   Compétences : Python, Django, PostgreSQL, Docker, Git
   Expérience avec Odoo ERP et méthodologies Agile/Scrum
   Maîtrise de l'anglais et du français
   Certifié AWS Solutions Architect
   ```

3. **Cliquer sur le bouton "🔍 Analyser le Profil"**

4. **Consulter l'onglet "📊 Analyse IA Smart Recruiter"**

   Vous verrez :
   - Le score calculé (ex: 85%)
   - Le verdict (🟢 Top Profil)
   - Le niveau d'expérience (Senior - 5-10 ans)
   - Les compétences détectées avec points
   - Les compétences manquantes

### Filtrage des Candidats

Dans la vue liste des contacts, utilisez les filtres :

- **🟢 Top Profils (70%+)** : Candidats à recruter en priorité
- **🟠 Profils Intéressants (30-69%)** : Candidats avec potentiel
- **🔴 Profils Faibles (<30%)** : Candidats non qualifiés

Vous pouvez également grouper par :
- Verdict IA
- Niveau d'expérience

---

## 🧠 Algorithme de Scoring

### Principe de Fonctionnement

L'algorithme utilise une approche de **Keyword Matching avec Pondération Intelligente**.

### Base de Connaissances

Le système dispose d'une base de 50+ compétences classées par catégories :

#### Compétences Critiques (20 points)
- Python, Odoo, Java, JavaScript, React, Angular, Vue.js, Node.js

#### Bases de Données (15 points)
- PostgreSQL, SQL, MySQL, MongoDB, Oracle

#### DevOps (12 points)
- Docker, Kubernetes, Jenkins, CI/CD

#### Méthodologies (10 points)
- Agile, Scrum, Kanban, DevOps

#### Langues (6-8 points)
- Anglais, Français, Espagnol, Allemand

#### Certifications (15 points bonus)
- Certifications professionnelles détectées

### Calcul du Score

```python
# Pseudo-code de l'algorithme

score = 0
for each skill in skills_database:
    if skill found in candidate_text:
        score += skill_weight

# Normalisation sur 100
base_score = min(70, (score / total_critical_skills) * 70)
bonus_score = min(30, number_of_skills * 2)
final_score = base_score + bonus_score
```

### Détection du Niveau d'Expérience

L'algorithme utilise des expressions régulières pour détecter :

1. **Mentions explicites** : "5 ans", "10 années", "3+ years"
2. **Mots-clés** : "junior", "senior", "expert", "lead", "manager"

Classification :
- **Junior** : 0-2 ans
- **Intermédiaire** : 2-5 ans
- **Senior** : 5-10 ans
- **Expert** : 10+ ans

---

## ⚙️ Configuration

### Créer un Profil de Poste Personnalisé

1. Aller dans : `Smart Recruiter AI > Configuration > Profils de Poste`

2. Cliquer sur "Créer"

3. Remplir les informations :
   - Nom : "Développeur Full-Stack Senior"
   - Priorité : Haute
   - Score minimum requis : 70%

4. Ajouter les compétences requises :

| Compétence | Type | Pondération | Critique |
|------------|------|-------------|----------|
| Python | Technique | 20 | ✓ |
| React | Technique | 18 | ✓ |
| PostgreSQL | Technique | 15 | ✓ |
| Docker | Technique | 12 | ✓ |
| Agile | Soft Skill | 10 | |
| Anglais | Langue | 8 | ✓ |

5. Enregistrer

---

## 📸 Captures d'écran

### Vue Formulaire - Onglet Analyse IA

![Analyse IA](docs/screenshots/screenshot_analysis.png)

**Éléments visibles :**
- Score en camembert (percentpie widget)
- Badge verdict coloré
- Niveau d'expérience détecté
- Date d'analyse
- Liste des compétences détectées avec points
- Compétences manquantes
- Guide d'interprétation des scores

### Vue Liste - Filtres Intelligents

![Vue Liste](docs/screenshots/screenshot_list.png)

**Fonctionnalités :**
- Colorisation automatique selon le score
- Colonnes Score IA et Verdict
- Filtres rapides (Top Profils, Intéressants, Faibles)
- Groupage par verdict ou expérience

### Configuration - Profils de Postes

![Profils de Postes](docs/screenshots/screenshot_job_profiles.png)

**Interface Kanban :**
- Création de profils personnalisés
- Gestion des compétences requises
- Pondération configurable
- Vue Kanban avec couleurs

---

## 🧪 Tests et Validation

### Cas de Test 1 : Profil vide

**Entrée :** Contact sans "Notes Internes"

**Résultat attendu :**
- Score : 0%
- Verdict : 🔴 Profil Faible
- Message : "Aucune note interne renseignée"

### Cas de Test 2 : Profil Junior

**Entrée :**
```
Jeune développeur avec 1 an d'expérience.
Compétences : Python, Git, HTML, CSS
```

**Résultat attendu :**
- Score : 25-35%
- Verdict : 🟠 Profil Intéressant
- Niveau : Junior (0-2 ans)
- Compétences détectées : Python (+20), Git (+10), HTML (+6), CSS (+6)

### Cas de Test 3 : Profil Senior Idéal

**Entrée :**
```
Développeur Full-Stack Senior avec 8 ans d'expérience.
Expertise : Python, Django, Odoo, PostgreSQL, Docker, Kubernetes
Méthodologies : Agile, Scrum, DevOps
Certifié AWS Solutions Architect
Bilingue anglais/français
```

**Résultat attendu :**
- Score : 85-95%
- Verdict : 🟢 Top Profil
- Niveau : Senior (5-10 ans)
- Compétences détectées : 10+ compétences

---

## 📊 Diagrammes Techniques

### Diagramme de Flux - Processus d'Analyse

```
┌─────────────────────┐
│ Utilisateur ouvre   │
│ fiche candidat      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Modification du     │
│ champ "Notes"       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Trigger automatique │
│ _compute_ai_score() │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Extraction du texte │
│ Normalisation       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Parcours de la base │
│ de compétences      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Détection mots-clés │
│ + Pondération       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Calcul score final  │
│ Normalisation /100  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Détection niveau    │
│ expérience (regex)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Assignation verdict │
│ (low/medium/high)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Mise à jour de      │
│ l'interface         │
└─────────────────────┘
```

---

## 🔒 Sécurité et Permissions

Le module respecte le système de droits d'accès Odoo :

- **Utilisateurs internes** : Lecture + Écriture + Création + Suppression
- **Portail** : Accès restreint (lecture seule de leur propre profil)

Fichier : `security/ir.model.access.csv`

---

## 🚧 Limitations Connues

1. **Langue** : Optimisé pour le français et l'anglais
2. **Synonymes** : Ne détecte pas les synonymes (ex: "JS" vs "JavaScript")
3. **Contexte** : Analyse basée uniquement sur mots-clés (pas de compréhension sémantique profonde)
4. **Données** : Nécessite que les CVs soient copiés dans "Notes Internes"

---

## 🔮 Évolutions Futures

- [ ] Intégration d'un vrai modèle NLP (spaCy, BERT)
- [ ] Import automatique de fichiers PDF/DOCX
- [ ] API REST pour analyse externe
- [ ] Dashboard statistiques RH
- [ ] Notifications automatiques pour nouveaux top profils
- [ ] Matching automatique candidat-poste
- [ ] Support multi-langues étendu
- [ ] Détection de soft skills avancée
- [ ] Intégration avec LinkedIn API

---

## 👨‍💻 Auteur

**Taha Naya**

- 📧 Email : taha.naya@example.com
- 🌐 GitHub : [github.com/tahanaya](https://github.com/tahanaya)
- 💼 LinkedIn : [linkedin.com/in/tahanaya](https://linkedin.com/in/tahanaya)

**Projet Académique** - Développé dans le cadre d'un projet de fin d'études

---

## 📄 Licence

Ce module est distribué sous licence **LGPL-3**.

Vous êtes libre de :
- Utiliser ce module à des fins commerciales ou personnelles
- Modifier le code source
- Distribuer des versions modifiées

À condition de :
- Conserver la licence LGPL-3
- Créditer l'auteur original
- Partager les modifications sous la même licence

---

## 🙏 Remerciements

- L'équipe Odoo pour le framework excellent
- La communauté open-source Python
- Les contributeurs du projet

---

## 📚 Ressources Complémentaires

- [Documentation Odoo](https://www.odoo.com/documentation)
- [Odoo Development Cookbook](https://www.packtpub.com/product/odoo-development-cookbook)
- [Python Documentation](https://docs.python.org/3/)

---

## 📞 Support

Pour toute question ou problème :

1. Ouvrir une issue sur GitHub
2. Consulter la documentation
3. Contacter l'auteur par email

**Bon recrutement avec Smart Recruiter AI ! 🚀**
