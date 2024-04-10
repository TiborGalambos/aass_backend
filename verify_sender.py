import sqlite3
from fastapi.responses import JSONResponse
from fastapi import FastAPI
app = FastAPI()
from typing import Optional

@app.get("/verify_sender/")
async def verify_sender(account_number: Optional[str] = None):

    conn = sqlite3.connect('internal')
    cursor = conn.cursor()

    # SQL query to fetch all records from the People table
    query = "SELECT * FROM People"

    try:
        print(f"Received account number: {account_number}")

        cursor.execute(query)
        accounts = cursor.fetchall()

        for account in accounts:
            if account[3] == account_number:
                return JSONResponse(content={"valid": True}, status_code=200)

        return JSONResponse(content={"valid": False}, status_code=400)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return JSONResponse(content={"valid": False}, status_code=400)


    finally:
        cursor.close()
        conn.close()





