#!/usr/bin/python3
from os import system as shell
import re
from time import sleep as delay
try:
    import pyufw as ufw
    from colorama import Fore
except ImportError:
    shell('./setup.sh')

st = '0'
try:
	f = open('status.fw', 'rb')
	st = f.read()
	f.close()
except Exception:
	if st == '0':
		f = open('status.fw','wb')
		f.write(b'1')
		f.close()
		shell('chmod +x ./setup.sh')
		shell('./setup.sh')

def resetFirewall():
	ufw.enable()
	ufw.reset()
	ufw.disable()
	ufw.enable()
	ufw.default(incoming='deny', outgoing='allow', routed='reject')

def logo():
	print(Fore.RED+"""
 ________    _                     ________   __                                          
|_   __  |  (_)                   |_   __  | [  |                                         
  | |_ \_|  __    _ .--.   .---.    | |_ \_|  | |    .--.    _   _   __   .---.   _ .--.  
  |  _|    [  |  [ `/'`\] / /__\\   |  _|     | |  / .'`\ \ [ \ [ \ [  ] / /__\\ [ `/'`\] 
 _| |_      | |   | |     | \__.,  _| |_      | |  | \__. |  \ \/\ \/ /  | \__.,  | |     
|_____|    [___] [___]     '.__.' |_____|    [___]  '.__.'    \__/\__/    '.__.' [___]    
                                                                                          
""")
	print(r"""
                              .... 
                           ,;;'''';;,                    ,;;;;, 
                 ,        ;;'      `;;,               .,;;;'   ; 
              ,;;;       ;;          `;;,';;;,.     ,%;;'     ' 
            ,;;,;;       ;;         ,;`;;;, `;::.  %%;' 
           ;;;,;;;       `'       ,;;; ;;,;;, `::,%%;' 
           ;;;,;;;,          .,%%%%%'% ;;;;,;;   %;;; 
 ,%,.      `;;;,;;;,    .,%%%%%%%%%'%; ;;;;;,;;  %;;; 
;,`%%%%%%%%%%`;;,;;'%%%%%%%%%%%%%'%%'  `;;;;;,;, %;;; 
;;;,`%%%%%%%%%%%,; ..`%%%%%%%%;'%%%'    `;;;;,;; %%;; 
 `;;;;;,`%%%%%,;;/, .. `\"\"\"'',%%%%%      `;;;;;; %%;;, 
    `;;;;;;;,;;/////,.    ,;%%%%%%%        `;;;;,`%%;; 
           ;;;/%%%%,%///;;;';%%%%%%,          `;;;%%;;, 
          ;;;/%%%,%%%%%/;;;';;'%%%%%,             `%%;; 
         .;;/%%,%%%%%//;;'  ;;;'%%%%%,             %%;;, 
         ;;//%,%%%%//;;;'   `;;;;'%%%%             `%;;; 
         ;;//%,%//;;;;'      `;;;;'%%%              %;;;, 
         `;;//,/;;;'          `;;;'%%'              `%;;; 
           `;;;;'               `;'%'                `;;;; 
                                  '      .,,,.        `;;;; 
                                      ,;;;;;;;;;;,     `;;;; 
                                     ;;;'    ;;;,;;,    `;;;; 
                                     ;;;      ;;;;,;;.   `;;;; 
                                      `;;      ;;;;;,;;   ;;;; 
                                        `'      `;;;;,;;  ;;;; 
                                                   `;;,;, ;;;; 
                                                      ;;, ;;;; 
                                                        ';;;;; 
                                                         ;;;;; 
                                                        .;;;;' 
                                                       .;;;;' 
                                                      ;;;;;' 
                                                     ,;;;;'
""")

def miniLogo(subtit):
	print(Fore.RED+"\nFireFlower!"+Fore.MAGENTA+subtit,end='')
	print(Fore.RED+"""
 _,-._
/ \_/ \\
>-(_)-<    
\_/ \_/
  `-'
""")

