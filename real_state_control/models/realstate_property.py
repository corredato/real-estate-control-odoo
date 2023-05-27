from odoo import api, fields, models, _


class RealStateProperty(models.Model):
    _name = 'real.state.property'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Propriedades"

    reference = fields.Char(string='Pedido', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Tipo da propriedade')
    type = fields.Char(string='Tipo da propriedade')
    realstate_cep = fields.Char(string='Código postal')
    date_when = fields.Date(string='Disponível desde')
    expected_price = fields.Float(string='Expectativa de preço')
    best_offer = fields.Float(string='Melhor oferta')
    selling_price = fields.Float(string='Preço de venda')
    description = fields.Text('Descrição')
    bedrooms = fields.Integer(string='Quartos')
    living_area = fields.Integer(string='Sala de estar (m²)')
    facade = fields.Integer(string='Fachada')
    garage = fields.Boolean(string='Garagem')
    garden = fields.Boolean(string='Quintal')
    total_area = fields.Integer(string='Área total (m²)')
    realstate_line = fields.One2many('real.state.line', 'type', string='Pedidos')