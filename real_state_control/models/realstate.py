from odoo import api, fields, models


class RealState(models.Model):
    _name = 'real.state'
    _description = 'Real State Control'

    type_property = fields.Selection([
        ('casa', 'Casa'),
        ('apto', 'Apartamento'),
    ],      string='Tipo da propriedade',
            required=True)
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