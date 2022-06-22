from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    # users
    async def add_user(self, user_id, username) -> None:
        """Store user in DB, ignore duplicates"""
        request = f"INSERT INTO tg_users(user_id, username) VALUES ({user_id}, '{username}') ON CONFLICT DO NOTHING;"
        await self.conn.execute(
            request
        )
        return

    async def list_users(self) -> List[int]:
        """List all bot users"""
        # return await self.conn.fetch(
        #     f"select userid from tg_users;"
        # )
        return [
            row[0]
            for row in await self.conn.fetch(
                "select user_id, username from tg_users;",
            )
        ]

    async def write_vacancy(self, main_part, tags, link, userid) -> bool:
        try:
            main_part = main_part.replace("'", "''")
            tags = tags.replace("'", "''")
            link = tags.replace("'", "''")
            request = fr"INSERT INTO user_vacancies(main_part, tags, link, date_time, user_id) VALUES " \
                      fr"('{main_part}', '{tags}', '{link}', CURRENT_TIMESTAMP, {userid}) ON CONFLICT DO NOTHING;"
            await self.conn.execute(
                request
            )
        except Exception as err:
            print(err)
            return False
        return True
