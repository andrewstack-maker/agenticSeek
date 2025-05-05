
import sys
import os
import re
from io import StringIO

if __name__ == "__main__": # if running as a script for individual testing
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sources.tools.tools import Tools

class PyInterpreter(Tools):
    """
    This class is a tool to allow agent for python code execution.
    """
    def __init__(self):
        super().__init__()
        self.tag = "python"
        self.name = "Python Interpreter"
        self.description = "This tool allows the agent to execute python code."

    def execute(self, codes:str, safety = False) -> str:
        """
        Execute python code.
        """
        output = ""
        if safety and input("Execute code ? y/n") != "y":
            return "Code rejected by user."
        stdout_buffer = StringIO()
        sys.stdout = stdout_buffer
        global_vars = {
            '__builtins__': __builtins__,
            'os': os,
            'sys': sys,
            '__name__': '__main__'
        }
        code = '\n\n'.join(codes)
        self.logger.info(f"Executing code:\n{code}")
        try:
            try:
                buffer = exec(code, global_vars)
                self.logger.info(f"Code executed successfully.\noutput:{buffer}")
                print(buffer)
                if buffer is not None:
                    output = buffer + '\n'
            except SystemExit:
                self.logger.info("SystemExit caught, code execution stopped.")
                output = stdout_buffer.getvalue()
                return f"[SystemExit caught] Output before exit:\n{output}"
            except Exception as e:
                self.logger.error(f"Code execution failed: {str(e)}")
                return "code execution failed:" + str(e)
            output = stdout_buffer.getvalue()
        finally:
            self.logger.info("Code execution finished.")
            sys.stdout = sys.__stdout__
        return output

    def interpreter_feedback(self, output:str) -> str:
        """
        Provide feedback based on the output of the code execution
        """
        if self.execution_failure_check(output):
            feedback = f"[failure] Error in execution:\n{output}"
        else:
            feedback = "[success] Execution success, code output:\n" + output
        return feedback

    def execution_failure_check(self, feedback:str) -> bool:
        """
        Check if the code execution failed.
        """
        error_patterns = [
            r"expected", 
            r"errno", 
            r"failed", 
            r"traceback", 
            r"invalid", 
            r"unrecognized", 
            r"exception", 
            r"syntax", 
            r"crash", 
            r"segmentation fault", 
            r"core dumped"
        ]
        combined_pattern = "|".join(error_patterns)
        if re.search(combined_pattern, feedback, re.IGNORECASE):
            self.logger.error(f"Execution failure detected: {feedback}")
            return True
        self.logger.info("No execution success detected.")
        return False

if __name__ == "__main__":
    text = """
For Python, let's also do a quick check:

```python
print("Hello from Python!")
```

If these work, you'll see the outputs in the next message. Let me know if you'd like me to test anything specific! 

here is a save test
```python:tmp.py

def print_hello():
    hello = "Hello World"
    print(hello)

if __name__ == "__main__":
    print_hello()
```
"""
    py = PyInterpreter()
    codes, save_path = py.load_exec_block(text)
    py.save_block(codes, save_path)
    print(py.execute(codes))