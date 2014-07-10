
import random

rankDict = {i:[str(i),i] for i in range(2,11)}
rankDict[11] = ['Jack', 10]
rankDict[12] = ['Queen', 10]
rankDict[13] = ['King', 10]
rankDict[14] = ['Ace', 11]

suitDict = {0: "Diamonds", 1:"Clubs", 2: "Hearts", 3: "Spades"}
class Card:
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit

	def __str__(self):
		return str(rankDict[self.rank][0]) + " of " + str(suitDict[self.suit])

class Deck:
	def __init__(self, numDecks = 1):
		for i in range(numDecks):
			self.cards = []
			for rank in range(2,15):
				for suit in range(4):
					self.cards += [Card(rank,suit)]
		self.shuffle()
	def shuffle(self):
		random.shuffle(self.cards)

	def __str__(self):
		returnString = ""
		for card in d.cards:
			returnString += str(card) + "\n"
		return returnString

	def __len__(self):
		return len(self.cards)
	
	def dealTop(self):
		return self.cards.pop()



class Hand:
	def __init__(self, card1,card2):
		if card1.rank != 14 and card2.rank != 14:
			#Easier to deal with, no aces so not a softhand
			self.isSoft = False
			self.total = rankDict[card1.rank][1] + rankDict[card2.rank][1]
		elif card1.rank == 14 and card2.rank == 14:
			print "Two Aces!  Split em for sure!"
			self.total = 12
			self.isSoft = True
		elif card1.rank == 14:
			self.total = rankDict[card2.rank][1]+ 11
			self.isSoft = True
		elif card2.rank == 14:
			self.total = rankDict[card1.rank][1] + 11
			self.isSoft = True
		else:
			print "THIS SHOULD NEVER HAPPEN"
		self.cards = [card1,card2]

	def __cmp__(self, other):
		if self.total > other.total:
			return 1
		elif self.total < other.total:
			return -1
		else:
			return 0
	def __str__(self):
		returnString = ""
		for card in self.cards:
			returnString += str(card) +", " 
		returnString = returnString[:-2]
		returnString += " for a total of " + str(self.total)
		return returnString
class Player:
	def __init__(self, startingCash=100, name= "Random Player"):
		self.cash = startingCash
		self.name = name

	def setHand(self, card1,card2):
		self.hand = Hand(card1,card2)

	def __str__(self):
		return self.name

	def setBet(self, value):
		if value <= self.cash and value > 0:
			self.bet = value
			return
		else:
			print value < self.cash
			print "Either you don't have enough money to place a bet that big, or your bet must be a positive number" 
			print "Cash remaining: ", self.cash
			newBet = int(raw_input("Enter a smaller bet value"))
			self.setBet(newBet)

	def revealOne(self):
		return self.hand.cards[0]		

	def getHandValue(self):
		return self.hand.total

	def displayMoney(self):
		print "Player: ", self.__str__(), " has " + str(self.cash) + " remaining"

	def hit(self, card):
		self.hand.cards +=[card]
		if card.rank == 14: 
			self.hand.isSoft = True
			self.hand.total = self.hand.total + 11
		else:
			self.hand.total += rankDict[card.rank][1]
		if self.hand.total > 21 and self.hand.isSoft:
			self.hand.total -= 10
			self.hand.isSoft = False
		#print "you're new hand value is "  + str(self.hand.total)


class BlackJack:
	def __init__(self, numPlayers=1, numDecks = 1, playerNames = None):
		self.gameDeck = Deck(numDecks)
		self.playerList = []
		for player in range(numPlayers):
			playerName = raw_input("What is your name?\n")
			self.playerList += [Player(100,playerName )]
		#start the dealer off with 1 million bucks
		self.Dealer = Player(startingCash =10**6)

	def dealHand(self):
		for player in self.playerList:
			while True:
				try:
					betSize = int(raw_input("How much would you like to bet, " + str(player)  + "?\n"))
					break
				except:
					print "please enter a valid bet size"
			player.setBet(betSize)
			player.setHand(self.gameDeck.dealTop(), self.gameDeck.dealTop())

		self.Dealer.setHand(self.gameDeck.dealTop(), self.gameDeck.dealTop())

	def playGame(self):
		self.dealHand()
		print "The dealer is showing a " + str(self.Dealer.revealOne())
		notBusted = []
		toRemove = []
		for player in self.playerList:
			print str(player) + " has " + str(player.hand)
			if player.getHandValue() < 21:
				stand = False
				busted = False
				while(True and not busted and not stand):
					display = "You are at " + str(player.getHandValue()) +". Would you like to hit? (y/n)"
					hit_stand = raw_input(display)
					if hit_stand == 'y' or hit_stand == 'Y':
						newCard = self.gameDeck.dealTop()
						print "You got the " + str(newCard)
						player.hit(newCard)
						if player.getHandValue() == 21:
							print "You hit 21 and will (probably) win"
							stand = True
							notBusted += [player]
						if player.getHandValue() > 21:
							player.cash -= player.bet
							self.Dealer.cash += player.bet
							print "You busted and you lose"
							player.displayMoney()
							if player.cash == 0:
								print "you have no money left"
								toRemove += [player]
							busted = True
					else:
						stand = True
						notBusted += [player]
			elif player.getHandValue() == 21:
				print "BLACKJACK!!! It pays 3/2"
				self.Dealer.cash -= 3.0/2*player.bet
				player.cash += 3.0/2*player.bet
				player.displayMoney()
		print "-" * 40
		dealerBusts = False
		if notBusted != []:
			print "Dealer's Starting Hand", self.Dealer.hand
			while self.Dealer.getHandValue() < 17:
				dealerHit = self.gameDeck.dealTop()
				print "The dealer hit and got a ", dealerHit
				self.Dealer.hit(dealerHit)
				if self.Dealer.getHandValue() > 21:
					print "The dealer busts, everybody in wins"
					for player in notBusted:
						player.cash += player.bet
						self.Dealer.cash -= player.bet
						player.displayMoney()
					dealerBusts = True
		if not dealerBusts:
			print "Dealers Hand", self.Dealer.hand
			for player in notBusted:
				print "The dealer has " + str(self.Dealer.getHandValue())
				print "And you have " + str(player.getHandValue())
				if player.getHandValue() < self.Dealer.getHandValue():
					print "You lose!"
					player.cash -= player.bet
					self.Dealer.cash += player.bet
					if player.cash == 0:
						toRemove += [player]
				elif player.getHandValue() == self.Dealer.getHandValue():
					print "Push, no money exchanged"
				else:
					print "Hooray, you win " + str(player.bet) + " dollars"
					player.cash += player.bet
					self.Dealer.cash -= player.bet
				player.displayMoney()
		for p in toRemove:
			self.playerList.remove(p)
		if self.playerList == []:
			print "No player's left; The game is over"
			exit()
		print "-"*100
	def displayPlayerTotals(self):
		for player in self.playerList:
			print str(player)
			print "Remaining money " + str(player.cash)
			print "-"*100


if __name__ == "__main__":
	B = BlackJack(1)
	play = raw_input("Do you want to play?")
	while(play[0] != 'N' and play[0] != 'n'):
		B.playGame()
		play = raw_input("Do you want to play again?")
	B.displayPlayerTotals()
	print "Thanks for Playing"
