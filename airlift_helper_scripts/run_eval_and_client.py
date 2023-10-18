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
        #time.sleep(15)
        run_submission()
        #time.sleep(15)
    
def run_evaluator():
    subproc_args = ["redis-server", "--daemonize", "yes"]
    eval_subproc = subprocess.Popen(subproc_args)
    #eval_subproc.wait()
    #subproc_args = ["export AICROWD_TESTS_FOLDER=/home/aicrowd/tests"]
    #setExport = subprocess.Popen(subproc_args)
    #setExport.wait()
    #subproc_args = ["/home/www/flatland/flatland/evaluators/service.py", "--id", str(submission_id), "--api_key", grader_api_key, "--test_folder", TEST_FOLDER]
    print("running evaluator")
    subproc_args = ["python3", "/home/airliftuser/airlift/airlift/evaluators/service.py", "--test_folder", TEST_FOLDER, "--output_dir", "/home/airliftuser/output_folder/eval/"]
    eval_subproc = subprocess.Popen(subproc_args, cwd="/home/airliftuser/airlift")
    

def run_submission():
    print("Running the client now")
    subproc_args = ["/home/airliftuser/evaluate.sh"]
    run_proc = subprocess.Popen(subproc_args, cwd="/home/airliftuser/" )
    run_proc.wait()
 
run_eval()
