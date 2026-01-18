from odoo import models, fields, api
import re

class ResPartnerAi(models.Model):
    _inherit = 'res.partner'

    # --- Nouveau Champ : Sélection du Profil ---
    job_profile_id = fields.Many2one(
        'smart.recruiter.job.profile',
        string="Profil Ciblé",
        help="Sélectionnez un profil pour comparer le candidat uniquement aux compétences de ce poste."
    )

    # --- Champs Existants ---
    ai_score = fields.Integer(
        string="Score de Pertinence (%)", 
        compute='_compute_ai_score', 
        store=True
    )
    
    ai_verdict = fields.Selection([
        ('low', '🔴 Profil Faible'),
        ('medium', '🟠 Profil Intéressant'),
        ('high', '🟢 Top Profil (A recruter)'),
    ], string="Verdict IA", compute='_compute_ai_score', store=True)

    ai_experience_level = fields.Selection([
        ('junior', 'Junior (0-2 ans)'),
        ('intermediate', 'Intermédiaire (2-5 ans)'),
        ('senior', 'Senior (5-10 ans)'),
        ('expert', 'Expert (10+ ans)'),
    ], string="Niveau d'Expérience", compute='_compute_ai_score', store=True)

    ai_detected_skills = fields.Text(string="Compétences Détectées", compute='_compute_ai_score', store=True)
    ai_missing_skills = fields.Text(string="Compétences Manquantes", compute='_compute_ai_score', store=True)
    ai_analysis_date = fields.Datetime(string="Date d'Analyse", compute='_compute_ai_score', store=True)

    # --- Détection Expérience ---
    def _detect_experience_level(self, text_content):
        if not text_content: return False
        
        # Regex pour "5 ans", "10 years"
        years_patterns = [r'(\d+)\s*(?:\+)?\s*an(?:s|née(?:s)?)', r'(\d+)\s*(?:\+)?\s*year(?:s)?']
        max_years = 0
        for pattern in years_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            for match in matches:
                if int(match) > max_years: max_years = int(match)
        
        if max_years > 0:
            if max_years < 2: return 'junior'
            elif max_years < 5: return 'intermediate'
            elif max_years < 10: return 'senior'
            else: return 'expert'

        # Mots-clés
        if any(w in text_content for w in ['junior', 'débutant', 'stagiaire']): return 'junior'
        if any(w in text_content for w in ['senior', 'confirmé', 'expert', 'lead']): return 'senior'
        if any(w in text_content for w in ['manager', 'directeur', 'chef']): return 'expert'
            
        return 'intermediate'

    # --- Moteur "IA" Intelligent (Avec Profil) ---
    @api.depends('comment', 'job_profile_id') # Déclenché si le profil change
    def _compute_ai_score(self):
        for record in self:
            score = 0
            detected_skills_list = []
            missing_skills_list = []
            
            # Reset
            record.ai_experience_level = False
            record.ai_detected_skills = ""
            record.ai_missing_skills = ""

            if record.comment:
                text_content = record.comment.lower()
                
                # --- LOGIQUE DE CIBLAGE ---
                # Si un profil est sélectionné, on ne charge QUE ses compétences
                if record.job_profile_id:
                    target_skills = record.job_profile_id.skill_ids
                else:
                    # Sinon, on charge tout (Scan Global)
                    target_skills = self.env['smart.recruiter.skill'].search([])
                
                skills_db = {}
                critical_skills_set = set()
                total_possible_score = 0

                # Construction du dictionnaire
                for skill in target_skills:
                    key_name = skill.name.lower()
                    if key_name not in skills_db or skill.weight > skills_db[key_name]:
                        skills_db[key_name] = skill.weight
                    if skill.is_critical:
                        critical_skills_set.add(key_name)

                # Comparaison
                for skill_name, weight in skills_db.items():
                    if skill_name in text_content:
                        score += weight
                        detected_skills_list.append(f"{skill_name.title()} (+{weight} pts)")
                    elif skill_name in critical_skills_set:
                        missing_skills_list.append(skill_name.title())
                    
                    # On calcule le score max sur les compétences critiques ou trouvées
                    if skill_name in critical_skills_set or skill_name in text_content:
                        total_possible_score += weight

                # Calcul Final
                if total_possible_score > 0:
                    base_score = min(70, (score / total_possible_score) * 70)
                    bonus_score = min(30, len(detected_skills_list) * 2)
                    score = int(base_score + bonus_score)
                else:
                    score = 0 if record.job_profile_id else min(100, score)

                record.ai_experience_level = self._detect_experience_level(text_content)
                record.ai_detected_skills = "✅ " + "\n✅ ".join(detected_skills_list) if detected_skills_list else "Rien détecté."
                record.ai_missing_skills = "⚠️ " + "\n⚠️ ".join(missing_skills_list) if missing_skills_list else "Aucun manque critique."

            else:
                score = 0
                record.ai_detected_skills = "⚠️ Veuillez remplir les notes."

            record.ai_score = min(100, score)

            if score < 30: record.ai_verdict = 'low'
            elif score < 70: record.ai_verdict = 'medium'
            else: record.ai_verdict = 'high'
            
            record.ai_analysis_date = fields.Datetime.now()

    def action_analyze_profile(self):
        self._compute_ai_score()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Analyse Terminée',
                'message': f'Nouveau Score : {self.ai_score}%',
                'type': 'success',
                'sticky': False,
            }
        }