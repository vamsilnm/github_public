# compare_colors.py
# v 1.0  30 April 2016 [KL]

######################
#
# Submission by Kendrick Lo (Harvard ID: 70984997) for
# AM 207 - Stochastic Methods for Data Analysis, Inference and Optimization
#
# Course Project
#
######################

# runs a comparison of the different algorithms for a particular
# set of game parameters
# to run, execute: python compare.py

import numpy as np
import time
import matplotlib.pyplot as plt

# individual algorithms
import knuth as kn  # Knuth algorithm
import randomsearch as rs  # Random search with constraints algorithm
import annealing as sa  # Simulated annealing
import entropy as e # Maximize information generated by guess
import genetic as ga

# supress warnings related to log(0) in entropy solution
np.seterr(divide='ignore')

# variable alphabet sizes (cardinality)
alphabet_sizes = [4, 5, 6, 7, 8, 9, 10]  # [4, 6, 8, 10]

# code length size (anything bigger than 6 can take very long to run)
length_sizes = [4]

# output modes
silent_mode = True  # detailed output for each iteration
summary_stats = True  # print number of guesses and time for each iteration

# store results of number of guesses and time, indexed by algorithm
# value is a list, first element is a tuple (digits, positions)
results = {}  # Algoname: [((digits, positions), guesses, time) ... ]

# number of simulations to average over
nsims = 20

for c in alphabet_sizes:

    for l in length_sizes:

        print "\n----------------------------------------------"
        print "possible colors: %i, number of positions: %i" % (c, l)
        print "----------------------------------------------"

        # generate random code for use in all algorithms
        secret = np.random.randint(0, c, size=l)

        ################
        print "\n*** KNUTH'S ALGORITHM ***"

        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)

        for i in range(nsims):
            start = time.time()
            cnt[i] = kn.knuth(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start

        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)

        if "knuth" not in results:
            results["knuth"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["knuth"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        ################

        ################
        print "\n*** RANDOM SEARCH UNDER CONSTRAINTS ***"

        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)

        for i in range(nsims):
            start = time.time()
            cnt[i] = rs.random_search(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start

        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)

        if "random_search" not in results:
            results["random_search"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["random_search"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        #################

        ################
        print "\n*** MAXIMIZING ENTROPY (ALL STEPS) ***"
        
        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)
        
        for i in range(nsims):
            start = time.time()
            cnt[i] = e.entropy_all(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start
        
        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)
        
        if "entropy-all" not in results:
            results["entropy-all"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["entropy-all"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        ################

        ################
        print "\n*** MAXIMIZING ENTROPY (EXCEPT FIRST STEP) ***"
        
        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)
        
        for i in range(nsims):
            start = time.time()
            cnt[i] = e.entropy_minusone(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start
        
        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)
        
        if "entropy-minusone" not in results:
            results["entropy-minusone"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["entropy-minusone"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        ################

        #################
        print "\n*** SIMULATED ANNEALING (BERNIER OBJECTIVE FUNCTION) ***"

        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)

        for i in range(nsims):
            start = time.time()
            cnt[i] = sa.SAsim().runSA(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start

        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)

        if "SA-bernier" not in results:
            results["SA-bernier"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["SA-bernier"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        #################

        ################
        print "\n*** SIMULATED ANNEALING (ENTROPY OBJECTIVE FUNCTION) ***"
        
        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)
        
        for i in range(nsims):
            start = time.time()
            cnt[i] = e.SAentropy().runSA(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start
        
        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)
        
        if "SA-entropy" not in results:
            results["SA-entropy"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["SA-entropy"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        ################

        ################
        print "\n*** GENETIC ALGORITHMS (BERNIER OBJECTIVE FUNCTION) ***"

        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)

        for i in range(nsims):
            start = time.time()
            cnt[i] = ga.GAsim().runGA(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start
        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)

        if "GA-bernier" not in results:
            results["GA-bernier"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["GA-bernier"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        ################

        ################
        print "\n*** GENETIC ALGORITHMS (ENTROPY OBJECTIVE FUNCTION) ***"

        cnt = np.zeros(nsims)
        runtime = np.zeros(nsims)

        for i in range(nsims):
            start = time.time()
            cnt[i] = e.GAentropy().runGA(cl=l, nc=c, code=secret, silent=silent_mode)
            runtime[i] = time.time() - start
        meancnt = np.mean(cnt)
        cnterror = np.std(cnt)
        meanrun = np.mean(runtime)
        runerror = np.std(runtime)

        if "GA-entropy" not in results:
            results["GA-entropy"] = [((c, l), meancnt, meanrun, cnterror, runerror)]
        else:
            results["GA-entropy"] += [((c, l), meancnt, meanrun, cnterror, runerror)]
        if summary_stats:
            print "avg number of guesses: %.1f (std: %.3f), avg run time: %.3f (std: %.3f)" % (meancnt, cnterror, meanrun, runerror)
        ################

##########
# results
##########

print "\n----------------------------------------------"
print "results"
print "----------------------------------------------"

print results

##########
# plots
##########

print "printing plot of number of guesses by character set (code length 4)..."
plt.figure()
plt.title("Number of Guesses (fixed code length 4)")
plt.xlabel("characters")
plt.ylabel("guesses")
plt.xlim(3, 11, 1)
plt.ylim(1, 11, 1)
for model in results.keys():
    # ((c, l), cnt, runtime)
    points_x, points_y, err = [], [], []
    for point in results[model]:
        if point[0][1] == 4:  # fix to standard length
            points_x += [point[0][0]]
            points_y += [point[1]]
            err += [point[3]]
    plt.errorbar(points_x, points_y, yerr=err, label=model)
plt.legend(loc="best")
plt.show()

print "printing plot of execution time by character set (code length 4)..."
plt.figure()
plt.title("Execution Time (fixed code length 4)")
plt.xlabel("characters")
plt.ylabel("execution time (seconds)")
plt.xlim(3, 11, 1)
for model in results.keys():
    # ((c, l), cnt, runtime)
    points_x, points_y, err = [], [], []
    for point in results[model]:
        if point[0][1] == 4:  # fix to standard length
            points_x += [point[0][0]]
            points_y += [point[2]]
            err += [point[4]]
    plt.ylim(0, 5)
    plt.errorbar(points_x, points_y, yerr=err, label=model)
plt.legend(loc="best")
plt.show()