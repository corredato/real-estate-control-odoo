from odoo import api, fields, models, _


class RealStateProperty(models.Model):
    _name = 'real.state.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
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
    realstate_line = fields.One2many('real.state.line', 'realstate_id', string='Pedidos')
    user_id = fields.Many2one('res.users', string='Vendedor', readonly=True, default=lambda self: self.env.user)
    buyer_name = fields.Char(string='Nome do Comprador', compute='_compute_buyer_name', store=True)
    state = fields.Selection([
        ('draft', 'Provisório'),
        ('sale', 'Vendido'),
    ], string='Status', default='draft')

    @api.depends('realstate_line.partner_id', 'realstate_line.state')
    def _compute_buyer_name(self):
        for record in self:
            accepted_line = record.realstate_line.filtered(lambda line: line.state == 'accepted')
            if accepted_line:
                record.buyer_name = accepted_line[0].partner_id.name
            else:
                record.buyer_name = False