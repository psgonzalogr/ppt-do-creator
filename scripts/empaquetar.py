#!/usr/bin/env python3
"""Crea ppt-do-creator.zip listo para subir como skill a Claude (Ajustes → Capacidades → Skills).

Uso:  python3 scripts/empaquetar.py
Deja el ZIP en la carpeta del repositorio. Excluye .git, carpetas «salida» y capturas.
"""
import os, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, 'ppt-do-creator.zip')
EXCLUIR = {'.git', 'salida', '__pycache__'}

with zipfile.ZipFile(DESTINO, 'w', zipfile.ZIP_DEFLATED) as z:
    for carpeta, dirs, archivos in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in EXCLUIR and not d.endswith('_capturas')]
        for n in archivos:
            if n.endswith('.zip'):
                continue
            ruta = os.path.join(carpeta, n)
            z.write(ruta, os.path.join('ppt-do-creator', os.path.relpath(ruta, RAIZ)))
print('Listo:', DESTINO, f'({os.path.getsize(DESTINO) // 1024} KB)')
