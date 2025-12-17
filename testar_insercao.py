import sqlite3

print("\n" + "=" * 70)
print("TESTE DE INSERCAO - CODIGO DUPLICADO COM TIPOS DIFERENTES")
print("=" * 70)

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

try:
    codigo = "TESTE123"
    
    # Remove testes anteriores
    cursor.execute("DELETE FROM equipments WHERE codigo = ?", (codigo,))
    
    # Teste 1: Inserir NOVO
    print(f"\n1. Inserindo: {codigo} - NOVO - 10 unidades")
    cursor.execute("""
        INSERT INTO equipments (codigo, nome, tipo, quantidade)
        VALUES (?, ?, ?, ?)
    """, (codigo, "Produto Teste", "NOVO", 10))
    print("OK - Inserido com sucesso!")
    
    # Teste 2: Inserir USADO (mesmo código)
    print(f"\n2. Inserindo: {codigo} - USADO - 5 unidades (mesmo codigo)")
    cursor.execute("""
        INSERT INTO equipments (codigo, nome, tipo, quantidade)
        VALUES (?, ?, ?, ?)
    """, (codigo, "Produto Teste", "USADO", 5))
    print("OK - Inserido com sucesso!")
    
    # Verifica
    print(f"\n3. Verificando registros com codigo '{codigo}':")
    cursor.execute("SELECT id, codigo, nome, tipo, quantidade FROM equipments WHERE codigo = ?", (codigo,))
    registros = cursor.fetchall()
    
    print(f"\nTotal: {len(registros)} registro(s)")
    for reg in registros:
        print(f"   ID: {reg[0]}, Codigo: {reg[1]}, Nome: {reg[2]}, Tipo: {reg[3]}, Qtd: {reg[4]}")
    
    # Remove testes
    cursor.execute("DELETE FROM equipments WHERE codigo = ?", (codigo,))
    conn.commit()
    
    print("\n" + "=" * 70)
    print("TESTE CONCLUIDO COM SUCESSO!")
    print("=" * 70)
    print("\nO banco esta funcionando corretamente!")
    print("Voce pode adicionar o mesmo codigo com NOVO e USADO separados.\n")
    
except Exception as e:
    print(f"\nERRO: {str(e)}")
    print("\nSe o erro persistir, execute: corrigir_indice.py")
    conn.rollback()
finally:
    conn.close()


