import simpy

def my_proc(env, delay, name, value=None):
        print(f't={env.now} Started "{name}"')
        yield env.timeout(delay,value)
        print(f't={env.now} Finished "{name}"')

def series(env, processes):
    for p in processes:
        yield env.process(p)

if __name__ == '__main__':

    ## creating a process
    print('Creating a process')
    env = simpy.Environment()
    long_proc = my_proc(env, 5, 'Long process')
    env.process(long_proc)
    env.run()
    print()

    ## running in parallel
    print('Running processes in parallel:')
    env = simpy.Environment()
    long_proc = my_proc(env, 5, 'Long process')
    short_proc = my_proc(env, 2, 'Short process')
    env.process(long_proc)
    env.process(short_proc)
    env.run()
    print()

    ## running in series
    print('Running processes in series')
    env = simpy.Environment()
    long_proc = my_proc(env, 5, 'Long process')
    short_proc = my_proc(env, 2, 'Short process')
    long_then_short_proc = series(env, [long_proc, short_proc])
    env.process(long_then_short_proc)
    env.run()
    print()