from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError

class EstatePropertyType(models.Model):
     _name = 'estate.property.type'
     _description = 'Real Estate Property Type'

     name = fields.Char(string='Name', required=True)

     property_ids = fields.One2many('estate.property', "property_type_id", string="Properties")

     _check_name = models.Constraint(
          'UNIQUE(name)',
          'A property type name must be unique.',
     )

     _order = "sequence,name"

     sequence = fields.Integer(string='Sequence', default=1)