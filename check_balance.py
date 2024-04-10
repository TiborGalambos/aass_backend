import sqlite3
from fastapi.responses import JSONResponse
from fastapi import FastAPI

app = FastAPI()
from typing import Optional


@app.get("/check_balance/")
async def check_balance(account_number: Optional[str] = None, amount: Optional[float] = None):
    conn = sqlite3.connect('internal')
    cursor = conn.cursor()

    # SQL query to fetch all records from the People table
    query = "SELECT * FROM People"

    try:
        print(f"Received account number: {account_number}, amount: {amount}")

        cursor.execute(query)
        accounts = cursor.fetchall()

        for account in accounts:
            if account[3] == account_number:
                if int(account[4]) - int(amount) > 0:
                    return JSONResponse(content={'valid': 'ok',
                                                 "amount": 'ok'
                                                 }, status_code=200)
                else:
                    return JSONResponse(content={'valid': 'ok',
                                                 "amount": 'malo'
                                                 }, status_code=400)



    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return JSONResponse(content={"valid": 'not valid', "amount": 'n/a'}, status_code=400)


    finally:
        cursor.close()
        conn.close()
