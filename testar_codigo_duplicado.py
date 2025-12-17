#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Teste - Código Duplicado com Tipos Diferentes
Testa se o sistema permite o mesmo código com NOVO e USADO
"""

from database import init_db, get_db_session
from models import Equipment
from datetime import datetime

print("\n" + "=" * 70)
print("🧪 TESTE: Código Duplicado com Tipos Diferentes")
print("=" * 70)

# Inicializa o banco (executa migrations)
print("\n1️⃣ Inicializando banco de dados...")
init_db()
print("✅ Banco inicializado")

# Obtém sessão
db = get_db_session()

try:
    print("\n2️⃣ Testando inserção de equipamentos...")
    
    # Código de teste
    codigo_teste = "TESTE-001"
    
    # Remove equipamentos de teste anteriores
    db.query(Equipment).filter(Equipment.codigo == codigo_teste).delete()
    db.commit()
    
    # Testa adicionar NOVO
    print(f"\n   📦 Adicionando: {codigo_teste} - NOVO")
    eq_novo = Equipment(
        codigo=codigo_teste,
        nome="Equipamento Teste",
        tipo="NOVO",
        quantidade=10,
        data_adicao=datetime.now(),
        ultima_atualizacao=datetime.now()
    )
    db.add(eq_novo)
    db.commit()
    print(f"   ✅ Sucesso! ID: {eq_novo.id}")
    
    # Testa adicionar USADO (mesmo código)
    print(f"\n   📦 Adicionando: {codigo_teste} - USADO (mesmo código)")
    eq_usado = Equipment(
        codigo=codigo_teste,
        nome="Equipamento Teste",
        tipo="USADO",
        quantidade=5,
        data_adicao=datetime.now(),
        ultima_atualizacao=datetime.now()
    )
    db.add(eq_usado)
    db.commit()
    print(f"   ✅ Sucesso! ID: {eq_usado.id}")
    
    # Verifica se ambos foram salvos
    print(f"\n3️⃣ Verificando registros salvos...")
    equipamentos = db.query(Equipment).filter(Equipment.codigo == codigo_teste).all()
    
    print(f"\n   Total de registros com código '{codigo_teste}': {len(equipamentos)}")
    
    for eq in equipamentos:
        print(f"\n   📋 ID: {eq.id}")
        print(f"      Código: {eq.codigo}")
        print(f"      Nome: {eq.nome}")
        print(f"      Tipo: {eq.tipo}")
        print(f"      Quantidade: {eq.quantidade}")
    
    # Remove os testes
    print(f"\n4️⃣ Limpando dados de teste...")
    db.query(Equipment).filter(Equipment.codigo == codigo_teste).delete()
    db.commit()
    print("   ✅ Dados de teste removidos")
    
    print("\n" + "=" * 70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print("\n💡 Resultado: O sistema permite o mesmo código com tipos diferentes!")
    print("   Exemplo: Você pode ter 'EQ001 - NOVO' e 'EQ001 - USADO' separados.\n")
    
except Exception as e:
    print("\n" + "=" * 70)
    print("❌ ERRO NO TESTE")
    print("=" * 70)
    print(f"\nErro: {str(e)}")
    print("\nPossíveis soluções:")
    print("1. Reinicie o Streamlit para executar a migration")
    print("2. Execute: python -c \"from database import init_db; init_db()\"")
    print("3. Se o erro persistir, delete estoque.db e execute novamente\n")
    
finally:
    db.close()



