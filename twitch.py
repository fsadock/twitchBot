import re, sys, socket
from random import randint
import os
from time import sleep

#-------------------TRY TO READ THE CHANNEL--------------------#

try:
	sys.argv[1]
except:
	print("\n>Please, type the channel name")
	sys.exit()


#------------------------MAIN VARIABLES------------------------#
HOST = "irc.twitch.tv"
PORT = 6667
CHAN = "#"+sys.argv[1]
NICK = "fsadock"
PASS = "oauth:bh7qc1d4v4qiz5m9nj2cgxo1y94hck"


#--------------------------CONNECTION--------------------------#
so = socket.socket()

so.connect((HOST,PORT))

so.send(('PASS ' + PASS + '\r\n').encode())
so.send(('NICK ' + NICK + '\r\n').encode())
so.send(('JOIN ' + CHAN + '\r\n').encode())

#--------------------------FUNCTIONS---------------------------#

def get_user(msg):
	user = ""
	for letter in msg:
		if letter == "!":
			break;
		if letter != ":":
			user += letter
	return user;

def get_message(msg):
	mesg = ""
	i = 3
	length = len(msg)
	while i < length:
		mesg += msg[i] + " "
		i += 1
	mesg = mesg.lstrip(':')
	return mesg;

def send_msg(msg):
	so.send(('PRIVMSG ' + CHAN +' :' + msg + '\r\n').encode());

#--------------------------PROCESSING--------------------------#

os.system('chcp 65001')                     #CHANGING THE COMMAND PROMPT ENCODING TO UTF-8

errorFile = open('twitcherror.txt', 'w+')   #CREATE A FILE FOR ERRORS

queue = 0

lol = ['lol', 'lul', 'lmao', 'haha', 'hahahah'] #ARRAY FOR MESSAGE SELECTION

data = ""

while True:
	try:
		data = data + so.recv(1024).decode('UTF-8')
		data_split = re.split(r"[~\r\n]+", data)
		data = data_split.pop()

		for linha in data_split:
			linha = linha.rstrip();
			linha = linha.split();


			if (len(linha) >= 1):
				if linha[0] == 'PING':                      #IF THE SERVER SEND PING, WE HAVE TO SEND PONG
					so.send(('PONG' + msg+ '\r\n').encode())

				try:
					linha[1]                                  #ERROR THAT SOMETIMES HAPPENS, DID NOT FIGURE IT OUT YET
				except :
					for i in linha:
						errorFile.write(i)
					errorFile.close()

				if linha[1] == 'PRIVMSG':
					user = get_user(linha[0])
					msg = get_message(linha)

					try:
						print(user + ": " + msg+'\n')       
					except:                               #TRYING TO FIGURE OUT ENCODING ERROR
						errorFile.write(msg)
						errorFile.close()

					#msg_split = msg.split()

					if('lol' in msg.lower()):
						sleep(3)
						send_msg(lol[randint(0, len(lol)-1)])
						queue+=1
						sleep(3/2)

					if(msg.lower() == 'pogchamp '):
						sleep(1)
						send_msg("PogChamp")
						queue+=1
						sleep(3/2)						

					if(msg == "123 "):
						sleep(1)
						send_msg("456 Kappa")
						queue+=1
						sleep(3/2)

					if(msg.lower() == "vapenation "):
						sleep(1)
						send_msg("\\//\\ VAPE NAESH YALL")
						queue+=1
						sleep(3/2)
					if(queue>=5):             #SEND 5 MESSAGES BEFORE EMPTYING THE QUEUE
					  queue = 0
						break;

					#if(len(msg_split)>10):
					#	send_msg("/timeout "+ user)
					#	sleep(30/20)



	except socket.error:
		print("SOCKET DIED")
	except socket.timeout:
		print("SOCKET TIMEOUT")
