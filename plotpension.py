'''
Last updated 16.09.2025 by piiamt
Here are different ways of plotting the results of pension.py
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator,
                               FormatStrFormatter,
                               AutoMinorLocator,
                               FuncFormatter)

from pension import optimise

plt.rcParams.update({'font.size'           : 9,#10, 
                     'mathtext.fontset'    : 'cm',
                     'font.family'         : 'serif',
                     'xtick.direction'     :'in',
                     'ytick.direction'     :'in',
                     'grid.alpha'          : 0.7,
                     'grid.linestyle'      : 'dashed',
                     'axes.linewidth'      : 0.7,
                     'xtick.minor.width'   : 0.7,
                     'ytick.minor.width'   : 0.7,
                     'xtick.major.width'   : 0.7,
                     'ytick.major.width'   : 0.7
                    })
colors = np.array(['k', '#009e73', '#d55e00', '#cc79a7', '#0072b2', '#e69f00', '#56b4e9'])
mm = 1/25.4

def plotsimulation(nesteggs, monthlynetos, monthlyexpenses, dividends, years):
    fig, ax = plt.subplots(1,4, figsize=(240*mm,90*mm))
    ax[0].plot(years, nesteggs, color=colors[1])
    ax[2].plot(years, monthlynetos, color=colors[2])
    ax[1].plot(years, monthlyexpenses, color=colors[3], 
               label='Total expense')
    ax[1].plot(years, dividends/12, color=colors[4],
               label='Dividends')
    ax[1].plot(years, monthlyexpenses-dividends/12, color=colors[5],
               label='Wage expenses')
    ax[3].plot(years, (dividends/12*100)/monthlyexpenses, color=colors[4])
    # plot 0 bc funds must not drop below it
    ax[0].plot([years[0], years[-1]], [0,0], ls='--', color='k', alpha=0.5)
    ax[0].set_xlabel('Year')
    ax[1].set_xlabel('Year')
    ax[2].set_xlabel('Year')
    ax[3].set_xlabel('Year')
    ax[0].set_title('Nest egg funds')
    ax[2].set_title('Monthly post-tax (neto)')
    ax[1].set_title('Monthly expenses')
    ax[1].legend()
    ax[3].set_title('Dividends percentage of total expense')
    ax[0].ticklabel_format(axis='both', style='plain')
    fig.tight_layout()
    plt.show()

def plot4sims(nesteggses, yearses, monthlys, startyears, ognesteggs):
    fig, ax = plt.subplots(2,2, figsize=(152*mm,140*mm))
    ax[0,0].plot(yearses[0][0], nesteggses[0][0], color=colors[0], 
                 label=format(round(ognesteggs[0]), ','))
    ax[0,0].set_title(str(monthlys[0])+' monthly')
    ax[0,1].plot(yearses[1][0], nesteggses[1][0], color=colors[1], 
                 label=format(round(ognesteggs[1]), ','))
    ax[0,1].set_title(str(monthlys[1])+' monthly')
    ax[1,0].plot(yearses[2][0], nesteggses[2][0], color=colors[2], 
                 label=format(round(ognesteggs[2]), ','))
    ax[0,0].set_ylabel('Start '+str(startyears[0]))
    ax[1,1].plot(yearses[3][0], nesteggses[3][0], color=colors[3], 
                 label=format(round(ognesteggs[3]), ','))
    ax[1,0].set_ylabel('Start '+str(startyears[2]))
    for a in ax.flatten():
        a.legend()
        a.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    fig.tight_layout()
    plt.savefig('C:/Users/Piia/Documents/CODE/PYTHON/plots/9stonkspension_2035_2040.pdf', bbox_inches='tight')
    plt.show()

### CONTANTS AND ASSUMPTIONS FOR SIMULATION
inflation = 3
stonks = 9
tax = 25
endyear = 2096
monthlys = np.array([2000, 3000, 2000, 3000])
startyears = np.array([2035, 2035, 2040, 2040]) #np.array([2025, 2025, 2030, 2030]) #
ognesteggs = np.array([360000, 400000, 400000, 400000])

### RUN SIMULATIONS
nesteggses = []
yearses = []
ogs = np.array([])

for i in range(4):
    nesteggs, monthlynetos, monthlyexpenses, dividends, years, og = optimise(ognesteggs[i], 
                monthlys[i], startyears[i], inflation, stonks, tax, endyear, 0)
    nesteggses.append(np.array([nesteggs]))
    yearses.append(np.array([years]))
    ogs = np.append(ogs, og)


plot4sims(nesteggses, yearses, monthlys, startyears, ogs)
print(yearses[0], len(yearses[0][0]))
