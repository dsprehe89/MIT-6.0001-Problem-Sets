"""
Created on Sun Apr  5 19:16:36 2020

@author: Daniel
MIT 6.0001 Problem Sets

"""

''' PROBLEM SET 0 '''
# import math

# x = int(input('Enter number x: '))
# y = int(input('Enter number y: '))

# print(f'x**y = {x**y}')
# print(f'log(x) = {math.log(x, 2)}')


''' PROBLEM SET 1 '''
''' Part A '''
# portion_down_payment = 0.25
# current_savings = 0
# months = 0
# annual_salary = int(input('Enter your starting salary: '))
# portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
# total_cost = int(input('Enter the cost of your dream home: '))

# while current_savings < (total_cost * portion_down_payment):
#     months += 1
#     current_savings += ((annual_salary/12) * portion_saved) + (current_savings*0.04/12)

# print(f'Number of months: {months}')


''' PROBLEM SET 1 '''
''' Part B '''
# portion_down_payment = 0.25
# current_savings = 0
# investment_return = 0.04
# annual_salary = int(input('Enter your current salary: '))
# portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
# total_cost = int(input('Enter the cost of your dream home: '))
# semi_annual_raise = float(input('Enter the semiannual raise, as a decimal: '))
# months = 0

# while current_savings < (total_cost * portion_down_payment):
#     months += 1
#     current_savings += ((annual_salary/12) * portion_saved) + (current_savings*investment_return/12)
#     if months % 6 == 0:
#         annual_salary = annual_salary * (1 + semi_annual_raise)

# print(f'Number of months: {months}')


''' PROBLEM SET 1 '''
''' Part C '''
# portion_down_payment = 0.25
# investment_return = 0.04
# total_cost = 1000000
# semi_annual_raise = 0.07
# portion_saved = 0
# savings_goal = total_cost * portion_down_payment

# low = 7500
# high = 10000
# guesses = 0
# guess = None

# start_salary = int(input('Enter your starting salary: '))

# while high <= 10000 and low >= 0:
#     current_savings = 0
#     annual_salary = start_salary

#     guesses += 1
#     guess = int((low + high) / 2)
#     portion_saved = guess / 10000.0

#     for i in range(1,37):
#         if i % 6 == 0:
#             annual_salary = annual_salary * (1 + semi_annual_raise)
#         current_savings += ((annual_salary/12) * portion_saved) + (current_savings*investment_return/12)

#     if abs(current_savings - savings_goal) < 100:
#         print(f'Best savings rate: {round(portion_saved, 4)}')
#         print(f'You saved: ${int(current_savings)}')
#         print(f'Steps in bisection search: {guesses}')
#         break
#     elif high - low <= 1:
#         print('You\'ve exceeded your maximum number of guesses')
#         print('It is not possible to pay the down payment in three years.')
#         break
#     elif (current_savings - savings_goal) > 100:
#         high = guess
#     elif (savings_goal - current_savings) > 100:
#         low = guess
