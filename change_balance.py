import sqlite3

from fastapi import FastAPI
app = FastAPI()
from typing import Optional
from fastapi.responses import JSONResponse
@app.get("/change_balance/")
async def change_balance(account_number: Optional[str] = None, amount: Optional[float] = None):

    conn = sqlite3.connect('internal')
    cursor = conn.cursor()

    # SQL query to fetch all records from the People table
    sql = "UPDATE People SET balance = balance - ? WHERE account_number = ?"

    try:

        cursor.execute(sql, (amount, account_number))
        conn.commit()

        print(f"Updated balance for account number {account_number}.")

        return JSONResponse(content={"transaction_ok": True}, status_code=200)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback any changes if an error occurs
        return JSONResponse(content={"transaction_ok": False}, status_code=400)

    finally:
        # Close the cursor and connection to the database
        cursor.close()
        conn.close()




