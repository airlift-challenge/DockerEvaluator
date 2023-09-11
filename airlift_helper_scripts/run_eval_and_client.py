"""
POST /api/external_graders
Create a submission record (including failed submission)
USAGE:
$ python post_external_graders.py [grader_api_key]
"""

import sys
import requests
import subprocess
import os
import _thread
import time
from datetime import date

grader_api_key = str(sys.argv[1])
submission_id = sys.argv[2]
TEST_FOLDER = "/home/airliftuser/scenarios"
INNER_FOLDER = "flatland-starter-kit"

def run_eval():
        print("running eval and client")
        run_evaluator()
        time.sleep(30)
        run_submission()
    
def run_evaluator():
    subproc_args = ["redis-server", "--daemonize", "yes"]
    eval_subproc = subprocess.Popen(subproc_args)
    print("running evaluator")
    subproc_args = ["python3", "/home/airliftuser/airlift-main/afrl/evaluators/service.py", "--test_folder", TEST_FOLDER, "--output_dir", "/home/airliftuser/output_folder/eval/"]
    eval_subproc = subprocess.Popen(subproc_args, cwd="/home/airliftuser/airlift-main")
    

def run_submission():
    print("Running the client now")
    subproc_args = ["/home/airliftuser/evaluate.sh"]
    run_proc = subprocess.Popen(subproc_args, cwd="/home/airliftuser/" )
    run_proc.wait()
 
run_eval()
