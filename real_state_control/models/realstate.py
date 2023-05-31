from odoo import api, fields, models, _


class RealState(models.Model):
    _name = 'real.state'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Real State Control'
    _rec_name = 'reference'

    reference = fields.Char(string='Referência', required=True, copy=False)
    type = fields.Many2one('real.state.property', string="Tipo da propriedade", required=True)
    realstate_cep = fields.Char(string='Código postal', required=True)
    date_when = fields.Date(string='Disponível desde')
    expected_price = fields.Float(string='Expectativa de preço')
    best_offer = fields.Float(string='Melhor oferta', readonly=True, compute='_compute_best_offer')
    selling_price = fields.Float(string='Preço de venda', readonly=True)
    description = fields.Text(string='Descrição')
    bedrooms = fields.Integer(string='Quartos')
    living_area = fields.Integer(string='Sala de estar (m²)')
    facade = fields.Integer(string='Fachada')
    garage = fields.Boolean(string='Garagem')
    garden = fields.Boolean(string='Quintal')
    total_area = fields.Integer(string='Área total (m²)')
    realstate_line = fields.One2many('real.state.line', 'realstate_id', string='Pedidos')
    state = fields.Selection([
        ('draft', 'Provisório'),
        ('sale', 'Vendido'),
    ], string='Status', default='draft', track_visibility='onchange')

    @api.depends('realstate_line.offer')
    def _compute_best_offer(self):
        for record in self:
            offers = record.realstate_line.mapped('offer')
            record.best_offer = max(offers) if offers else 0.0

    def action_confirm(self):
        self.ensure_one()
        accepted_offer = self.realstate_line.filtered(lambda line: line.state == 'accepted' and line.offer)
        if accepted_offer:
            self.selling_price = accepted_offer[0].offer
        self.state = 'sale'

    def action_cancel(self):
        self.state = 'draft'


class RealStateLine(models.Model):
    _name = 'real.state.line'
    
    partner_id = fields.Many2one('res.partner', string='Parceiro')
    realstate_id = fields.Many2one('real.state', string='Propriedade')
    offer = fields.Float(string='Oferta')
    state = fields.Selection([
        ('accepted', 'Aceito'),
        ('denied', 'Negado'),
    ], string='Status', track_visibility='onchange')
