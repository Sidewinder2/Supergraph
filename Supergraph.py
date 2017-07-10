
class Supergraph:
    def __init__(self):
        self.graphlist = {};        #dictionary maintaining a graph name to graph pointer conversion
        self.nodelist = {};         #dictionary maintaining a node name to node pointer conversion
        self.connectionlist = {};   #dictionary maintaining a connection name to connection pointer conversion
        #self.datatypelist = {};    #maintains the typing of all data stored in datalist
        self.datalist = {};         #dictionary maintaining a variable name to variable data conversion

    def addGraph(self, graphname, nodekeys = [], connectionkeys = []):
        #Adds a graph to the database
        if (graphname not in self.graphlist):
            self.graphlist[graphname] = Graph(self,graphname,nodekeys,connectionkeys);

    def removeGraph(self, graphname):
        # Removes a graph from the database
        if (graphname not in self.graphlist):
            del self.graphlist[graphname];

    def listGraphs(self):
        # Lists names of all existing graphs
        print self.graphlist.keys();

    def namesToGraphs(self, graphnames = []):
        #Converts a list of a keys to graph pointers
        returnlist = [];
        for i in graphnames:
            if (graphnames[i] in self.graphlist):
                returnlist.append(self.graphlist[graphnames[i]]);
        return returnlist;

    def addNode(self, nodename):
        # Adds a node to the database
        if (nodename not in self.nodelist):
            self.nodelist[nodename] = Node(self,nodename);

    def removeNodes(self, nodenames):
        verifiednodes = self.verifyNodeNames(nodenames);  # get list of nodes from keys
        for i in verifiednodes:
            del self.nodelist[i];

    def addNodeData(self, nodenames, varname, vardata):
        # Adds data to a list of nodes
        nodes = self.namesToNodes(nodenames);  # get list of nodes from keys
        for i in nodes:
            Node.addNodeData(nodes[i], varname, vardata);

    def removeNodeData(self, nodenames, varname, vardata):
        # Removes data from a list of nodes
        nodes = self.namesToNodes(nodenames);  # get list of nodes from keys
        for i in nodes:
            Node.removeNodeData(nodes[i], varname);

    def listNodes(self):
        #lists the node keys
        print self.nodelist.keys();

    def verifyNodeNames(self, nodenames = []):
        #Will remove any names from list that don't point to anything
        returnlist = [];
        for i in nodenames:
            if i in self.nodelist:
                returnlist.append(i); #get pointer from node list
        return returnlist;

    def namesToNodes(self, nodenames = []):
        #Converts a list of a keys to node pointers
        # Will remove any names from list that don't point to anything
        returnlist = [];
        names = Supergraph.verifyNodeNames(nodenames);
        for i in names:
            if names[i] in self.nodelist:
                returnlist.append(self.nodelist[nodenames[i]]); #get pointer from node list
        return returnlist;

    def addConnection(self, connectionname, leftname, rightname):
        #Adds a connection to the database
        if (connectionname not in self.connectionlist):
            self.connectionlist[connectionname] = Connection(self,connectionname,leftname, rightname);

    def removeConnection(self, connectionname):
        #removes the specified connection, if it exists
        if (connectionname in self.connectionlist):
            del self.connectionlist[connectionname];

    def addConnectionData(self, connectionnames, varname, vardata):
        # Adds data to a list of nodes
        nodes = self.namesToNodes(connectionnames);  # get list of nodes from keys
        for i in nodes:
            Node.addNodeData(nodes[i], varname, vardata);

    def removeNodeData(self, nodenames, varname, vardata):
        # Removes data from a list of nodes
        nodes = self.namesToNodes(nodenames);  # get list of nodes from keys
        for i in nodes:
            Node.removeNodeData(nodes[i], varname);

    def listConnections(self):
        # lists the connection keys
        print self.connectionlist.keys();

    def namesToConnections(self, connectionnames = []):
        #Converts a list of a keys to node pointers
        returnlist = [];
        for i in connectionnames:
            if (connectionnames[i] in self.connectionlist):
                returnlist.append(self.connectionlist[connectionnames[i]]); #get pointer from node list
        return returnlist;

