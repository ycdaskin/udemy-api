import sqlite3 as db
import os
import uuid
from psycopg2 import pool as p
from contextlib import contextmanager
from src.crypto.crypto import Crypto

crypt = Crypto()


DB_NAME = "db.db"
AUTH_DB = "sess.db"

cars = [
    ("13dce7ee-498b-4817-ac8d-d37f54ebd100", "Volvo", "V40", "Inscription", "Red", "#d91636", "Automatic", 152, 1499, "Gasoline", 18000, "Hatchback"),
    ("b12d732d-6684-4883-880c-36b88c50e89a", "BMW", "3 Series", "xDrive Premium ", "White", "#ffffff", "Automatic", 136, 1499, "Gasoline", 24000, "Sedan"),
    ("2eb9bdf5-4d00-4043-911a-8340f821e075", "Opel", "Astra", "1.4 T Dynamic", "White", "#ffffff", "Manual", 150, 1499, "Gasoline", 12000, "Sedan"),
    ("ddf4fccd-b421-45d7-8100-cccc6f8ba260", "BMW", "5 Series", "xDrive Premium ", "Black", "#000000", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
    ("5a1ebf8b-5317-4826-be4d-5aa46b954a66", "Volvo", "S90", "Inscription", "Grey", "#d4cfd0", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
    ("32ff8e5b-4e07-43a2-beba-ca4e9cb871b6", "Volvo", "V40", "Inscription", "Red", "#d91636", "Automatic", 152, 1499, "Gasoline", 18000, "Hatchback"),
    ("1db48e88-853a-4046-b1e3-9fa5f676a1f5", "BMW", "3 Series", "xDrive Premium ", "White", "#ffffff", "Automatic", 136, 1499, "Gasoline", 24000, "Sedan"),
    ("70760d72-99a6-4f2b-b1f5-b7ab0d994262", "Opel", "Astra", "1.4 T Dynamic", "White", "#ffffff", "Manual", 150, 1499, "Gasoline", 12000, "Sedan"),
    ("1458b277-091d-450b-9a9a-0b987214b8f1", "BMW", "5 Series", "xDrive Premium ", "Black", "#000000", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
    ("ad602222-4295-4830-b9f3-29a28ad83404", "Volvo", "S90", "Inscription", "Grey", "#d4cfd0", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
    ("5d78ded9-644f-4b51-be1b-840f487b59ba", "Volvo", "V40", "Inscription", "Red", "#d91636", "Automatic", 152, 1499, "Gasoline", 18000, "Hatchback"),
    ("6d39338e-79b6-4dc3-8fa2-a56153c1754c", "BMW", "3 Series", "xDrive Premium ", "White", "#ffffff", "Automatic", 136, 1499, "Gasoline", 24000, "Sedan"),
    ("235fbc69-6840-4b9d-9254-9f880f282885", "Opel", "Astra", "1.4 T Dynamic", "White", "#ffffff", "Manual", 150, 1499, "Gasoline", 12000, "Sedan"),
    ("cf6774ce-4b87-4979-aee9-33c34a96ea21", "BMW", "5 Series", "xDrive Premium ", "Black", "#000000", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
    ("6c86bbff-2143-41b2-a11e-5f9a0adac66d", "Volvo", "S90", "Inscription", "Grey", "#d4cfd0", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
    ("681e2cc6-d501-4c41-a884-87a50f01223f", "Volvo", "V40", "Inscription", "Red", "#d91636", "Automatic", 152, 1499, "Gasoline", 18000, "Hatchback"),
    ("5d41a290-2d96-480e-a6d8-cf4f890b2a90", "BMW", "3 Series", "xDrive Premium ", "White", "#ffffff", "Automatic", 136, 1499, "Gasoline", 24000, "Sedan"),
    ("4f3e7f27-4de0-4c0e-ba59-bfb320703641", "Opel", "Astra", "1.4 T Dynamic", "White", "#ffffff", "Manual", 150, 1499, "Gasoline", 12000, "Sedan"),
    ("b6949242-3abb-4af0-a4db-e6c05345e0a5", "BMW", "5 Series", "xDrive Premium ", "Black", "#000000", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
    ("8839eecd-2b03-45c0-99d3-9c65baf39ee6", "Volvo", "S90", "Inscription", "Grey", "#d4cfd0", "Automatic", 218, 1995, "Diesel", 38000, "Sedan"),
]


pictures = [
    ("8953e319-6904-4b64-8d63-ae3b4adbc864", "13dce7ee-498b-4817-ac8d-d37f54ebd100", "https://www.sifiraracal.com/resim/renk/203/volvo-v40-kirmizi.png"),
    ("cd88c035-e321-4749-98f1-4dfaee5d96d7", "13dce7ee-498b-4817-ac8d-d37f54ebd100", "https://cdn.ototeknikveri.com/Files/News/Big/619yeni-volvo-v40-ve-v40-cross-country-16-dizel-otomatik-satista-fiyati.jpg"),
    ("6fb802ee-d17c-4fe0-8312-9a399fe6ac3f", "13dce7ee-498b-4817-ac8d-d37f54ebd100", "https://i.ytimg.com/vi/Lr0_ifbvclQ/maxresdefault.jpg"),
    ("24d19711-4dae-49a2-9041-2e5c520a8611", "b12d732d-6684-4883-880c-36b88c50e89a", "https://cdn.motor1.com/images/mgl/NAWGY/s3/2019-bmw-3-series-m-performance-parts.jpg"),
    ("cca08cc6-ee41-4230-bb23-feff09223432", "b12d732d-6684-4883-880c-36b88c50e89a", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgBS7mBJDeqktED_ED8Z63NX3AxyOBjFoR7Q&usqp=CAU"),
    ("974676f0-d179-47c5-8aab-c3a10287492d", "b12d732d-6684-4883-880c-36b88c50e89a", "https://media.autoexpress.co.uk/image/private/s--X-WVjvBW--/f_auto,t_content-image-full-desktop@1/v1640099444/autoexpress/2021/12/BMW%203%20Series%20Mk7%20front%20static.jpg"),
    ("0620bf33-0149-4b4e-b0fb-126df1eac776", "2eb9bdf5-4d00-4043-911a-8340f821e075", "https://www.oscarrentacar.com/dosya/1694/sinif/14-23-50-opel-astra-dizel-otomatik.png"),
    ("69b95f80-7dbf-4fd4-84cb-5cf2dd62cf79", "ddf4fccd-b421-45d7-8100-cccc6f8ba260", "https://cars.usnews.com/static/images/Auto/izmo/i159614805/2022_bmw_5_series_angularfront.jpg"),
    ("b6105593-9279-481e-b1dd-64da188c0aa1", "ddf4fccd-b421-45d7-8100-cccc6f8ba260", "https://cdn.carbuzz.com/gallery-images/840x560/793000/800/793866.jpg"),
    ("4e75a006-db1b-476c-91fb-b8f7eb425c1d", "5a1ebf8b-5317-4826-be4d-5aa46b954a66", "https://i.ytimg.com/vi/pNIkEI-FqVw/maxresdefault.jpg"),

    ("b504d16a-e0ad-4f37-99b6-0812e7e336c2", "32ff8e5b-4e07-43a2-beba-ca4e9cb871b6", "https://www.sifiraracal.com/resim/renk/203/volvo-v40-kirmizi.png"),
    ("605219d3-24c9-4d42-a8e5-4c985c252226", "32ff8e5b-4e07-43a2-beba-ca4e9cb871b6", "https://cdn.ototeknikveri.com/Files/News/Big/619yeni-volvo-v40-ve-v40-cross-country-16-dizel-otomatik-satista-fiyati.jpg"),
    ("dca7ba51-09bb-4b1e-a444-201ba7a99408", "32ff8e5b-4e07-43a2-beba-ca4e9cb871b6", "https://i.ytimg.com/vi/Lr0_ifbvclQ/maxresdefault.jpg"),
    ("482bb79c-45c1-4d93-9e84-05a6729e0823", "1db48e88-853a-4046-b1e3-9fa5f676a1f5", "https://cdn.motor1.com/images/mgl/NAWGY/s3/2019-bmw-3-series-m-performance-parts.jpg"),
    ("42be2356-7738-4969-ba3b-ff641e76efda", "1db48e88-853a-4046-b1e3-9fa5f676a1f5", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgBS7mBJDeqktED_ED8Z63NX3AxyOBjFoR7Q&usqp=CAU"),
    ("a1b5f7e0-af16-4c51-b56c-b4d07ea4098a", "1db48e88-853a-4046-b1e3-9fa5f676a1f5", "https://media.autoexpress.co.uk/image/private/s--X-WVjvBW--/f_auto,t_content-image-full-desktop@1/v1640099444/autoexpress/2021/12/BMW%203%20Series%20Mk7%20front%20static.jpg"),
    ("6c8fc269-d8d6-4304-88a1-a5817dc1302c", "70760d72-99a6-4f2b-b1f5-b7ab0d994262", "https://www.oscarrentacar.com/dosya/1694/sinif/14-23-50-opel-astra-dizel-otomatik.png"),
    ("31e6ecc6-98e1-4fa2-b4ed-1cf211c037db", "1458b277-091d-450b-9a9a-0b987214b8f1", "https://cars.usnews.com/static/images/Auto/izmo/i159614805/2022_bmw_5_series_angularfront.jpg"),
    ("ad23dc2c-a8a9-4da2-901d-e4afffbfdaff", "1458b277-091d-450b-9a9a-0b987214b8f1", "https://cdn.carbuzz.com/gallery-images/840x560/793000/800/793866.jpg"),
    ("3968f75d-87dc-4c6b-bf7f-e3bd16eabf88", "ad602222-4295-4830-b9f3-29a28ad83404", "https://i.ytimg.com/vi/pNIkEI-FqVw/maxresdefault.jpg"),

    ("30e7024c-55af-4c23-b231-91243af6efc9", "5d78ded9-644f-4b51-be1b-840f487b59ba", "https://www.sifiraracal.com/resim/renk/203/volvo-v40-kirmizi.png"),
    ("a1a7b4db-d685-4659-9e44-ee4c7ff78607", "5d78ded9-644f-4b51-be1b-840f487b59ba", "https://cdn.ototeknikveri.com/Files/News/Big/619yeni-volvo-v40-ve-v40-cross-country-16-dizel-otomatik-satista-fiyati.jpg"),
    ("83fcaf9c-5e3c-44cb-9836-04b015b9d77e", "5d78ded9-644f-4b51-be1b-840f487b59ba", "https://i.ytimg.com/vi/Lr0_ifbvclQ/maxresdefault.jpg"),
    ("849ce361-2e98-4285-88f3-c91998f70add", "6d39338e-79b6-4dc3-8fa2-a56153c1754c", "https://cdn.motor1.com/images/mgl/NAWGY/s3/2019-bmw-3-series-m-performance-parts.jpg"),
    ("3c74b51b-0ab3-45a2-94d6-9f596d5c1156", "6d39338e-79b6-4dc3-8fa2-a56153c1754c", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgBS7mBJDeqktED_ED8Z63NX3AxyOBjFoR7Q&usqp=CAU"),
    ("7ef974b2-f778-4f08-ac7a-4ac31c156a30", "6d39338e-79b6-4dc3-8fa2-a56153c1754c", "https://media.autoexpress.co.uk/image/private/s--X-WVjvBW--/f_auto,t_content-image-full-desktop@1/v1640099444/autoexpress/2021/12/BMW%203%20Series%20Mk7%20front%20static.jpg"),
    ("9499124a-94ff-47e1-9471-1d19b828cb47", "235fbc69-6840-4b9d-9254-9f880f282885", "https://www.oscarrentacar.com/dosya/1694/sinif/14-23-50-opel-astra-dizel-otomatik.png"),
    ("bef1ebc9-b60a-4f40-8dea-6063f84b06d1", "cf6774ce-4b87-4979-aee9-33c34a96ea21", "https://cars.usnews.com/static/images/Auto/izmo/i159614805/2022_bmw_5_series_angularfront.jpg"),
    ("b1dc34bf-6937-44f4-8159-938b0542a4bb", "cf6774ce-4b87-4979-aee9-33c34a96ea21", "https://cdn.carbuzz.com/gallery-images/840x560/793000/800/793866.jpg"),
    ("a799c85b-a509-47ae-ba83-5b0fdd9863b6", "6c86bbff-2143-41b2-a11e-5f9a0adac66d", "https://i.ytimg.com/vi/pNIkEI-FqVw/maxresdefault.jpg"),

    ("6a69fd45-0b42-406b-8526-b5818af66567", "681e2cc6-d501-4c41-a884-87a50f01223f", "https://www.sifiraracal.com/resim/renk/203/volvo-v40-kirmizi.png"),
    ("80ad1e6f-cc26-4e1b-ade8-aaec40161f3e", "681e2cc6-d501-4c41-a884-87a50f01223f", "https://cdn.ototeknikveri.com/Files/News/Big/619yeni-volvo-v40-ve-v40-cross-country-16-dizel-otomatik-satista-fiyati.jpg"),
    ("62aa0f8c-cc3f-45cc-a4c2-922e77f25712", "681e2cc6-d501-4c41-a884-87a50f01223f", "https://i.ytimg.com/vi/Lr0_ifbvclQ/maxresdefault.jpg"),
    ("be66759c-4495-4505-926e-89c93648114f", "5d41a290-2d96-480e-a6d8-cf4f890b2a90", "https://cdn.motor1.com/images/mgl/NAWGY/s3/2019-bmw-3-series-m-performance-parts.jpg"),
    ("aaf00310-7c9d-4db0-9b93-298796ca4b26", "5d41a290-2d96-480e-a6d8-cf4f890b2a90", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSgBS7mBJDeqktED_ED8Z63NX3AxyOBjFoR7Q&usqp=CAU"),
    ("4ab552ca-2ccc-40ca-adbf-9a5a3148b8d0", "5d41a290-2d96-480e-a6d8-cf4f890b2a90", "https://media.autoexpress.co.uk/image/private/s--X-WVjvBW--/f_auto,t_content-image-full-desktop@1/v1640099444/autoexpress/2021/12/BMW%203%20Series%20Mk7%20front%20static.jpg"),
    ("5ba46f8e-09fb-4d4f-b895-5a5fbad445f6", "4f3e7f27-4de0-4c0e-ba59-bfb320703641", "https://www.oscarrentacar.com/dosya/1694/sinif/14-23-50-opel-astra-dizel-otomatik.png"),
    ("a6d2e5d1-3aaf-40cd-b18e-ba9f02c34a96", "b6949242-3abb-4af0-a4db-e6c05345e0a5", "https://cars.usnews.com/static/images/Auto/izmo/i159614805/2022_bmw_5_series_angularfront.jpg"),
    ("92852e37-a9e8-41de-b6eb-a75b75b36469", "b6949242-3abb-4af0-a4db-e6c05345e0a5", "https://cdn.carbuzz.com/gallery-images/840x560/793000/800/793866.jpg"),
    ("35e0f075-594f-4146-aac1-f99ce0b9787b", "8839eecd-2b03-45c0-99d3-9c65baf39ee6", "https://i.ytimg.com/vi/pNIkEI-FqVw/maxresdefault.jpg"),

]


pool = p.ThreadedConnectionPool(
    2,
    20,
    host='ec2-54-73-22-169.eu-west-1.compute.amazonaws.com',
    database='dbm5rut493hudn',
    user='rmgicawsisxtnu',
    password="475be76867cdbaf3edd0ba958b34ada8fe238d49079893a5f6e6c41716702346",
    port=5432,
    options="-c search_path=dbo,data"
)


def initialize_auth_db():
    if not os.path.exists(AUTH_DB):
        with db.connect(AUTH_DB) as conn:
            cur = conn.cursor()
            auth_sql = '''
                create table if not exists sess
                (id, user, token, refresh_token)
            '''
            cur.execute(auth_sql)
            conn.commit()


def initialize():
    if not os.path.exists(DB_NAME):
        with db.connect(DB_NAME) as conn:
            cur = conn.cursor()
            car_sql = """ 
                create table if not exists car
                (id, brand, series, trim, color, hex_color, transmission, hp, diplacement, fuel, price, body_type)
            """
            cur.execute(car_sql)
            for car in cars:
                car_insert = f"""insert into car values {car}"""
                cur.execute(car_insert)

            pictures_sql = """
                create table if not exists car_picture
                (id, car_id, picture_url)
            """
            cur.execute(pictures_sql)
            for picture in pictures:
                picture_insert = f"""insert into car_picture values {picture}"""
                cur.execute(picture_insert)

            company_sql = """
                create table if not exists company
                (id, name, address, latitude, longitude, responsible_person, phone, email, tax_office, tax_number)
            """
            cur.execute(company_sql)
            company_insert = """
                insert into company
                values('8307c770-82c9-4a80-948c-f4a114ddf164', 'Demo Company', 'Some Street', 0, 0, 
                'aeb47672-c010-4e47-9a63-59290905d64a', '555 873 37 68', 'info@democompany.com', 'Some office',
                12345678)
            """
            cur.execute(company_insert)

            user_sql = """
                create table if not exists user
                (id, name, last_name, user_name, password, company, phone, email, id_number, address, avatar)
            """
            cur.execute(user_sql)
            user_insert = """insert into user 
                values('aeb47672-c010-4e47-9a63-59290905d64a', 'Demo', 'User', "demouser", 'O/YAC1aOocM=',
                'aeb47672-c010-4e47-9a63-59290905d64a', '555 873 37 68', 'demouser@democompany.com', 11111111111,
                'Some address', null)
            """
            cur.execute(user_insert)

            privileges_sql = """
                create table if not exists privileges
                (id, name, description)
            """
            cur.execute(privileges_sql)

            user_privileges_sql = """
                create table if not exists user_privileges
                (id, privilege, user)
            """
            cur.execute(user_privileges_sql)

            conn.commit()


@contextmanager
def get_connection():
    #return db.connect(DB_NAME)
    con = pool.getconn()
    try:
        yield con
        con.commit()
    finally:
        pool.putconn(con)



def parse_params(data, auto_id_column=None, private_columns=[], columns_to_encyript=[]):
    keys = []
    values = []
    placeholders = "("
    if auto_id_column is not None:
        keys.append(auto_id_column)
        values.append(str(uuid.uuid4()))
    for key in data:
        if key in private_columns:
            continue
        keys.append(key)
        _val = crypt.encrypt(data[key]) if key in columns_to_encyript else data[key]
        values.append(_val)
    for value in values:
        placeholders += "%s, "
    placeholders = placeholders[:-2] + " )"
    return tuple(keys), tuple(values), placeholders


def parse_update_params(data):
    result = ""
    values = []
    for key in data:
        if key != "id":
            result += f"{key}=%s, "
            values.append(data[key])
    result = result[:-2] + " "
    return result, tuple(values)


def query_db(cursor, query, args=()):
    '''veri tabanından sorgu çekip sonnucu json serializable obje listesi olarak döndürür'''
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r


def group_by(array, selector):
    result = {}
    for item in array:
        if item[selector] in result:
            result[item[selector]].append(item)
        else:
            result[item[selector]] = [item]
    return result




