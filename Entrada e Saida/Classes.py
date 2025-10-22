class Process:
    def __init__(self, creation_time, pid, exec_time, priority, mem_qty, sequence, io_chance):
        self.creation_time = creation_time
        self.pid = pid
        self.exec_time = exec_time
        self.priority = priority
        self.mem_qty = mem_qty
        self.sequence = sequence
        self.io_chance = io_chance
        self.state = 'ready'

        self.io_device = None
        self.io_remain = 0
        self.completion_time = 0
        self.ready_state_time = -exec_time
        self.blocked_state_time = 0
        self.times_page_changed = 0

    def __repr__(self):
        return f'C_TIME: {self.creation_time} PID: {self.pid} EXEC_TIME: {self.exec_time} PRIORITY: {self.priority} MEM_QTY: {self.mem_qty} SEQUENCE: {self.sequence}'
    
    def repr(self):
        return f'PID : {self.pid} | Completion Time : {self.completion_time} | Ready State Time : {self.ready_state_time} | Blocked State Time : {self.blocked_state_time}'
    
    def finalInfo(self, completion_tick):
        self.completion_time = completion_tick - self.creation_time
        self.ready_state_time += self.completion_time - self.blocked_state_time

class Environment:
    def __init__(self, algorithm, quantum, mem_policy, mem_size, page_size, aloc_percentual):
        self.algorithm = algorithm
        self.quantum = quantum
        self.mem_policy = mem_policy
        self.mem_size = mem_size
        self.page_size = page_size
        self.aloc_percentual = aloc_percentual

    def __repr__(self):
        return f'Informações da página:\nPolítica : {self.mem_policy}\nTamanho memória: {self.mem_size}\nTamanho página : {self.page_size}\nPercentual de alocação : {self.aloc_percentual}'