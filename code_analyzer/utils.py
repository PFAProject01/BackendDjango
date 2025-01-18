import subprocess
import json

class PythonScriptExecutor:
    @staticmethod
    def execute_script(java_code):
        python_path = r'C:\Users\ayoub\AppData\Local\Programs\Python\Python313\python.exe'
        script_path = r'C:\Users\ayoub\Desktop\S==9\ace\project\analyze_java_django\code_analyzer\analyze_code.py'

        result = subprocess.run(
            [python_path, script_path],
            input=java_code.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout = result.stdout.decode('utf-8').strip()
        stderr = result.stderr.decode('utf-8').strip()
        print("Script stdout:", stdout)  # Debug output
        print("Script stderr:", stderr)  # Debug output

        if result.returncode != 0:
            raise Exception(f"Python script error: {stderr}")

        return json.loads(stdout)
