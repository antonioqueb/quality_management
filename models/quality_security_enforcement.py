# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import AccessError


class MrpProductionQualitySecurity(models.Model):
    _inherit = "mrp.production"

    @api.model_create_multi
    def create(self, vals_list):
        # FOLIO-QM-ODOO18-029: las reglas ir.rule no niegan create/write;
        # se agrega enforcement explícito para que inspectores no creen OP.
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede crear órdenes de producción."))
        return super().create(vals_list)

    def write(self, vals):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede modificar órdenes de producción."))
        return super().write(vals)

    def unlink(self):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede eliminar órdenes de producción."))
        return super().unlink()


class StockLotQualitySecurity(models.Model):
    _inherit = "stock.lot"

    @api.model_create_multi
    def create(self, vals_list):
        # FOLIO-QM-ODOO18-029: las reglas ir.rule no niegan create/write;
        # se agrega enforcement explícito para que inspectores no creen lotes.
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede crear lotes."))
        return super().create(vals_list)

    def write(self, vals):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede modificar lotes."))
        return super().write(vals)

    def unlink(self):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede eliminar lotes."))
        return super().unlink()