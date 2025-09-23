# --- Persistência de dados com SQLite

import sqlite3
import json
from typing import Optional
from datetime import datetime

DB_PATH = 'nfc_e.db'

def init_db():
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS notas (
			chave TEXT PRIMARY KEY,
			dados TEXT NOT NULL
		)
	''')
	conn.commit()
	conn.close()

def _json_default(obj):
	if isinstance(obj, datetime):
		return obj.isoformat()
	raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def salvar_nota(chave: str, dados: dict):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('REPLACE INTO notas (chave, dados) VALUES (?, ?)', (chave, json.dumps(dados, default=_json_default)))
	conn.commit()
	conn.close()

def buscar_nota(chave: str) -> Optional[dict]:
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('SELECT dados FROM notas WHERE chave = ?', (chave,))
	row = c.fetchone()
	conn.close()
	if row:
		return json.loads(row[0])
	return None

def deletar_nota(chave: str):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('DELETE FROM notas WHERE chave = ?', (chave,))
	conn.commit()
	conn.close()

def listar_notas():
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute('SELECT chave, dados FROM notas')
	rows = c.fetchall()
	conn.close()
	return [{"chave": chave, "dados": json.loads(dados)} for chave, dados in rows]

# Inicializa o banco ao importar
init_db()