# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Bilin Chen
# Collaborators : None
# Time spent    : 5 days

import math
import random
import string

VOWELS = 'aeiou'
WILDCARD = '*'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
	'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0,
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
	"""
	Returns a list of valid words. Words are strings of lowercase letters.
	
	Depending on the size of the word list, this function may
	take a while to finish.
	"""
	
	print("Loading word list from file...")
	# inFile: file
	inFile = open(WORDLIST_FILENAME, 'r')
	# wordlist: list of strings
	wordlist = []
	for line in inFile:
		wordlist.append(line.strip().lower())
	print("  ", len(wordlist), "words loaded.")
	return wordlist

def get_frequency_dict(sequence):
	"""
	Returns a dictionary where the keys are elements of the sequence
	and the values are integer counts, for the number of times that
	an element is repeated in the sequence.

	sequence: string or list
	return: dictionary
	"""
	
	# freqs: dictionary (element_type -> int)
	freq = {}
	for x in sequence:
		freq[x] = freq.get(x,0) + 1
	return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
	"""
	Returns the score for a word. Assumes the word is a
	valid word.

	You may assume that the input word is always either a string of letters, 
	or the empty string "". You may not assume that the string will only contain 
	lowercase letters, so you will have to handle uppercase and mixed case strings 
	appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
			1, or
			7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
			and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

	word: string
	n: int >= 0
	returns: int >= 0
	"""
	word = word.lower()

	first_component = 0
	second_component = 0
	
	if len(word) != 0:
		for w in word:
			first_component += SCRABBLE_LETTER_VALUES[w]
		
		second_component = max(7 * len(word) - 3 * (n - len(word)), 1)

	total_points = first_component * second_component

	return total_points

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
	"""
	Displays the letters currently in the hand.

	For example:
	   display_hand({'a':1, 'x':2, 'l':3, 'e':1})
	Should print out something like:
	   a x x l l l e
	The order of the letters is unimportant.

	hand: dictionary (string -> int)
	"""
	
	for letter in hand.keys():
		for j in range(hand[letter]):
			 print(letter, end=' ')      # print all on the same line
	print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
	"""
	Returns a random hand containing n lowercase letters.
	ceil(n/3) letters in the hand should be VOWELS (note,
	ceil(n/3) means the smallest integer not less than n/3).

	Hands are represented as dictionaries. The keys are
	letters and the values are the number of times the
	particular letter is repeated in that hand.

	n: int >= 0
	returns: dictionary (string -> int)
	"""
	
	hand={}
	# Remove a vowel slot for the wildcard
	num_vowels = int(math.ceil(n / 3)) - 1

	for i in range(num_vowels):
		x = random.choice(VOWELS)
		hand[x] = hand.get(x, 0) + 1
	
	# Add the wildcard
	hand[WILDCARD] = 1

	# The wildcard takes up a spot in num_vowels so it has to be readded
	for i in range(num_vowels + 1, n):
		x = random.choice(CONSONANTS)
		hand[x] = hand.get(x, 0) + 1
	
	return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
	"""
	Does NOT assume that hand contains every letter in word at least as
	many times as the letter appears in word. Letters in word that don't
	appear in hand should be ignored. Letters that appear in word more times
	than in hand should never result in a negative count; instead, set the
	count in the returned hand to 0 (or remove the letter from the
	dictionary, depending on how your code is structured). 

	Updates the hand: uses up the letters in the given word
	and returns the new hand, without those letters in it.

	Has no side effects: does not modify hand.

	word: string
	hand: dictionary (string -> int)    
	returns: dictionary (string -> int)
	"""

	word = word.lower()
	new_hand = hand.copy()

	for w in word:
		# Check if letter is actually part of the hand
		if not(new_hand.get(w, 'ignored') == 'ignored'):
			
			# Removes the used letter from the hand, sets it to zero if no uses are left
			new_hand[w] = max(new_hand[w] - 1, 0)
			
			# Deletes the letter if it is used up from the hand
			if new_hand[w] == 0:
				del new_hand[w]

	return new_hand
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
	"""
	Returns True if word is in the word_list and is entirely
	composed of letters in the hand. Otherwise, returns False.
	Does not mutate hand or word_list.
   
	word: string
	hand: dictionary (string -> int)
	word_list: list of lowercase strings
	returns: boolean
	"""

	word = word.lower()
	# gets the frequency of a letter in the word in a dict
	letter_count = get_frequency_dict(word)

	if WILDCARD in word:
		index = word.find(WILDCARD)

		for v in VOWELS:
			possible_word = word[0:index] + v + word[index+1:]

			if possible_word in word_list:
				return True

		# If none of the possible words are in the list return false
		return False

	else:

		if word in word_list:
			for w in word:		
				# Checks if the number of a letter in the word has the same number or more in the hand
				if not(letter_count[w] <= hand.get(w,0)):
					return False

			return True

		else:
			return False

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
	""" 
	Returns the length (number of letters) in the current hand.
	
	hand: dictionary (string-> int)
	returns: integer
	"""
	hand_len = 0
	for key in hand.keys():
		hand_len += hand[key]
	
	return hand_len