class Graph:
    def __init__(self,supergraph,name,nodekeys,connectionkeys):
        self.supergraph = supergraph;               ##parent supergraph
        self.name = name;                           ##name uniquely identifying the graph
        self.nodekeys = nodekeys;                   ## list of node keys used in this graph
        self.connectionkeys = connectionkeys;       ## list of connection keys used in this graph

class Node:
    def __init__(self,supergraph,name):
        self.supergraph = supergraph;
        self.name = name;
        self.nodedata = {};

    def getNodeName(self):
        return self.name;

    def addNodeData(self, varname, vardata):
        if (varname not in self.nodedata):
            self.nodedata[varname] = vardata;

    def getNodeData(self, varname):
        #gets value of requested variable, none if it doesn't exist
        if (varname in self.nodedata):
            return self.nodedata[varname];
        return None;

    def removeNodeData(self, varname):
        if (varname in self.nodedata):
            del self.nodedata[varname];

class Connection:
    def __init__(self,supergraph,name,leftkey,rightkey):
        self.name = name;   #unique name of the connection; used as a key
        self.leftkey = leftkey;     #name of left node
        self.rightkey = rightkey;  # name of left node
        self.connectiondata = {};   #maintains additional information about the connection

    def getConnectionName(self):
        return self.name;

    def getLeftName(self):
        return self.leftkey;

    def getRightName(self):
        return self.rightkey;

    def addConnectionData(self, varname, vardata):
        if (varname not in self.connectiondata):
            self.connectiondata[varname] = vardata;

    def getConnectionData(self, varname):
        #gets value of requested variable, none if it doesn't exist
        if (varname in self.connectiondata):
            return self.connectiondata[varname];
        return None;

    def removeConnectionData(self, varname):
        if (varname in self.connectiondata):
            del self.connectiondata[varname];

