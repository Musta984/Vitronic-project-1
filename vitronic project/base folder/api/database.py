import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="kafka_demo",
        user="kafka_user",
        password="kafka_pass"
    )
