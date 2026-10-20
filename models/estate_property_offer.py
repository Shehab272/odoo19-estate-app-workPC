from odoo import models, fields, api
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):

     _name = 'estate.property.offer'
     _description = 'Estate Property Offer'

     price = fields.Float(string='Price')
     status = fields.Selection([
          ('accepted','Accepted'),
          ('refused','Refused')
     ],string='Status',copy=False)

     partner_id = fields.Many2one('res.partner',string='Partner',required=True)
     property_id = fields.Many2one('estate.property',string='Property',required=True)

     validity = fields.Integer(string='Validity',required=True,Default=7,store=True)
     date_deadline = fields.Date(string='Date of Deadline',required=True,
                                 compute='_compute_date_deadline',
                                 inverse='_inverse_date_deadline',
                                 store=True)

     @api.depends('create_date','validity')
     def _compute_date_deadline(self):
          for record in self:
               start_date = record.create_date.date() if record.create_date else fields.Date.today()
               record.date_deadline = start_date + timedelta(days=record.validity)

     def _inverse_date_deadline(self):
          for record in self:
               start_date = record.create_date.date() if record.create_date else fields.Date.today()
               if record.date_deadline:
                    delta = record.date_deadline - start_date
                    record.validity = delta.days