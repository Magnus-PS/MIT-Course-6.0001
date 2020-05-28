#initialize state variables
mos = 0
portion_down_payment = 0.25  # portion of cost needed for down payment (ie. 25%)
current_savings = 0.0
r = 0.04 #4% annual rate of return on investments
monthly_salary = 0.0

#---ALL INPUTS TAKEN BELOW ---
#annual salary of the User
annual_salary = input('Enter your annual salary: \n')
annual_salary = float(annual_salary)

#portion_saved will be the percent saved each month to be set aside for down payment
portion_saved = input('Enter the percent of your salary to save, as a decimal: \n')
portion_saved = float(portion_saved)

#the total cost of your dream home
total_cost = input('Enter the cost of your dream home: \n')
total_cost = float(total_cost)

#calculate down_payment for dream home
down_payment = total_cost * portion_down_payment

#calculate monthly salary and update current_savings
monthly_salary = annual_salary / 12
while current_savings < down_payment:
    # update current savings per return on investment and salary
    current_savings += (current_savings * r / 12) + (monthly_salary * portion_saved)
    mos += 1

print('Number of months: ' + str(mos))