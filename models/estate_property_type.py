from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError

class EstatePropertyType(models.Model):
     _name = 'estate.property.type'
     _description = 'Real Estate Property Type'

     name = fields.Char(string='Name', required=True)