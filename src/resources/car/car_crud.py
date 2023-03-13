from src.resources.dbops import get_connection, query_db, group_by, parse_params, parse_update_params


def update_car(data, car_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            params, values = parse_update_params(data)
            sql = f"""update car set {params} where id = ?"""
            cur.execute(sql, values + (car_id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating car: {str(ex.args[0])}")


def get_cars(car_id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        car_sql = "select * from car where id = ?" if car_id else "select * from car"
        car_params = (car_id,) if car_id else ()
        cars = query_db(cur, car_sql, car_params)
        pic_sql = "select * from car_picture where car_id = ?" if car_id else "select * from car_picture"
        pictures = query_db(cur, pic_sql, car_params)
        grouped = group_by(array=pictures, selector="car_id")
        for car in cars:
            try:
                car["images"] = grouped[car["id"]]
            except:
                car["images"] = []
        return cars


def create_car(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f"""insert into car {columns} values {placeholders}"""
            cur.execute(sql, values)
            conn.commit()
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating car: {str(ex.args[0])}")


def delete_car(car_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from car where id = ?"""
            cur.execute(sql, (car_id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while deleting car: {str(ex.args[0])}")