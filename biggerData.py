#code for taking inputs on display
from tkinter import *
root= Tk()
import numpy as np   
import pandas as pd 
from collections import defaultdict
data= pd.read_csv(r'data.csv')
Graph={}
data.replace(to_replace=[None], value=np.nan, inplace=True)
amount = data["amount"]
sender = data["nameOrig"]
receiver = data["nameDest"]

Nodes = []
for i in range(len(sender)):
    if amount[i] != None:
        if sender[i] not in Nodes:
            Nodes.append(sender[i])
        if receiver[i] not in Nodes:
            Nodes.append(receiver[i])

edgeList = []
for people in range(len(amount)):
    edgeList.append((sender[people], receiver[people], amount[people]))

Initial_transactions=len(edgeList)
def addNodes(Graph,Nodes):
   
    for i in range(len(Nodes)):

        Graph[Nodes[i]]=[]
    return Graph

def addEdges(Graph,edgeList,directed):
    if directed==False:
      for i in range(len(edgeList)):
     
     
          Graph[edgeList[i][0]].append((edgeList[i][1],edgeList[i][2]))
          Graph[edgeList[i][1]].append((edgeList[i][0],edgeList[i][2]))
    elif directed==True:
      for i in range(len(edgeList)):
          Graph[edgeList[i][0]].append((edgeList[i][1],edgeList[i][2]))


    return Graph

Graph=addNodes(Graph, Nodes)
Graph=addEdges(Graph, edgeList, True)
final_lst=[]
def min_cash_flow(Graph):
    # calculate net amount for each person

    net_amount = defaultdict(int)
    
    for transaction in Graph:

        for edge in Graph[transaction]:
          net_amount[transaction] -= edge[1]
          net_amount[edge[0]] += edge[1]

    # create list of persons with non-zero net amount
    persons = [person for person in net_amount if net_amount[person] != 0]

    # sort persons in increasing order of net amount
    persons.sort(key=lambda x: net_amount[x])
    #persons.sort()
    # initialize minimum transactions count
    count = 0

    # iterate over persons and settle debts
    i, j = 0, len(persons)-1
    while i < j:
        # find the minimum debt to settle
        debt = min(-net_amount[persons[i]], net_amount[persons[j]])

        # update net amount for persons
        net_amount[persons[i]] += debt
        net_amount[persons[j]] -= debt

        # update minimum transactions count
        count += 1

        # print transaction details
        a=(f'{persons[i]} pays {debt} to {persons[j]}')
        print(f'{persons[i]} pays {debt} to {persons[j]}')

        final_lst.append(a)
        # remove persons with zero net amount
        if net_amount[persons[i]] == 0:
            i += 1
        if net_amount[persons[j]] == 0:
            j -= 1

    # return minimum transactions count
  
    return count

# example usage
# transactions = [('A', 'B', 100), ('B', 'C', 50), ('C', 'A', 75), ('D', 'A', 25)]
min_count = min_cash_flow(Graph)
print(f'Minimum transactions required: {min_count}')



root.configure(background="black")
def myclick():
    count=3
    for i in range(len(final_lst)):
        myLabel1=Label(root,text=final_lst[i],fg='cyan',bg='black').grid(row=count,column=0)

        count+=1

    myLabel2=Label(root,text='Minimum transaction required: '+str(min_count),fg='cyan',bg='black').grid(row=2,column=0)
    
    myLabel3=Label(root,text="Initial Transactions:"+str(Initial_transactions),fg='cyan',bg='black').grid(row=1,column=0, columnspan=10)

myButton=Button(root,text="Minimize Transactions",command=myclick,fg='blue',bg='black').grid(row=0,column=0, columnspan=10)

root.mainloop()