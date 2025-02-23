
import sys
import re
from io import StringIO
import subprocess

if __name__ == "__main__":
    from tools import Tools
else:
    from sources.tools.tools import Tools

class BashInterpreter(Tools):
    """
    This class is a tool to allow agent for bash code execution.
    """
    def __init__(self):
        super().__init__()
        self.tag = "bash"

    def execute(self, commands: str, safety = False, timeout = 1000):
        """
        Execute bash commands.
        """
        if safety and input("Execute command? y/n ") != "y":
            return "Command rejected by user."

        for command in commands:
            try:
                output = subprocess.check_output(command,
                                                 shell=True,
                                                 stderr=subprocess.STDOUT,
                                                 universal_newlines=True,
                                                 timeout=timeout
                                                )
                return output.strip()
            except subprocess.CalledProcessError as e:
                return f"Command execution failed:\n{e.output}"
            except subprocess.TimeoutExpired as e:
                return f"Command timed out. Output:\n{e.output}"

    def interpreter_feedback(self, output):
        """
        Provide feedback based on the output of the bash interpreter
        """
        if self.execution_failure_check(output):
            feedback = f"[failure] Error in execution:\n{output}"
        else:
            feedback = "[success] Execution success, code output:\n" + output
        return feedback

    def execution_failure_check(self, feedback):
        """
        check if bash command failed.
        """
        error_patterns = [
            r"expected",
            r"errno",
            r"failed",
            r"invalid",
            r"unrecognized",
            r"exception",
            r"syntax",
            r"segmentation fault",
            r"core dumped",
            r"unexpected",
            r"denied",
            r"not recognized",
            r"not permitted",
            r"not installed",
            r"not found",
            r"no such",
            r"too many",
            r"too few",
            r"busy",
            r"broken pipe",
            r"missing",
            r"undefined",
            r"refused",
            r"unreachable",
            r"not known"
        ]
        combined_pattern = "|".join(error_patterns)
        if re.search(combined_pattern, feedback, re.IGNORECASE):
            return True
        return False

if __name__ == "__main__":
    bash = BashInterpreter()
    print(bash.execute(["ls", "pwd"]))
