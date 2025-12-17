from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User, Equipment
import bcrypt
import os

# Suporte opcional a secrets do Streamlit e variável de ambiente para definir o caminho do SQLite
try:
    import streamlit as st  # type: ignore
    from streamlit.runtime.secrets import StreamlitSecretNotFoundError  # type: ignore
except Exception:
    st = None
    StreamlitSecretNotFoundError = Exception  # fallback


def _get_sqlite_url() -> str:
    """
    Retorna a URL do banco SQLite, permitindo configuração via:
    - Variável de ambiente: SQLITE_PATH
    - st.secrets["SQLITE_PATH"] (quando em Streamlit Cloud)
    Caso não definido, usa o estoque.db na pasta atual.
    """
    # 1) Variável de ambiente
    path = os.environ.get("SQLITE_PATH")

    # 2) Secrets do Streamlit
    if not path and st:
        try:
            path = st.secrets.get("SQLITE_PATH", None)
        except StreamlitSecretNotFoundError:
            path = None
        except Exception:
            path = None

    # 3) Padrão local
    if not path:
        path = os.path.join(os.getcwd(), "estoque.db")

    # Normaliza para URL SQLite
    if not path.startswith("sqlite:///"):
        # Substitui separador para não quebrar no Windows
        normalized = path.replace("\\", "/")
        path = f"sqlite:///{normalized}"

    return path

# Configuração do banco de dados SQLite
DATABASE_URL = _get_sqlite_url()
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def migrate_db():
    """Adiciona colunas necessárias e corrige constraints da tabela equipments"""
    try:
        with engine.connect() as conn:
            # Verifica se a tabela existe
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='equipments'"))
            if not result.fetchone():
                return  # Tabela não existe, será criada pelo create_all
            
            # Verifica quais colunas já existem
            result = conn.execute(text("PRAGMA table_info(equipments)"))
            columns = [row[1] for row in result]
            
            # Verifica se há constraint UNIQUE no código (problema a corrigir)
            result = conn.execute(text("SELECT sql FROM sqlite_master WHERE type='table' AND name='equipments'"))
            table_sql = result.fetchone()[0]
            
            # Verifica se o SQL da tabela contém UNIQUE na definição do código
            # Procura por padrões como "codigo TEXT UNIQUE" ou "codigo VARCHAR UNIQUE"
            needs_fix = False
            if table_sql:
                # Divide o SQL em linhas e procura pela definição do código
                lines = table_sql.split('\n')
                for line in lines:
                    line_upper = line.upper().strip()
                    if 'CODIGO' in line_upper and 'UNIQUE' in line_upper and 'CONSTRAINT' not in line_upper:
                        needs_fix = True
                        break
            
            # Se a tabela tem UNIQUE no codigo, precisamos recriá-la
            if needs_fix:
                print("🔄 Corrigindo constraint UNIQUE do código...")
                
                # Cria tabela temporária com estrutura correta
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS equipments_new (
                        id INTEGER PRIMARY KEY,
                        codigo TEXT NOT NULL,
                        nome TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        quantidade INTEGER NOT NULL DEFAULT 0,
                        data_adicao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Copia dados da tabela antiga para a nova
                conn.execute(text("""
                    INSERT INTO equipments_new (id, codigo, nome, tipo, quantidade, data_adicao, ultima_atualizacao)
                    SELECT id, codigo, 
                           COALESCE(nome, 'Sem nome'), 
                           tipo, 
                           quantidade,
                           COALESCE(data_adicao, CURRENT_TIMESTAMP),
                           COALESCE(ultima_atualizacao, CURRENT_TIMESTAMP)
                    FROM equipments
                """))
                
                # Remove tabela antiga
                conn.execute(text("DROP TABLE equipments"))
                
                # Renomeia tabela nova
                conn.execute(text("ALTER TABLE equipments_new RENAME TO equipments"))
                
                # Cria índice no código (mas não UNIQUE)
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_equipments_codigo ON equipments (codigo)"))
                
                conn.commit()
                print("✅ Constraint corrigida! Agora você pode ter o mesmo código com tipos diferentes.")
                
            else:
                # Adiciona colunas faltantes normalmente
                if 'nome' not in columns:
                    conn.execute(text("ALTER TABLE equipments ADD COLUMN nome TEXT DEFAULT ''"))
                    conn.execute(text("UPDATE equipments SET nome = 'Sem nome' WHERE nome IS NULL OR nome = ''"))
                
                if 'data_adicao' not in columns:
                    conn.execute(text("ALTER TABLE equipments ADD COLUMN data_adicao DATETIME DEFAULT CURRENT_TIMESTAMP"))
                
                if 'ultima_atualizacao' not in columns:
                    conn.execute(text("ALTER TABLE equipments ADD COLUMN ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP"))
                
                conn.commit()
                
    except Exception as e:
        print(f"⚠️ Erro na migração: {str(e)}")
        # Se der erro, pode ser que a tabela não exista ainda, então ignora
        pass


def init_db():
    """Inicializa o banco de dados e cria as tabelas"""
    Base.metadata.create_all(bind=engine)
    
    # Executa migração para adicionar coluna 'nome' se necessário
    migrate_db()
    
    # Cria usuários padrão se não existirem
    db = SessionLocal()
    try:
        # Verifica se já existem usuários
        admin_exists = db.query(User).filter(User.username == "admin").first()
        usuario_exists = db.query(User).filter(User.username == "usuario").first()
        
        if not admin_exists:
            # Senha padrão: admin123
            admin_password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = User(username="admin", password_hash=admin_password_hash, role="admin")
            db.add(admin)
        
        if not usuario_exists:
            # Senha padrão: usuario123
            usuario_password_hash = bcrypt.hashpw("usuario123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            usuario = User(username="usuario", password_hash=usuario_password_hash, role="usuario")
            db.add(usuario)
        
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db():
    """Retorna uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session() -> Session:
    """Retorna uma sessão do banco de dados diretamente"""
    return SessionLocal()

