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

    # --- Détection du Niveau d'Expérience ---
    def _detect_experience_level(self, text_content):
        """
        Analyse le texte pour détecter le niveau d'expérience basé sur :
        - Mentions explicites d'années d'expérience (Regex)
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
            if max_years < 2: return 'junior'
            elif max_years < 5: return 'intermediate'
            elif max_years < 10: return 'senior'
            else: return 'expert'

        # Détection par mots-clés si pas de mention d'années
        if any(word in text_content for word in ['junior', 'débutant', 'stagiaire', 'apprenti']):
            return 'junior'
        elif any(word in text_content for word in ['senior', 'confirmé', 'expert', 'lead', 'architect']):
            return 'senior'
        elif any(word in text_content for word in ['manager', 'directeur', 'chef', 'responsable']):
            return 'expert'
            
        return 'intermediate'  # Par défaut

    # --- Moteur "IA" Connecté à la BDD ---
    @api.depends('comment') # Déclenché quand les notes changent
    def _compute_ai_score(self):
        for record in self:
            score = 0
            detected_skills_list = []
            missing_skills_list = []
            
            # Initialisation des valeurs par défaut
            record.ai_experience_level = False
            record.ai_detected_skills = "En attente d'analyse..."
            record.ai_missing_skills = ""

            if record.comment:
                text_content = record.comment.lower()
                
                # ---------------------------------------------------------
                # PARTIE DYNAMIQUE : Récupération depuis la configuration
                # ---------------------------------------------------------
                # On cherche toutes les compétences configurées dans le module
                all_configured_skills = self.env['smart.recruiter.skill'].search([])
                
                skills_db = {}
                critical_skills_set = set()
                total_possible_score = 0

                # Construction du dictionnaire de compétences
                for skill in all_configured_skills:
                    key_name = skill.name.lower()
                    
                    # Si une compétence existe en double, on garde le poids le plus fort
                    if key_name not in skills_db or skill.weight > skills_db[key_name]:
                        skills_db[key_name] = skill.weight
                    
                    if skill.is_critical:
                        critical_skills_set.add(key_name)

                # ---------------------------------------------------------
                # PARTIE ANALYSE : Comparaison Texte vs BDD
                # ---------------------------------------------------------
                for skill_name, weight in skills_db.items():
                    # Si le mot-clé est dans le texte
                    if skill_name in text_content:
                        score += weight
                        detected_skills_list.append(f"{skill_name.title()} (+{weight} pts)")
                    elif skill_name in critical_skills_set:
                        missing_skills_list.append(skill_name.title())
                    
                    # On calcule le dénominateur (Score Max) basé sur les compétences critiques 
                    # ET les compétences trouvées (pour éviter de pénaliser sur des skills non pertinentes)
                    if skill_name in critical_skills_set or skill_name in text_content:
                        total_possible_score += weight

                # Normalisation du score
                if total_possible_score > 0:
                    # Formule : (Score Obtenu / Score Possible) * 70 + Bonus
                    base_score = min(70, (score / total_possible_score) * 70)
                    bonus_score = min(30, len(detected_skills_list) * 2)
                    score = int(base_score + bonus_score)
                else:
                    score = min(100, score) # Cas simple si pas de config complexe

                # Détection niveau expérience
                record.ai_experience_level = self._detect_experience_level(text_content)

                # Formatage du texte pour l'affichage
                if detected_skills_list:
                    record.ai_detected_skills = "✅ " + "\n✅ ".join(detected_skills_list)
                else:
                    record.ai_detected_skills = "Aucune compétence technique détectée."
                
                if missing_skills_list:
                    record.ai_missing_skills = "⚠️ " + "\n⚠️ ".join(missing_skills_list)
                else:
                    record.ai_missing_skills = "Aucune compétence critique manquante."

            else:
                # Cas où il n'y a pas de notes
                score = 0
                record.ai_detected_skills = "⚠️ Veuillez remplir les 'Notes Internes' pour lancer l'analyse."
                record.ai_missing_skills = ""

            # Assignation finale
            record.ai_score = min(100, score)

            # Verdict
            if score < 30:
                record.ai_verdict = 'low'
            elif score < 70:
                record.ai_verdict = 'medium'
            else:
                record.ai_verdict = 'high'
            
            record.ai_analysis_date = fields.Datetime.now()

    # --- Bouton d'Analyse Manuelle ---
    def action_analyze_profile(self):
        """ Force le recalcul """
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