import psycopg as ps

class PostgresDB:
    def __init__(self, bd_config):
        self.bd_config = bd_config

        self.tables = [
            'anime_ids',
            'anime_main',
            'ratings',
            'genres',
            'min_ages',
            'other_ids',
            'viewing_orders',
            'creators',
            'studios',
            'anime_other_titles',
            'ratings_distributions',
            'recommendations',
            'videos',
            'comments'
        ]

    def open_conn(self):
        self.conn = ps.connect(**self.bd_config)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()