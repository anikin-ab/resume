# import mysql.connector

from mysql.connector import connect, Error

global run_sql

def get_pass():
    'функция считывает пароль из файла'
    global TOKEN
    g_pas = open("password.txt", "r")
    TOKEN = g_pas.read()
    g_pas.close()
    return TOKEN

def common():
    'Основной модуль для выполнения запросов'
    global run_sql
    ins = ("INSERT", "UPDATE", "ALTER", "DELETE", "TRUNCATE") # для сохранения изм
    try:
        insert_i_t = ""
        print("\ninsert query (Enter to apply / 'stop' to finish):\n")
        while (string := input('')):
            insert_i_t = insert_i_t + "\n" + string  # построчный ввод
        print("Query is: \n", insert_i_t, "\n")

        # завершаем сеанс если stop
        if insert_i_t == "\nstop" or insert_i_t == "\nlogin":

            print(insert_i_t)
            return insert_i_t # завершаем сеанс

        # выполняем вводимые команды и сохарняем изменения
        with connection.cursor() as cursor:
            cursor.execute(insert_i_t)
            for word in ins:
                if word in insert_i_t:
                    print("query commited")
                    connection.commit() # сохраняем изменения

                # Выводим результат в случае SELECT
                else:
                    result = cursor.fetchall()
                    for row in result:
                        print(row) # выводим результат
            print("\nquery is done")
    except Error as e:
        print("Error in query is:\n", e)

s_start = "start"

# s_start = input("print 'start' to start MySQL server: ")

# модуль для подключения к СУБД
def sql_con():
    run_sql = ""
    chmod = ("\nstop", "\nlogin")
    if s_start == "start":
        get_pass() # считываем пароль
        try:
            print("login MySQL")
            # подключерние к СУБД
            global connection
            with connect(
                    host="localhost",
                    user="root", # user_name: root
                    password=TOKEN,
                    # user=input("user_name: "),  # user_name: root
                    # password=input("input password: "),
                    # database="lesson4",
                    database=input("input DB_name: ") #"python_db"
            ) as connection:
                print("connected well")
                # print(connection)

                # запуск функции запросов
                while run_sql not in chmod:
                    run_sql = common()

                else:
                    if run_sql == "\nstop":
                        connection.commit()
                        print("connection stopped")
                    elif run_sql == "\nlogin":
                        sql_con() # заново подключаемся к серверу

        except Error as e:
            print("Error in start is \n", e)
    else:
        print("MySQL80 server stopped")

sql_con()
