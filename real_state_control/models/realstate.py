from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RealState(models.Model):
    _name = 'real.state'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Real State Control'
    _rec_name = 'reference'

    reference = fields.Char(string='Referência', required=True, copy=False)
    type = fields.Many2one('real.state.property', string="Tipo da propriedade", required=True)
    realstate_cep = fields.Char(string='Código postal', required=True)
    date_when = fields.Date(string='Disponível desde')
    expected_price = fields.Float(string='Expectativa de preço', required=True)
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
    user_id = fields.Many2one('res.users', string='Vendedor', readonly=True, default=lambda self: self.env.user)
    buyer_name = fields.Char(string='Nome do Comprador', store=True)
    buyer_id = fields.Many2one('res.partner', string='Comprador', readonly=True)
    invoice_id = fields.Many2one('account.move', string='Fatura', readonly=True)
    state = fields.Selection([
        ('draft', 'Provisório'),
        ('sale', 'Vendido'),
    ], string='Status', default='draft', track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', string='Parceiro')
    currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=True,
                                  string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('realstate_line.offer')
    def _compute_best_offer(self):
        for record in self:
            offers = record.realstate_line.mapped('offer')
            record.best_offer = max(offers) if offers else 0.0

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError(_('Insira uma expectativa de preço válida'))

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
            self.buyer_id = accepted_offer[0].partner_id
        self.state = 'sale'
        for record in self:
            accepted_offer = record.realstate_line.filtered(lambda line: line.state == 'accepted')
            if not accepted_offer:
                raise ValidationError("Você não pode vendar um imóvel sem uma oferta")
            record.selling_price = accepted_offer[0].offer
            record.buyer_id = accepted_offer[0].partner_id
            record.state = 'sale'

    def action_cancel(self):
        self.state = 'draft'

    def action_create_invoice(self):
        vals = {
            'currency_id': self.currency_id
        }
        for record in self:
            delivey_invoice = self.env['account.move'].create([
                {
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.context_today(record),
                    'partner_id': record.buyer_id.id,
                    'currency_id': record.currency_id.id,
                    'amount_total': self.selling_price,
                    'invoice_line_ids': [
                        (0, None, {
                            'product_id': 1,
                            'name': record.description,
                            'quantity': 1,
                            'price_unit': record.selling_price,
                            'price_subtotal': record.selling_price,
                        }),
                    ],
                },
            ])
            delivey_invoice.action_post()
            return {
                'type': 'ir.actions.act_window',
                'name': 'Fatura',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': delivey_invoice.id,
            }




class RealStateLine(models.Model):
    _name = 'real.state.line'

    partner_id = fields.Many2one('res.partner', string='Parceiro', required=True)
    realstate_id = fields.Many2one('real.state', string='Propriedade')
    offer = fields.Float(string='Oferta')
    state = fields.Selection([
        ('accepted', 'Aceito'),
        ('denied', 'Negado'),
    ], string='Status', track_visibility='onchange')

    @api.constrains('offer')
    def _check_expected_price(self):
        for record in self:
            if record.offer < 0:
                raise ValidationError(_('Insira uma expectativa de preço válida'))

    @api.constrains('state')
    def _check_unique_accepted_state(self):
        for line in self:
            if line.state == 'accepted':
                lines = self.search(
                    [('realstate_id', '=', line.realstate_id.id), ('state', '=', 'accepted'), ('id', '!=', line.id)])
                if lines:
                    raise ValidationError('Apenas uma oferta pode estar selecionada como aceita no registro')

    @api.onchange('state')
    def _onchange_state(self):
        if self.realstate_id.state == 'sale' and self.state != 'accepted':
            raise ValidationError("Não é possível modificar as ofertas caso a propriedade esteja vendida.")

    @api.constrains('state')
    def _check_real_state_sold(self):
        for line in self:
            if line.realstate_id.state == 'sale' and line.state != 'accepted':
                raise ValidationError("Não é possível modificar as ofertas caso a propriedade esteja vendida.")