def play_hand(hand, word_list):

	"""
	Allows the user to play the given hand, as follows:

	* The hand is displayed.
	
	* The user may input a word.

	* When any word is entered (valid or invalid), it uses up letters
	  from the hand.

	* An invalid word is rejected, and a message is displayed asking
	  the user to choose another word.

	* After every valid word: the score for that word is displayed,
	  the remaining letters in the hand are displayed, and the user
	  is asked to input another word.

	* The sum of the word scores is displayed when the hand finishes.

	* The hand finishes when there are no more unused letters.
	  The user can also finish playing the hand by inputing two 
	  exclamation points (the string '!!') instead of a word.

	  hand: dictionary (string -> int)
	  word_list: list of lowercase strings
	  returns: the total score for the hand
	  
	"""
	
	# Keep track of the total score
	total_score = 0
	# As long as there are still letters left in the hand:
	while len(hand.keys()) > 0:

		# Display the hand
		print('Current hand:', end=' ')
		display_hand(hand)

		# Ask user for input
		user_input = input("Please enter a word, or '!!' to indicate that you are finished: ")
		# If the input is two exclamation points:
		if user_input == '!!':
			# End the game (break out of the loop)

			break
		
		# Otherwise (the input is not two exclamation points):
		# If the word is valid:
		elif is_valid_word(user_input, hand, word_list):
			# Tell the user how many points the word earned,
			print('"%s" earned %s points.' % (user_input, str(get_word_score(user_input, calculate_handlen(hand)))), end=' ')

			# and the updated total score
			total_score += get_word_score(user_input, calculate_handlen(hand))
			print('Total score: ' + str(total_score) + ' points')
			print() # print empty line

		# Otherwise (the word is not valid):
		# Reject invalid word (print a message)
		else:
			print('That is not a valid word. Please choose another word')
			print()	# prints empty line
		# update the user's hand by removing the letters of their inputted word
		hand = update_hand(hand, user_input)

	# Game is over (user entered '!!' or ran out of letters),
	# so tell user the total score
	if len(hand.keys()) == 0:
		print('Ran out of letters.', end=' ')
	
	print('Final score: {} points.'.format(str(total_score)))
	# Return the total score as result of function
	return total_score


# play_hand(deal_hand(HAND_SIZE), load_words())

#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
	""" 
	Allow the user to replace all copies of one letter in the hand (chosen by user)
	with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
	should be different from user's choice, and should not be any of the letters
	already in the hand.

	If user provide a letter not in the hand, the hand should be the same.

	Has no side effects: does not mutate hand.

	For example:
		substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
	might return:
		{'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
	The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
	already in the hand.
	
	hand: dictionary (string -> int)
	letter: string
	returns: dictionary (string -> int)
	"""
	
	sub_hand = hand.copy()


	# 1. check if the letter is in the hand
	# if it is not then ignore and just redisplay the hand
	if not(letter in sub_hand):
		return hand

	# if it is then go ahead and substitute it
	else:
	# 2. check what letters are in the current hand and remove them from the possible set of letters
		apet = (VOWELS + CONSONANTS).lower()
		apet.replace(letter, '')
	# 3. generate a new random letter
		sub_letter = random.choice(apet)


	# 4. switch out the old letter with the new. all copies of it should be replaced
		sub_hand[sub_letter] = hand[letter]
		del sub_hand[letter]

		return sub_hand
	


	   
	
