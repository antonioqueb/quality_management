# -*- coding: utf-8 -*-
"""
Integración con project.task — bloqueos al mover tarjetas en Kanban.
Cubre los requerimientos de Muestras & Prototipos y Altas & Actualizaciones
de Planos que nacen desde Proyectos.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTaskQuality(models.Model):
    _inherit = "project.task"

    quality_sample_release_id = fields.Many2one(
        "quality.sample.release", "Liberación de Muestra",
        help="Vinculación con la liberación de muestra de Calidad.")
    quality_drawing_release_id = fields.Many2one(
        "quality.drawing.release", "Liberación de Plano")

    quality_required_for_progress = fields.Boolean(
        "Requiere Liberación de Calidad",
        help="Si está activo, no se puede mover la tarjeta a etapas avanzadas "
             "sin liberación aprobada de Calidad.")
    quality_block_reason = fields.Char(
        "Motivo de Bloqueo de Etapa",
        compute="_compute_quality_block_reason")

    @api.depends("quality_sample_release_id.state",
                 "quality_drawing_release_id.state",
                 "quality_required_for_progress")
    def _compute_quality_block_reason(self):
        for task in self:
            reasons = []
            if task.quality_required_for_progress:
                if (task.quality_sample_release_id
                        and task.quality_sample_release_id.state != "aceptado"):
                    reasons.append(_("Muestra no liberada por Calidad"))
                if (task.quality_drawing_release_id
                        and task.quality_drawing_release_id.state != "aceptado_diseno"):
                    reasons.append(_("Plano no liberado (Calidad/Ventas/Diseño)"))
            task.quality_block_reason = "; ".join(reasons) if reasons else False

    def _quality_validate_stage_move(self, new_stage_id):
        """Llamada desde write() cuando cambia stage_id."""
        for task in self:
            if not task.quality_required_for_progress:
                continue

            new_stage = self.env["project.task.type"].browse(new_stage_id)
            # Permite regresar a etapas anteriores; bloquea solo avance.
            if task.stage_id and new_stage.sequence <= task.stage_id.sequence:
                continue

            sample = task.quality_sample_release_id
            drawing = task.quality_drawing_release_id

            if sample:
                if not sample.spec_pdf:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "no tiene Especificación PDF cargada."
                    ) % (task.name, sample.name))
                if not sample.inspection_line_ids:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "no tiene atributos de inspección capturados."
                    ) % (task.name, sample.name))
                if sample.state != "aceptado":
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "está en estado '%s' (debe estar Aceptada)."
                    ) % (task.name, sample.name,
                         dict(sample._fields["state"].selection).get(sample.state)))

            if drawing:
                if not drawing.drawing_pdf or not drawing.quotation_pdf:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': el plano '%s' "
                        "requiere AMBOS documentos (Plano + Cotización/Dibujo)."
                    ) % (task.name, drawing.name))
                if drawing.state != "aceptado_diseno":
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': el plano '%s' "
                        "no ha completado el triple-check (Calidad/Ventas/Diseño). "
                        "Estado actual: '%s'."
                    ) % (task.name, drawing.name,
                         dict(drawing._fields["state"].selection).get(drawing.state)))

    def write(self, vals):
        if "stage_id" in vals and vals["stage_id"]:
            self._quality_validate_stage_move(vals["stage_id"])
        return super().write(vals)


class QualitySampleReleaseTask(models.Model):
    _inherit = "quality.sample.release"

    project_task_ids = fields.One2many(
        "project.task", "quality_sample_release_id",
        string="Tareas Vinculadas")


class QualityDrawingReleaseTask(models.Model):
    _inherit = "quality.drawing.release"

    project_task_ids = fields.One2many(
        "project.task", "quality_drawing_release_id",
        string="Tareas Vinculadas")
