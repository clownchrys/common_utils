import time


class Retriable:
    """
    [Example]
    (
        Retriable(max_tries=5)
        .attach_exc(sagemaker.exceptions.CapacityError)
        .attach_exc(sagemaker.exceptions.UnexpectedClientError)
        .attach_exc(sagemaker.exceptions.UnexpectedStatusException)
        .detach_exc(IndexError)
        .execute(estimator.fit)
    )
    """
    def __init__(self, max_tries: int):
        self.max_tries = max_tries
        self.exceptions = set()
        
    def attach_exc(self, exc: Exception):
        self.exceptions.add(exc)
        return self
      
    def detach_exc(self, exc: Exception):
        if exc in self.exceptions:
            self.exceptions.remove(exc)
        return self
    
    def execute(self, f, *args, **kwargs):
        retry = 0
        exc = None
        while retry < self.max_tries:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                exc = e
                if type(e) in self.exceptions:
                    retry += 1
                    time.sleep(2 ** retry)
                else:
                    retry = max_retry
        raise exc