def enableDisable():
	shell('clear')
	print()
	miniLogo("\n(Enable/Disable)")
	if ufw.status()['status'] == 'inactive':
		print(Fore.GREEN+"The current status is INACTIVE!")
		print(Fore.CYAN+"Do you want to ACTIVE the Firewall? (y/n) -> "+Fore.WHITE,end='')
		s = input()
		print()
		if s.lower() == 'y':
			ufw.enable()
			print(Fore.GREEN+"The Firewall is now ACTIVE")
		elif s.lower() == 'n':
			ufw.disable()
			print(Fore.GREEN+"The Firewall is now INACTIVE")
		else:
			print(Fore.RED+"ANSWER ONLY Y FOR YES OR N FOR NO!")
	elif ufw.status()['status'] == 'active':
		print(Fore.GREEN+"The current status is ACTIVE!")
		print(Fore.CYAN+"Do you want to DISABLE the Firewall? (y/n) -> "+Fore.WHITE,end='')
		s = input()
		print()
		if s.lower() == 'y':
			ufw.disable()
			print(Fore.GREEN+"The Firewall is now INACTIVE")
		elif s.lower() == 'n':
			ufw.enable()
			print(Fore.GREEN+"The Firewall is now ACTIVE")
		else:
			print(Fore.RED+"ANSWER ONLY Y FOR YES OR N FOR NO!")
	else:
		print(Fore.RED+"Unknown Error :(")
		exit(-1)
	delay(2)
	shell('clear')
	miniLogo("\n(Main Menu)")
	menu()

