from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
     _name = 'estate.property'
     _description = 'Real Estate Property'

     name = fields.Char(string='Name', required=1)
     description = fields.Text(string='Description')
     postcode = fields.Char(string='Postcode',required=1)
     date_availability = fields.Date(string='Date Availability',copy=False,default=lambda self: fields.Date.today()+relativedelta(months=+3))
     expected_price = fields.Float(string='Expected Price',required=True)
     selling_price = fields.Float(string='Selling Price',copy=False,readonly=True)
     bedrooms = fields.Integer(string='Bedrooms',default=2)
     living_area = fields.Integer(string='Living Area')
     # facades => واجهات العقار
     facades = fields.Integer(string='Facades')
     garage = fields.Boolean(string='Garage')
     garden = fields.Boolean(string='Garden')
     garden_area =fields.Integer(string='Garden Area')
     garden_orientation = fields.Selection(
          [
               ('north', 'North'),
               ('south', 'South'),
               ('east', 'East'),
               ('west', 'West')
          ],
          string='Garden Orientation'
     )
     #chapter5
     state = fields.Selection(
          [
               ('offer', 'Offer'),
               ('offer_received', 'Offer Received'),
               ('new', 'New'),
               ('canceled', 'Canceled'),
               ('sold', 'Sold'),
               ('accepted', 'Accepted')
          ],
          string='Status',
          required=True,
          copy=False,
          default='new',
     )
     active = fields.Boolean(string='Active',default=True)

     total_area = fields.Integer(string='Total Area',compute='_compute_total_area')

     property_type_id = fields.Many2one('estate.property.type',string='Property Type')

     buyer_id = fields.Many2one('res.partner',string='Buyer',copy=False)
     salesperson_id = fields.Many2one('res.users',string='Salesperson',default=lambda self: self.env.user)
     tag_ids = fields.Many2many('estate.property.tag',string='Tags')
     offer_ids = fields.One2many('estate.property.offer','property_id',string='Offers')

     best_price = fields.Float(string='Best Price',compute='_compute_best_price')

     @api.constrains('facades')
     def check_facades(self):
          for record in self:
               if record.facades == 0 :
                    raise ValidationError('Facades cannot be zero')

     @api.depends('living_area','garden_area')
     def _compute_total_area(self):
          for record in self:
               record.total_area = record.living_area + record.garden_area

     @api.depends('offer_ids.price')
     def _compute_best_price(self):
          for record in self:
               prices = record.offer_ids.mapped('price')
               record.best_price = max(prices) if prices else 0.0

     @api.onchange('garden')
     def _compute_garden(self):
          if self.garden == True:
               self.garden_area = 10
               self.garden_orientation = 'north'
          else:
               self.garden_area = 0
               self.garden_orientation = False

     def action_sold(self):
          for record in self:
               if record.state == 'canceled':
                    raise UserError("A canceled property cannot be set as sold.")
               record.state = 'sold'
          return True

     def action_cancel(self):
          for record in self:
               if record.state == 'sold':
                    raise UserError("A sold property cannot be canceled.")
               record.state = 'canceled'
          return True

     _check_expected_price = models.Constraint(
          'CHECK(expected_price > 0)',
          'Expected price must be strictly positive.',
     )

     _check_selling_price = models.Constraint(
          'CHECK(selling_price >= 0)',
          'Selling Price must be strictly positive.',
     )

     @api.constrains('selling_price', 'expected_price')
     def _check_price(self):
          for record in self:
               if float_is_zero(record.selling_price, precision_digits=2):
                    continue

               minimum_allowed_price = record.expected_price * 0.9

               if float_compare(record.selling_price, minimum_allowed_price, precision_digits=2) < 0:
                    raise ValidationError(
                         "The selling price cannot be lower than 90% of the expected price! "
                         "You must reduce the expected price if you want to accept this offer."
                    )

     _order = "id desc"