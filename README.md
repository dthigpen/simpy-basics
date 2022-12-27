# SimPy Basics

Some useful tips to get started with the [SimPy](https://simpy.readthedocs.io/en/latest/simpy_intro/index.html) discrete event simulation library for Python.

## Creating a process

In SimPy, processes are created with Python generators. Typically by defining a generator function that yields events during its execution.

For example, let's create a process that wraps the `simpy` built-in `Environment.timeout()`.

```python
def my_proc(env, delay, name, value=None):
        print(f't={env.now} Started "{name}"')
        yield env.timeout(delay,value)
        print(f't={env.now} Finished "{name}"')
```

All we are doing here is printing the (simulation) time when the process is started, and when it finishes. Now we can create an instance and get some output when it runs:

```python
long_proc = my_proc(env, 5, 'Long process')
env.process(long_proc)
env.run()
```

Output:

```
t=0 Started "Long process"
t=5 Finished "Long process"
```

## Running processes in parallel

Running multiple processes at the same time is as simple as making multiple calls to the `env.process` function.

```python
long_proc = my_proc(env, 5, 'Long process')
short_proc = my_proc(env, 2, 'Short process')
env.process(long_proc)
env.process(short_proc)
env.run()
```
Output:
```
t=0 Started "Long process"
t=0 Started "Short process"
t=2 Finished "Short process"
t=5 Finished "Long process"
```

Notice that the order of the `env.process` calls actually does not matter, because the execution time in the sim will be the same. As a result, the short process with a `delay=2` will finish earlier.

## Running processes in series

Run multiple processes one after another requires us to wait using `yield` for each process before continuing to the next, similar to how we used `env.timeout` earlier.

```python
def series(processes):
    for p in processes:
        yield env.process(p)
```

Since we created a function to yield each process, we are actually creating a new process as a result. This new process can be queued up just like before.

```python
long_then_short_proc = series(env, [long_proc, short_proc])
env.process(long_then_short_proc)
env.run()
```

Output:

```
t=0 Started "Long process"
t=5 Finished "Long process"
t=5 Started "Short process"
t=7 Finished "Short process"
```

Notice that the first process to be queued up finishes before the next one starts.


