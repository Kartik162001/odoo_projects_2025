from odoo import models, fields, api

class WaterJugLine(models.Model):
    _name = 'water.jug.line'
    _description = 'Water Jug Line'

    delivery_id = fields.Many2one('delivery', string='Delivery')
    product_name = fields.Char(string='Product', default='Jug', readonly=True)
    quantity = fields.Integer(string='Quantity', required=True)
    unit_price = fields.Float(string='Price', required=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total', store=True)
    line_date = fields.Date(string='Delivery Date', required=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total(self):
        for line in self:
            line.total_amount = line.quantity * line.unit_price
