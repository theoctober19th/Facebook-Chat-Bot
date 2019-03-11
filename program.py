from fbchat import Client, log
from fbchat.models import *
import pickle
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import getpass as gp

# EMAIL = input('Email: ')
# PASSWORD = gp.getpass('Password: ')

#victims = [line.rstrip('\n') for line in open('victimlist')]

# with open("login.file", "r") as login_file:
# 	data = login_file.readlines()
# 	EMAIL = data[0].replace('\n', '')
# 	PASSWORD = data[1].replace('\n', '')

def getSessionCookies():
	with open('cookies', 'rb') as cookies_file:
		try:
			cookies = pickle.load(cookies_file)
			return cookies
		except:
			return None

def storeSessionCookies(client):
	open("cookies", "w").close()
	with open('cookies', 'wb') as cookies_file:
		cookies = client.getSession()
		pickle.dump(cookies, cookies_file)

def trainBot():
	chatBot = ChatBot('Bikalpa')

	trainer = ChatterBotCorpusTrainer(chatBot)
	# Train the chatbot based on the english corpus
	trainer.train("chatterbot.corpus.english")

	return chatBot

class BikalpaBot(Client):

	def setChatBot(self, chatBot):
		self.chatBot = chatBot

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(thread_id, message_object.uid)
		self.markAsRead(thread_id)

		if author_id in [line.rstrip('\n') for line in open('victimlist')]:
			response = self.chatBot.get_response(message_object.text)
			self.send(Message(text=response), thread_id = thread_id, thread_type = thread_type)

if __name__ == '__main__':
	#cookies = getSessionCookies()
	chatBot = trainBot()
	print('\nWelcome to Facebook ChatBot by bikalpa!\n')
	EMAIL = input('\n\nFacebook Email: ')
	PASSWORD = gp.getpass('Password: ')
	try:
		client = BikalpaBot(EMAIL, PASSWORD)
		client.setChatBot(chatBot)
		#storeSessionCookies(client)
		client.listen()
	except:
		print('Login Failed. Please make sure all credentials are correct. Or Facebook might have locked your account for suspicious activities.')
	
