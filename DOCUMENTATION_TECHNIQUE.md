# Documentation Technique - Smart Recruiter AI

## Table des Matières

1. [Architecture du Système](#architecture-du-système)
2. [Algorithme de Scoring Détaillé](#algorithme-de-scoring-détaillé)
3. [Structure de la Base de Données](#structure-de-la-base-de-données)
4. [API et Méthodes](#api-et-méthodes)
5. [Guide du Développeur](#guide-du-développeur)
6. [Tests et Débogage](#tests-et-débogage)
7. [Optimisations et Performance](#optimisations-et-performance)
8. [Évolutions Possibles](#évolutions-possibles)

---

## 1. Architecture du Système

### 1.1 Pattern MVC (Model-View-Controller)

Le module suit l'architecture MVC d'Odoo :

```
┌─────────────────────────────────────────────────────┐
│                     VUE (XML)                       │
│  - partner_view.xml: Interface utilisateur         │
│  - job_profile_views.xml: Configuration            │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│                 CONTRÔLEUR (Python)                 │
│  - action_analyze_profile(): Bouton d'analyse      │
│  - _compute_ai_score(): Calcul automatique         │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│                   MODÈLE (ORM)                      │
│  - ResPartnerAi: Extension res.partner             │
│  - JobProfile: Profils de postes                   │
│  - JobProfileSkill: Compétences                    │
└─────────────────────────────────────────────────────┘
```

### 1.2 Héritage de Modèle Odoo

Le module utilise l'héritage de modèle (`_inherit`) pour étendre `res.partner` sans modifier le code core d'Odoo.

```python
class ResPartnerAi(models.Model):
    _inherit = 'res.partner'  # Extension du modèle existant

    # Nouveaux champs ajoutés au modèle res.partner
    ai_score = fields.Integer(...)
    ai_verdict = fields.Selection(...)
```

**Avantages:**
- Pas de modification du code Odoo core
- Compatible avec d'autres modules
- Facilite les mises à jour Odoo

### 1.3 Déclencheurs Automatiques

Le calcul du score utilise le décorateur `@api.depends()` d'Odoo :

```python
@api.depends('comment')  # Recalcule quand 'comment' change
def _compute_ai_score(self):
    # Logique de calcul
```

**Flux d'exécution:**
1. L'utilisateur modifie le champ "Notes Internes" (`comment`)
2. Odoo détecte le changement via `@api.depends('comment')`
3. La méthode `_compute_ai_score()` est appelée automatiquement
4. Les champs calculés sont mis à jour (score, verdict, etc.)
5. L'interface se rafraîchit automatiquement

---

## 2. Algorithme de Scoring Détaillé

### 2.1 Base de Connaissances (Knowledge Base)

La méthode `_get_skills_database()` retourne un dictionnaire de compétences pondérées :

```python
{
    'python': 20,        # Compétence critique
    'odoo': 20,
    'docker': 12,        # Compétence importante
    'anglais': 8,        # Compétence standard
    'html': 6            # Compétence basique
}
```

**Hiérarchie de pondération:**

| Niveau | Points | Exemples |
|--------|--------|----------|
| Critique | 20 | Python, Odoo, Java, JavaScript |
| Très Important | 15-18 | PostgreSQL, React, Angular |
| Important | 12 | Docker, Kubernetes, Jenkins |
| Standard | 8-10 | Git, Agile, Scrum, Langues |
| Basique | 5-6 | HTML, CSS, Soft Skills |

### 2.2 Processus de Détection

#### Étape 1 : Normalisation du Texte

```python
text_content = record.comment.lower()
```

**Pourquoi :**
- Évite les problèmes de casse ("Python" vs "python")
- Simplifie la comparaison de chaînes

#### Étape 2 : Parcours de la Base de Compétences

```python
for skill, weight in skills_db.items():
    if skill in text_content:
        score += weight
        detected_skills_list.append(f"{skill.title()} (+{weight} pts)")
    elif skill in critical_skills:
        missing_skills_list.append(skill.title())
```

**Logique:**
- Si la compétence est trouvée → ajout au score
- Si la compétence est critique ET manquante → ajout à la liste des manquantes

#### Étape 3 : Normalisation du Score

```python
if total_possible_score > 0:
    base_score = min(70, (score / total_possible_score) * 70)
    bonus_score = min(30, len(detected_skills_list) * 2)
    score = int(base_score + bonus_score)
```

**Formule mathématique:**

```
Score_final = min(100, Score_base + Score_bonus)

où:
  Score_base = min(70, (Score_brut / Score_max_critique) × 70)
  Score_bonus = min(30, Nombre_compétences × 2)
```

**Exemple de calcul:**

Candidat avec : Python (20), Odoo (20), SQL (15), Docker (12)

```
Score_brut = 20 + 20 + 15 + 12 = 67
Score_max_critique = 20 + 20 + 20 + 15 + 12 + 10 = 97 (6 compétences critiques)
Score_base = min(70, (67/97) × 70) = min(70, 48.35) = 48.35
Score_bonus = min(30, 4 × 2) = min(30, 8) = 8
Score_final = 48.35 + 8 = 56%
```

### 2.3 Détection du Niveau d'Expérience

#### Méthode 1 : Expressions Régulières

```python
years_patterns = [
    r'(\d+)\s*(?:\+)?\s*an(?:s|née(?:s)?)',  # Français
    r'(\d+)\s*(?:\+)?\s*year(?:s)?',          # Anglais
]
```

**Cas gérés:**
- "5 ans"
- "10 années"
- "3+ ans"
- "7 years"
- "2+ years"

#### Méthode 2 : Détection par Mots-Clés

Si aucune mention d'années n'est trouvée :

```python
if 'junior' in text_content or 'débutant' in text_content:
    return 'junior'
elif 'senior' in text_content or 'expert' in text_content:
    return 'senior'
```

#### Classification

```python
if max_years < 2:
    return 'junior'
elif max_years < 5:
    return 'intermediate'
elif max_years < 10:
    return 'senior'
else:
    return 'expert'
```

---

## 3. Structure de la Base de Données

### 3.1 Table `res_partner` (Étendue)

**Nouveaux champs ajoutés:**

```sql
-- ai_score: INTEGER (0-100)
-- ai_verdict: VARCHAR (low/medium/high)
-- ai_experience_level: VARCHAR (junior/intermediate/senior/expert)
-- ai_detected_skills: TEXT
-- ai_missing_skills: TEXT
-- ai_analysis_date: TIMESTAMP
```

### 3.2 Table `smart_recruiter_job_profile`

```sql
CREATE TABLE smart_recruiter_job_profile (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    active BOOLEAN DEFAULT TRUE,
    min_score_threshold INTEGER DEFAULT 50,
    priority VARCHAR(20),  -- low/medium/high/urgent
    color INTEGER,
    create_date TIMESTAMP,
    write_date TIMESTAMP,
    create_uid INTEGER REFERENCES res_users(id),
    write_uid INTEGER REFERENCES res_users(id)
);
```

### 3.3 Table `smart_recruiter_skill`

```sql
CREATE TABLE smart_recruiter_skill (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    weight INTEGER DEFAULT 10,
    profile_id INTEGER REFERENCES smart_recruiter_job_profile(id) ON DELETE CASCADE,
    is_critical BOOLEAN DEFAULT FALSE,
    skill_type VARCHAR(20),  -- technical/soft/language/certification
    create_date TIMESTAMP,
    write_date TIMESTAMP
);
```

### 3.4 Relations

```
smart_recruiter_job_profile (1) ──< (N) smart_recruiter_skill
                                  (One-to-Many)
```

---

## 4. API et Méthodes

### 4.1 Méthodes Publiques

#### `action_analyze_profile()`

**Type:** Action Odoo (déclenchée par bouton)

**Signature:**
```python
def action_analyze_profile(self) -> dict
```

**Retour:**
```python
{
    'type': 'ir.actions.client',
    'tag': 'display_notification',
    'params': {
        'title': 'Analyse Terminée',
        'message': 'Score calculé: 85%',
        'type': 'success',
        'sticky': False,
    }
}
```

**Utilisation:**
```xml
<button name="action_analyze_profile" type="object" string="Analyser"/>
```

### 4.2 Méthodes Privées

#### `_compute_ai_score()`

**Type:** Méthode compute

**Déclenchement:** Automatique sur modification de `comment`

**Signature:**
```python
@api.depends('comment')
def _compute_ai_score(self) -> None
```

**Complexité:** O(n × m)
- n = nombre de candidats
- m = nombre de compétences dans la base

#### `_get_skills_database()`

**Type:** Méthode helper

**Retour:** dict[str, int]

**Utilisation:**
```python
skills = self._get_skills_database()
# {'python': 20, 'java': 20, ...}
```

#### `_detect_experience_level(text_content: str)`

**Type:** Méthode d'analyse

**Signature:**
```python
def _detect_experience_level(self, text_content: str) -> str
```

**Retour:** 'junior' | 'intermediate' | 'senior' | 'expert' | False

---

## 5. Guide du Développeur

### 5.1 Ajouter une Nouvelle Compétence

**Fichier:** `models/res_partner_ai.py`

```python
def _get_skills_database(self):
    return {
        # ... compétences existantes ...

        # Nouvelle compétence
        'flutter': 15,  # Ajouter ici
    }
```

### 5.2 Modifier la Pondération

Pour donner plus d'importance à une compétence :

```python
'python': 25,  # Au lieu de 20
```

### 5.3 Changer les Seuils de Verdict

**Fichier:** `models/res_partner_ai.py` (ligne ~244)

```python
if score < 40:  # Au lieu de 30
    record.ai_verdict = 'low'
elif score < 75:  # Au lieu de 70
    record.ai_verdict = 'medium'
else:
    record.ai_verdict = 'high'
```

### 5.4 Ajouter un Nouveau Champ Calculé

**Étape 1:** Définir le champ

```python
ai_custom_field = fields.Char(
    string="Mon Champ",
    compute='_compute_ai_score',
    store=True
)
```

**Étape 2:** Calculer dans `_compute_ai_score()`

```python
def _compute_ai_score(self):
    for record in self:
        # ... code existant ...

        record.ai_custom_field = "Valeur calculée"
```

**Étape 3:** Ajouter dans la vue XML

```xml
<field name="ai_custom_field"/>
```

### 5.5 Déboguer l'Algorithme

**Méthode 1 : Logs Python**

```python
import logging
_logger = logging.getLogger(__name__)

def _compute_ai_score(self):
    for record in self:
        _logger.info(f"Analyse du candidat: {record.name}")
        _logger.debug(f"Score calculé: {score}")
```

**Méthode 2 : Breakpoint**

```python
import pdb; pdb.set_trace()  # Arrêt pour débogage
```

**Méthode 3 : Raise Exception**

```python
raise UserError(f"Debug: score={score}, skills={detected_skills_list}")
```

---

## 6. Tests et Débogage

### 6.1 Tests Unitaires (Exemple)

```python
# tests/test_scoring.py
from odoo.tests.common import TransactionCase

class TestSmartRecruiterScoring(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Partner = self.env['res.partner']

    def test_empty_profile_score_zero(self):
        """Test: Un profil vide doit avoir un score de 0"""
        partner = self.Partner.create({
            'name': 'Test User',
            'comment': '',
        })
        self.assertEqual(partner.ai_score, 0)
        self.assertEqual(partner.ai_verdict, 'low')

    def test_python_skill_detected(self):
        """Test: La compétence Python doit être détectée"""
        partner = self.Partner.create({
            'name': 'Python Dev',
            'comment': 'Développeur Python avec 5 ans d\'expérience',
        })
        self.assertGreater(partner.ai_score, 0)
        self.assertIn('Python', partner.ai_detected_skills)

    def test_senior_experience_detection(self):
        """Test: Détection du niveau Senior"""
        partner = self.Partner.create({
            'name': 'Senior Dev',
            'comment': 'Développeur avec 8 ans d\'expérience',
        })
        self.assertEqual(partner.ai_experience_level, 'senior')
```

**Exécution:**
```bash
./odoo-bin -c odoo.conf -d test_db -i smart_recruiter_ai --test-enable --stop-after-init
```

### 6.2 Vérifications Manuelles

**Checklist de test:**

- [ ] Créer un contact sans notes → Score = 0%
- [ ] Ajouter "Python" → Score augmente
- [ ] Ajouter "5 ans" → Niveau = Senior
- [ ] Cliquer sur "Analyser le Profil" → Notification
- [ ] Filtrer par "Top Profils" → Uniquement score ≥ 70%
- [ ] Créer un profil de poste → Enregistrement OK
- [ ] Ajouter des compétences au profil → Liste visible

---

## 7. Optimisations et Performance

### 7.1 Problèmes de Performance Potentiels

**Problème 1:** Calcul sur tous les contacts

Si vous avez 10 000 contacts et que tous ont des notes, le calcul sera déclenché 10 000 fois.

**Solution:**
- Utiliser `store=True` pour mettre en cache
- Ajouter un index sur le champ `comment`

```python
comment = fields.Text(index=True)
```

**Problème 2:** Expressions régulières coûteuses

Chaque regex est exécutée sur tout le texte.

**Solution:**
- Compiler les regex une seule fois

```python
import re

YEARS_PATTERN = re.compile(r'(\d+)\s*(?:\+)?\s*an(?:s|née(?:s)?)', re.IGNORECASE)

def _detect_experience_level(self, text):
    matches = YEARS_PATTERN.findall(text)
    # ...
```

### 7.2 Optimisation Base de Données

**Index recommandés:**

```sql
CREATE INDEX idx_partner_ai_score ON res_partner(ai_score);
CREATE INDEX idx_partner_ai_verdict ON res_partner(ai_verdict);
CREATE INDEX idx_partner_comment ON res_partner(comment);
```

### 7.3 Limiter le Calcul

Calculer uniquement si le champ `comment` n'est pas vide :

```python
def _compute_ai_score(self):
    for record in self:
        if not record.comment:
            record.ai_score = 0
            # Skip calcul
            continue

        # Calcul normal...
```

---

## 8. Évolutions Possibles

### 8.1 Intégration NLP (Natural Language Processing)

**Librairie:** spaCy

```python
import spacy

nlp = spacy.load("fr_core_news_md")

def _extract_skills_nlp(self, text):
    doc = nlp(text)
    skills = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":  # Custom NER
            skills.append(ent.text)
    return skills
```

### 8.2 API REST

**Endpoint:** `/api/smart_recruiter/analyze`

```python
from odoo import http
from odoo.http import request

class SmartRecruiterAPI(http.Controller):

    @http.route('/api/smart_recruiter/analyze', type='json', auth='user')
    def analyze_profile(self, text):
        # Analyse du texte
        partner = request.env['res.partner'].create({
            'name': 'API Candidate',
            'comment': text,
        })

        return {
            'score': partner.ai_score,
            'verdict': partner.ai_verdict,
            'skills': partner.ai_detected_skills,
        }
```

### 8.3 Machine Learning

**Entraînement d'un modèle:**

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Dataset
X_train = [cv1, cv2, cv3, ...]  # Textes des CVs
y_train = [85, 60, 40, ...]      # Scores manuels

# Vectorisation
vectorizer = TfidfVectorizer()
X_vectors = vectorizer.fit_transform(X_train)

# Entraînement
model = RandomForestClassifier()
model.fit(X_vectors, y_train)

# Prédiction
new_cv_vector = vectorizer.transform([new_cv])
predicted_score = model.predict(new_cv_vector)
```

### 8.4 Import PDF/DOCX

**Librairie:** PyPDF2, python-docx

```python
import PyPDF2

def extract_text_from_pdf(self, pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
```

---

## Conclusion

Cette documentation technique fournit tous les détails nécessaires pour :
- Comprendre l'architecture du module
- Modifier et étendre les fonctionnalités
- Déboguer et optimiser les performances
- Planifier des évolutions futures

Pour toute question technique, référez-vous au code source ou contactez l'auteur.

**Taha Naya** - Développeur du module Smart Recruiter AI
