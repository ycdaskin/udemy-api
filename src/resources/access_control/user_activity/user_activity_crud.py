
from src.resources.dbops import get_connection, query_db, parse_params
from src.auth.auth import is_super_user


def get_user_activities(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user(cur=cur)
        if super_admin:
            sql = '''select ua.*, g.name as gate_name, u.name || ' ' || u.last_name as user_name, u.avatar,
                b.name as building_name
            from user_activity ua
            left join gate g on g.id = ua.gate_id
            left join building b on b.id = g.building
            left join company c on c.id = b.company
            left join app_user u on u.id = ua.user_id
            ''' if id is None else \
            '''select ua.*, g.name as gate_name, u.name || ' ' || u.last_name as user_name, u.avatar,
                b.name as building_name
            from user_activity ua
            left join gate g on g.id = ua.gate_id
            left join building b on b.id = g.building
            left join company c on c.id = b.company
            left join app_user u on u.id = ua.user_id
            where ua.id = %s '''
            params = (id,) if id else ()
        else:
            sql = '''select ua.*, g.name as gate_name, u.name || ' ' || u.last_name as user_name, u.avatar,
                b.name as building_name
            from user_activity ua
            left join gate g on g.id = ua.gate_id
            left join building b on b.id = g.building
            left join company c on c.id = b.company
            left join app_user u on u.id = ua.user_id
            where c.id = %s
            ''' if id is None else \
            '''select ua.*, g.name as gate_name, u.name || ' ' || u.last_name as user_name, u.avatar,
                b.name as building_name
            from user_activity ua
            left join gate g on g.id = ua.gate_id
            left join building b on b.id = g.building
            left join company c on c.id = b.company
            left join app_user u on u.id = ua.user_id
            where ua.id = %s and c.id = %s
            '''
            params = (id, company,) if id else (company,)
        data = query_db(cur, sql, params)
        return data



def create_user_activity(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f'insert into user_activity {columns} values {placeholders}'.replace("'", "")
            cur.execute(sql, values)
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating user activity: {str(ex.args[0])}")



def delete_user_activity(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from user_activity where id = %s"""
            cur.execute(sql, (id,))
    except Exception as ex:
        raise Exception(f"Error while deleting user activity: {str(ex.args[0])}")


def delete_user_activities(ids):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from user_activity where id in %s"""
            cur.execute(sql, (tuple(ids),))
    except Exception as ex:
        raise Exception(f"Error while deleting user activities: {str(ex.args[0])}")


def get_user_activities_by_user(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user(cur=cur)
        if super_admin:
            sql = '''select ua.*, g.name as gate_name, u.name || ' ' || u.last_name as user_name, u.avatar,
                b.name as building_name
            from user_activity ua
            left join gate g on g.id = ua.gate_id
            left join building b on b.id = g.building
            left join company c on c.id = b.company
            left join app_user u on u.id = ua.user_id
            where ua.user_id = %s'''
            params = (user_id,)
        else:
            sql = '''select ua.*, g.name as gate_name, u.name || ' ' || u.last_name as user_name, u.avatar, 
                b.name as building_name
            from user_activity ua
            left join gate g on g.id = ua.gate_id
            left join building b on b.id = g.building
            left join company c on c.id = b.company
            left join app_user u on u.id = ua.user_id
            where c.id = %s and ua.user_id = %s'''
            params = (company, user_id,)
        data = query_db(cur, sql, params)
        return data
