# import random
# import string
#
#
# class InternalDB:
#     def __init__(self):
#         self.people = []
#         random.seed(2)
#         self.__generate_random_internal_users()
#
#     def get_people(self):
#         return self.people
#
#     def __generate_random_account_number(self):
#         return ''.join(random.choices(string.digits, k=10))
#
#     def __generate_random_balance(self):
#         return round(random.uniform(1000.00, 10000.00), 2)
#
#     def __generate_random_internal_users(self):
#         for i in range(10):
#             person = {
#                 "name": f'user{i}',
#                 "surname": f'surname{i}',
#                 "account_number": self.__generate_random_account_number(),
#                 "balance": self.__generate_random_balance()
#             }
#             self.people.append(person)
#         return self.people
