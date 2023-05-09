from tkinter import *
from collections import defaultdict
import re
import math
import random

root= Tk()

Graph={}
Nodes = []
edgeList = []

def is_all_numbers(string):
    return bool(re.match('^[0-9]+$', string))

def label_tab(myText):
    myLabel = Label(root, text = myText).grid(column=65, row = 0)
    
def get_random_coords():
    return (50 + 400 * random.random()), (50 + 400 * random.random())

def check_overlap(x, y, nodes):
    for node, (nx, ny) in nodes.items():
        if (x - nx)**2 + (y - ny)**2 < 1600:
            return True
    return False

def draw_nodes(canvas, nodes):
    for node, (x, y) in nodes.items():
        size = 40
        canvas.create_oval(x-size, y-size, x+size, y+size, fill='blue', width=2)
        canvas.create_text(x, y, text=node)

def draw_edges(canvas, nodes, edges):
    for start, end, cost in edges:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        angle = math.atan2(y2-y1, x2-x1)
        x_offset, y_offset = 45*math.cos(angle), 45*math.sin(angle)
        x1, y1 = x1 + x_offset, y1 + y_offset
        x2, y2 = x2 - x_offset, y2 - y_offset
        canvas.create_line(x1, y1, x2, y2, arrow='last')
        canvas.create_text((x1+x2)/2, (y1+y2)/2-10, text=str(cost))
    
senderLabel = Label(root, text = "Sender").grid(column = 0, row = 0)
receiverLabel = Label(root, text = "Receiver").grid(column = 1, row = 0)
amountLabel = Label(root, text = "Amount").grid(column = 2, row = 0)

sender = Entry(root, width = 20)
sender.grid(row = 1, column = 0)

receiver = Entry(root, width = 20)
receiver.grid(row = 1, column = 1)

amount = Entry(root, width = 20)
amount.grid(row = 1, column = 2)

def make_transaction():
    sending = sender.get()
    receiving = receiver.get()
    total = amount.get()
    
    if len(sending) > 0 and len(receiving) > 0 and is_all_numbers(total):
        if sending not in Nodes:
            Nodes.append(sending)
        if receiving not in Nodes:
            Nodes.append(receiving)
        edgeList.append((sending, receiving, int(total)))
        print(edgeList)
        label_tab("Transaction made Successfully!")
        
    else:
        label_tab("Enter Correct Information!")
    
    sender.delete(0, END)
    receiver.delete(0, END)
    amount.delete(0, END)

sender_Button=Button(root,text="make transaction",command = make_transaction,fg='blue',bg='black', padx=90).grid(row=3,column=0, columnspan=60)

    
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


#Main Algorithm !!!

def min_cash_flow(Graph):
    
    Graph=addNodes(Graph, Nodes)
    Graph=addEdges(Graph, edgeList, True)
    final_lst=[]
    print(Graph)
    net_amount = defaultdict(int)
    
    # calculate net amount for each person
    
    for transaction in Graph:

        for edge in Graph[transaction]:
            net_amount[transaction] -= edge[1]
            net_amount[edge[0]] += edge[1]

    # create list of persons with non-zero net amount
    persons = [person for person in net_amount if net_amount[person] != 0]

    # sort persons in increasing order of net amount
    persons.sort(key=lambda x: net_amount[x])

    # initialize minimum transactions count
    count = 0
    #initialize new nodes and edgeLists
    
    newNodes = []
    newEdgeList = []
    
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
        payment = (f'{persons[i]} pays {debt} to {persons[j]}')
        print(payment)
        
        if persons[i] not in newNodes:
            newNodes.append(persons[i])
        if persons[j] not in newNodes:
            newNodes.append(persons[j])
            
        newEdgeList.append((persons[i], persons[j], debt))
        
        final_lst.append(payment)
        # remove persons with zero net amount
        if net_amount[persons[i]] == 0:
            i += 1
        if net_amount[persons[j]] == 0:
            j -= 1
            
    #printing in tikinter
    for i in range(len(final_lst)):
        myLabel1=Label(root,text=final_lst[i],fg='cyan',bg='black').grid(row=i+7,column=0, columnspan = 12)
    myLabel2=Label(root,text='Minimum transaction required: '+str(count),fg='cyan',bg='black').grid(row=len(final_lst) + 7,column=0, columnspan=12)
    
    #making new graph with reference to debt
    newGraph = {}
    newGraph = addNodes(newGraph, newNodes)
    newGraph = addEdges(newGraph, newEdgeList, True)
    
    print(newGraph)
    
    #graph = Graph(root, newGraph)
    create_graph(newGraph, final_lst)

    return count

def create_graph(data, final_lst):
    nodes = {}
    edges = []

    canvas = Canvas(root, width=500, height=500,bg='yellow')
    canvas.grid(row = len(final_lst)+10, column = 0, columnspan=500)

    for node, connections in data.items():
        while True:
            x, y = get_random_coords()
            if not check_overlap(x, y, nodes):
                break
        nodes[node] = (x, y)
        for connection, cost in connections:
            edges.append((node, connection, cost))

    draw_nodes(canvas, nodes)
    draw_edges(canvas, nodes, edges)

#reference of algorithm 
#https://www.codingninjas.com/codestudio/problem-details/minimize-cash-flow-among-a-given-set-of-friends-who-have-borrowed-money-from-each-other_1170048


# example usage
# transactions = [('A', 'B', 100), ('B', 'C', 50), ('C', 'A', 75), ('D', 'A', 25)]
# min_count = min_cash_flow(Graph)
# print(f'Minimum transactions required: {min_count}')

minimize_transaction=Button(root,text="minimize transaction",command =lambda: min_cash_flow(Graph),fg='blue',bg='black', padx=90).grid(row=6,column=0, columnspan=60)


root.configure(background="black")

root.mainloop()