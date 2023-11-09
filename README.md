# Using the standalone docker evaluator
## Overview
This tool allows participants to stand up their own evaluation environment that is the same as ours (except for the codalab queue delivery). 

### Prerequisites
Docker

## Usage Guide
The worker.py takes 4 arguments, all required.
* --solutionfolder is the folder containing your custom starter kit solution
* --scenariofolder is the folder containing the test scenarios
* --airliftlibrary is the folder containing the version of the airlift environment you wish to use, this is separate from what might be installed on your own computer
* --hostmountfolder is the output folder you want the evaluator to put your results into

## Instructions
1. Download the newest airlift challenge scenario:
* git clone https://github.com/airlift-challenge/airlift.git
2. Download the newest starter kit if you don't already have it:
* git clone https://github.com/airlift-challenge/airlift-starter-kit.git
3. Get sample scenarios:
* wget https://airliftchallenge.com/scenarios/scenarios_dev.zip

## Example command
worker.py --solutionfolder fullpathofmysolutionfolder --scenariofolder fullpathofmyscenariofolder --airliftlibrary fullpathofairliftenvfolder --hostmountfolder fullpathofoutputfolder
## Troubleshooting
After making any changes or updates to the airlift library, you should delete the docker image created by using docker image rm eval, and stop and remove any associated running containers to ensure the image builds with the new code.

Notes: There's no need to install anything except docker, but having a local instance of the airlift environment may speed up development.

Distribution Statement A: Approved for Public Release; Distribution Unlimited: Case Number AFRL-2023-5705, CLEARED on 8 Nov 2023
