import datetime
from typing import Union

from k16s import DB, Agent


class Customer():
    def __init__(
            self,
            id: int,
            name: str,
            price_plan: str,
            num_users: int,
            mb_storage: int,
            contract_start: datetime = datetime.now(),
            contract_end: Union[datetime, None] = None
    ):
        self.id = id
        self.name = name
        self.price_plan = price_plan
        self.num_users = num_users
        self.mb_storage = mb_storage
        self.contract_start = contract_start
        self.contract_end = contract_end

    def to_db(self, agent: Agent):
        upsert: str = f"""
        REPLACE INTO customer_info.customers (
          id,
          name,
          price_plan,
          num_users,
          mb_storage,
          contract_start,
          contract_end
        ) VALUES (
          {self.id},
          '{self.name}',
          '{self.price_plan}',
          {self.num_users},
          {self.mb_storage},
          '{self.contract_start}',
          '{self.contract_end}'
        )
        """
        db = DB(agent)
        db.cursor.execute(upsert)
        db.connection.commit()

    @classmethod
    def from_agent_and_id(cls, agent: Agent, id: int):
        select: str = f"""
        SELECT
          id,
          name,
          price_plan,
          num_users,
          mb_storage,
          contract_start,
          contract_end
        FROM customer_info.customers
        WHERE id = {id}"""
        db = DB(agent)
        db.cursor.execute(select)
        result = db.cursor.fetchone()
        return cls(
            id=result[0],
            name=result[1],
            price_plan=result[2],
            num_users=result[3],
            mb_storage=result[4],
            contract_start=result[5],
            contract_end=result[6]
        )
