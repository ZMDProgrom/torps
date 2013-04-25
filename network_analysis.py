import matplotlib
import matplotlib.pyplot
import os.path
import numpy
import cPickle as pickle
from pathsim import *

def linear_regression(x, y):
    """Does single linear regression on input data.
    Returns coefficients for line ax+b and r^2 coefficient."""
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    coefs, residuals, rank, s = numpy.linalg.lstsq(A, y)
    a, b = coefs
    y_avg = float(sum(y)) / len(y)
    ss = 0
    for i in xrange(len(y)):
        ss += (y[i] - y_avg)**2
    r_squared = 1 - residuals[0]/float(ss)
    return (a, b, r_squared)


def get_network_stats_from_output(filename):
    """Read in stats from output of
    pathsim_analysis.network_analysis_print_guards_and_exits()."""
    initial_guards = {}
    exits_tot_bw = {}
    
    in_reading = False
    with open(filename) as f:
        # read past initial lines showing network states files read
        while True:
            line = f.readline()
            if (line[0:5] == 'Using') or (line[0:7] == 'Filling'):
                in_reading = True
            if in_reading and (line[0:5] != 'Using') and (line[0:7] != 'Filling'):
                print('Left reading: {0}'.format(line))
                break
        # get past headers
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while (line[0:3] != 'Top'):
            line_split = line.split()
            id = int(line_split[0])
            if line_split[1]:
                prob = float(line_split[1])
            else:
                print('ERR: {0}'.format(id))
            uptime = int(line_split[2])
            if line_split[3]:
                cons_bw = float(line_split[3])
            else:
                print('ERR: {0}'.format(id))
            if line_split[4]:
                avg_average_bw = float(line_split[4])
            else:
                print('ERR: {0}'.format(id))
            if line_split[5]:
                avg_observed_bw = float(line_split[5])
            else:
                print('ERR: {0}'.format(id))
            fingerprint = line_split[6]
            nickname = line_split[7] 
            initial_guards[fingerprint] = {\
                'nickname':nickname,
                'prob':prob,
                'uptime':uptime,
                'cons_bw':cons_bw,
                'avg_average_bandwidth':avg_average_bw,
                'avg_observed_bandwidth':avg_observed_bw}
            line = f.readline()
        print('Reading exits')
        # get past next header
        line = f.readline()
        for line in f:
            line_split = line.split()
            id = int(line_split[0])
            if line_split[1]:
                tot_prob = float(line_split[1])
            else:
                print('ERR tot_prob: {0}'.format(id))            
            if line_split[2]:
                max_prob = float(line_split[2])
            else:
                print('ERR max_prob: {0}'.format(id))        
            if line_split[3]: 
                min_prob = float(line_split[3])
            else:
                print('ERR min_prob: {0}'.format(id))
            if line_split[4]:        
                avg_cons_bw = float(line_split[4])
            else:
                print('ERR avg_cons_bw: {0}'.format(id))
            if line_split[5]:        
                avg_average_bw = float(line_split[5])
            else:
                print('ERR avg_average_bw: {0}'.format(id))
            if line_split[6]:
                avg_observed_bw = float(line_split[6])
            else:
                print('ERR avg_observed_bw: {0}'.format(id))        
            uptime = int(line_split[7])
            fingerprint = line_split[8]
            nickname = line_split[9]
            exits_tot_bw[fingerprint] = {\
                'tot_prob':tot_prob,
                'nickname':nickname,
                'max_prob':max_prob,
                'min_prob':min_prob,
                'tot_cons_bw':avg_cons_bw,
                'tot_average_bandwidth':avg_average_bw,
                'tot_observed_bandwidth':avg_observed_bw,
                'uptime':uptime}
    return (initial_guards, exits_tot_bw)

def plot_against_consensus_bw(initial_guards, exits_tot_bw, out_dir):
    """Plot consensus bw against some other values."""
    guard_cons_bw = []
    guard_prob = []
    guard_avg_avg_bw = []
    guard_avg_obs_bw = []
    for fprint, guard in initial_guards.items():
        guard_cons_bw.append(guard['cons_bw'])
        guard_prob.append(guard['prob'])
        guard_avg_avg_bw.append(guard['avg_average_bandwidth'])
        guard_avg_obs_bw.append(guard['avg_observed_bandwidth'])
    fig = matplotlib.pyplot.figure()
    ax = subplot(111)
    ax.scatter(guard_cons_bw, guard_prob, label='prob')
    ax.set_xscale('log')
    ax.set_yscale('log')
    #matplotlib.pyplot.xlim(xmin=0.0)
    #matplotlib.pyplot.ylim(ymin=0.0)
    #matplotlib.pyplot.show()
    out_file = 'guard_cons_bw-prob.2013.01.01.pdf'
    out_path = os.path.join(out_dir, out_file)
    matplotlib.pyplot.savefig(out_path)
        
    fig = matplotlib.pyplot.figure()
    ax = matplotlib.pyplot.subplot(111)
    ax.scatter(guard_cons_bw, guard_avg_avg_bw, label='avg avg bw')
    ax.set_xscale('log')
    ax.set_yscale('log')
    #matplotlib.pyplot.xlim(xmin=0.0)
    #matplotlib.pyplot.ylim(ymin=0.0)    
    out_file = 'guard_cons_bw-avg_avg_bw.2013.01.01.pdf'
    out_path = os.path.join(out_dir, out_file)
    matplotlib.pyplot.savefig(out_path)
        
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.scatter(guard_cons_bw, guard_avg_obs_bw,
        label='avg obs bw')
    matplotlib.pyplot.xlim(xmin=0.0)
    matplotlib.pyplot.ylim(ymin=0.0)    
    out_file = 'guard_cons_bw-avg_obs_bw.2013.01.01.pdf'
    out_path = os.path.join(out_dir, out_file)
    matplotlib.pyplot.savefig(out_path)
    
    # linear regression on this data
    (a, b, r_squared) = linear_regression(guard_cons_bw, guard_avg_obs_bw)
    line_x1 = 0
    line_y1 = b
    line_x2 = max(x)
    line_y2 = a*line_x2 + b
    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.scatter(guard_cons_bw, guard_avg_obs_bw,
        label='avg obs bw')
    matplotlib.pyplot.plot([line_x1, line_x2], [line_y1, line_y2])
    matplotlib.pyplot.xlim(xmin=0.0)
    matplotlib.pyplot.ylim(ymin=0.0)  
    out_file = 'guard_cons_bw-avg_obs_bw-lstsq.2013.01.01.pdf'
    out_path = os.path.join(out_dir, out_file)
    matplotlib.pyplot.savefig(out_path)
   
    
