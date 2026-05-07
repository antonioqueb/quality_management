#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_troquel_smart_buttons.py
============================
Corrige el error de Odoo 18:
    "el campo 'active_id' no existe en el modelo 'quality.troquel'"

en views/quality_troquel_validation_views.xml.

Cambios:
  1. active_id  →  id   (en context de smart buttons)
  2. Agrega groups="quality_management.group_quality_manager" a los
     smart buttons y botones de acción para evitar inconsistencia
     de permisos.
  3. Valida XML después de parchar.
  4. Idempotente: re-ejecutarlo no rompe nada.

Uso:
    python3 fix_troquel_smart_buttons.py .
    python3 fix_troquel_smart_buttons.py /ruta/a/quality_management
"""
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 fix_troquel_smart_buttons.py <ruta_modulo>")
        sys.exit(1)

    module_root = Path(sys.argv[1]).resolve()
    target = module_root / "views" / "quality_troquel_validation_views.xml"

    if not target.exists():
        print(f"✗ ERROR: no encuentro {target}")
        sys.exit(1)

    print(f">>> Parchando: {target}")

    original = target.read_text(encoding="utf-8")
    text = original
    changes = []

    # 1) active_id → id
    pattern_active = re.compile(
        r"context=\"\{'search_default_troquel_id':\s*active_id\}\""
    )
    n = len(pattern_active.findall(text))
    if n:
        text = pattern_active.sub(
            "context=\"{'search_default_troquel_id': id}\"",
            text,
        )
        changes.append(f"active_id → id ({n} ocurrencias)")

    # 2) groups en smart buttons (oe_stat_button)
    smart_btn_re = re.compile(
        r"(<button\b[^>]*?\btype=\"action\"[^>]*?\bclass=\"oe_stat_button\"[^>]*?)(/?>)",
        re.DOTALL,
    )
    matches_needing = [m for m in smart_btn_re.finditer(text)
                       if "groups=" not in m.group(1)]
    if matches_needing:
        def add_group_smart(m):
            head, close = m.group(1), m.group(2)
            if "groups=" in head:
                return m.group(0)
            return head + ' groups="quality_management.group_quality_manager"' + close
        text = smart_btn_re.sub(add_group_smart, text)
        changes.append(f"groups en smart buttons (+{len(matches_needing)})")

    # 3) groups en botones de acción del header (action_open_*)
    action_btn_re = re.compile(
        r"(<button\b[^>]*?\bname=\"action_open_(validation|repair)\"[^>]*?)(/?>)",
        re.DOTALL,
    )
    matches_needing2 = [m for m in action_btn_re.finditer(text)
                        if "groups=" not in m.group(1)]
    if matches_needing2:
        def add_group_action(m):
            head, _action, close = m.group(1), m.group(2), m.group(3)
            if "groups=" in head:
                return m.group(0)
            return head + ' groups="quality_management.group_quality_manager"' + close
        text = action_btn_re.sub(add_group_action, text)
        changes.append(f"groups en botones de acción (+{len(matches_needing2)})")

    # ¿hubo cambios?
    if text == original:
        print("✓ Nada que parchar — ya estaba al día.")
        sys.exit(0)

    # validar XML
    try:
        ET.fromstring(text)
    except ET.ParseError as e:
        print(f"✗ ERROR: el XML resultante no es válido: {e}")
        print("  No se escribió ningún cambio.")
        sys.exit(2)

    # backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = target.with_suffix(f".xml.bak_{timestamp}")
    shutil.copy2(target, backup)
    target.write_text(text, encoding="utf-8")

    print()
    print("✓ Cambios aplicados:")
    for c in changes:
        print(f"   - {c}")
    print(f"\n✓ Backup: {backup}")
    print("\nSiguiente paso:")
    print("  docker compose exec odoo odoo -u quality_management -d <tu_db> --stop-after-init")


if __name__ == "__main__":
    main()