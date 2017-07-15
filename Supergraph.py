
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

    def getNodeList(self):
        #lists the node keys
        return self.nodelist.keys();

    def printNodeList(self):
        #lists the node keys
        print self.nodelist.keys();

    def addNodeData(self, nodenames, varname, vardata, vartype):
        # Adds data to a list of nodes
        nodes = self.namesToNodes(nodenames);  # get list of nodes from keys
        for i in nodes:
            Node.addNodeData(i, varname, vardata, vartype);

    def getNodeData(self, nodenames, varname):
        # Adds data to a list of nodes
        nodes = self.namesToNodes(nodenames);  # get list of nodes from keys
        returnlist = [[],[]];
        for i in nodes:
            typevalue = Node.getNodeData(i, varname);   #get the array containing the type and value of the data
            if typevalue is not None:
                type = typevalue[0];
                value = typevalue[1];
                returnlist[0].append(type);
                returnlist[1].append(value);
        return returnlist;

    def removeNodeData(self, nodenames, varname):
        # Removes data from a list of nodes
        nodes = self.namesToNodes(nodenames);  # get list of nodes from keys
        for i in nodes:
            Node.removeNodeData(nodes[i], varname);

    def verifyNodeNames(self, nodenames = []):
        #Will remove any names from list that don't point to anything
        returnlist = [];
        for i in nodenames:
            if i in self.nodelist.keys():
                returnlist.append(i); #get pointer from node list
        return returnlist;

    def namesToNodes(self, nodenames = []):
        #Converts a list of a keys to node pointers
        # Will remove any names from list that don't point to anything
        returnlist = [];
        names = Supergraph.verifyNodeNames(self,nodenames);
        for i in names:
            if i in self.nodelist.keys():
                returnlist.append(self.nodelist[i]); #get pointer from node list
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
        self.nodedatatype = {};

    def getNodeName(self):
        return self.name;

    def addNodeData(self, varname, vardata, vartype):
        if (varname not in self.nodedata) and varname != "name":
            self.nodedata[varname] = vardata;
            self.nodedatatype[varname] = vartype;

    def getNodeData(self, varname):
        #gets type and value of requested variable, none if it doesn't exist
        if (varname in self.nodedata):
            #print "RETURNING " + self.name + ": "+str([self.nodedatatype[varname],self.nodedata[varname]])
            return [self.nodedatatype[varname],self.nodedata[varname]];
        if varname == "name":
            return ["Str",self.name];
        return None;

    def removeNodeData(self, varname):
        if (varname in self.nodedata):
            del self.nodedata[varname];
            del self.nodedatatype[varname];

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
    S = Supergraph();
    functionNames = ['SUM','LOGBASE','LENGTH','ABS','SQRT',
                     'NOT','ISNUMERIC','HAMMING','LEVEN','MIN',
                     'MAX','SMALLEST','LARGEST','CHOOSE',
                     'AVG','STRREPLACE','PRINT','LISTNODES','ADDNODES',
                     'GETNODES','REMOVENODES','ADDNODEDATA','GETNODEDATA'];

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
    def categorizeToken(token):
        operators = ['-', '+', '/', '%', '.'];

        if token == '(':
           return '(';
        elif token == ')':
            return ')';
        elif token in Evaluator.functionNames:
            return 'Fun';
        elif token in operators:
            return 'Op';
        elif (len(token) >= 2) and ((token[0] == '"') and (token[len(token) - 1] == '"')):  # check if it's surrounded by quotes
            return 'Str';
        elif Evaluator.isInt_str(token):
            return 'Num';
        elif token == '\t':
            return 'Tab';
        elif token == ',':
            return 'Comma';
        elif token == '*':
            return '*';
        else:
            return '?';     #unknown; likely variable

    @staticmethod
    def checkAllTypes(paramtypes=[],validparamtypes=[]):
        #checks to see if all values in paramtypes match up with valid types
        for type in paramtypes:
            if type not in validparamtypes:
                return False;
        return True;

    @staticmethod
    def evaluateFunction(function,parameters,paramtypes):
        #returns a list of [returntype,returnvalue] after applying the designated function
        #Returns ["E","errormessage] in the event of failure

        if "E" in paramtypes:
            return ["E","General Failure"];
        if "V" in paramtypes:
            return ["E","Cannot manipulate Void type"];
        if(function == "PRINT"):
            print parameters;
            return ["V", ""];
        if (function in ["+","SUM"]):
            allDigits = True;
            result = 0;
            for type in paramtypes:
                if type not in ["Str","Num"]:
                    return ["E", "Input of type "+type+" cannot be summed"];
                if type != "Num":
                    result = "";
                    for param in parameters:
                        result += str(param);
                    return ["Str",result];
            result = 0;
            for param in parameters:
                result += int(param);
            return ["Num", result];

        if (function in ["ADDNODES"]):
            for type in paramtypes:
                if type not in ["Str"]:
                    return ["E", "Input of type "+type+" cannot be added to supergraph"];
            for param in parameters:
                Supergraph.addNode(Evaluator.S,param);
            return ["V", ""];

        if (function in ["LISTNODES"]):
            if len(parameters) > 0:
                return ["E", "Unexpected parameters given"];
            Supergraph.printNodeList(Evaluator.S);
            return ["V", ""];

        if (function in ["GETNODES"]):
            if len(parameters) > 1:
                if Evaluator.checkAllTypes(paramtypes,['Str']):
                    return ["N", Supergraph.verifyNodeNames(Evaluator.S, parameters)];
                return ["E", "Unexpected parameters given"];
            elif len(parameters) == 1:
                if paramtypes[0] == 'Str':
                    return ["N", Supergraph.verifyNodeNames(Evaluator.S,parameters)];
                if paramtypes[0] == '*':
                    return ["N", Supergraph.getNodeList(Evaluator.S)];
            else:
                return ["N", Supergraph.getNodeList(Evaluator.S)];

        if (function in ["ADDNODEDATA"]):
            if len(parameters) == 3:
                #nodenames, varname, vardata
                if (paramtypes[0:2] == ['N','Str']) and (paramtypes[2] in ['Str','Num']):
                    Supergraph.printNodeList(Evaluator.S)
                    #print Supergraph.verifyNodeNames(Evaluator.S,parameters[0])
                    Supergraph.addNodeData(Evaluator.S,parameters[0],parameters[1],parameters[2],paramtypes[2])
                    return ["V", ""];
                else:
                    return ["E", "Unexpected parameters given"];
            else:
                return ["E", "Unexpected parameters given"];

        if (function in ["GETNODEDATA"]):
            if len(parameters) == 2:
                #nodenames, varname, vardata
                if (paramtypes[0:2] == ['N','Str']):
                    returnlist = Evaluator.S.getNodeData(parameters[0],parameters[1]);
                    return ["L", returnlist];
                else:
                    return ["E", "Unexpected parameters given"];
            else:
                return ["E", "Unexpected parameters given"];

        if (function in ["REMOVENODES"]):
            if len(parameters) > 1:
                if Evaluator.checkAllTypes(paramtypes,['Str']):
                    Evaluator.S.removeNodes(Supergraph.verifyNodeNames(Evaluator.S, parameters));
                    return ["V", ""];
                return ["E", "Unexpected parameters given"];
            elif len(parameters) == 1:
                if paramtypes[0] == 'Str':
                    Evaluator.S.removeNodes(Supergraph.verifyNodeNames(Evaluator.S,parameters));
                    return ["V", ""];
                if paramtypes[0] == 'N':
                    Evaluator.S.removeNodes(Supergraph.verifyNodeNames(Evaluator.S, parameters));
                    return ["V", ""];
                if paramtypes[0] == '*':
                    Evaluator.S.removeNodes(Supergraph.getNodeList(Evaluator.S))
                    return ["V", ""];
            else:
                return ["E", "Unexpected parameters given"];

        return ["E", "Unknown function "+function];


    @staticmethod
    def evaluateExpression(expression):
        #parameter stacks
        paramStack = [[]];  #holds parameter lists
        paramHeights = [0]; #Maintains the parenthesis depth of each list in paramStack
        paramType = [[]];   #details what type of variable is held. Corresponds to each value in paramStack
        #operation/function stacks
        opStack = [];       #Actual operation/function name
        opHeight = [];      #Parenthesis depth of function/operator
        opType = [];        #Determines whether an operator or a function
        #height
        current_height = 0; #Used for keeping track of the current parenthesis depth

        #tokenize the input expression
        tokenlist = Evaluator.tokenizeExpression(expression);
        #print tokenlist;

        #run through each token and evaluate expression
        for token in tokenlist:
            #get the category of the current token to determine what to do
            category = Evaluator.categorizeToken(token);
            #print category;

            if category == '(':
                #increase the height
                current_height += 1;
                #make a new parameter list at new height
                paramStack.append([]);
                paramHeights.append(current_height);
                paramType.append([]);
            elif category == ')':
                #set height to one less, and update height of topmost parameters
                current_height -= 1;
                paramHeights[-1] = current_height;

                # check for possible function call
                if (len(opStack) > 0) and opType[-1] == 'Fun':
                    #check if function and current parameter heights match up
                    if opHeight[-1] == paramHeights[-1]:
                        #Evaluate result of function call
                        result = Evaluator.evaluateFunction(opStack[-1],paramStack[-1],paramType[-1]);
                        #report any errors
                        if (result[0] == "E"):
                            print result;
                            return;

                        #Add results to stacks
                        paramStack[-1] = [result[1]];
                        paramType[-1] = [result[0]];
                        # (paramType[-1])[-1] = result[0];

                        #pop function from stack
                        opType.pop()
                        opHeight.pop()
                        opStack.pop()

                #merge the paramaters list within the parenthesis with ones "below" them
                #EX: 3,(4,5) <-> [[3],[4,5]] becomes  3,4,5 <-> [[3,4,5]]
                paramStack[-2] = paramStack[-2] + paramStack[-1];
                paramStack.pop()
                paramHeights.pop()
                paramType[-2] = paramType[-2] + paramType[-1];
                paramType.pop()

            elif category == "Fun" or category == "Op":
                #Add operation/function to operation stack
                opStack.append(token);
                opType.append(category);
                opHeight.append(current_height);
            elif category == "Str":
                #Add new parameter to the list at the top of the stack
                paramStack[-1].append(token[1:-1]); #remove the " from start and end of string
                #paramStack[-1].append(token);
                paramType[-1].append(category);
            elif category == "Num":
                paramStack[-1].append(int(token));
                paramType[-1].append(category);
            elif category == "*":
                paramStack[-1].append(token);
                paramType[-1].append(category);

            #At end, check if a binary operation is possible
            if (len(opStack) > 0):
                if opType[-1] == 'Op':
                    #check if 2 or more parameters in topmost list
                    if len(paramStack[-1]) > 1:
                        #check if height of top list and top operator match
                        if opHeight[-1] == paramHeights[-1]:
                            #get left and right values
                            p2 = paramStack[-1].pop()
                            pt2 = paramType[-1].pop()
                            p1 = paramStack[-1].pop()
                            pt1 = paramType[-1].pop()
                            #Evaluate the binary operator
                            result = Evaluator.evaluateFunction("+",[p1,p2],[pt1,pt2]);
                            #Report error
                            if(result[0] == "E"):
                                print result;
                                return;
                            #put results in stacks
                            paramStack[-1].append(result[1]);
                            paramType[-1].append(result[0]);
                            #remove operator from top of stack
                            opType.pop()
                            opHeight.pop()
                            opStack.pop()

        print 'END OF EVALUATION PARAMETERS: ' +str(paramStack);

    #@staticmethod
    @staticmethod
    def tokenizeExpression(expression):
        #returns a list of tokens in the expression
        #tokens are parentheses, math operators, commas, function names, and literals
        print 'Expression: ' + expression;

        specialchars = ['\t','-','+','/','*','%','(',')','.',','];
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

file = open('script.txt','r');
x = file.readlines();
for i in x:
#     #print Evaluator.tokenizeExpression(i.rstrip());
     Evaluator.evaluateExpression(i.rstrip());


#                     __
#        _______     /*_)-< HISS HISS
#  ___ /  _____  \__/ /
# < ____ /     \____ /