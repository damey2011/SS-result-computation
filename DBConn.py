import psycopg2


def connection():
    conn = psycopg2.connect(host="localhost",
                        user="root",
                        passwd="nifemi3",
                        db="secondary_results")
    print("Connect Success")
    c = conn.cursor()

    return c, conn


