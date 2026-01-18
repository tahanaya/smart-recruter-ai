# Guide de Tests - Smart Recruiter AI

## Objectif

Ce guide fournit des scénarios de tests détaillés pour valider le bon fonctionnement du module Smart Recruiter AI.

---

## Table des Matières

1. [Tests Fonctionnels](#tests-fonctionnels)
2. [Tests de l'Algorithme](#tests-de-lalgorithme)
3. [Tests d'Interface](#tests-dinterface)
4. [Tests de Performance](#tests-de-performance)
5. [Tests de Sécurité](#tests-de-sécurité)
6. [Scénarios Utilisateurs](#scénarios-utilisateurs)

---

## 1. Tests Fonctionnels

### Test 1.1 : Installation du Module

**Objectif :** Vérifier que le module s'installe correctement

**Procédure :**
1. Activer le mode développeur
2. Applications > Mettre à jour la liste des applications
3. Rechercher "Smart Recruiter AI"
4. Cliquer sur "Installer"

**Résultat attendu :**
- ✅ Installation réussie sans erreur
- ✅ Module visible dans la liste des applications installées
- ✅ Pas d'erreur dans les logs Odoo

**Commande pour vérifier les logs :**
```bash
tail -f /var/log/odoo/odoo.log | grep -i error
```

---

### Test 1.2 : Champs Ajoutés sur Contact

**Objectif :** Vérifier que les nouveaux champs sont bien ajoutés au modèle res.partner

**Procédure :**
1. Aller dans Contacts
2. Créer un nouveau contact
3. Vérifier la présence de l'onglet "Analyse IA Smart Recruiter"

**Résultat attendu :**
- ✅ Onglet "📊 Analyse IA Smart Recruiter" visible
- ✅ Champs présents :
  - Score de Pertinence (%)
  - Verdict IA
  - Niveau d'Expérience
  - Date d'Analyse
  - Compétences Détectées
  - Compétences Manquantes
- ✅ Bouton "🔍 Analyser le Profil" visible dans le header

---

### Test 1.3 : Données de Démonstration

**Objectif :** Vérifier que les données de démo sont chargées

**Procédure :**
1. Aller dans Smart Recruiter AI > Configuration > Profils de Poste
2. Vérifier la présence des profils prédéfinis

**Résultat attendu :**
- ✅ 3 profils de postes visibles :
  - Développeur Python Senior
  - Développeur Full-Stack
  - Ingénieur DevOps
- ✅ Chaque profil contient des compétences configurées

**Procédure (Candidats) :**
1. Aller dans Contacts
2. Filtrer par nom : "Jean Dupont", "Marie Martin", "Ahmed Ben Ali", "Sophie Leclerc"

**Résultat attendu :**
- ✅ 4 candidats de démonstration présents
- ✅ Chaque candidat a des notes internes remplies
- ✅ Les scores sont déjà calculés

---

## 2. Tests de l'Algorithme

### Test 2.1 : Profil Vide (Score = 0)

**Objectif :** Vérifier le comportement avec un profil sans notes

**Procédure :**
1. Créer un contact "Test Vide"
2. Ne rien mettre dans "Notes Internes"
3. Aller dans l'onglet "Analyse IA"

**Résultat attendu :**
- ✅ Score : 0%
- ✅ Verdict : 🔴 Profil Faible
- ✅ Niveau d'Expérience : (vide)
- ✅ Compétences Détectées : "⚠️ Aucune note interne renseignée"
- ✅ Compétences Manquantes : "Impossible d'analyser sans données"

---

### Test 2.2 : Détection de Compétences Simples

**Objectif :** Vérifier la détection de compétences de base

**Procédure :**
1. Créer un contact "Test Python"
2. Ajouter dans Notes Internes :
   ```
   Développeur avec compétence en Python
   ```
3. Cliquer sur "Analyser le Profil"

**Résultat attendu :**
- ✅ Score : Entre 15% et 30%
- ✅ Verdict : 🟠 Profil Intéressant (si >30) ou 🔴 Profil Faible (si <30)
- ✅ Compétences Détectées : "✅ Python (+20 pts)"
- ✅ Compétences Manquantes : Liste contenant "Odoo", "Java", "SQL", "Docker", "Agile"

---

### Test 2.3 : Profil avec Multiples Compétences

**Objectif :** Tester le scoring avec plusieurs compétences

**Procédure :**
1. Créer un contact "Test Multi Compétences"
2. Ajouter dans Notes Internes :
   ```
   Développeur Full-Stack
   Compétences : Python, Java, PostgreSQL, Docker, Git, Agile
   ```
3. Analyser le profil

**Résultat attendu :**
- ✅ Score : Entre 60% et 80%
- ✅ Verdict : 🟢 Top Profil (si ≥70%) ou 🟠 Profil Intéressant (si <70%)
- ✅ Compétences Détectées contient :
  - Python (+20 pts)
  - Java (+20 pts)
  - Postgresql (+15 pts)
  - Docker (+12 pts)
  - Git (+10 pts)
  - Agile (+10 pts)
- ✅ Score total calculé correctement

**Calcul manuel attendu :**
```
Score brut = 20+20+15+12+10+10 = 87 points
Compétences critiques trouvées : Python, Java, PostgreSQL, Docker, Agile = 5/6
Score base = min(70, (87/97) * 70) = 62.8
Score bonus = min(30, 6 compétences * 2) = 12
Score final = 62.8 + 12 = 74.8% → Arrondi à 74%
```

---

### Test 2.4 : Détection Niveau d'Expérience (Années)

**Objectif :** Vérifier la détection du niveau via années d'expérience

**Scénarios :**

| Texte | Niveau Attendu |
|-------|----------------|
| "Développeur avec 1 an d'expérience" | Junior (0-2 ans) |
| "3 années d'expérience en Python" | Intermédiaire (2-5 ans) |
| "7 ans d'expérience professionnelle" | Senior (5-10 ans) |
| "Expert avec 15 ans d'expérience" | Expert (10+ ans) |
| "2+ ans dans le développement" | Intermédiaire |

**Procédure pour chaque scénario :**
1. Créer un contact
2. Ajouter le texte dans Notes Internes
3. Analyser
4. Vérifier le champ "Niveau d'Expérience"

---

### Test 2.5 : Détection Niveau d'Expérience (Mots-clés)

**Objectif :** Vérifier la détection du niveau via mots-clés

**Scénarios :**

| Texte | Niveau Attendu |
|-------|----------------|
| "Développeur junior cherchant opportunité" | Junior |
| "Profil senior avec expertise en Odoo" | Senior |
| "Lead developer avec 5 ans d'XP" | Senior |
| "Chef de projet et manager" | Expert |
| "Architecte logiciel confirmé" | Senior |

---

### Test 2.6 : Pondération des Compétences

**Objectif :** Vérifier que les compétences ont des poids différents

**Procédure :**
1. **Test A :** Profil avec seulement "Python" (20 pts)
2. **Test B :** Profil avec seulement "HTML" (6 pts)
3. Comparer les scores

**Résultat attendu :**
- ✅ Test A a un score supérieur à Test B
- ✅ Python vaut plus de points que HTML

---

### Test 2.7 : Score Maximum

**Objectif :** Vérifier que le score ne dépasse jamais 100%

**Procédure :**
1. Créer un contact avec toutes les 50+ compétences dans les notes
2. Analyser le profil

**Résultat attendu :**
- ✅ Score = 100% (plafonné)
- ✅ Pas d'erreur de calcul

---

## 3. Tests d'Interface

### Test 3.1 : Bouton "Analyser le Profil"

**Objectif :** Vérifier le fonctionnement du bouton

**Procédure :**
1. Ouvrir un contact existant
2. Modifier les Notes Internes
3. Cliquer sur "🔍 Analyser le Profil"

**Résultat attendu :**
- ✅ Notification verte affichée : "Analyse Terminée"
- ✅ Message contient le score calculé
- ✅ Les champs sont mis à jour
- ✅ Pas d'erreur JavaScript dans la console

---

### Test 3.2 : Widget PercentPie

**Objectif :** Vérifier l'affichage du score en camembert

**Procédure :**
1. Créer un contact avec un score de 75%
2. Ouvrir l'onglet Analyse IA

**Résultat attendu :**
- ✅ Camembert affiché avec 75% en vert
- ✅ Tooltip indique "75%"
- ✅ Pas d'erreur de rendu

---

### Test 3.3 : Badges Colorés

**Objectif :** Vérifier la colorisation des badges

**Scénarios :**

| Score | Verdict Attendu | Couleur Badge |
|-------|----------------|---------------|
| 15% | 🔴 Profil Faible | Rouge (danger) |
| 50% | 🟠 Profil Intéressant | Orange (warning) |
| 85% | 🟢 Top Profil | Vert (success) |

**Résultat attendu :**
- ✅ Badges correctement colorés selon le verdict

---

### Test 3.4 : Filtres dans Vue Liste

**Objectif :** Vérifier les filtres intelligents

**Procédure :**
1. Aller dans Contacts
2. Cliquer sur le filtre "🟢 Top Profils (70%+)"
3. Vérifier que seuls les contacts avec score ≥ 70% sont affichés

**Procédure pour autres filtres :**
- Filtre "🟠 Profils Intéressants (30-69%)"
- Filtre "🔴 Profils Faibles (<30%)"
- Filtre "Junior"
- Filtre "Senior"

**Résultat attendu :**
- ✅ Filtres fonctionnent correctement
- ✅ Nombre de résultats cohérent

---

### Test 3.5 : Colorisation des Lignes

**Objectif :** Vérifier la colorisation automatique dans la vue liste

**Procédure :**
1. Aller dans Contacts (vue liste)
2. Observer les couleurs des lignes

**Résultat attendu :**
- ✅ Lignes vertes pour score ≥ 70%
- ✅ Lignes oranges pour score 30-69%
- ✅ Lignes rouges pour score < 30%

---

### Test 3.6 : Groupage

**Objectif :** Tester le groupage par verdict et expérience

**Procédure :**
1. Vue liste Contacts
2. Grouper par "Verdict IA"
3. Observer les groupes

**Résultat attendu :**
- ✅ 3 groupes visibles :
  - 🔴 Profil Faible
  - 🟠 Profil Intéressant
  - 🟢 Top Profil
- ✅ Compteur correct pour chaque groupe

**Procédure (Niveau d'Expérience) :**
1. Grouper par "Niveau d'Expérience"
2. Observer les groupes

**Résultat attendu :**
- ✅ Groupes : Junior, Intermédiaire, Senior, Expert

---

## 4. Tests de Performance

### Test 4.1 : Temps de Calcul

**Objectif :** Mesurer le temps de calcul pour 1 contact

**Procédure :**
1. Activer les logs de performance dans Odoo
2. Analyser un profil
3. Mesurer le temps

**Résultat attendu :**
- ✅ Temps < 100ms pour 1 contact
- ✅ Pas de timeout

---

### Test 4.2 : Calcul en Masse

**Objectif :** Tester le calcul sur plusieurs contacts

**Procédure :**
1. Créer 100 contacts de test avec notes
2. Forcer le recalcul :
   ```python
   partners = self.env['res.partner'].search([('comment', '!=', False)])
   partners._compute_ai_score()
   ```
3. Mesurer le temps total

**Résultat attendu :**
- ✅ Temps < 10 secondes pour 100 contacts
- ✅ Pas de crash mémoire

---

### Test 4.3 : Stockage en Cache

**Objectif :** Vérifier que `store=True` fonctionne

**Procédure :**
1. Analyser un contact
2. Vérifier dans la BDD :
   ```sql
   SELECT name, ai_score, ai_verdict FROM res_partner WHERE id = X;
   ```

**Résultat attendu :**
- ✅ Valeurs stockées en base de données
- ✅ Pas de recalcul à chaque lecture

---

## 5. Tests de Sécurité

### Test 5.1 : Droits d'Accès

**Objectif :** Vérifier les permissions

**Procédure :**
1. Créer un utilisateur "Test User" avec groupe "Utilisateur / Employé"
2. Se connecter avec cet utilisateur
3. Essayer de créer un profil de poste

**Résultat attendu :**
- ✅ Accès autorisé (lecture + écriture)
- ✅ Pas d'erreur de permission

---

### Test 5.2 : Injection SQL

**Objectif :** Vérifier qu'il n'y a pas de faille SQL

**Procédure :**
1. Créer un contact
2. Ajouter dans Notes Internes :
   ```
   '; DROP TABLE res_partner; --
   ```
3. Analyser le profil

**Résultat attendu :**
- ✅ Pas de crash
- ✅ Table res_partner toujours présente
- ✅ Texte traité comme une chaîne normale

---

### Test 5.3 : XSS (Cross-Site Scripting)

**Objectif :** Vérifier la protection contre XSS

**Procédure :**
1. Ajouter dans Notes Internes :
   ```html
   <script>alert('XSS')</script>
   ```
2. Ouvrir l'onglet Analyse IA

**Résultat attendu :**
- ✅ Pas d'alerte JavaScript
- ✅ Balises HTML échappées
- ✅ Texte affiché tel quel

---

## 6. Scénarios Utilisateurs

### Scénario 1 : Recrutement d'un Développeur Python

**Contexte :**
Un RH cherche un développeur Python senior avec au moins 5 ans d'expérience.

**Étapes :**
1. Recevoir 10 candidatures par email
2. Copier-coller chaque CV dans "Notes Internes" d'un contact
3. Analyser les profils
4. Filtrer par "Top Profils" ET "Senior"
5. Sélectionner les 3 meilleurs candidats

**Résultat attendu :**
- ✅ Temps de traitement : < 10 minutes (vs 1 heure manuellement)
- ✅ Les 3 meilleurs candidats identifiés rapidement
- ✅ Compétences manquantes visibles pour chaque profil

---

### Scénario 2 : Configuration d'un Nouveau Profil de Poste

**Contexte :**
L'entreprise recrute un "Data Scientist" et veut adapter l'algorithme.

**Étapes :**
1. Aller dans Smart Recruiter AI > Configuration > Profils de Poste
2. Créer un nouveau profil "Data Scientist"
3. Ajouter les compétences :
   - Python (20 pts, critique)
   - Machine Learning (20 pts, critique)
   - TensorFlow (18 pts, critique)
   - Pandas (15 pts)
   - NumPy (15 pts)
   - Statistiques (12 pts)
4. Définir le seuil minimum à 70%
5. Enregistrer

**Résultat attendu :**
- ✅ Profil créé avec succès
- ✅ Compétences configurées et affichées
- ✅ Utilisable pour futurs recrutements

---

### Scénario 3 : Analyse Rapide d'un Profil Prometteur

**Contexte :**
Un recruteur reçoit un CV exceptionnel et veut une analyse immédiate.

**Étapes :**
1. Créer un contact "Candidat Urgent"
2. Copier le CV dans Notes Internes
3. Cliquer sur "🔍 Analyser le Profil"
4. Lire le verdict instantanément

**Résultat attendu :**
- ✅ Analyse en moins de 5 secondes
- ✅ Notification affichée : "Analyse Terminée - Score: 92%"
- ✅ Verdict : 🟢 Top Profil
- ✅ Décision immédiate : Planifier un entretien

---

## Checklist Complète de Tests

### Installation et Configuration
- [ ] Installation sans erreur
- [ ] Données de démo chargées
- [ ] Menu visible
- [ ] Droits d'accès configurés

### Fonctionnalités de Base
- [ ] Onglet Analyse IA visible
- [ ] Bouton "Analyser le Profil" fonctionne
- [ ] Score calculé automatiquement
- [ ] Verdict assigné correctement

### Algorithme
- [ ] Profil vide = Score 0
- [ ] Détection compétences simple
- [ ] Détection compétences multiples
- [ ] Pondération respectée
- [ ] Détection niveau d'expérience (années)
- [ ] Détection niveau d'expérience (mots-clés)
- [ ] Score plafonné à 100%

### Interface
- [ ] Widget PercentPie affiché
- [ ] Badges colorés correctement
- [ ] Filtres fonctionnent
- [ ] Colorisation des lignes
- [ ] Groupages opérationnels
- [ ] Notifications affichées

### Performance
- [ ] Calcul rapide (< 100ms)
- [ ] Calcul en masse OK
- [ ] Valeurs en cache

### Sécurité
- [ ] Droits d'accès OK
- [ ] Pas d'injection SQL
- [ ] Pas de faille XSS

---

## Rapporter un Bug

Si vous trouvez un bug lors des tests :

1. **Vérifier les logs Odoo**
   ```bash
   tail -f /var/log/odoo/odoo.log
   ```

2. **Noter les informations :**
   - Version Odoo
   - Version du module
   - Étapes pour reproduire
   - Résultat obtenu vs attendu
   - Message d'erreur complet

3. **Ouvrir une issue GitHub**
   - https://github.com/tahanaya/smart_recruiter_ai/issues

---

## Conclusion

Ce guide de tests permet de valider l'intégralité des fonctionnalités du module Smart Recruiter AI.

**Temps estimé pour tous les tests :** 2-3 heures

**Fréquence recommandée :**
- Tests fonctionnels : À chaque déploiement
- Tests de performance : Mensuellement
- Tests de sécurité : Trimestriellement

---

**Module développé par Taha Naya**
Version 2.0 - Janvier 2026
