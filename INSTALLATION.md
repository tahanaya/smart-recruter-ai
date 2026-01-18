# Guide d'Installation - Smart Recruiter AI

## Prérequis Système

### Configuration Minimale

- **Système d'exploitation:** Linux (Ubuntu 20.04+), Windows 10+, macOS 10.14+
- **Python:** 3.7, 3.8, 3.9 ou 3.10
- **PostgreSQL:** 10.0 ou supérieur
- **RAM:** 4 GB minimum (8 GB recommandé)
- **Espace disque:** 500 MB minimum

### Versions Odoo Supportées

✅ Odoo 14.0
✅ Odoo 15.0
✅ Odoo 16.0
⚠️ Odoo 17.0 (non testé)

---

## Installation sur Linux (Ubuntu/Debian)

### Méthode 1 : Installation Manuelle

#### Étape 1 : Vérifier l'installation Odoo

```bash
# Vérifier que Odoo est installé
odoo --version

# Ou pour une installation personnalisée
/path/to/odoo-bin --version
```

#### Étape 2 : Télécharger le module

**Option A : Via Git (Recommandé)**

```bash
cd /path/to/odoo/addons/
git clone https://github.com/tahanaya/smart_recruiter_ai.git
```

**Option B : Téléchargement manuel**

```bash
cd /path/to/odoo/addons/
wget https://github.com/tahanaya/smart_recruiter_ai/archive/main.zip
unzip main.zip
mv smart_recruiter_ai-main smart_recruiter_ai
```

#### Étape 3 : Vérifier les permissions

```bash
cd /path/to/odoo/addons/smart_recruiter_ai
chmod -R 755 .
chown -R odoo:odoo .
```

#### Étape 4 : Redémarrer Odoo

**Avec systemd:**
```bash
sudo systemctl restart odoo
```

**Manuellement:**
```bash
./odoo-bin -c /etc/odoo/odoo.conf
```

#### Étape 5 : Activer le mode développeur

