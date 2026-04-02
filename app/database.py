import sqlite3
from .schemas import Shipment
from typing import Any

class Database:
    def connect_to_db(self):
        # Make connection with databse
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        
        #Get cursor to execute queries and fetch data
        self.cur = self.conn.cursor()

    def create_table(self):
        # 1. Create a table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY, 
                content TEXT, 
                weight REAL, 
                status TEXT
            )
        """)

    def create(self, shipment: Shipment) -> int:
        #Find a new id
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()

        new_id = result[0] + 1

        # Add shipment data
        self.cur.execute("""
            INSERT INTO shipment 
            VALUES (:id, :content, :weight, :status)
        """,
            {
                **shipment.model_dump(),
                "id": new_id,
                "status": "placed"
            }
        )

        self.conn.commit()
        return new_id

    def get(self, id: int) -> dict[str, Any]:
        # 3. Read a shipment by id
        self.cur.execute("""
            SELECT * FROM shipment 
            WHERE id = ?
        """, (id, ))
        row = self.cur.fetchone()

        return {
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3],
        } if row else None

    def update(self, id: int, shipment: Shipment)-> dict[str, Any]:
        # 4. Update shipment by id
        self.cur.execute("""
            UPDATE shipment SET status = :status
            WHERE id = :id
            """, 
                {
                    "id": id,
                    **shipment.model_dump()
                } 
        )
        self.conn.commit()
        return self.get(id)
    
    def delete(self, id: int):
        # 5. Delete shipment by id
        self.cur.execute("""
            DELETE FROM shipment
            WHERE id = ?
        """, (id,))

        self.conn.commit()

    def close(self):
        # Close the connection when done
        self.conn.close()

    def __enter__(self):
        self.connect_to_db()
        self.create_table()
        return self

    def __exit__(self, *arg):
        self.close()

def managed_db(self):
    db = Database()

    #Setup
    self.connect_to_db()
    self.create_table()

    yield db

    # Dispose
    db.close()

if __name__ == "__main__":    
    with Database() as db:
        print(db.get(12701))
        print(db.get(12702))