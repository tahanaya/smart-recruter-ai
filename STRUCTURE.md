# Structure du Projet - Smart Recruiter AI

## Arborescence Complète

```
smart_recruiter_ai/
│
├── 📄 __init__.py                      # Point d'entrée du module Python
├── 📄 __manifest__.py                  # Manifeste du module Odoo
├── 📄 README.md                        # Documentation principale
├── 📄 DOCUMENTATION_TECHNIQUE.md       # Documentation technique détaillée
├── 📄 INSTALLATION.md                  # Guide d'installation
├── 📄 CHANGELOG.md                     # Historique des modifications
├── 📄 STRUCTURE.md                     # Ce fichier
│
├── 📁 models/                          # Modèles de données (Business Logic)
│   ├── 📄 __init__.py                  # Import des modèles
│   ├── 📄 res_partner_ai.py            # Extension du modèle Contact/Candidat
│   └── 📄 job_profile.py               # Modèle Profils de Postes
│
├── 📁 views/                           # Vues XML (Interface Utilisateur)
│   ├── 📄 partner_view.xml             # Vues enrichies pour les contacts
│   └── 📄 job_profile_views.xml        # Vues pour la configuration
│
├── 📁 security/                        # Sécurité et Permissions
│   └── 📄 ir.model.access.csv          # Droits d'accès aux modèles
│
├── 📁 data/                            # Données de démonstration
│   └── 📄 demo_data.xml                # Profils de postes et candidats exemples
│
└── 📁 static/                          # Ressources statiques (à créer)
    └── 📁 description/
        ├── 🖼️ icon.png                 # Icône du module (128x128)
        ├── 🖼️ banner.png               # Bannière (560x280)
        └── 📁 screenshots/
            ├── 🖼️ screenshot_analysis.png
            ├── 🖼️ screenshot_list.png
            └── 🖼️ screenshot_job_profiles.png
```

---

## Description des Fichiers

### 📁 Racine du Module

#### `__init__.py`
```python
# Point d'entrée du module
# Importe le package 'models'
from . import models
```

**Rôle :** Fichier d'initialisation Python obligatoire pour que le répertoire soit reconnu comme un package.

---

#### `__manifest__.py`
```python
{
    'name': 'Smart Recruiter AI',
    'version': '2.0.0',
    'category': 'Human Resources',
    # ... configuration du module
}
```

**Rôle :**
- Déclare le module à Odoo
- Définit les métadonnées (nom, version, auteur)
- Liste les dépendances
- Référence les fichiers de données (XML, CSV)

**Importance :** ⭐⭐⭐⭐⭐ (Obligatoire)

---

### 📁 models/

#### `models/__init__.py`
```python
from . import res_partner_ai
from . import job_profile
```

**Rôle :** Importe tous les modèles du package.

---

#### `models/res_partner_ai.py` (270 lignes)

**Classe principale :** `ResPartnerAi`

**Responsabilités :**
- Extension du modèle `res.partner` (Contacts)
- Définition des nouveaux champs calculés
- Algorithme de scoring IA
- Détection du niveau d'expérience
- Méthode d'analyse manuelle

**Champs ajoutés :**
| Champ | Type | Description |
|-------|------|-------------|
| `ai_score` | Integer | Score 0-100% |
| `ai_verdict` | Selection | Badge (low/medium/high) |
| `ai_experience_level` | Selection | Junior/Intermédiaire/Senior/Expert |
| `ai_detected_skills` | Text | Compétences trouvées |
| `ai_missing_skills` | Text | Compétences manquantes |
| `ai_analysis_date` | Datetime | Date de l'analyse |

**Méthodes principales :**

1. **`_get_skills_database()`**
   - Retourne le dictionnaire des 50+ compétences avec pondération
   - Type : Helper method
   - Complexité : O(1)

2. **`_detect_experience_level(text_content)`**
   - Analyse le texte pour détecter le niveau d'expérience
   - Type : Analyseur
   - Utilise : Regex + Keyword matching
   - Complexité : O(n) où n = longueur du texte

3. **`_compute_ai_score()`** ⭐
   - Cœur de l'algorithme de scoring
   - Type : Computed method (décorée avec `@api.depends('comment')`)
   - Déclenchement : Automatique sur modification de `comment`
   - Complexité : O(n × m) où n = nb candidats, m = nb compétences

4. **`action_analyze_profile()`**
   - Action déclenchée par le bouton "Analyser le Profil"
   - Type : Action Odoo
   - Retour : Notification utilisateur

**Importance :** ⭐⭐⭐⭐⭐ (Fichier central du module)

---

#### `models/job_profile.py` (78 lignes)

**Classes :**

1. **`JobProfile` (Modèle : `smart.recruiter.job.profile`)**
   - Définit les profils de postes personnalisés
   - Champs : name, description, priority, min_score_threshold, color
   - Relation : One2many avec `JobProfileSkill`

2. **`JobProfileSkill` (Modèle : `smart.recruiter.skill`)**
   - Définit les compétences requises par profil
   - Champs : name, weight, skill_type, is_critical
   - Relation : Many2one avec `JobProfile`

