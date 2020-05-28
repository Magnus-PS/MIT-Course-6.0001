#initialize default variables
semi_annual_raise = 0.07
r = 0.04 #4% annual rate of return on investments
down_payment = 250000 #hard-coded 1000000 * 0.25 to compress space
current_savings = 0
savingsRate = 0.50

#initialize counters
mos = 0
steps = 1

#set savingsRate range
min = 0
max = 10000
in_range = False

#---INPUT TAKEN BELOW ---
#starting salary of the User
starting_salary = input('Enter the starting salary: \n')
starting_salary = float(starting_salary)

#save to separate variable so it can be reset later
c_salary = starting_salary

def findRate(lower, upper):

    #bring in all variables to be modified
    global current_savings, c_salary, mos, savingsRate, min, max, steps

    while (current_savings < down_payment):

        savingsRate = ((upper + lower)/2) / 10000 #taking average of min, max and converting to decimal
        monthly_salary = c_salary / 12

        current_savings += (current_savings * r / 12) + (monthly_salary * savingsRate)
        mos += 1

        if mos != 0 and mos % 6 == 0:
            monthly_salary += monthly_salary * semi_annual_raise

while in_range == False:

    if current_savings >= down_payment - 100 and current_savings <= down_payment + 100:
        in_range = True
    else:
        #if the entered salary is below a reasonable range
        if c_salary < 79000:
            break
        # if we aren't getting there fast enough or we're below range, increase the min
        if mos > 36 or current_savings <= down_payment - 100:
            mos = 0
            current_savings = 0
            c_salary = starting_salary
            min = int(savingsRate * 10000) # set min to midpoint

        # if we're getting there too fast or we're above range, reduce the max
        elif mos < 36 or current_savings >= down_payment + 100:
            mos = 0
            current_savings = 0
            c_salary = starting_salary
            max = int(savingsRate * 10000) # set max to midpoint

        savingsRate = (min + max) // 2
        findRate(min, max) #keep re-running the function until we're in range
        steps += 1
# --- OUTPUT BELOW ---
if c_salary < 79000:
    print('It is not possible to pay the down payment in three years.')
else:
    print('Best savings rate: ' + str(savingsRate))
    print('Steps in bisection search: ' + str(steps))
