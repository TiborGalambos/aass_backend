# aass_backend
uvicorn gateway:app --reload --port 8005
uvicorn change_balance:app --reload --port 8004
uvicorn check_balance:app --reload --port 8003
uvicorn verify_sender:app --reload --port 8002
verify_account_number:app --reload --port 8001
uvicorn main:app --reload --port 8000
