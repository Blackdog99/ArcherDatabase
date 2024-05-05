import subprocess

def run_pytest():
    # Define the command you want to run as a list of strings
    command = ["pytest","--verbose", "UnitTests\\UnitMain.py"]
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print the output and error (if any)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    # Check the return code (0 is success, non-zero indicates an error)
    if result.returncode == 0:
        print("Pytest ran successfully.")
    else:
        print("Pytest encountered an error.")

def run_db_pytest():
    # Define the command you want to run as a list of strings
    command = ["pytest","--verbose", "UnitTests\\dbtests.py"]
    
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print the output and error (if any)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    # Check the return code (0 is success, non-zero indicates an error)
    if result.returncode == 0:
        print("Pytest ran successfully.")
    else:
        print("Pytest encountered an error.")

# Call the function to execute the command
#run_pytest()
run_db_pytest
