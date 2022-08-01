import time
import types
import json
from warnings import warn
from typing import List, Tuple, Callable
from functools import wraps, partial, reduce, update_wrapper
from sagemaker.estimator import EstimatorBase
#from airflow.models import Variable


## Dummy Class (from airflow.models import Variable)
class AirflowVariable(dict):
    def set(self, k, v):
        self[k] = v
        warn("Dummy airflow variable using now...")
Variable = AirflowVariable()
## Dummy Class End


def override(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class BaseWrapper:
    """
    * def __init__(self, *args, **kwargs): parameter definition
    * def wrap(self, func: Callable): actual implementation
    """
    def __repr__(self):
        class_name = self.__class__.__name__
        parameters = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith("_"))
        return f"{class_name}({parameters})"
    
    def wrap(self, func: Callable):
        raise NotImplementedError("Subclass of BaseWrapper must implement wrap method")


class RetryWrapper(BaseWrapper):
    def __init__(self, max_tries: int, wait: int or float, is_exponential: bool, exceptions: List[BaseException] or Tuple[BaseException]):
        self.max_tries = max_tries
        self.wait = wait
        self.is_exponential = is_exponential
        self.exceptions = exceptions
        
    @override
    def wrap(self, func: Callable):
        # initialize
        retry = 0
        last_exception = None
        
        # run within loop
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if type(e) in self.exceptions:
                    retry += 1
                else:
                    retry = self.max_tries
                    
                if retry < self.max_tries:
                    seconds = (self.wait ** retry) if self.is_exponential else self.wait
                    time.sleep(seconds)
                    print(f"... retrying ({retry})")
                else:
                    break
        
        # throw exception, when retry exceeded
        raise last_exception


class DynamicTrainWrapper(BaseWrapper):
    def __init__(self, estimator: EstimatorBase, env_name: str, airflow_variable: str, dynamic_run_types: List[str]):
        self.estimator = estimator
        self.env_name = env_name
        self.airflow_variable = airflow_variable
        self.dynamic_run_types = dynamic_run_types
        
    @override
    def wrap(self, func: Callable):
        # get current run type
        last_run_index = self.dynamic_run_types.index(
            Variable.get(self.airflow_variable, self.dynamic_run_types[-1])
        )
        current_run_index = (last_run_index + 1) % len(self.dynamic_run_types)
        current_run_type = self.dynamic_run_types[current_run_index]
        
        # set environment
        if self.estimator.__dict__.get("environment") is None:
            self.estimator.environment = {}
        self.estimator.environment[self.env_name] = current_run_type
        
        # run estimator
        ret = func(*args, **kwargs)
        
        # save last run type
        Variable.set(self.airflow_variable, current_run_type)
        return ret


class WrappedFunction:
    def __init__(self, function: Callable):
        """
        Order of wrappers is important in some cases.
        They are wrapping target function sequentially.
        
        Example 1)
            `f.set_wrappers(retry_wrapper, some_wrapper)`
        
        This means `some_wrapper(retry_wrapper(target_function))`.
        So, this cannot be run some_wrapper twice.
        
        Example 2)
            `f.set_wrappers(some_wrapper, retry_wrapper)`
        
        This means `retry_wrapper(some_wrapper(target_function))`.
        So, this can be run some_wrapper as times of retrying.
        
        In conclusion, I recommend you to use like this: `f.set_wrappers(inner_wrapper, outer_wrapper)`
        """
        self.function = function
        self.wrappers = tuple()
        update_wrapper(self, function)
        
    def __call__(self, *args, **kwargs):
        _init = partial(self.function, *args, **kwargs)
        _reducer = lambda func, wrapper: partial(wrapper.wrap, func=func)
        return reduce(_reducer, self.wrappers, _init)()

    def __repr__(self):
        def json_default(obj):
            if isinstance(obj, types.BuiltinFunctionType) or isinstance(obj, types.FunctionType):
                return obj.__qualname__
            elif isinstance(obj, types.BuiltinMethodType) or isinstance(obj, types.MethodType):
                return obj.__func__.__qualname__
            elif isinstance(obj, BaseWrapper):
                return str(obj)
            else:
                raise TypeError('not JSON serializable')
        attrs = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return f"{self.__class__.__name__} {json.dumps(attrs, indent=4, default=json_default)}"
        
    def set_wrappers(self, *wrappers: BaseWrapper):
        self.wrappers = wrappers


if __name__ == "__main__":
    class DummyEstimator():
        def fit(self):
            """
            test docstring
            """
            import random
            if random.random() > 0.5:
                raise ValueError
            else:
                return 1

    estimator = DummyEstimator()

    f = WrappedFunction(estimator.fit)
    f.set_wrappers(
        RetryWrapper(max_tries=3, wait=1, is_exponential=False, exceptions=[ValueError]),
        DynamicTrainWrapper(estimator=estimator, env_name="TRAIN_TYPE", airflow_variable="TEST_FLAG", dynamic_run_types=["A", "B"]),
    )
    f()
