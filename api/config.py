class Config:
    PG_USER = 'postgres'
    PG_PASSWORD = 'postgres'
    PG_HOST = 'localhost'
    PG_DATABASE = 'AchievementsServiceDB'

    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'

    connection_string = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:5432/{PG_DATABASE}"