1. Connectez-vous à Odoo (http://localhost:8069)
2. Allez dans **Paramètres**
3. En bas de page, cliquez sur **Activer le mode développeur**

#### Étape 6 : Mettre à jour la liste des applications

1. Allez dans **Applications**
2. Cliquez sur **Mettre à jour la liste des applications**
3. Recherchez "Smart Recruiter AI"
4. Cliquez sur **Installer**

---

## Installation sur Windows

### Méthode 1 : Avec Odoo Community Edition

#### Étape 1 : Télécharger Odoo

Téléchargez l'installateur depuis [odoo.com/download](https://www.odoo.com/download)

#### Étape 2 : Installer Odoo

Double-cliquez sur l'installateur et suivez les instructions.

**Chemin d'installation par défaut:**
```
C:\Program Files\Odoo 15.0\
```

#### Étape 3 : Télécharger le module

**Option A : Git Bash**

```bash
cd "C:\Program Files\Odoo 15.0\server\odoo\addons"
git clone https://github.com/tahanaya/smart_recruiter_ai.git
```

**Option B : Manuel**

1. Téléchargez le ZIP depuis GitHub
2. Extrayez dans `C:\Program Files\Odoo 15.0\server\odoo\addons\`

#### Étape 4 : Configurer le chemin des addons

Éditez `C:\Program Files\Odoo 15.0\server\odoo.conf` :

```ini
[options]
addons_path = C:\Program Files\Odoo 15.0\server\odoo\addons,C:\Program Files\Odoo 15.0\server\odoo\addons\smart_recruiter_ai
```

#### Étape 5 : Redémarrer le service Odoo

**Via Services Windows:**

1. Appuyez sur `Win + R`
2. Tapez `services.msc`
3. Recherchez "Odoo"
4. Clic droit → **Redémarrer**

**Via ligne de commande (Admin):**

```cmd
net stop odoo-server-15.0
net start odoo-server-15.0
```

#### Étape 6 : Installer le module

Suivez les étapes 5 et 6 de l'installation Linux ci-dessus.

---

## Installation avec Docker

### Dockerfile personnalisé

Créez un `Dockerfile` :

```dockerfile
FROM odoo:15.0

# Copier le module custom
COPY ./smart_recruiter_ai /mnt/extra-addons/smart_recruiter_ai

# Installer les dépendances Python supplémentaires (si nécessaire)
# RUN pip3 install numpy pandas

USER odoo
```

### Docker Compose

Créez `docker-compose.yml` :

```yaml
version: '3.1'
services:
  web:
    build: .
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./smart_recruiter_ai:/mnt/extra-addons/smart_recruiter_ai
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

volumes:
  odoo-web-data:
  odoo-db-data:
```

### Lancement

```bash
docker-compose up -d
```

Accédez à http://localhost:8069

---

## Vérification de l'Installation

### Tests de Base

1. **Vérifier que le module apparaît dans Applications**

   Recherchez "Smart Recruiter AI" dans le menu Applications.

2. **Vérifier les nouveaux champs sur un contact**

   ```
   Contacts > Créer > Onglet "Analyse IA Smart Recruiter"
   ```

   Vous devriez voir :
   - Score de Pertinence
   - Verdict IA
   - Niveau d'Expérience
   - Bouton "Analyser le Profil"

3. **Tester l'analyse**

   Ajoutez dans "Notes Internes" :
   ```
   Développeur Python avec 5 ans d'expérience
   Compétences: Python, PostgreSQL, Docker
   ```

   Cliquez sur "Analyser le Profil" → Un score devrait apparaître

### Vérification des Logs

**Linux:**
```bash
tail -f /var/log/odoo/odoo.log
```

**Windows:**
```
C:\Program Files\Odoo 15.0\server\odoo.log
```

**Docker:**
```bash
docker-compose logs -f web
```

### Erreurs Courantes

#### Erreur 1: Module non trouvé

**Message:**
```
Module smart_recruiter_ai not found
```

**Solution:**
- Vérifiez que le module est dans le bon dossier addons
- Redémarrez Odoo
- Mettez à jour la liste des applications

#### Erreur 2: Erreur de permission

**Message:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution Linux:**
```bash
sudo chown -R odoo:odoo /path/to/addons/smart_recruiter_ai
sudo chmod -R 755 /path/to/addons/smart_recruiter_ai
```

#### Erreur 3: Dépendance PostgreSQL

**Message:**
```
FATAL: database "dbname" does not exist
```

**Solution:**
```bash
sudo -u postgres createdb nom_db
```

#### Erreur 4: Port déjà utilisé

**Message:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
sudo lsof -i :8069
sudo kill -9 <PID>
```

---

## Installation des Données de Démonstration

### Lors de l'installation

Lors de l'installation du module, cochez la case **"Installer les données de démonstration"**.

Cela créera automatiquement :
- 3 profils de postes (Développeur Python, Full-Stack, DevOps)
- 4 candidats exemples (Profil Faible, Moyen, Top, Expert)
- Compétences associées

### Manuellement après installation

Si vous n'avez pas installé les données de démo, vous pouvez les charger manuellement :

```bash
./odoo-bin -c odoo.conf -d your_database -i smart_recruiter_ai --load-language=fr_FR
```

---

## Désinstallation

### Via l'interface Odoo

1. Allez dans **Applications**
2. Recherchez "Smart Recruiter AI"
3. Cliquez sur **Désinstaller**

### Manuelle

**Supprimer le module:**
```bash
rm -rf /path/to/addons/smart_recruiter_ai
```

**Nettoyer la base de données:**
```sql
DELETE FROM ir_module_module WHERE name = 'smart_recruiter_ai';
DROP TABLE smart_recruiter_job_profile CASCADE;
DROP TABLE smart_recruiter_skill CASCADE;
```

---

## Mise à Jour du Module

### Depuis Git

```bash
cd /path/to/addons/smart_recruiter_ai
git pull origin main
```

### Appliquer la mise à jour dans Odoo

**Méthode 1 : Interface**

1. Mode développeur activé
2. Applications > Smart Recruiter AI
3. Cliquer sur **Mettre à niveau**

**Méthode 2 : Ligne de commande**

```bash
./odoo-bin -c odoo.conf -d your_database -u smart_recruiter_ai
```

---

## Configuration Post-Installation

### Créer un Profil de Poste

1. **Smart Recruiter AI > Configuration > Profils de Poste**
2. **Créer**
3. Remplir :
   - Nom : "Développeur Python Senior"
   - Priorité : Haute
   - Score minimum : 70%
4. Ajouter les compétences requises
5. **Enregistrer**

### Configurer les Permissions

Si vous souhaitez restreindre l'accès :

1. **Paramètres > Utilisateurs et Entreprises > Groupes**
2. Créer un groupe "Recruteur"
3. Assigner les droits sur `smart.recruiter.job.profile`

---

## Support et Aide

### Documentation

- [README.md](README.md) - Vue d'ensemble
- [DOCUMENTATION_TECHNIQUE.md](DOCUMENTATION_TECHNIQUE.md) - Détails techniques

### Problèmes

Si vous rencontrez des problèmes :

1. Consultez les [Issues GitHub](https://github.com/tahanaya/smart_recruiter_ai/issues)
2. Ouvrez une nouvelle issue si nécessaire
3. Contactez l'auteur : taha.naya@example.com

### Communauté Odoo

- [Forum Odoo](https://www.odoo.com/forum)
- [Documentation Odoo](https://www.odoo.com/documentation)

---

## Checklist Finale

Après installation, vérifiez :

- [ ] Le module apparaît dans Applications
- [ ] L'onglet "Analyse IA" est visible sur les contacts
- [ ] Le bouton "Analyser le Profil" fonctionne
- [ ] Les données de démo sont chargées (si activées)
- [ ] Les filtres IA sont disponibles dans la vue liste
- [ ] Le menu "Smart Recruiter AI" est visible
- [ ] Les profils de postes peuvent être créés
- [ ] Aucune erreur dans les logs

✅ **Installation réussie !**

---

**Module développé par Taha Naya**
Version 2.0 - Janvier 2026
