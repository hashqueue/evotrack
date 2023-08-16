import environ
import MySQLdb

env = environ.Env(DEBUG=(bool, False))
env.read_env(env.str('ENV_PATH', '.env.dev'))

print(f'Create MySQL database {env("DB_NAME")} if it does not exist.')
database_name = env('DB_NAME')

conn = MySQLdb.connect(host=env('DB_HOST'), port=int(env('DB_PORT')), user=env('DB_USER'), passwd=env('DB_PASSWORD'))
cursor = conn.cursor()
cursor.execute(
    f"CREATE DATABASE IF NOT EXISTS {database_name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
cursor.close()
conn.close()
print(f'Database {database_name} created or already exists.')
