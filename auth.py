import bcrypt
from database import get_db_session
from models import User


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def authenticate_user(username: str, password: str) -> dict:
    """
    Autentica um usuário e retorna informações do usuário se válido
    
    Returns:
        dict: {'success': bool, 'user': User ou None, 'message': str}
    """
    db = get_db_session()
    try:
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return {'success': False, 'user': None, 'message': 'Usuário não encontrado'}
        
        if not verify_password(password, user.password_hash):
            return {'success': False, 'user': None, 'message': 'Senha incorreta'}
        
        return {
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            },
            'message': 'Login realizado com sucesso'
        }
    except Exception as e:
        return {'success': False, 'user': None, 'message': f'Erro ao autenticar: {str(e)}'}
    finally:
        db.close()

