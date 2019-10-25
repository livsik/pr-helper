#!/usr/local/bin/python
import os
import argparse
import pickle

# Chek If we are in folder with git repo 
if os.path.exists(".git") == False:
	print("Should be used in folder with git repo") #TODO: add red color
	exit(1)


#*** Git utility functions
def getCurrentGitBranch():
	return os.popen("git branch | grep \* | cut -d ' ' -f2").read()

def checkGitBranchExists(name):
	branchFilter = "\s" + name + "$"
	grepResult = os.popen("git branch | grep '" + branchFilter + "'").read()
	return len(grepResult) > 0

#*** WorkBranch utility functions
branchFileName = ".workBranch"
def save_workBranch(branch_name):
    with open(branchFileName + '.pkl', 'wb') as f:
        pickle.dump(branch_name, f, pickle.HIGHEST_PROTOCOL)

def load_workBranch():
    with open(branchFileName + '.pkl', 'rb') as f:
        return pickle.load(f)

def tryToSaveCurrentBranch(name):
	if checkGitBranchExists(name):
		print("Branch '" + name + "' set as new working branch")
		save_workBranch(name)
	else:
		print("Bad branch name, '" + name + "' doesn't exist in repo")
		exit(1)


#*** App Arguments Setup

parser = argparse.ArgumentParser(description='A little helper for git flow!')
parser.add_argument("--work-branch", type=str, help="Set default working branch")

#*** App Flow

args = parser.parse_args()

newWorkBranch = args.work_branch
if newWorkBranch is not None:
	tryToSaveCurrentBranch(newWorkBranch)
else:
	print(load_workBranch())