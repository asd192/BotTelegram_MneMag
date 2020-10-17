import datetime
import pymysql


def log_errors(message_error):
    # TODO не работает
    with open("db_queries.log", "a", encoding="UTF8") as dbq_log:
        dbq_log.write(f'{datetime.datetime.now()} - {message_error}\n')


try:
    with open("database_access.txt", "r", encoding="UTF8") as dt_acc:
        param_db = [val.strip() for val in dt_acc]

    connect = pymysql.connect(
        host=param_db[0],
        db=param_db[1],
        user=param_db[2],
        password=param_db[3],
        charset=param_db[4],
        cursorclass=pymysql.cursors.DictCursor
    )
    log_errors("Успешное подключение к БД\n")
except:
    log_errors("Не удалось подключиться к БД\n")


def link_shops_read(call_data='Мегамаркеты'):
    """запрос ссылок магазинов из БД"""
    try:
        with connect.cursor() as cursor:
            sql_shops = """
            SELECT
                SUBSTRING_INDEX(ccs.s_url, '|', 1) url
            FROM cms_con_shop ccs
            JOIN cms_con_shop_cats ccsc ON ccsc.id = ccs.category_id
            WHERE
                ccsc.title = (%s) AND
                is_hidden IS null AND
                date_approved IS NOT null AND
                is_pub = 1 AND
                is_deleted IS null AND
                is_private = 0
            ORDER BY RAND()
            LIMIT 5
            """
            cursor.execute(sql_shops, call_data)
        url = [row['url'] for row in cursor]
        return url
    except:
        log_errors("Неудачный запрос ссылок\n")


if __name__ == '__main__':
    print(link_shops_read())
