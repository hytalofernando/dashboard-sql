#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico de Conexão
Adicione isto temporariamente ao início do main.py para ver o que está acontecendo
"""

import os

print("\n" + "="*70)
print("DIAGNÓSTICO DE CONEXÃO")
print("="*70)

# Verifica variáveis de ambiente
print("\n1. Variáveis de Ambiente:")
print(f"   DATABASE_URL definida? {bool(os.environ.get('DATABASE_URL'))}")
print(f"   SQLITE_PATH definida? {bool(os.environ.get('SQLITE_PATH'))}")

# Verifica Streamlit secrets
print("\n2. Streamlit Secrets:")
try:
    import streamlit as st
    try:
        db_url = st.secrets.get("DATABASE_URL", None)
        if db_url:
            # Mascara a senha
            if "@" in db_url:
                parts = db_url.split("@")
                user_pass = parts[0].split("://")[1]
                if ":" in user_pass:
                    user = user_pass.split(":")[0]
                    masked = f"postgresql+psycopg2://{user}:***@{parts[1]}"
                else:
                    masked = f"{parts[0]}:***@{parts[1]}"
            else:
                masked = "***"
            print(f"   DATABASE_URL: {masked}")
        else:
            print(f"   DATABASE_URL: NÃO ENCONTRADA")
            
        sqlite_path = st.secrets.get("SQLITE_PATH", None)
        print(f"   SQLITE_PATH: {sqlite_path if sqlite_path else 'NÃO ENCONTRADA'}")
        
    except Exception as e:
        print(f"   Erro ao ler secrets: {str(e)}")
except ImportError:
    print("   Streamlit não disponível")

# Testa conexão
print("\n3. Teste de Conexão:")
try:
    from database import DATABASE_URL, engine
    from sqlalchemy import text
    
    print(f"   URL final (mascarada): {DATABASE_URL.split('@')[0][:30]}***" if "@" in DATABASE_URL else DATABASE_URL[:50])
    
    with engine.connect() as conn:
        if DATABASE_URL.startswith("postgresql"):
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"   ✅ PostgreSQL: {version[:60]}...")
        else:
            print(f"   ✅ SQLite: Conectado")
            
except Exception as e:
    print(f"   ❌ ERRO: {str(e)}")
    print(f"   Tipo: {type(e).__name__}")

print("\n" + "="*70)
print("FIM DO DIAGNÓSTICO")
print("="*70 + "\n")

