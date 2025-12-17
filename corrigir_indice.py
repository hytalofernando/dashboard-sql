import sqlite3

print("\n" + "=" * 70)
print("CORRIGINDO INDICE UNIQUE")
print("=" * 70)

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

try:
    # Remove índice UNIQUE antigo
    print("\n1. Removendo indice UNIQUE antigo...")
    cursor.execute("DROP INDEX IF EXISTS ix_equipments_codigo")
    print("OK - Indice removido")
    
    # Cria índice normal (não-único)
    print("\n2. Criando indice normal (nao-unico)...")
    cursor.execute("CREATE INDEX IF NOT EXISTS ix_equipments_codigo ON equipments (codigo)")
    print("OK - Indice criado")
    
    # Verifica
    print("\n3. Verificando indices...")
    cursor.execute("PRAGMA index_list(equipments)")
    indices = cursor.fetchall()
    
    for idx in indices:
        is_unique = "SIM" if idx[2] == 1 else "NAO"
        print(f"   - {idx[1]}: Unique = {is_unique}")
    
    conn.commit()
    
    print("\n" + "=" * 70)
    print("CORRECAO CONCLUIDA!")
    print("=" * 70)
    print("\nAgora voce pode adicionar o mesmo codigo com tipos diferentes!\n")
    
except Exception as e:
    print(f"\nERRO: {str(e)}")
    conn.rollback()
finally:
    conn.close()