**Utilité :** Configuration avancée pour adapter le scoring par type de poste.

**Importance :** ⭐⭐⭐⭐ (Fonctionnalité avancée)

---

### 📁 views/

#### `views/partner_view.xml` (152 lignes)

**Records définis :**

1. **`view_partner_form_ai_inherit`**
   - Type : Vue Formulaire (inherit)
   - Hérite de : `base.view_partner_form`
   - Ajoute :
     - Bouton "Analyser le Profil" dans le header
     - Onglet "Analyse IA Smart Recruiter" dans le notebook
   - Contenu :
     - Section "Résultat de l'Analyse" (score, verdict, niveau)
     - Section "Mode d'emploi"
     - Section "Compétences Détectées"
     - Section "Compétences Manquantes"
     - Section "Interprétation du Score"

2. **`view_partner_tree_ai_inherit`**
   - Type : Vue Liste (inherit)
   - Hérite de : `base.view_partner_tree`
   - Ajoute :
     - Colonnes Score IA, Verdict, Niveau d'expérience
     - Colorisation des lignes (decoration-success/warning/danger)

3. **`view_partner_search_ai_inherit`**
   - Type : Vue Recherche (inherit)
   - Hérite de : `base.view_res_partner_filter`
   - Ajoute :
     - Filtres "Top Profils", "Profils Intéressants", "Profils Faibles"
     - Filtres par niveau (Junior/Senior/Expert)
     - Groupages par Verdict et Niveau

**Importance :** ⭐⭐⭐⭐⭐ (Interface principale)

---

#### `views/job_profile_views.xml` (150 lignes)

**Records définis :**

1. **`view_job_profile_form`** - Vue Formulaire
2. **`view_job_profile_tree`** - Vue Liste
3. **`view_job_profile_kanban`** - Vue Kanban
4. **`view_job_profile_search`** - Vue Recherche
5. **`action_job_profile`** - Action pour ouvrir les profils
6. **Menus :**
   - `menu_smart_recruiter_root` (Menu principal)
   - `menu_smart_recruiter_config` (Configuration)
   - `menu_job_profile` (Profils de Poste)

**Importance :** ⭐⭐⭐⭐ (Configuration)

---

### 📁 security/

#### `security/ir.model.access.csv`

**Format :**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_smart_recruiter_job_profile_user,smart.recruiter.job.profile.user,model_smart_recruiter_job_profile,base.group_user,1,1,1,1
```

**Droits définis :**
- Tous les utilisateurs internes (`base.group_user`) ont accès complet (CRUD) aux profils de postes et compétences

**Importance :** ⭐⭐⭐⭐⭐ (Obligatoire pour tout nouveau modèle)

---

### 📁 data/

#### `data/demo_data.xml` (238 lignes)

**Contenu :**

1. **3 Profils de Postes :**
   - Développeur Python Senior
   - Développeur Full-Stack
   - Ingénieur DevOps

2. **Compétences associées :**
   - 15+ compétences configurées avec pondération

3. **4 Candidats de test :**
   - Jean Dupont (Profil Faible - ~15%)
   - Marie Martin (Profil Moyen - ~45%)
   - Ahmed Ben Ali (Top Profil - ~85%)
   - Sophie Leclerc (Expert - ~95%)

**Utilité :** Facilite les tests et la démonstration du module

**Importance :** ⭐⭐⭐ (Optionnel mais recommandé)

---

### 📁 Documentation

#### `README.md` (600+ lignes)

**Sections :**
- Contexte du projet
- Fonctionnalités
- Installation
- Utilisation
- Algorithme de scoring
- Configuration
- Screenshots
- Tests et validation
- Support

**Public cible :** Utilisateurs finaux et décideurs

**Importance :** ⭐⭐⭐⭐⭐

---

#### `DOCUMENTATION_TECHNIQUE.md` (800+ lignes)

**Sections :**
- Architecture du système
- Algorithme détaillé
- Structure BDD
- API et méthodes
- Guide développeur
- Tests et débogage
- Optimisations
- Évolutions

**Public cible :** Développeurs et mainteneurs

**Importance :** ⭐⭐⭐⭐⭐

---

#### `INSTALLATION.md` (500+ lignes)

**Sections :**
- Prérequis
- Installation Linux/Windows/Docker
- Vérification
- Erreurs courantes
- Configuration post-installation
- Désinstallation

**Public cible :** Administrateurs système

**Importance :** ⭐⭐⭐⭐⭐

---

#### `CHANGELOG.md`

**Format :** Keep a Changelog

**Contenu :**
- Historique des versions
- Notes de migration
- Roadmap

**Importance :** ⭐⭐⭐⭐

---

## Flux de Données

### Diagramme de Séquence - Analyse d'un Candidat

```
┌─────────┐        ┌──────────┐         ┌────────────┐        ┌──────────┐
│  User   │        │   View   │         │   Model    │        │   BDD    │
└────┬────┘        └─────┬────┘         └──────┬─────┘        └─────┬────┘
     │                   │                     │                    │
     │ 1. Modifie Notes  │                     │                    │
     ├──────────────────>│                     │                    │
     │                   │                     │                    │
     │                   │ 2. onchange trigger │                    │
     │                   ├────────────────────>│                    │
     │                   │                     │                    │
     │                   │                     │ 3. _compute_ai_score()
     │                   │                     ├────────┐           │
     │                   │                     │        │           │
     │                   │                     │ 4. Analyse texte   │
     │                   │                     │ 5. Calcul score    │
     │                   │                     │ 6. Détecte niveau  │
     │                   │                     │<───────┘           │
     │                   │                     │                    │
     │                   │                     │ 7. UPDATE res_partner
     │                   │                     ├───────────────────>│
     │                   │                     │                    │
     │                   │                     │ 8. OK              │
     │                   │                     │<───────────────────┤
     │                   │                     │                    │
     │                   │ 9. Rafraîchit vue  │                    │
     │                   │<────────────────────┤                    │
     │                   │                     │                    │
     │ 10. Affichage     │                     │                    │
     │<──────────────────┤                     │                    │
     │                   │                     │                    │
