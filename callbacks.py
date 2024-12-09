import time


class Retriable:
    """
    [Example]
    (
        Retriable(max_tries=5)
        .retry_when(sagemaker.exceptions.CapacityError)
        .retry_when(sagemaker.exceptions.UnexpectedClientError, sagemaker.exceptions.UnexpectedStatusException)
        .not_retry_when(IndexError)
        .execute(estimator.fit)
    )
    """
    def __init__(self, max_tries: int):
        self.max_tries = max_tries
        self.exceptions = set()
        
    def retry_when(self, *exceptions: Exception):
        self.exceptions.update(exceptions)
        return self
      
    def not_retry_when(self, *exceptions: Exception):
        self.exceptions.difference_update(exceptions)
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

