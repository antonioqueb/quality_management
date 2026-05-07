#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_customer_return_filter.py
=============================
Hotfix: hace que is_within_period sea stored para poder usarse como filtro
de búsqueda en quality.customer.return.

USO:
    python3 fix_customer_return_filter.py /ruta/a/quality_management
"""
import sys
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("Uso: python3 fix_customer_return_filter.py /ruta/a/quality_management")

MODULE = Path(sys.argv[1]).resolve()
target = MODULE / "models" / "quality_customer_return.py"

if not target.exists():
    sys.exit(f"❌ No se encontró {target}")

src = target.read_text(encoding="utf-8")

old = '''    days_since_production = fields.Integer(
        compute="_compute_days_since_production")
    is_within_period = fields.Boolean(
        compute="_compute_days_since_production")'''

new = '''    days_since_production = fields.Integer(
        compute="_compute_days_since_production", store=True)
    is_within_period = fields.Boolean(
        compute="_compute_days_since_production", store=True)'''

if old not in src:
    if "is_within_period" in src and "store=True" in src:
        print("ℹ  El archivo parece ya tener store=True. Nada que hacer.")
        sys.exit(0)
    sys.exit("❌ No se encontró el patrón a reemplazar. Edita manualmente "
             "models/quality_customer_return.py y agrega store=True a "
             "is_within_period y days_since_production.")

target.write_text(src.replace(old, new), encoding="utf-8")
print(f"✅ Patch aplicado a {target.relative_to(MODULE)}")
print()
print("Reinicia Odoo:")
print("    odoo-bin -d <db> -u quality_management --stop-after-init")