
from graphviz import Graph
from collections import defaultdict


import tkinter.messagebox as messagebox

class Node:
    def __init__(self, parent, level, text, nodes):
        self.parent = parent
        self.level = level
        self.text = text
        self.children = []
        if parent > -1:
            nodes[parent].children.append(self)

    def __str__(self):
        return self.text

    def inc_level(self):
        self.level += 1
        if len(self.children) == 0: return
        for x in self.children:
            x.inc_level()

    def chg_parent(self, new):
        if self.parent > -1:
            nodes[self.parent].children.remove(self)
        self.parent = new
        if new > -1:
            nodes[new].children.append(self)


def match(token):
    global i
    global tokens
    if i >= len(tokens):
        messagebox.showerror(title="syntax Error", message=f'expected "{token}" but found nothing')

    if tokens[i][1] == token:
        i += 1
        return 1

    messagebox.showerror(title="token mismatch", message=f'expected "{token}" but found "{tokens[i][1]}"')
    
    return -1
   


def program():
    if tokens[-1][1] not in ";}" : 
        messagebox.showerror(title="syntax Error", message=f'error')
        return -1
    stmt_sequence(-1, 0)
    print('compiled successfully')


def stmt_sequence(parent, level):
    global i
    global tokens

    x = statement(parent, level)

    while i < len(tokens)-1 :
        
        if tokens[i][1] == ';' and tokens[i+1][1] == "}" :
                match(';')
                return 
        elif tokens[i][1] != ";" and tokens[i+1][1] == "}" :
               match(';')
       
        else:
             if tokens[i-1][1] != "}":
                match(";")
             elif tokens[i][1] == ";" and tokens[i-1][1] == "}":
                match(";")
             x = statement(x, level)


def statement(parent, level):
    global i
    global tokens
    if i >= len(tokens):  
        match('statement')
    if tokens[i][1] == 'if':
        return if_stmt(parent, level)
    elif tokens[i][1] == 'while':
        return while_stmt(parent, level)
    elif tokens[i][1] == 'identifier':
        return assign_stmt(parent, level)
    elif tokens[i][1] == 'cin>>':
        return cin_stmt(parent, level)
    elif tokens[i][1] == 'cout<<':
        return cout_stmt(parent, level)
    elif tokens[i][1] == 'for':
        return for_stmt(parent, level)
    else:           
        match('statement')


def if_stmt(parent, level):
    global i
    global tokens
    nodes.append(Node(parent, level, 'if', nodes))
    level += 1
    x = len(nodes) - 1
    match('if')
    match("(")
    exp(x, level)
    match(")")
    match('{')
    stmt_sequence(x, level)
    match('}')
    if i < len(tokens) and tokens[i][1] == 'else':
        nodes.append(Node(x, level, 'else', nodes))
        y = len(nodes) - 1
        match('else')
        match('{')
        stmt_sequence(y, level-1)
        match('}')
    return x


def for_stmt(parent, level):
    global i
    global tokens
    nodes.append(Node(parent, level, 'for', nodes))
    level += 1
    match('for')
    match("(")
    x = len(nodes) - 1
    if i < len(tokens) and tokens[i][1] != ";":
        assign_stmt(x, level)
    match(";")
    exp(x, level)
    match(";")
    if i < len(tokens) and tokens[i][1] != ")":
        assign_stmt(x, level)
    match(")")
    match("{")
    stmt_sequence(x, level)
    match('}')
    return x

def while_stmt(parent, level):
    global i
    global tokens
    nodes.append(Node(parent, level, 'while', nodes))
    level += 1
    match('while')
    match("(")
    x = len(nodes) - 1
    exp(x, level)
    match(")")
    match("{")
    stmt_sequence(x, level)
    match('}')
    # exp(x, level)
    return x

def assign_stmt(parent, level):
    global i
    global tokens
    nodes.append(Node(parent, level, f'assign ({tokens[i][0]})', nodes))
    x = len(nodes) - 1
    match('identifier')
    match('=')
    exp(x, level + 1)
    return x


def cin_stmt(parent, level):
    global i
    global tokens
    match('cin>>')
    nodes.append(Node(parent, level, f'cin>> ({tokens[i][0]})', nodes))
    match('identifier')
    x = len(nodes) - 1
    return x


def cout_stmt(parent, level):
    global i
    global tokens
    match('cout<<')
    nodes.append(Node(parent, level, 'cout<<', nodes))
    x = len(nodes) - 1
    exp(x, level + 1)
    return x


def exp(parent, level):
    global i
    global tokens
    x = simple_exp(parent, level)
    # op = tokens[i][1]
    if i < len(tokens) and (tokens[i][1] == '<' or tokens[i][1] == '==' or tokens[i][1] == '>' or tokens[i][1] == '!' or tokens[i][1] == '<=' or tokens[i][1] == '>=' or tokens[i][1] == '!='):
        nodes.append(Node(parent, level, f'op ({tokens[i][1]})', nodes))
        nodes[x].chg_parent(len(nodes) - 1)
        nodes[x].inc_level()
        x = len(nodes) - 1
        comparison_op()
        simple_exp(x, level + 1)
    return x


def comparison_op():
    match(tokens[i][1])


def simple_exp(parent, level):
    global i
    global tokens
    x = term(parent, level)
    while i < len(tokens) and (tokens[i][1] == '+' or tokens[i][1] == '-'):
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})', nodes))
        nodes[x].chg_parent(len(nodes) - 1)
        nodes[x].inc_level()
        x = len(nodes) - 1
        addop()
        term(x, level + 1)
    return x


def addop():
    match(tokens[i][1])


def term(parent, level):
    global i
    global tokens
    x = factor(parent, level)
    while i < len(tokens) and (tokens[i][1] == '*' or tokens[i][1] == '/'):
        nodes.append(Node(parent, level, f'op ({tokens[i][0]})', nodes))
        nodes[x].chg_parent(len(nodes) - 1)
        nodes[x].inc_level()
        x = len(nodes) - 1
        mulop()
        factor(x, level + 1)
    return x


def mulop():
    match(tokens[i][1])


def factor(parent, level):
    global i
    global tokens

    if tokens[i][1] == 'identifier':
        nodes.append(Node(parent, level, f'id ({tokens[i][0]})', nodes))
        match('identifier')
    elif tokens[i][1] == 'number':
        nodes.append(Node(parent, level, f'const ({tokens[i][0]})', nodes))
        match('number')
  
    return len(nodes) - 1


def get_shape(label):
    label = label.split(' ', 1)[0]
    if label in ['read', 'assign', 'if', 'repeat', 'write']:
        return 'rectangle'
    return ''


def draw(nodes):
    nodes_clustered = defaultdict(list)
    for i, node in enumerate(nodes):
        nodes_clustered[node.level].append((i,node))

    g = Graph('tree', format='png')
    g.attr(ordering="out")
    g.attr(nodesep='0.5;')
    for level, node_list in sorted(nodes_clustered.items()):
      
        with g.subgraph() as s:
            s.attr(rank='same')
            for data in node_list: s.node(str(data[0]), data[1].text,shape=get_shape(data[1].text))

    for i, node in enumerate(nodes):
        if i == 0: continue
        g.edge(str(node.parent), str(i))
    g.view()
