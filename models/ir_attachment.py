# -*- coding: utf-8 -*-
from odoo import models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    # FOLIO-QM-ODOO18-060: el check() de ir.attachment NO se controla con ACL ni
    # record rules: delega el permiso al registro padre (res_model/res_id). Por eso
    # un Responsable/Administrador de Calidad podía toparse con un error de
    # ir.attachment al abrir un adjunto cuyo registro padre estaba filtrado o sin
    # ACL. Aquí damos acceso TOTAL (lectura/escritura/creación/borrado) a todos los
    # adjuntos del módulo —los que cuelgan de un modelo 'quality.*'— sin exigir
    # acceso al registro padre. Para cualquier otro adjunto o usuario, el
    # comportamiento estándar de Odoo queda intacto.
    _QUALITY_MODEL_PREFIX = "quality."

    def _is_quality_full_access_user(self):
        # Responsable implica Inspector/Usuario; Administrador implica Responsable.
        return self.env.user.has_group("quality_management.group_quality_manager")

    def check(self, mode, values=None):
        # Superusuario o usuarios sin el grupo: comportamiento estándar.
        if self.env.su or not self._is_quality_full_access_user():
            return super().check(mode, values=values)

        prefix = self._QUALITY_MODEL_PREFIX

        # Creación: el res_model viaja en values (self normalmente está vacío).
        if values is not None and (values.get("res_model") or "").startswith(prefix):
            values = None  # no exigir acceso al registro padre del módulo

        # Adjuntos existentes: excluimos del check estándar los que pertenecen al
        # módulo. Leemos res_model con sudo para no re-disparar check() (recursión).
        remaining = self
        if self:
            res_models = {
                rec["id"]: (rec["res_model"] or "")
                for rec in self.sudo().read(["res_model"])
            }
            remaining = self.filtered(
                lambda att: not res_models.get(att.id, "").startswith(prefix)
            )

        if remaining or values is not None:
            return super(IrAttachment, remaining).check(mode, values=values)
        return None
