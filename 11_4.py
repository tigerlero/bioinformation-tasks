from math import log10
infinity = float('inf')


def Viterbi(transitionProb, startProb, emissionProb, states, observations, n):
    V = [];
    firstObs = observations[0];

    #Calculate first column
    v = {}; #Temp dict to hold state data
    for s in states:
        #Add dummy value to PrevState key
        v[s] = {"PrevState": "Start"};
        v[s]["Prob"] = log10(emissionProb[s][firstObs]);
    V.append(v.copy());

    for i in range(1,n):
        obs = observations[i];

        v = {};
        for s in states:
            #Find max prob of states for current observation
            maxProb = -infinity;
            state = ""; #Hold previous state where maxProb occured

            emission = log10(emissionProb[s][obs]);
            for prevState in states:
                #Find max from previous column
                prevProb = V[i-1][prevState]["Prob"];
                prob = prevProb + log10(transitionProb[prevState][s]);

                if(prob > maxProb):
                    maxProb = prob;
                    state = prevState;

            v[s] = {};
            v[s]["Prob"] = emission + maxProb;
            v[s]["PrevState"] = state;

        V.append(v.copy());

    #Find max probability
    maxProb = -infinity;
    state = "";
    for s in states:
        if(V[-1][s]["Prob"] > maxProb):
            maxProb = V[-1][s]["Prob"];
            state = s;

    #Find sequence by moving back from the final state
    sequence = [state];
    for i in range(n-2,-1,-1):
        prevState = V[i+1][state]["PrevState"]
        sequence.insert(0,prevState); #Insert prevState to start of sequence
        state = prevState;

    print(sequence);
    print(maxProb);


def Initialization():
    transitionProb = {
        "a": {"a":0.9, "b":0.1},
        "b": {"a":0.1, "b":0.9}
    };

    emissionProb = {
        "a": {"A":0.4, "C":0.1, "G":0.4, "T":0.1},
        "b": {"A":0.2, "C":0.3, "G":0.2, "T":0.3}
    };

    startProb = {"a":0.5, "b":0.5};

    states = ["a", "b"];
    observations = ["G", "G", "C", "T"];
    n = len(observations);

    return transitionProb, startProb, emissionProb, states, observations, n;



transitionProb, startProb, emissionProb, states, observations, n = Initialization();
Viterbi(transitionProb, startProb, emissionProb, states, observations, n);
