# Fichier: smart_recruiter_ai/__manifest__.py
{
    'name': 'Smart Recruiter AI',
    'version': '2.0',
    'category': 'Human Resources',
    'summary': 'Analyse automatique et intelligente des CVs avec scoring avancé',
    'description': """
        Smart Recruiter AI - Module de Recrutement Intelligent
        ========================================================

        Ce module intègre un algorithme de scoring avancé pour évaluer
        automatiquement la pertinence des candidats.

        Fonctionnalités principales:
        ----------------------------
        * Scoring automatique sur 100 avec pondération intelligente
        * Détection automatique du niveau d'expérience (Junior/Senior/Expert)
        * Analyse détaillée des compétences techniques détectées
        * Identification des compétences manquantes critiques
        * Système de badges visuels (Profil Faible/Intéressant/Top)
        * Bouton d'analyse manuelle pour recalcul du score
        * Filtres intelligents pour trier les candidats
        * Support de 50+ compétences techniques avec pondération
        * Configuration personnalisable des profils de postes
        * Historique des analyses avec horodatage

        Base de connaissances:
        ---------------------
        * Langages: Python, Java, JavaScript, etc.
        * Frameworks: Odoo, Django, React, Angular, etc.
        * Bases de données: PostgreSQL, MySQL, MongoDB, etc.
        * DevOps: Docker, Kubernetes, CI/CD, etc.
        * Méthodologies: Agile, Scrum, Kanban, etc.
        * Cloud: AWS, Azure, Google Cloud
        * Langues: Anglais, Français, Espagnol, etc.

        Module développé par Taha Naya dans le cadre d'un projet académique.
    """,
    'author': 'Taha Naya',
    'website': 'https://github.com/tahanaya',
    'license': 'LGPL-3',
    'version': '2.0.0',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/job_profile_views.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}