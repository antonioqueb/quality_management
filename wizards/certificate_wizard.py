from odoo import models, fields, api, _


class QualityCertificateWizard(models.TransientModel):
    _name = 'quality.certificate.wizard'
    _description = 'Asistente para Crear Certificado'

    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección',
        required=True, readonly=True
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True
    )
    inspection_type = fields.Selection(
        related='inspection_id.inspection_type'
    )
    # Checkboxes para seleccionar qué atributos incluir
    include_largo = fields.Boolean('Incluir Largo', default=True)
    include_ancho = fields.Boolean('Incluir Ancho', default=True)
    include_espesor = fields.Boolean('Incluir Espesor', default=True)
    include_hexagono = fields.Boolean('Incluir Hexágono', default=True)
    include_resistencia = fields.Boolean('Incluir Resistencia', default=True)
    include_apariencia = fields.Boolean('Incluir Apariencia')
    include_humedad = fields.Boolean('Incluir % Humedad')
    include_pegado = fields.Boolean('Incluir Pegado')
    include_retiramiento = fields.Boolean('Incluir Retiramiento')
    include_calibracion = fields.Boolean('Incluir Calibración')
    include_engomado = fields.Boolean('Incluir Engomado')

    def action_create_certificate(self):
        self.ensure_one()
        insp = self.inspection_id
        vals = {
            'inspection_id': insp.id,
            'partner_id': self.partner_id.id,
            'certified_by': self.env.user.id,
        }
        # Poblar valores según tipo y selección
        if insp.inspection_type == 'laminadora_remanejo':
            if self.include_largo:
                vals['certified_largo'] = insp.largo
            if self.include_ancho:
                vals['certified_ancho'] = insp.ancho
            if self.include_espesor:
                vals['certified_espesor'] = insp.espesor
            if self.include_hexagono:
                vals['certified_hexagono'] = insp.hexagono
            if self.include_resistencia:
                vals['certified_resistencia'] = insp.resistencia
            if self.include_apariencia:
                vals['certified_apariencia'] = dict(
                    insp._fields['apariencia'].selection
                ).get(insp.apariencia, '')
            if self.include_humedad:
                vals['certified_humedad'] = insp.humedad_pct
            if self.include_pegado:
                vals['certified_pegado'] = dict(
                    insp._fields['pegado_result'].selection
                ).get(insp.pegado_result, '')
        elif insp.inspection_type == 'octagono':
            if self.include_ancho:
                vals['certified_ancho'] = insp.oct_ancho
            if self.include_espesor:
                vals['certified_espesor'] = insp.oct_espesor
            if self.include_hexagono:
                vals['certified_hexagono'] = insp.oct_hexagono
            if self.include_retiramiento:
                vals['certified_retiramiento'] = insp.oct_retiramiento
            if self.include_pegado:
                vals['certified_pegado'] = dict(
                    insp._fields['oct_pegado'].selection
                ).get(insp.oct_pegado, '')
        elif insp.inspection_type == 'guillotina_pegado':
            if self.include_calibracion:
                vals['certified_calibracion'] = insp.calibracion
            if self.include_engomado:
                vals['certified_engomado'] = dict(
                    insp._fields['engomado'].selection
                ).get(insp.engomado, '')

        cert = self.env['quality.certificate'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificado'),
            'res_model': 'quality.certificate',
            'res_id': cert.id,
            'view_mode': 'form',
            'target': 'current',
        }
