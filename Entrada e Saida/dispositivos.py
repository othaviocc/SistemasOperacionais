class Dispositivo:
    def __init__(self, id, simultaneous_use_limit, op_time):
        self.id = id
        self.simultaneous_use_limit = simultaneous_use_limit
        self.simultaneous_use = 0
        self.op_time = op_time
        self.queue = []

    def increment_simultaneous_use(self):
        self.simultaneous_use += 1

    def decrement_simultaneous_use(self):
        self.simultaneous_use -= 1

    def add_process_queue(self, process):
        self.queue.append(process)

    def remove_process_queue(self, process):
        self.queue.remove(process)