class Evaluator:
    functionNames = ['SUM','LOGBASE','LENGTH','ABS','SQRT',
                     'NOT','ISNUMERIC','HAMMING','LEVEN','MIN',
                     'MAX','SMALLEST','LARGEST','CHOOSE',
                     'AVG','STRREPLACE'];

    @staticmethod
    def isInt_str(v):
        v = str(v).strip()
        return v == '0' or (v if v.find('..') > -1 else v.lstrip('-+').rstrip('0').rstrip('.')).isdigit();

    @staticmethod
    def checkParenCount(expression):
        if(expression.count('(') == expression.count(')')):
            return True;
        return False;

    @staticmethod
    def checkParenStacks(expression):
        #runs through the expression and checks if parentheses are paired up properly
        parencount = 0;
        for char in expression:
            if (char == '('):
                parencount += 1;
            if (char == ')'):
                parencount -= 1;
                if (parencount < 0):
                    return False;
        return True;

    @staticmethod
    def loadKeywords():
        file = open('keywords.txt', 'r');
        keywords = file.readlines();
        for i in keywords:
            Evaluator.functionNames.append(i.rstrip());
        return False;

    @staticmethod
    def evaluateExpression(expression):
        paramList = [];
        paramHeights = [];
        paramType = [];
        current_height = 0;
        operators = ['-','+','/','*','%','.'];

        tokenlist = Evaluator.tokenizeExpression(expression);


        print tokenlist;
        for token in tokenlist:
            if token == '(':
                current_height += 1;
                #print ' height ' + str(current_height);
            elif token == ')':
                current_height -= 1;
                #print ' height '+str(current_height);
            elif token in Evaluator.functionNames:
                #print ' dis be a function: ' + token;
                paramList.append(token);
                paramHeights.append(current_height);
                paramType.append('Fun');  #is a function
            elif token in operators:
                #print ' dis be an operator: ' + token;
                paramList.append(token);
                paramHeights.append(current_height);
                paramType.append('Op');  # is a literal
            elif (len(token) >= 2) and ((token[0] == '"') and (token[len(token)-1] == '"')):    #check if it's surrounded by quotes
                #print ' dis be a string: ' + token;
                paramList.append(token);
                paramHeights.append(current_height);
                paramType.append('Str');  # is a literal
            elif Evaluator.isInt_str(token):
                #print ' dis be a number: ' + token;
                paramList.append(token);
                paramHeights.append(current_height);
                paramType.append('Lit');  # is a literal
            elif token == '\t':
                placeholderforinterpreter = 0;
                #print ' this is a tab';
            elif token == ',':
                #print ' this is a comma';
                placeholderforinterpreter = 0;
            else:
                #print 'this is something else';
                paramList.append(token);
                paramHeights.append(current_height);
                paramType.append('?');  # is a literal

    #@staticmethod
    @staticmethod
    def tokenizeExpression(expression):
        #returns a list of tokens in the expression
        #tokens are parentheses, math operators, commas, function names, and literals
        print 'Expression: ' + expression;

        specialchars = ['\t','-','+','/','*','%','(',')','.'];
        literalchar = '"';      #
        returnlist = [];        #return list, containing the tokens
        current_token = '';
        isQuoted = 0;

        for char in expression:
            # if the chars are currently being parsed as literals
            if isQuoted == 1:
                if char == literalchar:     #check if the literal ends

                    returnlist.append(literalchar+current_token+literalchar);
                    current_token = "";             #reset token
                    #returnlist.append(literalchar)  #add closing marker to signify end of literal in tokens list
                    isQuoted = 0;                   #no longer interpretting text as a literal
                    #print 'UNQUOTED';
                # literal does not end
                else:
                    current_token += char;  #add current char to current literal string
            # chars are not being parsed as literals
            else:
                if char == literalchar: #check opening to literal
                    cleantoken = current_token.replace(' ', '');  # strip whitespace from current token
                    if len(cleantoken) > 0:  # check if whitespace removed token is not empty
                        returnlist.append(cleantoken);  # add it then
                    current_token = "";
                    #returnlist.append(literalchar);
                    isQuoted = 1;
                    #print 'QUOTED';
                else:
                    if char in specialchars:
                        cleantoken = current_token.replace(' ', '');  # strip whitespace from current token
                        if len(cleantoken) > 0:  # check if whitespace removed token is not empty
                            returnlist.append(cleantoken);  # add it then
                            current_token = '';
                        returnlist.append(char);
                    else:
                        current_token += char;

        #check if open quote
        if isQuoted == 1:
            print 'open quote!';

        if len(current_token) > 0:
            returnlist.append(current_token);

        return returnlist;


###DRIVER CODE###

file = open('graphdata.txt','r');
x = file.readlines();
for i in x:
    #print Evaluator.tokenizeExpression(i.rstrip());
    Evaluator.evaluateExpression(i.rstrip());
#print (file.readlines());


S = Supergraph();
S.addGraph('testgraph');
S.addNode('testnode1');
S.addNode('testnode1');
S.addNode('testnode2');
S.addNode('testnode3');
#S.listGraphs();
#S.listNodes();
#S.removeNodes(['foo','testnode2','testnode1']);
#S.removeNodes('testnode1');
#S.listNodes();

#print Evaluator.checkParenCount('())')
#print Evaluator.checkParenStacks('((())')

#print Evaluator.tokenizeExpression('((+awdtheawdaw\'d\')')

#print Evaluator.checkKeyword('LENGTH')

#print Evaluator.isInt_str('1')
#print Evaluator.isInt_str('+1')
#print Evaluator.isInt_str('-1.123')
#print Evaluator.isInt_str('12a')
#print Evaluator.isInt_str('1.a')
#Evaluator.checkKeyword('test');
#Evaluator.checkKeyword('nope');

#testlist = [1,2,3,4,5,6,7,8];
#print testlist[4:7]