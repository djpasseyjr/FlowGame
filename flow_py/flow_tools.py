def in_interval(x: float, interval: tuple):
    """Check if the x is in the given interval."""
    return (x > min(interval)) and (x <= max(interval))

def interval_indicator_dt(interval, idx, on_true=1., on_false=-1.):
    """Creates a function that checks if the first argument at index `idx`
    is in the given interval. If it is, return `on_true` otherwise return
    `on_false`."""
    a = on_true - on_false
    b = on_false
    ddt = lambda x, t, inp: a * in_interval(x[idx], interval) + b
    return ddt

def input_switched_constants_dt(input_rate=1., no_input_rate=-1):
    """Returns an input dependent derivative function. The returned function
    switches between two constant rates depending on input. You can specify
    the two rates with the `input_rate` and `no_input_rate` arguments to
    this function."""
    flow = lambda x, t, inp: input_rate if inp else no_input_rate
    return flow