def play_game(word_list):
	"""
	Allow the user to play a series of hands

	* Asks the user to input a total number of hands

	* Accumulates the score for each hand into a total score for the 
	  entire series
 
	* For each hand, before playing, ask the user if they want to substitute
	  one letter for another. If the user inputs 'yes', prompt them for their
	  desired letter. This can only be done once during the game. Once the
	  substitue option is used, the user should not be asked if they want to
	  substitute letters in the future.

	* For each hand, ask the user if they would like to replay the hand.
	  If the user inputs 'yes', they will replay the hand and keep 
	  the better of the two scores for that hand.  This can only be done once 
	  during the game. Once the replay option is used, the user should not
	  be asked if they want to replay future hands. Replaying the hand does
	  not count as one of the total number of hands the user initially
	  wanted to play.

			* Note: if you replay a hand, you do not get the option to substitute
					a letter - you must play whatever hand you just had.
	  
	* Returns the total score for the series of hands

	word_list: list of lowercase strings
	"""
	print('-----------------------')
	print(' PLAYING THE WORD GAME ')
	print('-----------------------')
	print()
	# ask user for number of hands to play
	while True:
		try:
			num_hands = int(input("Enter total number of hands: "))
		except ValueError:
			print('Sorry but the input was not of the correct format. Please enter a number.\n')
			# try again
			continue
		else:
			# successfully parsed
			break
	
	played_hands = 0		# number of played hands
	
	substitute_counter = 0 	# number of times substitute letter has been used
	
	replay_counter = 0		# number of times replay of hand has been used

	all_scores = []			# storing all the scores to sum up at the end
	
	# Play until all hands are finished
	while played_hands < num_hands:
		print('----------')
		print('Playing hand %s.' % (str(played_hands + 1)))
		print('----------\n')
		# present the user with a hand
		hand = deal_hand(HAND_SIZE)
			# save the hand in a new variable as not to mutate it
		
		change = ''
		# Allow substitue of letter only once for all hands
		if substitute_counter < 1:
			# ask the user if they want to substitute a letter
			print('Current hand:', end=' ')
			display_hand(hand)

			while not(change == 'yes' or change =='no'):
				change = input('Would you like to substitute a letter? ').lower()
				

				if not(change == 'yes' or change == 'no'):
					print(">Please type 'yes' or 'no'!")

			# if they say no nothing happens, the substitution is saved for next time
			if change == 'yes':
				# ask for letter to replace
				letter = input('Which letter would you like to replace: ').lower()
				print()	# print empty line
				# replace letter in hand
				hand = substitute_hand(hand, letter)

				# a substitution shall not be asked again if it has been used
				substitute_counter += 1
			# if they don't wanna replace a letter the hand is unchanged 
			else:
				hand = hand
			
		hand_copy = hand.copy()		# saved in for replay case
		score = play_hand(hand, word_list)	# play the hand and returns a score (will also display the hand)
		score_replay = 0

		# after a played hand ask if they want to replay it
		if replay_counter < 1:
			replay = input('Would you like to replay hand: ').lower()
		
			# if yes then redisplay the umutated hand
			# do not give option to substitute
			if replay == 'yes':
				# only one replay is allowed per hand
				replay_counter += 1
				print()
				score_replay = play_hand(hand, word_list)	# save the score from the replay hand
		print()
		# compare scores and save the highest one
		all_scores.append(max(score, score_replay))

		played_hands += 1

	# end game (display total score for all hands)
	total_score = 0
	for s in all_scores:
		total_score += s
	print('----------')
	print('Total score over all hands: %d' % (total_score))	
	

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
	word_list = load_words()
	play_game(word_list)
