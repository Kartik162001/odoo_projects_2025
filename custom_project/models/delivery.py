from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
import re
import urllib.parse


class delivery(models.Model):
    _name = 'delivery'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one('res.partner',string='Customer', required=True)
    customer_address = fields.Text(string="Customer Address", compute = '_onchange_partner_id')
    date = fields.Date(string='Order Date', default=fields.Date.today)
    pieces = fields.Integer(string='Pieces')
    price = fields.Float(string='Price')
    state = fields.Selection([('draft','Draft'),('done','Done'), ('one_month', 'One Month')],string='State')
    line_ids = fields.One2many('water.jug.line', 'delivery_id', string='Delivery Lines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)

    def action_state(self):
        if self.state == 'draft':
            self.state = 'draft'

    @api.onchange('pieces','price')
    def _onchange_pieces(self):
        if self.pieces:
            # Create a new line in One2many
            self.line_ids = [(0, 0, {
                'product_name': 'jug',  # fixed jug product
                'quantity': self.pieces,
                'unit_price': self.price,
                'total_amount': self.pieces * 50,
                'line_date': date.today()
            })]

    @api.depends('line_ids.total_amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.total_amount for line in record.line_ids)

    @api.depends('customer_id')
    def _onchange_partner_id(self):
        """Automatically fill address using switch-case style."""
        match bool(self.customer_id):
            case True:
                # Build address components
                address_parts = [
                    self.customer_id.street or '',
                    self.customer_id.city or '',
                    self.customer_id.zip or '',
                    self.customer_id.country_id.name or '',
                ]
                address_line = ', '.join(filter(None, address_parts))

                # Switch-case for phone existence
                match bool(self.customer_id.phone):
                    case True:
                        self.customer_address = f"{address_line}\nPhone: {self.customer_id.phone}"
                    case False:
                        self.customer_address = address_line
            case False:
                self.customer_address = False

    def action_send_whatsapp(self):
        self.ensure_one()

        # Make sure customer and phone exist
        if not self.customer_id or not self.customer_id.phone:
            raise ValidationError("Please enter a valid customer phone number.")

        # Build message directly
        customer_name = self.customer_id.name or "Customer"
        address = self.customer_address or "Address not available"
        order_date = self.date or "N/A"
        total = self.total_amount or 0.0

        message = (
            f"Hello {customer_name},\n\n"
            f"We are confirming your delivery:\n\n"
            f"Address:\n{address}\n"
            f"Order Date: {order_date}\n"
            f"Total Amount: {total}\n\n"
            "Thank you for your order!"
        )

        # URL encode message
        whatsapp_message = urllib.parse.quote(message)

        # Construct WhatsApp URL
        whatsapp_url = f"https://api.whatsapp.com/send?phone={self.customer_id.phone}&text={whatsapp_message}"

        # Open WhatsApp link
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new',
        }

    def action_done(self):
        self.state = 'done'