import allure
from faker import Faker

fake = Faker()


@allure.step("Создание нового клиента")
def create_customer(connection, customer_data: dict = None) -> int:
    if customer_data is None:
        customer_data = {
            "customer_group_id": 1,
            "store_id": 0,
            "language_id": 1,
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "email": fake.email(),
            "telephone": fake.phone_number(),
            "password": fake.password(),
            "custom_field": "",
            "newsletter": 0,
            "ip": fake.ipv4(),
            "status": 1,
            "safe": 0,
            "token": "",
            "code": "",
            "date_added": fake.date_time_this_year()
        }

    with connection.cursor() as cursor:
        sql = """
        INSERT INTO oc_customer 
        (customer_group_id, store_id, language_id, firstname, lastname, 
         email, telephone, password, custom_field, newsletter, 
         ip, status, safe, token, code, date_added) 
        VALUES 
        (%(customer_group_id)s, %(store_id)s, %(language_id)s, %(firstname)s, %(lastname)s, 
         %(email)s, %(telephone)s, %(password)s, %(custom_field)s, %(newsletter)s, 
         %(ip)s, %(status)s, %(safe)s, %(token)s, %(code)s, %(date_added)s)
        """
        cursor.execute(sql, customer_data)
        customer_id = cursor.lastrowid
        connection.commit()

    return customer_id


@allure.step("Получение данных клиента по ID")
def get_customer_by_id(connection, customer_id: int) -> dict:
    with connection.cursor() as cursor:
        sql = """
        SELECT customer_id, customer_group_id, store_id, language_id, 
               firstname, lastname, email, telephone, password, custom_field, 
               newsletter, ip, status, safe, token, code, date_added 
        FROM oc_customer 
        WHERE customer_id = %s
        """
        cursor.execute(sql, (customer_id,))
        return cursor.fetchone()


@allure.step("Обновление данных клиента")
def update_customer(connection, customer_id: int, update_data: dict) -> bool:
    if not update_data:
        return False

    # Получаем текущие данные клиента
    current_data = get_customer_by_id(connection, customer_id)
    if not current_data:
        return False

    merged_data = {**current_data, **update_data}
    merged_data['customer_id'] = customer_id

    set_parts = []
    params = {}
    for key, value in update_data.items():
        set_parts.append(f"{key} = %({key})s")
        params[key] = value
    params['customer_id'] = customer_id

    if not set_parts:
        return False

    sql = f"UPDATE oc_customer SET {', '.join(set_parts)} WHERE customer_id = %(customer_id)s"

    with connection.cursor() as cursor:
        affected_rows = cursor.execute(sql, params)
        connection.commit()
        return affected_rows > 0


@allure.step("Удаление клиента по ID")
def delete_customer(connection, customer_id: int) -> bool:
    with connection.cursor() as cursor:
        sql = "DELETE FROM oc_customer WHERE customer_id = %s"
        affected_rows = cursor.execute(sql, (customer_id,))
        connection.commit()
        return affected_rows > 0