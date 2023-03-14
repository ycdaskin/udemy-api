from src.resources.dbops import get_connection, query_db, parse_params


def scan_qr(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f'insert into user_activity {columns} values {placeholders}'.replace("'", "")
            cur.execute(sql, values)
            trigger_relay()
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while scanning qr: {str(ex.args[0])}")


'''TODO'''
def trigger_relay():
    '''
    röle tetiklenere kapı açılması gerekiyorsa burası çalışacak
    :return:
    '''
    pass


