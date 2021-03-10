from datetime import datetime


class ETA:
    def __init__(self, total_length: int):
        self.init_time = datetime.now()
        self.total_length = total_length

    def __call__(self, current_position: int):
        if current_position:
            cur_time = datetime.now()
            rest_length = self.total_length - current_position
            per_time = (cur_time - self.init_time) / current_position
            return cur_time + (rest_length * per_time)
        
        else:
            return float('inf')


class TimeElapsed:
    def __init__(self, desc=None):
        self.desc = desc if desc else 'No desc'

    def __enter__(self):
        self.begin_at = datetime.now()
        print(f"[Begin] {self.desc}")

    def __exit__(self, type, value, tb):
        print(f"[End] {self.desc} ({datetime.now() - self.begin_at} elapsed)")
