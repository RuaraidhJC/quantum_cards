import qiskit
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import IBMQ
from configparser import RawConfigParser
import math

def runSim(program, shots=1):
    job = qiskit.execute(program, qiskit.Aer.get_backend('qasm_simulator'), shots=shots)
    return job.result().get_counts()

def bitCount(val):
    return math.floor(math.log(val, 2)) + 1

def bitsToInt(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out

def random(max=15):
    shots = 1024
    bits = bitCount(max)
    x = math.ceil(math.log(bits, 2))
    #print(bits, x, max)
    qr = QuantumRegister(x)
    cr = ClassicalRegister(x)
    program = QuantumCircuit(qr, cr)
    program.h(qr)
    program.measure(qr, cr)
    results = runSim(program, shots)
    avgProb = shots / math.pow(2, x)
   
    randomBits = [1 if value > avgProb else 0 for key, value in results.items()]
    #print('len', len(results.items()), avgProb, randomBits)
    return randomBits

def randomInt(max, count=1):
    randomVals = [bitsToInt(random(max)) for i in range(count)]
    return randomVals[0] if count == 1 else randomVals
