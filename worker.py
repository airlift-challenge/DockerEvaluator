#!/usr/bin/env python
import sys
import urllib
import subprocess

import argparse
import json
import logging.config
import os
import uuid

#import psutil
import signal
import math
import re
import shutil
import socket
import tempfile
import time
import traceback

import requests

from os.path import join, exists
from glob import glob
from subprocess import Popen, call, check_output, CalledProcessError, PIPE

parser = argparse.ArgumentParser(description='Tool to run eval on solution code in a docker container similar to the official evaluation environment.')
parser.add_argument('--solutionfolder', required = True, help = "Folder containing solution")
parser.add_argument('--scenariofolder', required = True, help = "Folder containing scenarios")
parser.add_argument('--airliftlibrary', required = True, help = "Folder containing the airlift environment")
parser.add_argument('--hostmountfolder', required = True, help = "Folder to send detailed results to.")
args = parser.parse_args()
logger = logging.getLogger()

def do_docker_pull(image_name, task_id, secret):
    logger.info("Running evaluation docker build for image: {}".format(image_name))
    print("building the image")
    try:
        subproc_args = ['docker', 'build', '--build-arg', 'NB_USER=airliftuser',
               '--build-arg', 'NB_UID=1001', '-t', image_name, '-f', './submissionDF', '.']
        build_process = subprocess.Popen(subproc_args)
        logger.info("Started build process, pid=%s" % build_process.pid)
        build_process.wait()
    except CalledProcessError as error:
        logger.info("Docker evaluation build for image: {} returned a non-zero exit code!".format(image_name))


def run_repo(submission_id, docker_mount_folder, container_name, user_name):
    subproc_args = ["docker",
                    "run",
                    "--name", container_name,
                    "--rm",
                    "--net=host",
                    "--pull=never",
                    "--env", "AICROWD_TESTS_FOLDER=/home/" + user_name + "/test_folder",
                    "--env", "PYTHONPATH=${PYTHONPATH}:/home/" + user_name + "/airlift-main",
                    "-v", args.hostmountfolder + ":" + "/home/" + user_name + "/output_folder/eval",
                    "--security-opt=no-new-privileges",
                    "--entrypoint", "python", "eval:latest", "./run_eval_and_client.py", "none", "0"]
    logger.info("Invoking program: %s", " ".join(subproc_args))
    evaluator_process = subprocess.Popen(subproc_args)
    logger.info("Started evaluation process, pid=%s" % evaluator_process.pid)
    evaluator_process.wait()
    return evaluator_process

def delete_evaluation_image():
    subproc_args = ["docker", "image", "rm", "eval", "-f"]
    create_repo = subprocess.Popen(subproc_args)
    create_repo.wait()

class ExecutionTimeLimitExceeded(Exception):
    pass


def alarm_handler(signum, frame):
    raise ExecutionTimeLimitExceeded

def convert_crlf():
    logger.info("Converting crlf line endings to lf")
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    for root, dirnames, filenames in os.walk('./submission_folder/run/input/code_for_eval'):
        for f in filenames:
            full_path = os.path.join(root, f)
            with open(full_path, 'rb') as open_file:
                content = open_file.read()
            content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
            with open(full_path, 'wb') as open_file:
                open_file.write(content)
                
def copy_files():
    shutil.copytree(args.solutionfolder, "./submission_folder/run/input/code_for_eval/")
    shutil.copytree(args.scenariofolder, "./scenarios")
    shutil.copytree(args.airliftlibrary, "./airlift")
    
def run():
    # Set folders / files
    try:
    	shutil.rmtree("./submission_folder/")
    	shutil.rmtree("./scenarios")
    	shutil.rmtree("./airlift")
    except OSError:
        print("Folders don't exist, ignoring deletion.")
        
    os.makedirs("./submission_folder/run/input/")
    copy_files ()  
    # output_dir = "./output_folder"
    output_name = "output"
    output_ext = "zip"
    docker_mount_folder = "/output_folder"
    log_dir = "./logs"
    output_dir = "./" + docker_mount_folder + "/eval"
    eval_container_name = "eval"

    convert_crlf()

    #delete_evaluation_image()
    do_docker_pull('eval', 0, 0)
    startTime = time.time()
    
    evaluator_process = run_repo(0, docker_mount_folder, eval_container_name, "airliftuser")
    time_difference = time.time() - startTime
    #signal.signal(signal.SIGALRM, alarm_handler)
    #signal.alarm(int(math.fabs(math.ceil(execution_time_limit - time_difference))))

def main():
    run()

if __name__ == "__main__":
    main()

