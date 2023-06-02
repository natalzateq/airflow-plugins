import inspect
import os

class PythonPodOperatorTest:
    def __init__(self, python_callable):  
        self.python_callable = python_callable  
        
    def podOperatorTest(self):
        func_path = os.path.abspath(inspect.getfile(self.python_callable)) 
        return func_path 