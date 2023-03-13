from src.resources.dbops import get_connection, query_db


def get_user_privileges(user_id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select p.name from user_privileges as up
        left join privileges as p
        on up.privilege = p.id
        where up.user_id = %s'''
        priv_data = query_db(cur, sql, (user_id,))
        sql = '''select p.name from role_priv_crs rpc
        left join privileges p on p.id = rpc.priv
        where rpc.user_role in (select role_id from user_role_rel urr where urr.user_id = %s)'''
        role_priv_data = query_db(cur, sql, (user_id,))
        priv_arr = [d["name"] for d in priv_data]
        role_priv_arr = [d["name"] for d in role_priv_data]
        return priv_arr + role_priv_arr


def get_user(user_name, password):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select name, last_name, user_name, company, email, id, avatar 
        from app_user where password is not null and (phone = %s or email = %s) and password = %s'''
        data = query_db(cur, sql, (user_name, user_name, password,))
        if len(data) == 0:
            return None
        return data[0]