def showRules(rulesS):
	print(Fore.BLUE+"ACTIVE RULES -> {")
	rules = []
	for r in range(len(rulesS)):
		rules.append(rulesS[r+1])
	i = 0
	for rule in rules:
		spec = False
		prot = False
		ip = False
		i += 1
		print(Fore.GREEN+"\t("+str(i)+") ",end='')
		if 'allow' in rule:
			print(Fore.GREEN+"ALLOW ",end='')
		elif 'deny' in rule:
			print(Fore.RED+"DENY ",end='')
		elif 'limit' in rule:
			print(Fore.YELLOW+"LIMIT ",end='')
		elif 'reject' in rule:
			print(Fore.YELLOW+"REJECT ",end='')
		elif 'route' in rule:
			print(Fore.YELLOW+"ROUTE ",end='')
		if 'in' in rule:
			print(Fore.GREEN+"incoming ",end='')
		elif 'out' in rule:
			print(Fore.RED+"outgoing ",end='')
		else:
			spec = True
			print(Fore.YELLOW+"every ",end='')
		print(Fore.CYAN+"connection",end='')
		if '/t' in rule:
			prot = True		
		elif '/u' in rule:
			prot = True	
		elif bool(re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', rule)):
			ip = true
	
		if prot == False and ip == False:
			print(Fore.CYAN+" on port ",end='')
			if spec == True:
				print(Fore.YELLOW+rule.split(" ")[1])
			else:
				print(Fore.YELLOW+rule.split(" ")[2])
		elif prot == True and ip == False:
			print(Fore.CYAN+" on port ",end='')
			if spec == True:
				print(Fore.YELLOW+rule.split(" ")[1].split("/")[0],end='')
				print(Fore.CYAN+" for protocol "+Fore.YELLOW+rule.split(" ")[1].split("/")[1])
			else:
				print(Fore.YELLOW+rule.split(" ")[2].split("/")[0],end='')
				print(Fore.CYAN+" for protocol "+Fore.YELLOW+rule.split(" ")[2].split("/")[1])
		elif prot == False and ip == True:
			if spec == True:
				print(Fore.CYAN+" for the IP addresses from "+Fore.YELLOW+rule.split(" ")[2]+Fore.CYAN+" to "+Fore.YELLOW+rule.split(" ")[4])
				print(Fore.CYAN+" on port ",end='')
				print(Fore.YELLOW+rule.split(" ")[6])
			else:
				print(Fore.CYAN+" for the IP addresses from "+Fore.YELLOW+rule.split(" ")[3]+Fore.CYAN+" to "+Fore.YELLOW+rule.split(" ")[5])
				print(Fore.CYAN+" on port ",end='')
				print(Fore.YELLOW+rule.split(" ")[7])
		elif prot == True and ip == True:
			if spec == True:
				print(Fore.CYAN+" for the IP addresses from "+Fore.YELLOW+rule.split(" ")[2]+Fore.CYAN+" to "+Fore.YELLOW+rule.split(" ")[4])
				print(Fore.CYAN+" on port ",end='')
				print(Fore.YELLOW+rule.split(" ")[6])
				print(Fore.CYAN+" for protocol "+Fore.YELLOW+rule.split(" ")[6].split("/")[1])	
			else:
				print(Fore.CYAN+" for the IP addresses from "+Fore.YELLOW+rule.split(" ")[3]+Fore.CYAN+" to "+Fore.YELLOW+rule.split(" ")[5])
				print(Fore.CYAN+" on port ",end='')
				print(Fore.YELLOW+rule.split(" ")[7])
				print(Fore.CYAN+" for protocol "+Fore.YELLOW+rule.split(" ")[7].split("/")[1])
	print(Fore.BLUE+"}")
	

def showStatus():	
	shell('clear')
	miniLogo("\n(Show Status)")
	totS = ufw.status()
	able = totS['status']
	if able == 'active':
		defaul = totS['default']
		rules = totS['rules']
		print(Fore.YELLOW+"FireFlower Status =>")
		print(Fore.BLUE+"STATUS -> "+Fore.GREEN+able)
		print(Fore.BLUE+"DEFAULT RULES -> {"+Fore.CYAN+"incoming => ",end='')
		if defaul['incoming'] == 'deny':
			print(Fore.RED+defaul['incoming'],end='')
		elif defaul['incoming'] == 'reject':
			print(Fore.YELLOW+defaul['incoming'],end='')
		elif defaul['incoming'] == 'route':
			print(Fore.YELLOW+defaul['incoming'],end='')
		elif defaul['incoming'] == 'limit':
			print(Fore.YELLOW+defaul['incoming'],end='')
		else:
			print(Fore.GREEN+defaul['incoming'],end='')
		print(Fore.BLUE+" | "+Fore.CYAN+"outgoing => ",end='')
		if defaul['outgoing'] == 'deny':
			print(Fore.RED+defaul['outgoing'],end='')
		elif defaul['outgoing'] == 'reject':
			print(Fore.YELLOW+defaul['outgoing'],end='')
		elif defaul['outgoing'] == 'route':
			print(Fore.YELLOW+defaul['outgoing'],end='')
		elif defaul['outgoing'] == 'limit':
			print(Fore.YELLOW+defaul['outgoing'],end='')
		else:
			print(Fore.GREEN+defaul['outgoing'],end='')
		print(Fore.BLUE+" | "+Fore.CYAN+"routed => ",end='')
		if defaul['routed'] == 'deny':
			print(Fore.RED+defaul['routed'],end='')
		elif defaul['routed'] == 'reject':
			print(Fore.YELLOW+defaul['routed'],end='')
		elif defaul['routed'] == 'route':
			print(Fore.YELLOW+defaul['routed'],end='')
		elif defaul['routed'] == 'limit':
			print(Fore.YELLOW+defaul['routed'],end='')
		else:
			print(Fore.GREEN+defaul['routed'],end='')
		print(Fore.BLUE+"}")
		showRules(rules)
	else:
		print(Fore.YELLOW+"FireFlower Status =>")
		print(Fore.BLUE+"STATUS -> "+Fore.RED+able)
	input(Fore.CYAN+'\nPress Enter to back at Main Menu...\n'+Fore.WHITE)
	shell('clear')
	miniLogo("\n(Main Menu)")
	menu()

def how():
	shell('clear')
	miniLogo("\n(How does it work?)")
	print(Fore.GREEN+"What is it?"+Fore.YELLOW+"\nHi User!\nThis is an easy software to manage your Linux's Firewall. It allows you to create new rules, delete old ones, check the current status and lots of other features! It's still in beta, so some error may occours, but you can signal them to me and i'll fix that. It works only on Linux! based on UFW and iptables;\nNB: This is a tool very easy to use, so it doesn't have every options of iptables. Soon i'll add the rules for IP address and group of ports and protocols. This is still a beta!\n")
	input(Fore.CYAN+'\nPress Enter to back at Main Menu...\n'+Fore.WHITE)
	shell('clear')
	miniLogo("\n(Main Menu)")
	menu()

def resetta():
	shell('clear')
	miniLogo("\n(Reset FireGarden)")
	print(Fore.GREEN+"Reset Options =>"+Fore.YELLOW+"\n1) Total Reset (erase every rule and set the default ones)\n2) Base Reset (erase every rule except the ones for base services (80-8080,443,23 etc.))\n3) Delete every rule\n4) Back")
	while True:
		s = input(Fore.CYAN+"insert your choice -> "+Fore.WHITE)
		if s == '1':
			print(Fore.RED+"Resetting Firewall...")
			ufw.delete('*')
			resetFirewall()
			print(Fore.RED+"Firewall Total Resetted!")
			delay(2)
			break
		elif s == '2':
			print(Fore.RED+"Resetting Firewall...")
			rules = ufw.status()['rules']
			for r in range(len(rules)):
				if '80' in rules[r] or '8080' in rules[r] or '23' in rules[r] or '443' in rules[r] or '20' in rules[r] or '110' in rules[r] or '143' in rules[r] or '465' in rules[r] or '995' in rules[r] or '666' in rules[r]:
					pass
				else:
					ufw.delete(r)
			print(Fore.RED+"Firewall Base Resetted!")
			delay(2)
			break
		elif s == '3':
			print(Fore.RED+"Resetting Firewall...")
			ufw.delete('*')
			print(Fore.RED+"Rules Deleted!")
			delay(2)
			break
		elif s == '4':
			break
		else:
			print(Fore.GREEN+"You need to choose one of the numbers from 1 to 4!")
	shell('clear')
	miniLogo("\n(Main Menu)")
	menu()

def addRule():
	shell('clear')
	miniLogo("\n(Add a New Rule)")
	direction = ''
	directive = 'deny'
	port = '1'
	print(Fore.YELLOW+"1) Rule for "+Fore.GREEN+"incoming"+Fore.YELLOW+" connections\n2) Rule for "+Fore.RED+"outgoing"+Fore.YELLOW+" connections\n3) Rule for all connections\n4) Back")
	while True:
		s = input(Fore.CYAN+"insert your choice -> "+Fore.WHITE)
		if s == '1':
			direction = 'in'
			break
		elif s == '2':
			direction = 'out'
			break
		elif s == '3':
			direction = ''
			break
		elif s == '4':
			shell('clear')
			miniLogo("\n(Rules Editor)")
			editR()
			break
		else:
			print(Fore.GREEN+"You need to choose one of the numbers from 1 to 4!")
	print(Fore.YELLOW+"1) "+Fore.GREEN+"Allow"+Fore.YELLOW+" connections\n2) "+Fore.RED+"Deny"+Fore.YELLOW+" connections\n3) Reject connections\n4) Limit connections\n5) Route connections\n6) Back")
	while True:
		s = input(Fore.CYAN+"insert your choice -> "+Fore.WHITE)
		if s == '1':
			directive = 'allow'
			break
		elif s == '2':
			directive = 'deny'
			break
		elif s == '3':
			directive = 'reject'
			break
		elif s == '4':
			directive = 'limit'
			break
		elif s == '5':
			directive = 'route'
			break
		elif s == '6':
			shell('clear')
			miniLogo("\n(Rules Editor)")
			editR()
			break
		else:
			print(Fore.GREEN+"You need to choose one of the numbers from 1 to 6!")
	while True:
		s = input(Fore.CYAN+"insert the port -> "+Fore.WHITE)
		try:
			if int(s) > 0 and int(s) < 65536:
				port = s
				break
			else:
				print(Fore.GREEN+"You need to choose one of the numbers from 1 to 6!")
		except ValueError:
			print(Fore.GREEN+"You need to choose one of the numbers from 1 to 6!")
	print(Fore.GREEN+"Creating the New Rule...")
	if direction != '':
		NNrule = directive+" "+direction+" "+port
	else:
		NNrule = directive+" "+port
	if NNrule in ufw.status()['rules']:
		print(Fore.RED+"Impossible add the Rule, it already exists!")
	else:
		ufw.add(NNrule)
		print(Fore.GREEN+"Rule successfully added!")
	delay(2)
	shell('clear')
	miniLogo("\n(Rules Editor)")
	editR()

def rmRule():
	shell('clear')
	miniLogo("\n(Remove an existing Rule)")
	showRules(ufw.status()['rules'])
	while True:
		s = input(Fore.CYAN+"insert the number of the rule you want to delete -> "+Fore.WHITE)
		try:
			if int(s) > len(ufw.status()['rules']) and int(s) <= 0:
				print(Fore.GREEN+"It look like, this isn't a rule :(")
			else:
				print(Fore.RED+"Removing the rule...")
				ufw.delete(int(s))
				print("Rule deleted!")
				break
		except ValueError:
			print(Fore.GREEN+"It look like, this isn't a rule :(")
	delay(2)
	shell('clear')
	miniLogo("\n(Rules Editor)")
	editR()

def defRule():
	shell('clear')
	miniLogo("\n(Default Rules)")
	defaul = ufw.status()['default']
	print(Fore.BLUE+"CURRENT DEFAULT RULES -> {"+Fore.CYAN+"incoming => ",end='')
	if True:
		if defaul['incoming'] == 'deny':
			print(Fore.RED+defaul['incoming'],end='')
		elif defaul['incoming'] == 'reject':
			print(Fore.YELLOW+defaul['incoming'],end='')
		elif defaul['incoming'] == 'route':
			print(Fore.YELLOW+defaul['incoming'],end='')
		elif defaul['incoming'] == 'limit':
			print(Fore.YELLOW+defaul['incoming'],end='')
		else:
			print(Fore.GREEN+defaul['incoming'],end='')
		print(Fore.BLUE+" | "+Fore.CYAN+"outgoing => ",end='')
		if defaul['outgoing'] == 'deny':
			print(Fore.RED+defaul['outgoing'],end='')
		elif defaul['outgoing'] == 'reject':
			print(Fore.YELLOW+defaul['outgoing'],end='')
		elif defaul['outgoing'] == 'route':
			print(Fore.YELLOW+defaul['outgoing'],end='')
		elif defaul['outgoing'] == 'limit':
			print(Fore.YELLOW+defaul['outgoing'],end='')
		else:
			print(Fore.GREEN+defaul['outgoing'],end='')
		print(Fore.BLUE+" | "+Fore.CYAN+"routed => ",end='')
		if defaul['routed'] == 'deny':
			print(Fore.RED+defaul['routed'],end='')
		elif defaul['routed'] == 'reject':
			print(Fore.YELLOW+defaul['routed'],end='')
		elif defaul['routed'] == 'route':
			print(Fore.YELLOW+defaul['routed'],end='')
		elif defaul['routed'] == 'limit':
			print(Fore.YELLOW+defaul['routed'],end='')
		else:
			print(Fore.GREEN+defaul['routed'],end='')
		print(Fore.BLUE+"}")
		print(Fore.YELLOW+"POSSIBLE SETTINGS => \n1) Allow the connection\n2) Deny the connection (the connection close after the timeout)\n3) Reject (refuse the connection immediatly)\n4) Limit (limit the connection)\n5) Route the connection")
	print(Fore.CYAN+"insert the number of the setting (from the upper list)")
	while True:
		s = input(Fore.CYAN+"Set the default for incoming connection -> "+Fore.WHITE)
		try:
			if int(s) > 5 and int(s) < 0:
				print(Fore.GREEN+"It look like this isn't a setting :(")
			else:
				print(Fore.RED+"Setting...")
				if s == '1':
					first = 'allow'
				elif s == '2':
					first = 'deny'
				elif s == '3':
					first = 'reject'
				elif s == '4':
					first = 'limit'
				elif s == '5':
					first = 'route'
				print(first+" set for incoming connections!")
				break
		except ValueError:
			print(Fore.GREEN+"It look like this isn't a setting :(")
	while True:
		s = input(Fore.CYAN+"Set the default for outgoing connection -> "+Fore.WHITE)
		try:
			if int(s) > 5 and int(s) < 0:
				print(Fore.GREEN+"It look like this isn't a setting :(")
			else:
				print(Fore.RED+"Setting...")
				if s == '1':
					second = 'allow'
				elif s == '2':
					second = 'deny'
				elif s == '3':
					second = 'reject'
				elif s == '4':
					second = 'limit'
				elif s == '5':
					second = 'route'
				print(second+" set for outgoing connections!")
				break
		except ValueError:
			print(Fore.GREEN+"It look like this isn't a setting :(")
	while True:
		s = input(Fore.CYAN+"Set the default for routed connection -> "+Fore.WHITE)
		try:
			if int(s) > 5 and int(s) < 0:
				print(Fore.GREEN+"It look like this isn't a setting :(")
			else:
				print(Fore.RED+"Setting...")
				if s == '1':
					thirdd = 'allow'
				elif s == '2':
					thirdd = 'deny'
				elif s == '3':
					thirdd = 'reject'
				elif s == '4':
					thirdd = 'limit'
				elif s == '5':
					thirdd = 'route'
				print(thirdd+" set for routed connections!")
				break
		except ValueError:
			print(Fore.GREEN+"It look like this isn't a setting :(")
	ufw.default(incoming=first, outgoing=second, routed=thirdd)
	print(Fore.GREEN+"Default Rules successfully set!")
	delay(2)
	shell('clear')
	miniLogo("\n(Rules Editor)")
	editR()


def editR():
	shell('clear')
	miniLogo("\n(Rules Editor)")
	showRules(ufw.status()['rules'])
	print(Fore.GREEN+"Editor Options =>"+Fore.YELLOW+"\n1) Add a New Rule\n2) Delete an existing Rule\n3) Change the Default Rules\n4) Back")
	while True:
		s = input(Fore.CYAN+"insert your choice -> "+Fore.WHITE)
		if s == '1':
			addRule()
			break
		elif s == '2':
			rmRule()
		elif s == '3':
			defRule()
		elif s == '4':
			break
		else:
			print(Fore.GREEN+"You need to choose one of the numbers from 1 to 4!")
	shell('clear')
	miniLogo("\n(Main Menu)")
	menu()

def menu():
	print(Fore.YELLOW+"\nMAIN MENU =>")
	print("1) Show Status\n2) Edit the Rules\n3) Reset to Default\n4) Enable/Disable\n5) How does it works?\n6) Exit")
	while True:
		try:
			s = input(Fore.CYAN+'insert your choice-> '+Fore.WHITE)
			if s == '1':
				try:
					showStatus()
					break
				except KeyboardInterrupt:
					print("\n"+Fore.GREEN+"You can exit by choosing '6' in the main menu!"+Fore.WHITE)
					shell('clear')
					miniLogo("\n(Main Menu)")
					menu()
					break
			elif s == '2':
				try:
					editR()
					break
				except KeyboardInterrupt:
					print("\n"+Fore.GREEN+"You can exit by choosing '6' in the main menu!"+Fore.WHITE)
					shell('clear')
					miniLogo("\n(Main Menu)")
					menu()
					break
			elif s == '3':
				try:
					resetta()
					break
				except KeyboardInterrupt:
					print("\n"+Fore.GREEN+"You can exit by choosing '6' in the main menu!"+Fore.WHITE)
					shell('clear')
					miniLogo("\n(Main Menu)")
					menu()
					break
			elif s == '4':
				try:
					enableDisable()
					break
				except KeyboardInterrupt:
					print("\n"+Fore.GREEN+"You can exit by choosing '6' in the main menu!"+Fore.WHITE)
					shell('clear')
					miniLogo("\n(Main Menu)")
					menu()
					break
			elif s == '5':
				try:
					how()
					break
				except KeyboardInterrupt:
					print("\n"+Fore.GREEN+"You can exit by choosing '6' in the main menu!"+Fore.WHITE)
					shell('clear')
					miniLogo("\n(Main Menu)")
					menu()
					break
			elif s == '6':
				print(Fore.RED+"\nBye Bye! I'll stay here and protect your Network!"+Fore.WHITE)
				break
			else:
				print(Fore.GREEN+"You need to choose one of the numbers from 1 to 6!")
		except KeyboardInterrupt:
			print("\n"+Fore.GREEN+"You can exit by choosing '6' in the main menu!"+Fore.WHITE)

def init():
	print()
	shell('clear')
	logo()
	print(Fore.MAGENTA+"Welcome on FireFlower!\n"+Fore.GREEN+"The easiest firewall..."+Fore.BLUE+"\nBy Master Radon")
	menu()

init()
