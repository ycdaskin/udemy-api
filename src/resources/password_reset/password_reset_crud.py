from src.resources.dbops import get_connection
from src.crypto.crypto import Crypto


def update_password(user, password):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            crypto = Crypto()
            pwd = crypto.encrypt(password)
            cur.execute('''update app_user set password = %s where id = %s''', (pwd, user))
    except Exception as ex:
        raise Exception(f"Error while resetting password: {str(ex.args[0])}")




