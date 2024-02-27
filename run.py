

import Utils.toolkit as toolkit, Utils.helpers as helpers

from instagrapi import Client, exceptions
import requests, os, time, random, argparse
from colorama import Fore

argParser = argparse.ArgumentParser(description='Instagram cross refrence tool')

argParser.add_argument('-f', '--fix', help='fix any issues with the session, if you run into any API errors or somthing thats isnt handled in the code you can run with -f/--fix to fix any possible issues', action='store_true')
argParser.add_argument('-a', '--savedAccount', help='show the account that is currently saved in the sessions', action='store_true')
argParser.add_argument('-p', '--proxy', help='pass in a porxy you want to send the requests through. (<ip>/<port>/<username>/<pass>)')

parsedArgObj = argParser.parse_args()

def main(tarUsername: str) -> bool:
	helpersObj.Default.printInfo(f"Gathering target account info => {tarUsername}")


	tarInfo = toolkitObj.getAccountInfo(tarUsername)

	helpersObj.Default.printArgsInfo(Target_Username=tarInfo.username, Target_PK=tarInfo.pk, Target_Followers=tarInfo.follower_count, Target_Following=tarInfo.following_count)


	toolkitObj.handlePrivateStatus(tarInfo)
 

	time.sleep(random.randint(10, 15))


	mutuals = toolkitObj.crossReferenceAccounts(tarInfo.pk)
	
	time.sleep(random.randint(10, 15))
 

	tarPostLikers = toolkitObj.crossReferencePostsLikers(tarInfo.pk, mutuals)
	

	if not tarPostLikers:
		helpersObj.Default.printError("No posts found on target account, exiting...")



	commonQ = toolkitObj.pharseMisc(mutuals["mutuals"])

	
	Rating = toolkitObj.calcRating(mutuals, tarPostLikers)


	if Rating <= 0 and Rating >= 40 :
		print(Fore.YELLOW + f"[Result] This account is most likely fake. {Fore.RED}RATING: {Rating}% ")
	elif Rating <= 40 and Rating >= 60:
		print(Fore.YELLOW + f"[Result] This account is less likely not fake. {Fore.RED}RATING: {Rating}% ")
	elif Rating <= 60 and Rating >= 100:
		print(Fore.GREEN + f"[Result] This account is most likely real. {Fore.RED}RATING: {Rating}% ")
	else:
		print(Fore.YELLOW + f" + [Result] {Fore.RED}RATING: {Rating}% ")
  
	outputLeads = helpersObj.Default.getUserInput("would you like to see the details of the leads?")	
	print("Coming Soon (:")
 
if __name__ == '__main__':

	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
  
	clientObj = Client()

	helpersObj = helpers.IOFuncs()

	toolkitObj = toolkit.tools(clientObj)

	for _ in helpersObj.Default.banner.splitlines():
		print(_)
		time.sleep(0.1)
	helpersObj.Default.printInfo("Welcome to Kuro's Instagram cross refrence tool!")
	helpersObj.Default.printInfo("This tool will allow you to cross refrence a target's followers, following, and posts to see how real an account is")

	if parsedArgObj.fix:
		helpersObj.Default.printInfo("Fixing session...")
		if toolkitObj.__fix__():
			helpersObj.Default.printSuccess("Session fixed! You can now log in again.")
		else: helpersObj.Default.printError(f"Session error! Unable to fix session.")
		
	if parsedArgObj.savedAccount:
		savedUsername = toolkitObj.__getSavedAccount__()
		if savedUsername != "": helpersObj.Default.printInfo(f"Saved account: {savedUsername}"); exit(0)
		else: helpersObj.Default.printError(f"There is no saved account!"); exit(0)
  
	if parsedArgObj.proxy:
		ip, port, username, password = parsedArgObj.proxy.split(":")
		proxyString = f"http://{username}:{password}@{ip}:{port}"
		beforeIp = clientObj._send_public_request("https://api.ipify.org/")
		clientObj.set_proxy(proxyString)
		afterIp = clientObj._send_public_request("https://api.ipify.org/")
		if beforeIp != afterIp: helpersObj.Default.printSuccess(f"Proxy set to {ip}:{port}")
  
	target = helpersObj.Default.getTextInput("Enter the target username you want info on")

	try:  

		toolkitObj.sessionSetup()
	
		main(target)
	except exceptions.BadPassword: helpersObj.Default.printError("Bad password!")
	except exceptions.ClientNotFoundError: helpersObj.Default.printError("The username used to login was not found!")
	except exceptions.ChallengeRequired: helpersObj.Default.printError("Challenge error! Please log in on the web and try again.")
	except requests.exceptions.HTTPError: helpersObj.Default.printError("Request error! Could be any issue with the request. Please log in on the web to see any possible issues.")
	except exceptions.ChallengeUnknownStep: helpersObj.Default.printError("Challenge error! Please log in on the web and try again.")
	except exceptions.UserNotFound: helpersObj.Default.printError("Username not found! Please enter a valid username.")