```

---

## Dépendances entre Fichiers

### Graphe de Dépendances

```
__manifest__.py
    ├── depends: ['base', 'contacts']
    ├── data: [
    │   ├── security/ir.model.access.csv
    │   ├── views/partner_view.xml
    │   └── views/job_profile_views.xml
    │   ]
    └── demo: [
        └── data/demo_data.xml
        ]

__init__.py
    └── from . import models

models/__init__.py
    ├── from . import res_partner_ai
    └── from . import job_profile

res_partner_ai.py
    └── _inherit: 'res.partner'  (module 'base')

job_profile.py
    └── _name: 'smart.recruiter.job.profile'  (nouveau modèle)

views/partner_view.xml
    └── inherit_id: 'base.view_partner_form'

views/job_profile_views.xml
    ├── model: 'smart.recruiter.job.profile'
    └── model: 'smart.recruiter.skill'
```

---

## Points d'Extension

### 1. Ajouter une Compétence

**Fichier :** `models/res_partner_ai.py`

**Ligne :** ~65-133 (méthode `_get_skills_database()`)

```python
'nouvelle_competence': 15,  # Ajouter ici
```

### 2. Modifier l'Algorithme de Scoring

**Fichier :** `models/res_partner_ai.py`

**Ligne :** ~212-216 (normalisation du score)

### 3. Ajouter un Champ dans l'Interface

**Fichier :** `views/partner_view.xml`

**Ligne :** ~26-37 (section "Résultat de l'Analyse")

```xml
<field name="nouveau_champ"/>
```

### 4. Créer un Nouveau Rapport

**Nouveau fichier :** `report/candidate_report.xml`

### 5. Ajouter une Action Planifiée

**Nouveau fichier :** `data/ir_cron.xml`

---

## Métriques du Code

| Métrique | Valeur |
|----------|--------|
| Lignes de code Python | ~500 |
| Lignes de code XML | ~400 |
| Nombre de modèles | 3 (res.partner étendu + 2 nouveaux) |
| Nombre de vues | 7 |
| Nombre de champs ajoutés | 6 |
| Nombre de méthodes | 4 principales |
| Compétences détectées | 50+ |
| Taille estimée du module | ~2 MB |

---

## Checklist de Développement

### Avant de Modifier le Code

- [ ] Lire la DOCUMENTATION_TECHNIQUE.md
- [ ] Activer le mode développeur dans Odoo
- [ ] Créer une branche Git
- [ ] Sauvegarder la base de données

### Après Modification

- [ ] Tester manuellement
- [ ] Vérifier les logs Odoo
- [ ] Mettre à jour le CHANGELOG.md
- [ ] Mettre à jour la documentation si nécessaire
- [ ] Commiter avec message clair

### Avant de Déployer

- [ ] Tester sur base de données de test
- [ ] Vérifier la migration
- [ ] Informer les utilisateurs
- [ ] Planifier un rollback si nécessaire

---

## Glossaire des Termes Odoo

| Terme | Définition |
|-------|------------|
| **Model** | Classe Python représentant une table BDD |
| **View** | Fichier XML définissant l'interface |
| **Record** | Enregistrement XML créant des données |
| **Inherit** | Héritage de modèle ou vue existante |
| **Compute** | Champ calculé automatiquement |
| **Store** | Mise en cache en BDD |
| **ORM** | Object-Relational Mapping |
| **Action** | Méthode déclenchée par bouton |
| **Domain** | Filtre de recherche |
| **Context** | Contexte d'exécution |

---

## Ressources

### Liens Utiles

- [Documentation Odoo](https://www.odoo.com/documentation)
- [Odoo GitHub](https://github.com/odoo/odoo)
- [Forum Odoo](https://www.odoo.com/forum)

### Fichiers de Référence

- Architecture : DOCUMENTATION_TECHNIQUE.md
- Installation : INSTALLATION.md
- Utilisation : README.md
- Historique : CHANGELOG.md

---

**Module développé par Taha Naya**
Version 2.0 - Janvier 2026
