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

     ################### ^-^ #####################
     offer_ids = fields.One2many(
          "estate.property.offer",
          "property_type_id",
          string="Offers",
     )

     offer_count = fields.Integer(
          string="Offer Count",
          compute="_compute_offer_count",
     )

     @api.depends("offer_ids")
     def _compute_offer_count(self):
          for record in self:
               record.offer_count = len(record.offer_ids)