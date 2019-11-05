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
	command = "git branch | grep \* | cut -d ' ' -f2"
	return os.popen(command).read().strip()

def checkGitBranchExists(name):
	branchFilter = "\s" + name + "$"
	command = "git branch | grep '" + branchFilter + "'"
	grepResult = os.popen(command).read()
	return len(grepResult) > 0

def checkoutGitBranch(name):
	command = "git checkout " + name
	os.system(command)

def newGitBranch(name):
	print("Creating bracnh: " + newBranchName)
	command = "git checkout -b " + name
	os.system(command)	

def checkGitBranchHasRemote(branchName):
	command = "git branch -vv | grep '" + branchName + "' | grep origin"
	print(command)
	grepResult = os.popen(command).read()
	return len(grepResult) > 0
	
def pushRemoteBranch(branchName):
	command = "git push --set-upstream origin " + branchName
	os.system(command)	

#*** Model

def checkIfTicketIdCorrect(ticketId):
	return len(ticketId) > 0 # For now just check it's not empty

def checkIfTicketDescription(ticketDescription):
	return len(ticketDescription) > 0 # For now just check it's not empty

def generateBranchName(ticketId, ticketDescription):
	niceDescription = "_".join(ticketDescription.split())
	return "fix/" + ticketId.upper() + "_" + niceDescription

def descriptionFromBranchName(branchName):
	branchNameWithoutPrefix = branchName.replace("fix/", "").replace("feature/", "")
	niceDescription = branchNameWithoutPrefix.replace("_", " ")
	return niceDescription


#*** Github utility functions

def openPrWebPageWithBaseBranch(baseBranch, branchName, title):
	# https://github.com/octo-org/octo-repo/compare/master...pull-request-test?quick_pull=1&body=Fixes+the+problem.
	preparedBody = "+".join(title.split())
	url = githubUrl() + "/compare/" + baseBranch + "..." + branchName + "?quick_pull=1&title=" + preparedBody
	print("opening url " + url)
	command = "open '" + url + "'"
	os.system(command)

def openPrWebPage(branchName):
	url = githubUrl() + "/pull/new/" + branchName
	command = "open " + url
	os.system(command)

def githubUrl():
	command = "git config --get remote.origin.url"
	remoteResult = os.popen(command).read()
	#As we use ssh clone we will recive something like this -  git@github.com:readdle/spark-client.git
	#and we need this "https://github.com/readdle/spark-client/pull/new/"
	result = "https://github.com/" + remoteResult.replace('.git', "").split(':')[1].strip()
	return result


#*** WorkBranch utility functions

branchFileName = ".workBranch"

def save_workBranch(branch_name):
    with open(branchFileName + '.pkl', 'wb') as f:
        pickle.dump(branch_name, f, pickle.HIGHEST_PROTOCOL)

def load_workBranch():
    with open(branchFileName + '.pkl', 'rb') as f:
        return pickle.load(f).strip()

def tryToSaveCurrentBranch(name):
	if checkGitBranchExists(name):
		print("Branch '" + name + "' set as new working branch")
		save_workBranch(name)
	else:
		print("Bad branch name, '" + name + "' doesn't exist in repo")
		exit(1)

def isWorkBranchNow():
	branchName = load_workBranch()
	if branchName is None:
		print("Work branch not set!")
		exit(1)
	return getCurrentGitBranch() == branchName

#*** Small Helpers

def die(errorText):
	print(errorText)
	exit(1)

#*** App Arguments Setup

parser = argparse.ArgumentParser(description='A little helper for git flow!')
group = parser.add_mutually_exclusive_group()
group.add_argument("--work-branch", type=str, help="Set default working branch")
group.add_argument("--work", action='store_true', help="Switch default working branch")
group.add_argument("--new-ticket", action='store_true', help="Create new ticket branch")
group.add_argument("--new-pr", action='store_true', help="Create new pr on github")

#*** App Flow

args = parser.parse_args()

newWorkBranch = args.work_branch
if newWorkBranch is not None:
	tryToSaveCurrentBranch(newWorkBranch)
	exit(0)

if args.work:
	if isWorkBranchNow():
		print("Already work branch")
		exit(0)
		
	checkoutGitBranch(load_workBranch())

if args.new_ticket:
	if isWorkBranchNow() == False:
		die("Not work branch branch")

	ticketId = raw_input("Enter Ticket Id : ") 
	if checkIfTicketIdCorrect(ticketId) == False:
		die("Bad Ticket Id")

	ticketDescription = raw_input("Enter Ticket Description : ") 
	if checkIfTicketDescription(ticketDescription) == False:
		die("Bad Ticket Description")


	newBranchName = generateBranchName(ticketId, ticketDescription)
	newGitBranch(newBranchName)

if args.new_pr:
	if isWorkBranchNow():
		die("You should create separate branch")

	currentBranch = getCurrentGitBranch()
	if checkGitBranchHasRemote(currentBranch) == False:
		print("no remote branch - pushing")
		pushRemoteBranch(currentBranch)
	# openPrWebPage(currentBranch)
	openPrWebPageWithBaseBranch(load_workBranch(), currentBranch, descriptionFromBranchName(currentBranch))







	
		