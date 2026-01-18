# Fichier: smart_recruiter_ai/models/job_profile.py
from odoo import models, fields, api

class JobProfile(models.Model):
    _name = 'smart.recruiter.job.profile'
    _description = 'Profils de Poste pour Smart Recruiter AI'
    _order = 'name'

    name = fields.Char(
        string="Nom du Profil",
        required=True,
        help="Ex: Développeur Python, Commercial Senior, Chef de Projet"
    )

    description = fields.Text(
        string="Description",
        help="Description détaillée du profil de poste"
    )

    active = fields.Boolean(
        string="Actif",
        default=True
    )

    skill_ids = fields.One2many(
        'smart.recruiter.skill',
        'profile_id',
        string="Compétences Requises"
    )

    min_score_threshold = fields.Integer(
        string="Score Minimum Requis (%)",
        default=50,
        help="Score minimum pour considérer un candidat comme pertinent"
    )

    priority = fields.Selection(
        [
            ('low', 'Basse'),
            ('medium', 'Moyenne'),
            ('high', 'Haute'),
            ('urgent', 'Urgente'),
        ],
        string="Priorité",
        default='medium'
    )

    color = fields.Integer(string='Color Index', default=0)


class JobProfileSkill(models.Model):
    _name = 'smart.recruiter.skill'
    _description = 'Compétences pour Profils de Poste'
    _order = 'weight desc, name'

    name = fields.Char(
        string="Compétence",
        required=True,
        help="Ex: Python, Java, Gestion de projet"
    )

    weight = fields.Integer(
        string="Pondération",
        default=10,
        help="Importance de la compétence (0-20 points)"
    )

    profile_id = fields.Many2one(
        'smart.recruiter.job.profile',
        string="Profil de Poste",
        required=True,
        ondelete='cascade'
    )

    is_critical = fields.Boolean(
        string="Compétence Critique",
        default=False,
        help="Si coché, cette compétence est obligatoire pour le poste"
    )

    skill_type = fields.Selection(
        [
            ('technical', 'Technique'),
            ('soft', 'Soft Skill'),
            ('language', 'Langue'),
            ('certification', 'Certification'),
        ],
        string="Type de Compétence",
        default='technical'
    )
