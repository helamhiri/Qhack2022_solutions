#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """
    
   
    # QHACK 
    
    def h_oracle():
        
        #preparing the ancillary qubit(2) of the h oracle
        qml.PauliX(wires=2)
        qml.Hadamard(wires=2)

        
        ################DJ circuit on the h oracle###############
        
            
        #---------------implementing the h oracle---------------#
        
        #Preparing the multiplexer: we use 2 additional qubits(6 and 7) to create |1>|1> state for each i in {0,1,2,3}
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        qml.CNOT(wires=[0,6])
        qml.CNOT(wires=[1,7])
        qml.PauliX(wires=0)
        qml.PauliX(wires=1)
        
        
        ######DJ circuit on fi######
        
        #hadamard transform on input wires of fi oracle [3,4]
        for i in range(3,5):
            qml.Hadamard(wires=i)
        
        #preparing the ancillary qubit(5) of the fi oracle
        qml.PauliX(wires=5)
        qml.Hadamard(wires=5)
        
        #applying the fi oracle depending on the entry i using the multiplexer
        qml.ctrl(fs[3], control=[0,1])([3,4,5])
        qml.ctrl(fs[0], control=[6,7])([3,4,5])
        qml.ctrl(fs[1], control=[1,6])([3,4,5])
        qml.ctrl(fs[2], control=[0,7])([3,4,5])
        
        
        #hadamard transform on input wires of fi oracle [3,4]
        for i in range(3,5):
            qml.Hadamard(wires=i)
            
        ###########################
        
        
        #flipping the ancillary qubit of the h oracle(2) if the state '00' is present 
        #in the output state of the DJ circuit on fi
        qml.MultiControlledX(control_wires=[3,4], wires=2, control_values='00')
        
        #All input wires [3,4,6,7] should return to their initial state 
        for i in range(3,5):
            qml.Hadamard(wires=i)
        qml.adjoint(qml.ctrl(fs[3], control=[0,1]))([3,4,5])
        qml.adjoint(qml.ctrl(fs[0], control=[6,7]))([3,4,5])
        qml.adjoint(qml.ctrl(fs[1], control=[1,6]))([3,4,5])
        qml.adjoint(qml.ctrl(fs[2], control=[0,7]))([3,4,5])
        for i in range(3,5):
            qml.Hadamard(wires=i)
            
        qml.CNOT(wires=[0,6])
        qml.CNOT(wires=[1,7])
        ############################
        
        
    dev = qml.device("default.qubit", wires=8,shots=1)
    @qml.qnode(dev)
    def DJ_h():
        
        for i in range(2):
            qml.Hadamard(i)
        h_oracle()
        for i in range(2):
            qml.Hadamard(i)
        return qml.probs(wires=[0,1])
        
    
    
    val=DJ_h()
    #print(val)
    ch="4 same"
    if (val[0]<0.1):
        ch="2 and 2"
       
    return ch
    # QHACK #




if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")
