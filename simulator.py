import numpy as np
from queue import PriorityQueue


class Task:
    def __init__(self, time, simulator, server):
        self.time = time
        self.simulator = simulator
        self.server = server

    def __lt__(self, other):
        return self.time < other.time


class ArrivalTask(Task):
    def __init__(self, time, simulator, server):
        super().__init__(time, simulator, server)

    def process(self):
        if self.server.busy:
            if self.server.is_full():
                self.simulator.rejected += 1
            else:
                self.server.enqueue(self)
        else:
            self.server.busy = True
            service_time = np.random.exponential(1 / self.server.μ)
            exit_time = self.time + service_time
            self.simulator.schedule(
                ServiceTask(
                    self.time, exit_time, service_time, self.simulator, self.server
                )
            )


class ServiceTask(Task):
    def __init__(self, arrival_time, time, service_time, simulator, server):
        super().__init__(time, simulator, server)
        self.arrival_time = arrival_time
        self.service_time = service_time

    def process(self):
        self.simulator.accepted += 1
        # Update wait_time and service_time
        self.simulator.wait_time += self.time - self.service_time - self.arrival_time
        self.simulator.service_time += self.service_time
        # If there are unprocessed Arrival Tasks, process the first one
        if self.server.queue:
            service_time = np.random.exponential(1 / self.server.μ)
            task = self.server.dequeue()
            self.simulator.schedule(
                ServiceTask(
                    task.time,
                    self.time + service_time,
                    service_time,
                    self.simulator,
                    self.server,
                )
            )
        else:
            self.server.busy = False


class Server:
    def __init__(self, queue_size, μ):
        self.queue_size = queue_size
        self.queue = []
        self.busy = False
        self.μ = μ

    def enqueue(self, task):
        self.queue.append(task)

    def dequeue(self):
        return self.queue.pop(0)

    def is_full(self):
        return len(self.queue) >= self.queue_size


class Simulator:
    def __init__(self, T, N, P, λ, Q, μ):
        # Input parameters
        self.time_limit = T
        self.N = N
        self.P = P
        self.λ = λ
        self.Q = Q
        self.μ = μ

        # Output parameters
        self.accepted = 0
        self.rejected = 0
        self.wait_time = 0
        self.service_time = 0

        # Simulation objects
        self.curr_time = 0
        self.servers = []
        self.task_queue = PriorityQueue()

    def initialize_simulation(self):
        self.servers = [Server(self.Q[i], self.μ[i]) for i in range(self.N)]
        time = 0
        self.schedule(
            ArrivalTask(time, self, self.servers[np.random.choice(self.N, p=self.P)])
        )
        while time < self.time_limit:
            time += np.random.exponential(1 / self.λ)
            self.schedule(
                ArrivalTask(
                    time, self, self.servers[np.random.choice(self.N, p=self.P)]
                )
            )

    def run(self):
        self.initialize_simulation()

        while not self.task_queue.empty():
            task = self.task_queue.get()
            self.curr_time = task.time
            task.process()

    def schedule(self, task):
        self.task_queue.put(task)

    def print_results(self):
        if self.accepted > 0:
            avg_wait_time = self.wait_time / self.accepted
            avg_service_time = self.service_time / self.accepted
        else:
            avg_wait_time = avg_service_time = 0
        print(
            f"{self.accepted} {self.rejected} {self.curr_time} {avg_wait_time} {avg_service_time}"
        )
