# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        _logger.info(vals)
        product_id = self.env['product.product'].browse(vals.get('product_id'))
        if product_id.pack_ok:
            res = self.env['stock.move']
            pack_lines = product_id.get_pack_lines()
            for pack_line in pack_lines:
                new_vals = vals.copy()
                new_vals['product_id'] = pack_line['product_id']
                new_vals.update({
                    'product_id': pack_line.product_id.id,
                    'product_uom_qty': pack_line.quantity * vals['product_uom_qty']
                })
                res += self.create(new_vals)
            return res

            #raise UserError('product is in pack')
        else:
            return super(StockMove, self).create(vals)

