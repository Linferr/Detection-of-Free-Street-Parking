import subprocess
import time

def run_script():
    while True:
        try:
            subprocess.run(['python', 'database/updateAllData.py']) # path to updateAllData.py
            print("Script executed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(120)  # sleep for 120 seconds

if __name__ == "__main__":
    run_script()
