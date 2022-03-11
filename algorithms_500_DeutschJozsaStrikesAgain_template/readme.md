# Deutsch Jozsa Strikes Again

I am writing this documentation to share with you the line of thinking that led me to the problem solution as well as to explain the code more thoroughly.

Let’s first start with the problem statement:
> The Deutsch-Jozsa algorithm was one of the first to demonstrate a quantum advantage. 
> Briefly, we are given a black-box function (or oracle) f : {0, 1}<sup>N</sup> → {0, 1} , which satisfies one of these two properties: 
> - f is constant: it always returns the same value (it can be 0 or 1). 
> - f is balanced: half of the values, it takes the value 0 and for the other half, the value 1. 
> 
> An oracle with these characteristics needs three qubits: the first two qubits represent the input x, and the third qubit marks the output f(x). 
> 
> Here, we will be looking at a variation of the original Deutsch-Jozsa problem: we are given four different functions f0, f1, f2 and f3 representing four different oracles which are either constant or balanced. As before, each oracle is a 3-qubit 1 operator: the first two qubits represent the input to the function and the third qubit is the output. We are guaranteed that this set of functions satisfies one of the following conditions: 
> - All functions are constant. 
> - All functions are balanced. 
> - Two functions are constant and two are balanced. 
> 
> The objective of this challenge is to determine whether the four functions are of the same type (all constant or all balanced) or are equally split (two functions are constant and two are balanced). You are only allowed to run one shot in one circuit, and you may not use more than eight qubits.

For the sake of the compactness of the explanation, I am going to go through some essential elements already mentioned in the problem statement in order to build our understanding of the task at hand.

1. Oracle

Given a function f:{0,1}<sup>N</sup> →{0,1} , it can be encoded with a combination of quantum gates such that:

![of1](./Images/of1.png)

The input is a bit string of length N (presented by n qubits) and the output is represented by a single qubit: y=f(i).

But, as we know, quantum computation theory implies that any transformation should be unitary and thus invertible meaning that given the output of the oracle, one can systematically determine the input value.
In order to ensure this high order rule, a quantum oracle is rather represented in this way where we add an ancillary qubit in which we encode the output of the function:

![of2](./Images/of2.png)

A more general representation of an oracle is the following where the ancillary qubit is arbitrary( a superposition of the basis states |0> and |1>) and the effect of encoding the function output in the ancillary qubit is given by the formula: y xor f(i).

![xor](./Images/xor.png)

If we prepare the ancillary qubit in |-> state, we will obtain an oracle independent of |y>, which performs the map U<sub>f</sub>|i>=(-1)<sup>f(i)</sup>|i>:

![phase](./Images/phase_oracle.png)

2. Deutsch Jozsa algorithm

The goal of the Deutsh Josa algorithm is to determine whether a function of the type  f:{0,1}<sup>N</sup> →{0,1} is constant or balanced using only one call to the corresponding oracle.

![dj](./Images/DJ_.png)

<img src="https://render.githubusercontent.com/render/math?math={|\phi1>=|0>^{n}|y> }">

<img src="https://render.githubusercontent.com/render/math?math={|\phi2>=H^{n}|\phi1>=\frac{1}{\sqrt{2^{n}}}\displaystyle\sum_{x \in \{0,1\}^{n}} |x>|y> }">

<img src="https://render.githubusercontent.com/render/math?math={|\phi3>=U_{f} |\phi2> =\frac{1}{\sqrt{2^{n}}}\displaystyle\sum_{x \in \{0,1\}^{n}} U_{f}|x>|y>= \frac{1}{\sqrt{2^{n}}}\displaystyle\sum_{x \in \{0,1\}^{n}} (-1)^{f(x)}|x>|y>}">


<img src="https://render.githubusercontent.com/render/math?math={|\phi4>=H^{n}|\phi3>=\frac{1}{\sqrt{2^{n}}}\displaystyle\sum_{x \in \{0,1\}^{n}} (-1)^{f(x)}H^{n}|x>|y> = \frac{1}{2^{n}}\displaystyle\sum_{x \in \{0,1\}^{n}} (-1)^{f(x)}\displaystyle\sum_{k \in \{0,1\}^{n}} (-1)^{k.x}|k>|y> = \displaystyle\sum_{k \in \{0,1\}^{n}} (\displaystyle\sum_{x \in \{0,1\}^{n}} \frac{1}{2^{n}}(-1)^{f(x) + k.x})|k>|y> = \displaystyle\sum_{k \in \{0,1\}^{n}} C_{k} |k>|y>}">

<img src="https://render.githubusercontent.com/render/math?math={C_{0}=\frac{1}{2^{n}}\displaystyle\sum_{x \in \{0,1\}^{n}} (-1)^{f(x)}= \left\{\begin{array}{ll}1 \text{ if} f=0 \Rightarrow |\phi4>=|0>^{n}|y> \text{(because the state is normalized)}  \\ -1 \text{ if} f=1 \Rightarrow |\phi4>=-|0>^{n}|y>\\0 \text{ if} f balanced \Rightarrow |\phi4>=\displaystyle\sum_{\mathclap{k \in \{0,1\}^{n}, k \ne 0^{n}}} C_{k} |k>|y> \end{array}\right.   }">


All these details being set up, we are now ready to build our solution.
We are now dealing with the following function: h:{f1,f2,f3,f4} → {0,1} modeled by this oracle:

![oh](./Images/oh.png)

As mentioned in the problem statement, the task at hand is to determine whether h is constant or balanced which is equivalent to determining if all f<sub>i</sub>  are of the same type (all balanced : h=0 /all constant: h=1 → h is constant) or if two are constant and two are balanced (h(i)=h(i')=1 and h(j)=h(j')=0 → h is balanced)

Clearly, if we succeed in implementing such an oracle and feed it to the DJ circuit, our problem will be solved. 

Now the question that should be raised is, during the implementation of the h oracle how can we determine for a specific input |i> if fi is whether constant or balanced ?
The best algorithm that we know of for this task is the DJ algorithm.
Moreover, we notice that h(fi) is equal to the probability of the |00..000> basis state in the DJ fi circuit final state. Therefore, if we apply the following circuit and extract the information about the probability of the |00..000> basis state after applying DJ on fi we can obtain the desired output for the h oracle.

![circuit](./Images/struct_annot.png)

Another small detail is the multiplexer gate that will enable us to select the oracle fi in the DJ circuit when the input to the global oracle(h oracle) is |i>.
The structure of this gate will be further explained in the code implementation.



