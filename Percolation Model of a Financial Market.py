import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import PolyCollection
import random as rand
import csv
from collections import Counter

G=nx.Graph()
an=0
a=0.002399
b=0.00099
c=0.001053999
S=300
e=2.718282
run=0
DELTAS= []


#___________________________________________________________________
#create traders represented by nodes with the attribute of either going bull(+1) or bear(-1)

n=0
m=0
for n in range (0,51):
    for m in range (0,51):
        G.add_node((n,m), pos=(n,m))
        nx.set_node_attributes(G,{(n,m):an},'animal')
        m+=1
    n+=1

pos=nx.get_node_attributes(G,'pos')

#____________________________________________________________________
#connecting each node to 4 adjacent nodes(representing a shared stock) and assigning a variable weight to each

w=0
n=0
m=0
for n in range (0,50):
    for m in range (0,50):
        G.add_edge((n,m),(n,m+1), weight=w)
        G.add_edge((n,m),(n+1,m), weight=w)
        m+=1
    n+=1

n=0
for n in range(0,50):
    G.add_edge((n,50),(n+1,50),weight=w)
    G.add_edge((n,50),(n,0),weight=w)
    n+=1

n=0
for n in range(0,50):
    G.add_edge((50,n),(50,n+1),weight=w)
    G.add_edge((50,n),(0,n),weight=w)
    n+=1

G.add_edge((50,50),(50,0),weight=w)
G.add_edge((50,50),(0,50),weight=w)

for run in range(0,4397):
    #______________________________________________________________________
    #node chosen at random and goes bull or bear

    rnn=rand.randint(0,50)
    rnm=rand.randint(0,50)
    RN=rand.random()
    if RN>0.5:
        an=1
        nx.set_node_attributes(G, {(rnn,rnm):an}, 'animal')
    else:
        an=-1
        nx.set_node_attributes(G, {(rnn,rnm):an}, 'animal')
    
    #________________________________________________________________________
    #spread effect to all nodes

    visited= []

    def BFS(graph, node, visited):
        visited.append(node)
        queue = []
        queue.append(node)
        while queue:
            s = queue.pop(0)
            for (x,y) in graph[s]:
                if (x,y) not in visited:
                    queue.append((x,y))
                    visited.append((x,y))
                    if G.nodes[s]['animal'] is 1:
                        probability=e**((-a)*(S))
                        rn=rand.random()
                        if rn<probability:
                            an=1
                            nx.set_node_attributes(G, {(x,y):an}, 'animal')
                        else:
                            an=-1
                            nx.set_node_attributes(G, {(x,y):an}, 'animal')
                    elif G.nodes[s]['animal'] is -1:
                        probability=1-(e**((-b)*(S)))
                        rn=rand.random()
                        if rn<probability:
                            an=-1
                            nx.set_node_attributes(G, {(x,y):an}, 'animal')
                        else:
                            an=1
                            nx.set_node_attributes(G, {(x,y):an}, 'animal')

    BFS(G,(rnn,rnm), [])

    #________________________________________________________________________
    #find the new stock price

    node= (rnn,rnm)
    countup=0
    countdwn=0
    if G.nodes[node]['animal'] == 1:
        countup += 1
    elif G.nodes[node]['animal'] == -1:
        countdwn -= 1
    visited= []
    visited.append(node)
    queue= []
    queue.append(node)
    while queue:
        s = queue.pop(0)
        for (x,y) in G[s]:
                if (x,y) not in visited:
                    queue.append((x,y))
                    visited.append((x,y))
                    if G.nodes[(x,y)]['animal'] is 1:
                        countup+=1
                    else:
                        countdwn -=1

    deltaS=(c*(countup+countdwn))*100
    DELTAS.append(deltaS)
    Sdash=S*(1+(deltaS/100))
    SDASH= []
    SDASH.append(Sdash)
    print(run+1)
    print('delta S=', deltaS, '   ')
    print('the new stock price is:', Sdash,'\n ______')
    S=Sdash
    run+=1
    
    
d=0
avg=0
for d in range(0,run):
    avg=avg + DELTAS[d]
    d+=1
trueavg=avg/run
e=0
maxi=DELTAS[0]
for e in range(1,run):
    if DELTAS[e]>maxi:
        maxi=DELTAS[e]
        e+=1
    else: e+=1
f=0
mini=DELTAS[0]
for f in range(1,run):
    if DELTAS[f]<mini:
        mini=DELTAS[f]
        f+=1
    else: f+=1
g=0
fxsq=0
for g in range(0,run):
    fxsq=fxsq+(DELTAS[g])**2
    g+=1
stdev=((fxsq/run)-(trueavg)**2)**0.5
print('average delta:', trueavg)
print('max delta: ', maxi)
print('min delta: ', mini)
print('std dev: ', stdev,'\n______')

with open('deltas.csv', 'w') as csvfile:
    writer=csv.writer(csvfile, lineterminator='\n')
    for val in DELTAS:
        writer.writerow([val])

#____________________________________________________
#to show the clusters through a plot
node= (rnn,rnm)
green=[]
red=[]
if G.nodes[node]['animal'] is 1:
    green.append(node)
elif G.nodes[node]['animal'] is -1:
    red.append(node)
visited= []
visited.append(node)
queue= []
queue.append(node)
while queue:
    s = queue.pop(0)
    for (x,y) in G[s]:
        if (x,y) not in visited:
            queue.append((x,y))
            visited.append((x,y))
            if G.nodes[(x,y)]['animal'] is 1:
                green.append((x,y))
            else:
                red.append((x,y))
               
nx.draw(G,pos)
nx.draw_networkx_nodes(G, pos, nodelist=green, node_color='g')
nx.draw_networkx_nodes(G, pos, nodelist=red, node_color='r')
nx.draw_networkx_edges(G,pos,width=4)
plt.show()


