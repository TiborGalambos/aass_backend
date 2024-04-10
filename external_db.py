# import random
# import string
# import sqlite3
#
# class ExternalDB:
#     def __init__(self):
#         self.accounts = []
#         random.seed(2)
#         # self.__generate_random_internal_users()
#         self.__load_internal_users()
#
#     def get_accounts(self):
#         return self.accounts
#
#     # def __generate_random_account_number(self):
#     #     return ''.join(random.choices(string.digits, k=10))
#
#     # def __generate_random_internal_users(self):
#     #     for i in range(10):
#     #         account = {
#     #             "account_number": self.__generate_random_account_number(),
#     #         }
#     #         self.accounts.append(account)
#     #     return self.accounts
#
#     def __load_internal_users(self):
#
#
#
#         # Connect to the SQLite database
#         # Replace 'your_database.db' with the path to your actual SQLite database file
#         conn = sqlite3.connect('external')
#         cursor = conn.cursor()
#
#         # SQL query to fetch all records from the People table
#         query = "SELECT * FROM People"
#
#         try:
#             cursor.execute(query)
#             accounts = cursor.fetchall()  # Fetches all rows from the result of the query
#
#
#         except sqlite3.Error as e:
#             print(f"An error occurred: {e}")
#
#         finally:
#             # Close the cursor and connection to the database
#             cursor.close()
#             conn.close()
#
