from odoo import api, fields, models, _


class RealState(models.Model):
    _name = 'real.state'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'real.state.line']
    _description = 'Real State Control'
    _rec_name = 'type'

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    type = fields.Many2one('real.state.property', string="Tipo da propriedade", required=True)
    realstate_cep = fields.Char(string='Código postal',
                                required=True)
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
    realstate_line = fields.One2many('real.state.line', 'newtype', string='Pedidos')

    class RealStateLine(models.Model):
        _name = 'real.state.line'

        partner_id = fields.Many2one('res.partner', string='Parceiro', required=True)
        offer = fields.Float(string='Oferta', required=True)
        newtype = fields.Many2one('real.state.property', string="Tipo da propriedade")
