import json
import socket
import random

Host = "proj1.3700.network"
Port = 27993
message1 = '{"type": "hello", "northeastern_username": "chen.eric2"}\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((Host, Port))

f = open('project1-words.txt', 'r')
readF = f.read()
wordList = readF.split()

wordFound = False

#Function to both send and recieve messages from the server
def communicate(message):
    s.sendall(message.encode())
    message = s.recv(1024)
    return message

id = communicate(message1).decode()
response_id = json.loads(id)
newId = response_id.get("id")

#global set of conditions learned from previous guesses
notIncludedLetters = set()
includedLetters = set()
correctLetters = dict()
pastGuesses = list()

def guessWord(marks: list, word: str):
    for i in range(5):
        if marks[i] == 0:
            notIncludedLetters.add(word[i])
        elif marks[i] == 2:
            correctLetters[word[i]] = i
            includedLetters.add(word[i])
        elif marks[i] == 1:
            includedLetters.add(word[i])

    for s in includedLetters:
        if s in notIncludedLetters:
            notIncludedLetters.remove(s)

    possibleWords = [word for word in wordList if not any(letter in word for letter in notIncludedLetters)]

    if(len(includedLetters) > 0):
        possibleWords = [word for word in possibleWords if all(letter in word for letter in includedLetters)]

    for letter, position in correctLetters.items():
        possibleWords = [word for word in possibleWords if word[position] == letter]

    possibleWords = [word for word in possibleWords if not word in pastGuesses]

    print(notIncludedLetters)
    print(includedLetters)
    print(correctLetters)
    choice = possibleWords[0]
    pastGuesses.append(choice)
    return choice

guess = random.choice(wordList)
#guessing loop
while wordFound != True:
    #message template
    guess_message = '{"type": "guess", "id": "' + newId + '", "word":' + ' "' + guess + '"}\n'
    response = communicate(guess_message).decode()

    print(guess_message )
    print(response)

    response_json = json.loads(response)
    marks = []
    if (response_json.get("type") == "retry"):
        marks = response_json.get("guesses")[-1].get("marks")
    elif(response_json.get("type") == "bye"):
        wordFound = True

    if(wordFound != True):
        guess = guessWord(marks, response_json.get("guesses")[-1].get("word"))
    print(marks)







