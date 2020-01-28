import matplotlib.pyplot as plt
import matplotlib
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
import numpy as np
import operator
import os
from randomInt import random, randomInt, bitsToInt, runSim

verbose = True

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'quantum_circuit.jpg')

tutorialLines = {
    "REG_SETUP": \
        "\nFirstly we setup our 4 quantum and 4 classical registers (allowing us to handle decks of 4^2=16 cards).\n" \
        "We immediately put all our qubits into a state of superposition using the Hadamard gate as to represent all posibilites.\n" \
        "When measured, our qubits will be 1 or 0 with equal probability.\n",
    "ORACLE_SETUP": \
        "\nOnce our qubits are in superposition, we can apply our \"oracle\".\n"\
        "We begin by inverting the qubits that are associated with a value of 0 in our search term using a Pauli-X gate.\n"
}

def get_deck(size=16):
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ['\u2660', '\u2665', '\u2666', '\u2663']
    deck = [values[randomInt(15) % len(values)] + suits[randomInt(15) % len(suits)] for x in range(size)]
    return deck


def oracle(program, qr, secret):
    secret = np.asarray(secret)
    indices = np.where(secret == 0)[0] 
    for i in range(len(indices)):
        index = int(len(secret) - 1 - indices[i])
        program.x(qr[index])
  
    pressEnterToContinue()

def pressEnterToContinue():
    input("Press enter to continue...")

def guess(secret):

    # Register setup and superposition
    print(tutorialLines["REG_SETUP"]) if verbose else ""
    qr = QuantumRegister(4)
    cr = ClassicalRegister(4)
    program = QuantumCircuit(qr, cr)
    program.h(qr)
    print(program) if verbose else ""
    pressEnterToContinue() if verbose else ""

    # Oracle (qubit inversion)
    print(tutorialLines["ORACLE_SETUP"]) if verbose else ""
    oracle(program, qr, secret)
    print(program) if verbose else ""


    # Triple controlled Pauli Z-Gate (cccZ).
    program.cu1(np.pi / 4, qr[0], qr[3])
    program.cx(qr[0], qr[1])
    program.cu1(-np.pi / 4, qr[1], qr[3])
    program.cx(qr[0], qr[1])
    program.cu1(np.pi/4, qr[1], qr[3])
    program.cx(qr[1], qr[2])
    program.cu1(-np.pi/4, qr[2], qr[3])
    program.cx(qr[0], qr[2])
    program.cu1(np.pi/4, qr[2], qr[3])
    program.cx(qr[1], qr[2])
    program.cu1(-np.pi/4, qr[2], qr[3])
    program.cx(qr[0], qr[2])
    program.cu1(np.pi/4, qr[2], qr[3])

    # Same inversion
    oracle(program, qr, secret)

    # Amplification
    program.h(qr)
    program.x(qr)

    program.cu1(np.pi/4, qr[0], qr[3])  
    program.cx(qr[0], qr[1])
    program.cu1(-np.pi/4, qr[1], qr[3])
    program.cx(qr[0], qr[1])
    program.cu1(np.pi/4, qr[1], qr[3])
    program.cx(qr[1], qr[2])
    program.cu1(-np.pi/4, qr[2], qr[3])
    program.cx(qr[0], qr[2])
    program.cu1(np.pi/4, qr[2], qr[3])
    program.cx(qr[1], qr[2])
    program.cu1(-np.pi/4, qr[2], qr[3])
    program.cx(qr[0], qr[2])
    program.cu1(np.pi/4, qr[2], qr[3])

    program.x(qr)
    program.h(qr)

    program.barrier(qr)
    program.measure(qr, cr)
    program.draw(filename=filename, output='mpl')
    
    results = runSim(program, 1024)
    answer = max(results.items(), key=operator.itemgetter(1))[0]
    ret = bitsToInt([int(i)for i in list(answer)])
    return ret
    

def getDeckFromUser():
    chooseDeck = False
    deck = []
    while not chooseDeck: 
        print('Dealing deck...')
        deck = get_deck()
        print('Current deck: ', deck)
        keepDeck = input("Do you wish to keep current deck? [Y/n]: ").lower()
        chooseDeck = False if keepDeck and keepDeck[0] == 'n' else True
    return deck


def getCardChoice(max=16):
    userHasChosen = False
    paddedBitArray = []
    while not userHasChosen:
        userHasChosen = True
        cardChoice = input("Choose a card [1 - %d]: " % (max)).lower()
        try:
            bitArray = str(bin(int(cardChoice) - 1))[2:]
            paddedBitArray = [0] * (4 - len(bitArray))
            paddedBitArray.extend([int(ch) for ch in bitArray])
        except (ValueError, TypeError):
            print("Current input: %s\nPlease specify a correct input" % (cardChoice))
            userHasChosen = False
        return paddedBitArray


def printDeck(deck):
    outputStr = "\n\t"
    for index, card in enumerate(deck):
        cardStr = "{ %d: %s }" % (index + 1, card)
        outputStr += cardStr + " " * (12 - len(cardStr))
        outputStr += "\n\t" if (index + 1) % 4 == 0 else ""
    print(outputStr)

gameRun = True
while gameRun:
    deck = getDeckFromUser()
    printDeck(deck)
    cardChoice = getCardChoice()
    foundCardIndex = guess(cardChoice)
    print("Grover's algorithm guess is %s ! (card choice: %d)" % (deck[foundCardIndex], foundCardIndex + 1))
    playAgain = input("Do you want to play again? [Y/n]: ").lower()
    gameRun = False if playAgain and playAgain[0] == 'n' else True