def find_needed_guard_bws():
    """Find consensus values and matching bandwidth that would give you some
    fraction of guard selection prob."""
    filename = 'out/analyze/network/analyze.network.2013-01--03.out'
    out_dir = 'out/analyze/network/'       
#    (initial_guards, exits_tot_bw) = get_network_stats_from_output(filename)
#    plot_against_consensus_bw(initial_guards, exits_tot_bw, out_dir)

    initial_guards_file = \
        'out/analyze/network/initial_guards.2013-01--03.pickle'
    f = open(initial_guards_file)
    initial_guards = pickle.load(f)
    f.close()
    exits_tot_bw_file = \
        'out/analyze/network/exits_tot_bw.2013-01--03.pickle'
    f = open(exits_tot_bw_file)
    exits_tot_bw = pickle.load(f)
    f.close()

    ns_file = 'out/network-state/slim-filtered/network-state-2013-01/2013-01-01-00-00-00-network_state'
    f = open(ns_file)
    consensus = pickle.load(f)
    f.close()

    guard_cons_bw = []
    guard_prob = []
    guard_avg_avg_bw = []
    guard_avg_obs_bw = []
    for fprint, guard in initial_guards.items():
        guard_cons_bw.append(guard['rel_stat'].bandwidth)
        guard_prob.append(guard['prob'])
        guard_avg_avg_bw.append(float(guard['tot_average_bandwidth'])/\
            float(guard['uptime']))
        guard_avg_obs_bw.append(float(guard['tot_observed_bandwidth'])/\
            float(guard['uptime']))
    
    desired_prob = .1
    needed_weighted_cons_bw = 0
    guard_weights = get_position_weights(initial_guards.keys(),
                    consensus.relays, 'g', consensus.bandwidth_weights, 
                    consensus.bwweightscale)
    tot_cons_bw = 0
    for fprint, guard in initial_guards.items():
        tot_cons_bw += guard_weights[fprint]
    needed_weighted_cons_bw = desired_prob * float(tot_cons_bw) / (1-desired_prob)
    adv_guard_flags = [stem.Flag.FAST, stem.Flag.GUARD, stem.Flag.RUNNING, \
                stem.Flag.STABLE, stem.Flag.VALID]
    adv_bw_weight = get_bw_weight(adv_guard_flags, 'g',
        consensus.bandwidth_weights)    
    needed_cons_bw = needed_weighted_cons_bw *\
        float(consensus.bwweightscale)/adv_bw_weight
        
    # linear regression on this data
    (a, b, r_squared) = linear_regression(guard_cons_bw, guard_avg_obs_bw)
    needed_bw = a*needed_cons_bw + b       
        
### Output:
### a = 299.45192815560563
### b = 1104612.6683457776
### r_squared = 0.74124917207592156
### needed_cons_bw = 365924.087681159
### needed_bw = 110681286.28304975

    return (needed_cons_bw, needed_bw)


if __name__ == '__main__':
    (needed_cons_bw, needed_bw) = find_needed_guard_bws()

    in_dir = 'out/network-state/fat/ns-2013-01--03'
    
    network_state_files = []
    for dirpath, dirnames, filenames in os.walk(in_dir, followlinks=True):
        for filename in filenames:
            if (filename[0] != '.'):
                network_state_files.append(os.path.join(dirpath,filename))
    
    network_state_files.sort(key = lambda x: os.path.basename(x))
    exits_cons_bws = []
    exits_obs_bws = []
    
    need_fast = True
    need_stable = False
    need_internal = False
    
    consensus = None
    for ns_file in network_state_files:
        print('Using file {0}'.format(ns_file))
        with open(ns_file, 'r') as nsf:
            consensus = pickle.load(nsf)
            descriptors = pickle.load(nsf)
            cons_rel_stats = {}
            
            for relay in consensus.routers:
                if (relay in descriptors):
                    cons_rel_stats[relay] = consensus.routers[relay]
                    
        # get exit relays - with no ip:port in mind, we just look for
        # not policy_is_reject_star(exit_policy) 
        # with sum of weighted selection probabilities
        exits = filter_exits(cons_rel_stats, descriptors, need_fast,\
            need_stable, need_internal, None, None)    
        for fprint in exits:
            exits_cons_bws.append(cons_rel_stats[fprint].bandwidth)
            exits_obs_bws.append(descriptors[fprint].observed_bandwidth)