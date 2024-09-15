import builtins
import inspect

class MalformedOutputError(Exception):
    pass

class EvaluationError(Exception):
    pass

class TaskError(Exception):
    pass

class SubmissionError(Exception):
    pass

class TimeLimitExceeded(Exception):
    pass

class MemoryLimitExceeded(Exception):
    pass

class PackageError(Exception):
    pass

builtin_exceptions = [obj for name, obj in inspect.getmembers(builtins, inspect.isclass)
                      if issubclass(obj, BaseException) and obj is not BaseException]
