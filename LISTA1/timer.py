from time import time

class Timer:

    def __init__(self):
        self.time = 0
        self.result = None

    def run(self, func, *args):
        start_time = time()
        self.result = func(*args)
        self.time = time() - start_time
        return self.time, self.result
    
    def create(self, clss, *args):
        start_time = time()
        self.result = clss.__init__(*args)
        self.time = time() - start_time
        return self.time, self.result
    
    def get_stats_time(self, n_times, func, *args):
        time_sum = 0.0
        min_time, max_time = float('inf'), 0.0
        for _ in range(n_times):
            self.run(func, *args)
            time_sum = time_sum + self.time
            if min_time > self.time: min_time = self.time
            elif max_time < self.time: max_time = self.time
        return time_sum / (n_times * 1.0), min_time, max_time
