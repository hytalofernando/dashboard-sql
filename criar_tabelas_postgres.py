#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para Criar Tabelas no PostgreSQL
Executa localmente para testar e criar estrutura no banco remoto
"""

from sqlalchemy import create_engine, text
from models import Base
import bcrypt

# Connection string CORRETA com senha substituída
DATABASE_URL = "postgresql+psycopg2://postgres:hytalobb3030@db.kkfwxabdkdgrkxcselyg.supabase.co:5432/postgres"

print("\n" + "=" * 70)
print("CRIANDO TABELAS NO POSTGRESQL")
print("=" * 70)

try:
    # Cria engine
    print(f"\n1. Conectando ao banco...")
    print(f"   Host: db.kkfwxabdkdgrkxcselyg.supabase.co")
    engine = create_engine(DATABASE_URL, echo=False)
    
    # Testa conexão
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"   OK - PostgreSQL conectado!")
        print(f"   Versao: {version[:50]}...")
    
    # Cria todas as tabelas
    print(f"\n2. Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print(f"   OK - Tabelas criadas!")
    
    # Verifica tabelas criadas
    print(f"\n3. Verificando tabelas criadas...")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tabelas = result.fetchall()
        
        print(f"   Total de tabelas: {len(tabelas)}")
        for (tabela,) in tabelas:
            print(f"   - {tabela}")
    
    # Cria usuários padrão
    print(f"\n4. Criando usuarios padrao...")
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        from models import User
        
        # Verifica se usuários já existem
        admin_exists = session.query(User).filter(User.username == "admin").first()
        usuario_exists = session.query(User).filter(User.username == "usuario").first()
        
        if not admin_exists:
            admin_password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = User(username="admin", password_hash=admin_password_hash, role="admin")
            session.add(admin)
            print("   - Usuario 'admin' criado")
        else:
            print("   - Usuario 'admin' ja existe")
        
        if not usuario_exists:
            usuario_password_hash = bcrypt.hashpw("usuario123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            usuario = User(username="usuario", password_hash=usuario_password_hash, role="usuario")
            session.add(usuario)
            print("   - Usuario 'usuario' criado")
        else:
            print("   - Usuario 'usuario' ja existe")
        
        session.commit()
        print("   OK - Usuarios prontos!")
        
    except Exception as e:
        session.rollback()
        print(f"   Erro: {str(e)}")
    finally:
        session.close()
    
    # Verifica estrutura das tabelas
    print(f"\n5. Estrutura das tabelas:")
    print("-" * 70)
    
    with engine.connect() as conn:
        # Estrutura de users
        print("\nTabela: users")
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """))
        for col, tipo, nullable in result:
            print(f"   - {col:<20} {tipo:<15} Nullable: {nullable}")
        
        # Estrutura de equipments
        print("\nTabela: equipments")
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'equipments'
            ORDER BY ordinal_position
        """))
        for col, tipo, nullable in result:
            print(f"   - {col:<20} {tipo:<15} Nullable: {nullable}")
    
    print("\n" + "=" * 70)
    print("SUCESSO! BANCO POSTGRESQL CONFIGURADO!")
    print("=" * 70)
    print("\nProximos passos:")
    print("1. Acesse o Supabase: https://app.supabase.com")
    print("2. Va em 'Table Editor'")
    print("3. Voce vera as tabelas: users e equipments")
    print("4. Agora os dados serao permanentes!")
    print("\n")
    
except Exception as e:
    print("\n" + "=" * 70)
    print("ERRO AO CONECTAR/CRIAR TABELAS")
    print("=" * 70)
    print(f"\nErro: {str(e)}")
    print("\nVerifique:")
    print("1. A senha esta correta?")
    print("2. O host esta correto?")
    print("3. A porta 5432 esta acessivel?")
    print("4. Voce tem conexao com internet?")
    print("\n")

