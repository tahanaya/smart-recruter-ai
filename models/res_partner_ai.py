# Fichier: smart_recruiter_ai/models/res_partner_ai.py
from odoo import models, fields, api
import re

class ResPartnerAi(models.Model):
    _inherit = 'res.partner'

    # --- Nouveaux Champs ---
    ai_score = fields.Integer(
        string="Score de Pertinence (%)",
        compute='_compute_ai_score',
        store=True,
        help="Score calculé automatiquement basé sur les mots-clés trouvés."
    )

    ai_verdict = fields.Selection(
        [
            ('low', '🔴 Profil Faible'),
            ('medium', '🟠 Profil Intéressant'),
            ('high', '🟢 Top Profil (A recruter)'),
        ],
        string="Verdict IA",
        compute='_compute_ai_score',
        store=True
    )

    ai_experience_level = fields.Selection(
        [
            ('junior', 'Junior (0-2 ans)'),
            ('intermediate', 'Intermédiaire (2-5 ans)'),
            ('senior', 'Senior (5-10 ans)'),
            ('expert', 'Expert (10+ ans)'),
        ],
        string="Niveau d'Expérience",
        compute='_compute_ai_score',
        store=True
    )

    ai_detected_skills = fields.Text(
        string="Compétences Détectées",
        compute='_compute_ai_score',
        store=True,
        help="Liste des compétences techniques identifiées dans le profil."
    )

    ai_missing_skills = fields.Text(
        string="Compétences Manquantes",
        compute='_compute_ai_score',
        store=True,
        help="Compétences critiques non détectées dans le profil."
    )

    ai_analysis_date = fields.Datetime(
        string="Date d'Analyse",
        compute='_compute_ai_score',
        store=True
    )

    # --- Base de Connaissances des Compétences avec Pondération ---
    def _get_skills_database(self):
        """
        Retourne un dictionnaire de compétences avec leur pondération.
        Plus la valeur est élevée, plus la compétence est importante.
        """
        return {
            # Compétences Techniques Critiques (20 points chacune)
            'python': 20,
            'odoo': 20,
            'java': 20,
            'javascript': 18,
            'react': 18,
            'angular': 18,
            'vue.js': 18,
            'node.js': 18,

            # Bases de Données (15 points)
            'postgresql': 15,
            'sql': 15,
            'mysql': 15,
            'mongodb': 15,
            'oracle': 15,

            # DevOps et Outils (12 points)
            'docker': 12,
            'kubernetes': 12,
            'jenkins': 12,
            'gitlab': 10,
            'github': 10,
            'git': 10,
            'ci/cd': 12,

            # Méthodologies (10 points)
            'agile': 10,
            'scrum': 10,
            'kanban': 8,
            'devops': 12,

            # Langues (8 points)
            'anglais': 8,
            'français': 8,
            'espagnol': 6,
            'allemand': 6,

            # Soft Skills (5 points)
            'leadership': 5,
            'communication': 5,
            'travail d\'équipe': 5,
            'gestion de projet': 8,

            # Autres Compétences Techniques (10 points)
            'rest api': 10,
            'api': 8,
            'xml': 8,
            'json': 8,
            'html': 6,
            'css': 6,
            'django': 15,
            'flask': 12,
            'fastapi': 12,

            # Cloud (12 points)
            'aws': 12,
            'azure': 12,
            'google cloud': 12,
            'gcp': 12,

            # Certifications (15 points bonus)
            'certifié': 15,
            'certification': 15,
            'diplôme': 10,
            'master': 10,
            'ingénieur': 8,
        }

    # --- Détection du Niveau d'Expérience ---
    def _detect_experience_level(self, text_content):
        """
        Analyse le texte pour détecter le niveau d'expérience basé sur :
        - Mentions explicites d'années d'expérience
        - Mots-clés indiquant le niveau de séniorité
        """
        if not text_content:
            return False

        # Recherche de mentions d'années d'expérience (ex: "5 ans", "10 années", "3+ ans")
        years_patterns = [
            r'(\d+)\s*(?:\+)?\s*an(?:s|née(?:s)?)',  # "5 ans", "10 années", "3+ ans"
            r'(\d+)\s*(?:\+)?\s*year(?:s)?',          # "5 years", "10+ years"
        ]

        max_years = 0
        for pattern in years_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                for match in matches:
                    years = int(match)
                    if years > max_years:
                        max_years = years

        if max_years > 0:
            if max_years < 2:
                return 'junior'
            elif max_years < 5:
                return 'intermediate'
            elif max_years < 10:
                return 'senior'
            else:
                return 'expert'

        # Détection par mots-clés si pas de mention d'années
        if any(word in text_content for word in ['junior', 'débutant', 'stagiaire', 'apprenti']):
            return 'junior'
        elif any(word in text_content for word in ['senior', 'confirmé', 'expert', 'lead', 'architect']):
            return 'senior'
        elif any(word in text_content for word in ['manager', 'directeur', 'chef', 'responsable']):
            return 'expert'

        return 'intermediate'  # Par défaut

    # --- Moteur "IA" Amélioré (Logique de Scoring Avancée) ---
    @api.depends('comment') # 'comment' est le champ "Notes internes" dans Odoo
    def _compute_ai_score(self):
        for record in self:
            score = 0
            detected_skills_list = []
            missing_skills_list = []

            if record.comment:
                # Normalisation du texte (tout en minuscule pour la comparaison)
                text_content = record.comment.lower()

                # Récupération de la base de compétences
                skills_db = self._get_skills_database()

                # Détection des compétences avec pondération
                total_possible_score = 0
                critical_skills = ['python', 'odoo', 'java', 'sql', 'docker', 'agile']

                for skill, weight in skills_db.items():
                    if skill in text_content:
                        score += weight
                        detected_skills_list.append(f"{skill.title()} (+{weight} pts)")
                    elif skill in critical_skills:
                        missing_skills_list.append(skill.title())

                    # Calcul du score maximum possible (basé sur les compétences critiques)
                    if skill in critical_skills:
                        total_possible_score += weight

                # Normalisation du score sur 100
                # On prend en compte les compétences critiques pour le calcul
                if total_possible_score > 0:
                    # Score proportionnel + bonus pour compétences supplémentaires
                    base_score = min(70, (score / total_possible_score) * 70)
                    bonus_score = min(30, len(detected_skills_list) * 2)
                    score = int(base_score + bonus_score)
                else:
                    score = min(100, score)

                # Détection du niveau d'expérience
                record.ai_experience_level = self._detect_experience_level(text_content)

                # Formatage des compétences détectées
                if detected_skills_list:
                    record.ai_detected_skills = "✅ " + "\n✅ ".join(detected_skills_list)
                else:
                    record.ai_detected_skills = "Aucune compétence technique détectée."

                # Formatage des compétences manquantes
                if missing_skills_list:
                    record.ai_missing_skills = "⚠️ " + "\n⚠️ ".join(missing_skills_list)
                else:
                    record.ai_missing_skills = "Aucune compétence critique manquante."
            else:
                # Pas de description fournie
                record.ai_experience_level = False
                record.ai_detected_skills = "⚠️ Aucune note interne renseignée. Veuillez ajouter une description du profil."
                record.ai_missing_skills = "Impossible d'analyser sans données."

            # Assignation du score final
            record.ai_score = min(100, score)

            # Définition du verdict
            if score < 30:
                record.ai_verdict = 'low'
            elif score < 70:
                record.ai_verdict = 'medium'
            else:
                record.ai_verdict = 'high'

            # Date de l'analyse
            record.ai_analysis_date = fields.Datetime.now()

    # --- Bouton d'Analyse Manuelle ---
    def action_analyze_profile(self):
        """
        Bouton pour forcer le recalcul du score.
        Utile si l'utilisateur modifie manuellement les notes.
        """
        self._compute_ai_score()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Analyse Terminée',
                'message': f'Score calculé: {self.ai_score}% | Verdict: {dict(self._fields["ai_verdict"].selection).get(self.ai_verdict)}',
                'type': 'success',
                'sticky': False,
            }
        }