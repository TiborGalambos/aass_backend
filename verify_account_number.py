import sqlite3

from fastapi import FastAPI
app = FastAPI()
from fastapi.responses import JSONResponse


@app.get("/verify_receiver/{account_number}")
async def verify_receiver(account_number: int):
    conn = sqlite3.connect('external')
    cursor = conn.cursor()

    # SQL query to fetch all records from the People table
    query = "SELECT * FROM People"

    try:
        cursor.execute(query)
        accounts = cursor.fetchall()

        print(type(accounts))
        print(accounts)
        print(account_number)

        for account_num in accounts:
            if str(account_num[1]) == str(account_number):
                return JSONResponse(content={"valid": True}, status_code=200)
        return JSONResponse(content={"valid": False}, status_code=400)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return JSONResponse(content={"valid": False}, status_code=400)

    finally:
        cursor.close()
        conn.close()






