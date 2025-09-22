'''
Last updated 16.09.2025 by piiamt
THE GOAL is to have a sizeable nest egg in a company investment fund. Every year
I remove a portion from the fund, pay the income tax and then use the remainder
as a salary to live off of, allowing me to retire earlier than age 70 while still
having health insurance because of paying this out as a salary with all the taxes.
This program takes into account an inflation of 3% and a yearly accumulating 
interest of 7% (though the actual average stock market yearly return from 1993-2024 
has been 9% but I like to be careful).
'''
import numpy as np
import matplotlib.pyplot as plt


minimumbruto = 10632 # minimum yearly wage at 2025
taxfreemin = 9312   # yearly income tax free minimum at 2025

# WAGES TAXES
# The wages goal is to only pay out the minimum wage (886€ in 2025) to optimise taxes
# First the income tax free minimum is omitted, this is 776€ in 2025
# So if X is neto, Z is bruto and Y is total employer expenses we have
# Y = Z + 0.33Z + 0.008Z                    # 33% social tax & 0.8% unemployed insurance
# X = Z - (Z - taxfreemin - 0.036Z) * 0.22  # 2% pension + 1.6% unemployment + 22% income tax
# DIVIDENDS TAXES
# Dividends are only taxed by income tax, 22% in 2025
# so getting rid of Z we get Y=1.338Z and X=Z-(z-taxfreemin-0,036Z)*0.22

def yearstep(year, nestegg, monthly, inflation, stonks, tax):
    '''
    Takes a year step of pension
    INPUTS: 
    year    : the current simulation year
    nestegg : the current nest egg funds
    monthly : the desired monthly post-tax income at 2025 value
    inflation : yearly inflation factor, usually 3%
    stonks  : yearly stock market increase percentage, assumed 7-9%
    tax     : income tax percentage, in 2025 is 22%
    OUTPUTS:
    newnestegg        : the nest egg after removing wages and adding stock income
    newmonthlyneto    : the monthly post-tax income at 'year' value
    newmonthlyexpense : the total monthly expense at 'year' value
    dividend          : the yearly dividend taken out from the company investment
    '''
    # monthly is the amount of money total that we want to receive post-tax
    # newmonthly is the monthly at 'year' after inflation has eaten away at value
    newmonthly = monthly * (1 + inflation/100)**(year-2025)
    newyearly = newmonthly*12
    minbruto = minimumbruto * (1 + inflation/100)**(year-2025)
    minneto = minbruto - (0.964*minbruto - taxfreemin)*tax/100
    # dividend is how much dividends I have to take out to achieve 'newmonthly'
    # with paying income tax on the dividend.
    # Since newyearly = minnneto + (100%-tax%)dividend we get that
    dividend = (newyearly - minneto) / (100 - tax)
    newmonthlyneto = newmonthly#(minneto + 0.75*dividend)/12
    newmonthlyexpense = (dividend + 1.338*minbruto)/12
    # Companies do not pay income tax!
    newnestegg = nestegg - 12*newmonthlyexpense
    # then assume that the reduced nest egg grows from stonks:
    newnestegg = newnestegg * (1 + stonks/100)
    return(newnestegg, newmonthlyneto, newmonthlyexpense, dividend)

def pensionsim(ognestegg, monthly, year1, inflation, stonks, tax, endyear):
    '''
    Utilises 'yearstep' to simulate pension from year1 to endyear
    INPUTS: 
    ognestegg : the starting nest egg funds
    monthly : the desired monthly post-tax income at 2025 value
    year1   : the starting year of the simulation
    inflation : yearly inflation factor, usually 3%
    stonks  : yearly stock market increase percentage, assumed 7-9%
    tax     : income tax percentage, in 2025 is 22%, assumed 25%
    endyear : the ending year of the simulation aka death
    OUTPUTS:
    nesteggs        : the nest egg funds array over the years
    monthlynetos    : the monthly post-tax income array over the years
    monthlyexpenses : the total monthly expense to the company over the years
    dividends       : the yearly dividend taken out from the company investment over the years
    years           : the years array
    '''
    nesteggs = np.array([])
    # assume pension ends at year 'endyear' so
    years = np.linspace(year1, endyear, num=(endyear-year1+1))
    monthlynetos = np.array([])
    monthlyexpenses = np.array([])
    dividends = np.array([])
    nestegg = ognestegg
    for year in years:
        nestegg, newmonthly, newmonthlyexpense, dividend = yearstep(year, nestegg, monthly,
                                                                    inflation, stonks, tax)
        nesteggs = np.append(nesteggs, nestegg)
        monthlynetos = np.append(monthlynetos, newmonthly)
        monthlyexpenses = np.append(monthlyexpenses, newmonthlyexpense)
        dividends = np.append(dividends, dividend)
    return(nesteggs, monthlynetos, monthlyexpenses, dividends, years)

def optimise(ognestegg, monthly, startyear, inflation, stonks, tax, endyear, x):
        '''
        Incrementally finds the optimal ognestegg value, starting with a guess value
        Maximum number of increments is currently set to 30, if this is reached it is 
        possible to get a bad result (negative end fund value), thus x is printed at end
        Inputs and outputs are the same as pensionsim with an added x for recursion count
        '''
        nesteggs, monthlynetos, monthlyexpenses, dividends, years = pensionsim(ognestegg, 
                monthly, startyear, inflation, stonks, tax, endyear)
        if (nesteggs[-1]<(0.75*max(nesteggs)))&(nesteggs[-1]>nesteggs[0])|(x>=30):
            # Attempt to find solution with end nest egg between 75% of max and more than at start
            print('Solution found at value', ognestegg, 'at iteration', x)
            return(nesteggs, monthlynetos, monthlyexpenses, dividends, years, ognestegg)
        elif (nesteggs[-1]>=(0.75*max(nesteggs)))&(x<=30):
            ognestegg = round(ognestegg*0.98, -1)
            x = x + 1
            return(optimise(ognestegg, monthly, startyear, inflation, stonks, tax, endyear, x))
        elif (nesteggs[-1]<=nesteggs[0])&(x<=30):
            ognestegg = round(ognestegg*1.02, -1)
            x = x + 1
            return(optimise(ognestegg, monthly, startyear, inflation, stonks, tax, endyear, x))
        elif x>30:
            print('MISTAKES HAVE HAPPENED',ognestegg)
            return(nesteggs, monthlynetos, monthlyexpenses, dividends, years, ognestegg)