import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt
import math


def FSim1(n, l):
    return np.array([np.random.exponential(1.0 / l) for i in range(n)])


def funnel_vis(n, start, stop, increment):
    for l in np.arange(start, stop + increment, increment):
        steps = float(stop - start) / increment + 1
        sims = FSim1(n, l)
        x_min, x_max = 0, math.ceil(max(sims) / 0.25) * 0.25
        breakpoints = np.arange(0.0, x_max, 0.25)
        dist = [sum([1 if val > float(time) else 0 for val in sims]) for time in breakpoints]

        plt.suptitle('Survival Rates', fontsize = 20)
        plt.subplot(math.ceil(np.sqrt(steps)), math.ceil(np.sqrt(steps)), (l - start) / increment + 1)
        plt.title('$\lambda$ = ' + str(l))
        plt.scatter(breakpoints, dist, marker = 'o', s = 30)
        #plt.plot(np.arange(0.0, x_max, 0.25), dist)
        plt.bar(breakpoints, dist, 0.001)
        plt.axis([-0.05, 5.0, -50, 1100])

    plt.show()


## question 2
def FSim2(quit_times, breakpoints):
    breakpoints = sorted(list(set([0.0] + breakpoints + [np.inf])))
    return np.array([sum([1 if quit_time < breakpoints[i] and quit_time >= breakpoints[i - 1] else 0 for quit_time in quit_times]) for i in range(1, len(breakpoints))])

funnel_vis(1000, 2, 3, 0.25)
funnel_vis(1000, .2, 3.0, 0.2)
print FSim2([0.2, 0.2, 0.4], [0.25, 0.5])

## question 3
def bootstrap(sample, num_bootstraps):
    return np.array([np.mean(np.random.choice(sample, len(sample), replace = True)) for i in range(num_bootstraps)])


def EstLam1(simulations, num_bootstraps):
    return 1.0 / np.mean(bootstrap(simulations, num_bootstraps))


estimates = []
lowerCI = []
upperCI = []

n_user_range = [100, 200, 500, 1000, 2000, 5000, 10000]

def plotLambdaEstCI(n_user_range):
    for n_users in n_user_range:
        sample = bootstrap(FSim1(n_users, 1), 500)
        estMu = 1.0/np.mean(sample)
        estimates.append(estMu)
        lowerCI.append(estMu + 1.96*np.std(sample))
        upperCI.append(estMu - 1.96*np.std(sample))
        print np.array([estMu - 1.96*np.std(sample), estMu, estMu + 1.96*np.std(sample)])

    plt.plot(n_user_range, lowerCI, color = 'blue')
    plt.plot(n_user_range, estimates, color = 'red', linewidth = 2)
    plt.scatter(n_user_range, estimates, color = 'red', marker = 'o', s=15)
    plt.plot(n_user_range, upperCI, color = 'blue')
    plt.suptitle('$\lambda$ estimate and 95% CI', fontsize=20)
    plt.show()

plotLambdaEstCI(n_user_range)

## question 4
def MLE1(counts, breakpoints):
    return lambda l: counts[0] * np.log(1 - np.exp(-l * breakpoints[0])) \
                     + np.dot(counts[1:-1], [np.log(np.exp(-l * breakpoints[i]) - np.exp(-l * breakpoints[i + 1])) for i in range(len(breakpoints) - 1)]) \
                     - l * counts[-1] * breakpoints[-1]


def MaxMLE(counts, breakpoints, l_range):
    return max([(l, MLE1(counts, breakpoints)(l)) for l in l_range], key = lambda p: p[1])[0]


simulations = [FSim1(100, 1) for i in range(1000)]
breakpoints_list = [[.25, .75], [.25, 3], [.25, 10]]
l_range = np.arange(.1, 5, .05)

print [np.mean([abs(EstLam1(simulation, 500) - MaxMLE(FSim2(simulation, breakpoints), breakpoints, l_range)) for simulation in simulations]) for breakpoints in breakpoints_list]
