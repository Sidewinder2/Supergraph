
class Supergraph:
    def __init__(self):
        self.graphlist = {}        # dictionary maintaining a graph name to graph pointer conversion
        self.nodelist = {}         # dictionary maintaining a node name to node pointer conversion
        self.connectionlist = {}   # dictionary maintaining a connection name to connection pointer conversion
        self.supergraphdata = {}   # dictionary maintaining a variable name to variable data conversion
        self.supergraphdatatype = {}   # maintains the typing of all data stored in datalist

        self.connectionidprefix = "Connection"
        self.connectionidsuffix = 0   # ID counter for naming connections automatically

    def addData(self,  varname,  vardata,  vartype):
        if (varname not in self.supergraphdata) and varname != "name":
            self.supergraphdata[varname] = vardata
            self.supergraphdatatype[varname] = vartype

    def getData(self,  varname):
        # gets type and value of requested variable,  none if it doesn't exist
        if varname in self.supergraphdata:
            # print "RETURNING " + self.name + ": "+str([self.nodedatatype[varname], self.nodedata[varname]])
            return [self.supergraphdatatype[varname], self.supergraphdata[varname]]
        return None

    def removeData(self,  varname):
        if varname in self.supergraphdata:
            del self.supergraphdata[varname]
            del self.supergraphdatatype[varname]

    def addGraph(self,  graphname,  nodekeys = [],  connectionkeys = []):
        # Adds a graph to the database
        if (graphname not in self.graphlist):
            self.graphlist[graphname] = Graph(self,  graphname,  nodekeys,  connectionkeys)

    def removeGraph(self,  graphname):
        #  Removes a graph from the database
        if (graphname not in self.graphlist):
            del self.graphlist[graphname]

    def listGraphs(self):
        #  Lists names of all existing graphs
        print self.graphlist.keys()

    def namesToGraphs(self,  graphnames = []):
        # Converts a list of a keys to graph pointers
        returnlist = []
        for i in graphnames:
            if (graphnames[i] in self.graphlist):
                returnlist.append(self.graphlist[graphnames[i]])
        return returnlist

    def addNode(self,  nodename):
        #  Adds a node to the database
        if (nodename not in self.nodelist):
            self.nodelist[nodename] = Node(self, nodename)

    def removeNodes(self,  nodenames):
        verifiednodes = self.verifyNodeNames(nodenames)     # get list of nodes from keys
        for nodename in verifiednodes:
            del self.nodelist[nodename]

    def getNodeList(self):
        # lists the node keys
        return self.nodelist.keys()

    def printNodeList(self):
        # lists the node keys
        print self.nodelist.keys()

    def verifyNodeNames(self,  nodenames = []):
        # Will remove any names from list that don't point to anything
        returnlist = []
        for name in nodenames:
            if name in self.nodelist.keys():
                returnlist.append(name) # add valid name to list
        return returnlist

    def namesToNodes(self,  nodenames = []):
        # Converts a list of a keys to node pointers
        #  Will remove any names from list that don't point to anything
        returnlist = []
        names = Supergraph.verifyNodeNames(self, nodenames)
        for i in names:
            returnlist.append(self.nodelist[i]) # get pointer from node list
        return returnlist

    def addNodeData(self,  nodenames,  varname,  vardata,  vartype):
        #  Adds data to a list of nodes
        nodes = self.namesToNodes(nodenames)  #  get list of nodes from keys
        for i in nodes:
            Node.addNodeData(i,  varname,  vardata,  vartype)

    def getNodeData(self,  nodenames,  varname):
        #  Adds data to a list of nodes
        nodes = self.namesToNodes(nodenames)  #  get list of nodes from keys
        returnlist = [[], []]
        for i in nodes:
            typevalue = Node.getNodeData(i,  varname)   # get the array containing the type and value of the data
            if typevalue is not None:
                type = typevalue[0]
                value = typevalue[1]
                returnlist[0].append(type)
                returnlist[1].append(value)
        return returnlist

    def removeNodeData(self,  nodenames,  varname):
        #  Removes data from a list of nodes
        nodes = self.namesToNodes(nodenames)  #  get list of nodes from keys
        for node in nodes:
            Node.removeNodeData(nodes[i],  varname)
            
    def addConnection(self,  connectionname,  leftname,  rightname):
        # Adds a connection to the database
        if (connectionname not in self.connectionlist):
            self.connectionlist[connectionname] = Connection(self, connectionname, leftname,  rightname)

    def addConnections(self,  leftnames,  rightnames):
        # Adds connections to the database
        # Will connect every node from left side to right side,  resulting in L * R connections
        for left in leftnames:
            for right in rightnames:
                connectionname = self.getNextConnectionName()
                self.addConnection(connectionname, left, right)

    def removeConnections(self,  connectionnames):
        # removes the specified connections,  if they exist
        for connection in connectionnames:
            if (connection in self.connectionlist):
                del self.connectionlist[connection]

    def getConnectionList(self):
        # lists the node keys
        return self.connectionlist.keys()

    def printConnectionList(self):
        # lists the node keys
        print self.connectionlist.keys()
        
    def getNextConnectionName(self):
        # Used for automatically naming connections
        # Will update id counter to make it as up to date as possible
        connectname = self.connectionidprefix + str(self.connectionidsuffix)
        while connectname in self.connectionlist:
            self.connectionidsuffix += 1
            connectname = self.connectionidprefix + str(self.connectionidsuffix)
        return connectname

    def verifyConnectionNames(self,  connectionnames = []):
        # Will remove any names from list that don't point to anything
        returnlist = []
        for name in connectionnames:
            if name in self.connectionlist.keys():
                returnlist.append(name) #append valid name to list
        return returnlist

    def namesToConnections(self,  connectionnames = []):
        # Converts a list of a keys to connection pointers
        #  Will remove any names from list that don't point to anything
        returnlist = []
        verifiednames = Supergraph.verifyConnectionNames(self, connectionnames)
        for name in verifiednames:
            returnlist.append(self.connectionlist[name]) # get pointer from node list
        return returnlist

class Graph:
    def __init__(self, supergraph, name, nodekeys, connectionkeys):
        self.supergraph = supergraph               # parent supergraph
        self.name = name                           # name uniquely identifying the graph
        self.nodekeys = nodekeys                   # list of node keys used in this graph
        self.connectionkeys = connectionkeys       # list of connection keys used in this graph

class Node:
    def __init__(self, supergraph, name):
        self.supergraph = supergraph
        self.name = name
        self.nodedata = {}
        self.nodedatatype = {}

    def getNodeName(self):
        return self.name

    def addNodeData(self,  varname,  vardata,  vartype):
        if varname not in self.nodedata and varname != "name":
            self.nodedata[varname] = vardata
            self.nodedatatype[varname] = vartype

    def getNodeData(self,  varname):
        # gets type and value of requested variable,  none if it doesn't exist
        if varname in self.nodedata:
            # print "RETURNING " + self.name + ": "+str([self.nodedatatype[varname], self.nodedata[varname]])
            return [self.nodedatatype[varname], self.nodedata[varname]]
        if varname == "name":
            return ["Str", self.name]
        return None

    def removeNodeData(self,  varname):
        if varname in self.nodedata:
            del self.nodedata[varname]
            del self.nodedatatype[varname]


class Connection:
    def __init__(self, supergraph, name, leftkey, rightkey):
        self.name = name   # unique name of the connection used as a key
        self.supergraph = supergraph;
        self.leftkey = leftkey     # name of left node
        self.rightkey = rightkey    #  name of left node
        self.connectiondata = {}    # maintains additional information about the connection
        self.connectiondatatype = {}  # maintains additional information about the connection

    def getConnectionName(self):
        return self.name

    def getLeftName(self):
        return self.leftkey

    def getRightName(self):
        return self.rightkey

    def addConnectionData(self,  varname,  vardata,  vartype):
        if varname not in self.connectiondata and varname != "name":
            self.connectiondata[varname] = vardata
            self.connectiondatatype[varname] = vartype

    def getConnectionData(self,  varname):
        # gets type and value of requested variable,  none if it doesn't exist
        if varname in self.connectiondata:
            # print "RETURNING " + self.name + ": "+str([self.nodedatatype[varname], self.nodedata[varname]])
            return [self.connectiondatatype[varname], self.connectiondata[varname]]
        if varname == "leftname":
            return ["Str", self.leftkey]
        if varname == "rightname":
            return ["Str", self.rightkey]
        if varname == "name":
            return ["Str", self.name]
        return None

    def removeConnectionData(self,  varname):
        if varname in self.connectiondata:
            del self.connectiondata[varname]
            del self.connectiondatatype[varname]

class Evaluator:
    S = Supergraph()
    function_names = ['PRINT', 'GETTIME',
                      'SUM', 'SUBTRACT','MULTIPLY', 'DIVIDE',
                      'ABS', 'SQRT', 'SIZE',
                      'LOGBASE', 'LENGTH',
                      'NOT', 'ISNUMERIC', 'HAMMING', 'LEVEN', 'MIN',
                      'MAX', 'SMALLEST', 'LARGEST', 'CHOOSE',
                      'AVG', 'STRREPLACE',
                      'ADDDATA', 'REMOVEDATA',
                      'LISTNODES', 'ADDNODES', 'GETNODES', 'REMOVENODES',
                      'ADDNODEDATA', 'GETNODEDATA', 'REMOVENODEDATA',
                      'LISTCONNECTIONS','ADDCONNECTIONS','GETCONNECTIONS','REMOVECONNECTIONS']


    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def checkParenCount(expression):
        if(expression.count('(') == expression.count(')')):
            return True
        return False

    @staticmethod
    def checkParenStacks(expression):
        # runs through the expression and checks if parentheses are paired up properly
        parencount = 0
        for char in expression:
            if char == '(':
                parencount += 1
            if char == ')':
                parencount -= 1
                if parencount < 0:
                    return False
        return True

    @staticmethod
    def loadKeywords():
        file = open('keywords.txt', 'r')
        keywords = file.readlines()
        for keyword in keywords:
            Evaluator.function_names.append(keyword.rstrip())
        return False

    @staticmethod
    def categorizeToken(token):
        operators = ['-',  '+',  '/',  '%']
        quote_chars = ["'", '"']

        if token == '(':
            return '('
        elif token == ')':
            return ')'
        elif token in Evaluator.function_names:
            return 'Fun'
        elif token in operators:
            return 'Op'
        elif (len(token) >= 2) and ((token[0] in quote_chars) and (token[len(token) - 1] in quote_chars)):
            return 'Str'
        elif Evaluator.is_number(token):
            return 'Num'
        elif token == '\t':
            return 'Tab'
        elif token == ', ':
            return 'Comma'
        elif token == '*':
            return '*'
        else:
            return '?'     # unknown likely variable

    @staticmethod
    def checkAllTypes(paramtypes=[], validparamtypes=[]):
        # checks to see if all values in paramtypes match up with valid types
        for paramtype in paramtypes:
            if paramtype not in validparamtypes:
                return False
        return True

    @staticmethod
    def evaluateFunction(function, parameters, paramtypes):
        # returns a list of [returntype, returnvalue] after applying the designated function
        # Returns ["E", "errormessage] in the event of failure

        if "E" in paramtypes:
            return ["E",  "General Failure"]
        if "V" in paramtypes:
            return ["E",  "Cannot manipulate Void type"]

        if function == "PRINT":
            print parameters
            return ["V",  ""]

        if function == "GETTIME":
            if len(parameters) == 0:
                return ["Num", time.time()]
            else:
                return ["E", "Unexpected parameters given"]

        if function in ["+", "SUM"]:
            for type in paramtypes:
                if type not in ["Str", "Num"]:
                    return ["E",  "Input of type "+type+" cannot be summed"]
                if type != "Num":
                    result = ""
                    for param in parameters:
                        result += str(param)
                    return ["Str", result]
            result = 0
            for param in parameters:
                result += float(param)
            return ["Num",  result]

        if function in ["-", "SUBTRACT"]:
            if len(parameters) == 2:
                if Evaluator.checkAllTypes(paramtypes,  ['Num']):
                    return ["Num",  float(parameters[0]) - float(parameters[1])]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "2 Parameters expected"]

        if (function in ["*", "MULTIPLY"]):
            if len(parameters) == 2:
                if Evaluator.checkAllTypes(paramtypes, ['Num']):
                    return ["Num", float(parameters[0]) * float(parameters[1])]
                else:
                    return ["E", "Unexpected parameters given"]
            else:
                return ["E", "2 Parameters expected"]

        if (function in ["/", "DIVIDE"]):
            if len(parameters) == 2:
                if Evaluator.checkAllTypes(paramtypes,  ['Num']):
                    return ["Num",  float(parameters[0]) / float(parameters[1])]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "2 Parameters expected"]

        if (function in ["ABS"]):
            if len(parameters) == 1:
                if Evaluator.checkAllTypes(paramtypes,  ['Num']):
                    return ["Num",  abs(float(parameters[0]))]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "1 Parameter expected"]

        if (function in ["SQRT"]):
            print parameters
            if len(parameters) == 1:
                if Evaluator.checkAllTypes(paramtypes,  ['Num']):
                    result = parameters[0] ** (1.0 / 2) #raise the power of parameter to 1/2, giving square root
                    return ["Num",  result]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "1 Parameter expected"]

        if function == "SIZE":
            if len(parameters) == 1:
                if paramtypes[0] in ["L", "N", "C"]:
                    return ["Num", len(parameters[0])]
                else:
                    return ["E", "Unexpected parameters given"]
            else:
                return ["E", "Too many parameters given"]

        if function in ["AVG"]:
            if Evaluator.checkAllTypes(paramtypes,  ['Num']):
                if len(parameters) > 0:
                    print "AVG: "+str(parameters)
                    sum = 0
                    result = 0
                    for param in parameters:
                        sum += float(param)
                    result = sum / len(parameters)
                    return ["Num",  result]
                else:
                    return ["E",  "At least one parameter must be supplied"]
            else:
                return ["E",  "Unexpected parameters given"]

        if function in ["ADDDATA"]:
            if len(parameters) == 2:
                #  varname,  vardata
                if (paramtypes[0] == 'Str') and (paramtypes[1] in ['Str', 'Num', 'N', 'C', 'L']):
                    # print Supergraph.verifyNodeNames(Evaluator.S, parameters[0])
                    Supergraph.addData(Evaluator.S, parameters[0], parameters[1], paramtypes[1])
                    return ["V",  ""]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "Unexpected parameters given"]

        if function in ["REMOVEDATA"]:
            if len(parameters) == 1:
                #  varname,  vardata
                if (paramtypes[0] == 'Str'):
                    # print Supergraph.verifyNodeNames(Evaluator.S, parameters[0])
                    Supergraph.removeData(Evaluator.S, parameters[0])
                    return ["V",  ""]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "Unexpected parameters given"]

        if function in ["LISTNODES"]:
            if len(parameters) > 0:
                return ["E",  "Unexpected parameters given"]
            Supergraph.printNodeList(Evaluator.S)
            return ["V",  ""]

        if function in ["ADDNODES"]:
            for type in paramtypes:
                if type not in ["Str"]:
                    return ["E", "Input of type " + type + " cannot be added to supergraph"]
            for param in parameters:
                Supergraph.addNode(Evaluator.S, param)
            return ["V", ""]

        if function in ["GETNODES"]:
            # converts a list of names into a nodelist,  removing ones that don't exist in the supergraph
            if len(parameters) > 1:
                if Evaluator.checkAllTypes(paramtypes, ['Str']):
                    return ["N",  Supergraph.verifyNodeNames(Evaluator.S,  parameters)]
                return ["E",  "Unexpected parameters given"]
            elif len(parameters) == 1:
                if paramtypes[0] == 'Str':
                    return ["N",  Supergraph.verifyNodeNames(Evaluator.S, parameters)]
                if paramtypes[0] == '*':
                    return ["N",  Supergraph.getNodeList(Evaluator.S)]
            else:
                return ["N",  Supergraph.getNodeList(Evaluator.S)]

        if function in ["REMOVENODES"]:
            if len(parameters) > 1:
                if Evaluator.checkAllTypes(paramtypes, ['Str']):
                    Evaluator.S.removeNodes(Supergraph.verifyNodeNames(Evaluator.S, parameters))
                    return ["V", ""]
                return ["E", "Unexpected parameters given"]
            elif len(parameters) == 1:
                if paramtypes[0] == 'Str':
                    Evaluator.S.removeNodes(Supergraph.verifyNodeNames(Evaluator.S, parameters))
                    return ["V", ""]
                if paramtypes[0] == 'N':
                    Evaluator.S.removeNodes(Supergraph.verifyNodeNames(Evaluator.S, parameters))
                    return ["V", ""]
                if paramtypes[0] == '*':
                    Evaluator.S.removeNodes(Supergraph.getNodeList(Evaluator.S))
                    return ["V", ""]
            else:
                return ["E", "Unexpected parameters given"]

        if function in ["ADDNODEDATA"]:
            if len(parameters) == 3:
                # nodenames,  varname,  vardata
                if (paramtypes[0:2] == ['N', 'Str']) and (paramtypes[2] in ['Str', 'Num']):
                    # print Supergraph.verifyNodeNames(Evaluator.S, parameters[0])
                    Supergraph.addNodeData(Evaluator.S, parameters[0], parameters[1], parameters[2], paramtypes[2])
                    return ["V",  ""]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "Unexpected parameters given"]

        if function in ["REMOVENODEDATA"]:
            if len(parameters) == 3:
                # nodenames,  varname
                if (paramtypes[0:2] == ['N', 'Str']):
                    # print Supergraph.verifyNodeNames(Evaluator.S, parameters[0])
                    Supergraph.removeNodeData(Evaluator.S, parameters[0], parameters[1])
                    return ["V",  ""]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "Unexpected parameters given"]

        if function in ["GETNODEDATA"]:
            if len(parameters) == 2:
                # nodenames,  varname,  vardata
                if paramtypes[0:2] == ['N', 'Str']:
                    returnlist = Evaluator.S.getNodeData(parameters[0], parameters[1])
                    return ["L",  returnlist]
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "Unexpected parameters given"]

        if function in ["LISTCONNECTIONS"]:
            if len(parameters) > 0:
                return ["E", "Unexpected parameters given"]
            Supergraph.printConnectionList(Evaluator.S)
            return ["V", ""]

        if function in ["ADDCONNECTIONS"]:
            if len(parameters) == 2:
                if Evaluator.checkAllTypes(paramtypes,  ['N']):
                    Evaluator.S.addConnections(parameters[0], parameters[1])
                else:
                    return ["E",  "Unexpected parameters given"]
            else:
                return ["E",  "Unexpected parameters given"]

        if function in ["GETCONNECTIONS"]:
            # converts a list of names into a nodelist,  removing ones that don't exist in the supergraph
            if len(parameters) > 1:
                if Evaluator.checkAllTypes(paramtypes, ['Str']):
                    return ["N", Supergraph.verifyConnectionNames(Evaluator.S, parameters)]
                return ["E", "Unexpected parameters given"]
            elif len(parameters) == 1:
                if paramtypes[0] == 'Str':
                    return ["N", Supergraph.verifyConnectionNames(Evaluator.S, parameters)]
                if paramtypes[0] == '*':
                    return ["N", Supergraph.getConnectionList(Evaluator.S)]
            else:
                return ["N", Supergraph.getConnectionList(Evaluator.S)]

        if function in ["REMOVECONNECTIONS"]:
            if len(parameters) > 1:
                if Evaluator.checkAllTypes(paramtypes, ['Str']):
                    Evaluator.S.removeConnections(Supergraph.verifyConnectionNames(Evaluator.S,  parameters))
                    return ["V",  ""]
                return ["E",  "Unexpected parameters given"]
            elif len(parameters) == 1:
                if paramtypes[0] == 'Str':
                    Evaluator.S.removeConnections(Supergraph.verifyConnectionNames(Evaluator.S,  parameters))
                    return ["V",  ""]
                if paramtypes[0] == 'C':
                    Evaluator.S.removeConnections(Supergraph.verifyConnectionNames(Evaluator.S,  parameters))
                    return ["V",  ""]
                if paramtypes[0] == '*':
                    Evaluator.S.removeConnections(Supergraph.getConnectionList(Evaluator.S))
                    return ["V",  ""]
            else:
                return ["E",  "Unexpected parameters given"]

        # return error if no function defintion found
        return ["E", "Unknown function " + function]

    @staticmethod
    def evaluateExpression(expression):
        # parameter stacks
        paramStack = [[]]  # holds parameter lists
        paramHeights = [0] # Maintains the parenthesis depth of each list in paramStack
        paramType = [[]]   # details what type of variable is held. Corresponds to each value in paramStack
        # operation/function stacks
        opStack = []       # Actual operation/function name
        opHeight = []      # Parenthesis depth of function/operator
        opType = []        # Determines whether an operator or a function
        # height
        current_height = 0 # Used for keeping track of the current parenthesis depth

        # tokenize the input expression
        tokenlist = Evaluator.tokenizeExpression(expression)
        # print tokenlist

        # run through each token and evaluate expression
        for token in tokenlist:
            # get the category of the current token to determine what to do
            category = Evaluator.categorizeToken(token)
            # print category

            if category == '(':
                # increase the height
                current_height += 1
                # make a new parameter list at new height
                paramStack.append([])
                paramHeights.append(current_height)
                paramType.append([])
            elif category == ')':
                # set height to one less,  and update height of topmost parameters
                current_height -= 1
                paramHeights[-1] = current_height

                #  check for possible function call
                if (len(opStack) > 0) and opType[-1] == 'Fun':
                    # check if function and current parameter heights match up
                    if opHeight[-1] == paramHeights[-1]:
                        # Evaluate result of function call
                        result = Evaluator.evaluateFunction(opStack[-1], paramStack[-1], paramType[-1])
                        # report any errors
                        if result[0] == "E":
                            print result
                            return

                        # Add results to stacks
                        paramStack[-1] = [result[1]]
                        paramType[-1] = [result[0]]
                        #  (paramType[-1])[-1] = result[0]

                        # pop function from stack
                        opType.pop()
                        opHeight.pop()
                        opStack.pop()

                # merge the paramaters list within the parenthesis with ones "below" them
                # EX: 3, (4, 5) <-> [[3], [4, 5]] becomes  3, 4, 5 <-> [[3, 4, 5]]
                paramStack[-2] = paramStack[-2] + paramStack[-1]
                paramStack.pop()
                paramHeights.pop()
                paramType[-2] = paramType[-2] + paramType[-1]
                paramType.pop()

            elif category == "Fun" or category == "Op":
                # Add operation/function to operation stack
                opStack.append(token)
                opType.append(category)
                opHeight.append(current_height)
            elif category == "Str":
                # Add new parameter to the list at the top of the stack
                paramStack[-1].append(token[1:-1]) # remove the " from start and end of string
                # paramStack[-1].append(token)
                paramType[-1].append(category)
            elif category == "Num":
                paramStack[-1].append(float(token))
                paramType[-1].append(category)
            elif category == "*":
                paramStack[-1].append(token)
                paramType[-1].append(category)
            elif category == "?":
                data = Evaluator.S.getData(token)
                if data is not None:
                    paramStack[-1].append(data[1])
                    paramType[-1].append(data[0])

            # At end,  check if a binary operation is possible
            if len(opStack) > 0:
                if opType[-1] == 'Op':
                    # check if 2 or more parameters in topmost list
                    if len(paramStack[-1]) > 1:
                        # check if height of top list and top operator match
                        if opHeight[-1] == paramHeights[-1]:
                            # get left and right values
                            rightparam = paramStack[-1].pop()
                            righttype = paramType[-1].pop()
                            leftparam = paramStack[-1].pop()
                            lefttype = paramType[-1].pop()
                            # Evaluate the binary operator
                            result = Evaluator.evaluateFunction(opStack[-1], [leftparam, rightparam], [lefttype, righttype])
                            # Report error
                            if result[0] == "E":
                                print result
                                return
                            # put results in stacks
                            paramStack[-1].append(result[1])
                            paramType[-1].append(result[0])
                            # remove operator from top of stack
                            opType.pop()
                            opHeight.pop()
                            opStack.pop()
                    # Negating numbers. Check if only 1 number on stack,  and topmost operator is -
                    elif len(paramStack[-1]) == 1 and opStack[-1] == "-":
                        # check if height of top list and top operator match,  and current token is not operator
                        if (opHeight[-1] == paramHeights[-1]) and category != "Op":
                            # get topmost parameter
                            rightparam = paramStack[-1].pop()
                            righttype = paramType[-1].pop()
                            # Negate the value
                            result = Evaluator.evaluateFunction(opStack[-1], [0, rightparam], ["Num", righttype])
                            # Report error
                            if result[0] == "E":
                                print result
                                return
                            # put results in stacks
                            paramStack[-1].append(result[1])
                            paramType[-1].append(result[0])
                            # remove operator from top of stack
                            opType.pop()
                            opHeight.pop()
                            opStack.pop()

        print 'END OF EVALUATION PARAMETERS: ' +str(paramStack)

    # @staticmethod
    @staticmethod
    def tokenizeExpression(expression):
        # returns a list of tokens in the expression
        # tokens are parentheses,  math operators,  commas,  function names,  and literals
        print 'Expression: ' + expression

        comment_char = "#"  # character indicating start of comment and to stop tokenizing

        specialchars = ['\t', '-', '+', '/', '*', '%', '(', ')', ',']
        specialchars.append(comment_char)   #add comment character to list of special chars
        returnlist = []        # return list,  containing the tokens
        current_token = ''

        quote_chars = ["'", '"']    # Characters indicating a quote
        is_quoted = False           # If the text is being processed as a string token
        # The outermost quote character. Determines if ' or " is used to end the string token
        # This allows the user to use ' or " in strings by using the other one as the outer
        outer_quote_char = None # will be ' or " once a quote starts

        for char in expression:
            #  if the chars are currently being parsed as strings
            if is_quoted:
                # check if the string ends
                if char == outer_quote_char:
                    returnlist.append(outer_quote_char+current_token+outer_quote_char) # add string token
                    current_token = ""                  # reset token
                    is_quoted = False                   # no longer parsing text as a string
                #  string does not end
                else:
                    current_token += char  # add current char to current string
            #  chars are not being parsed as strings
            else:
                # check opening to string
                if char in quote_chars:
                    cleantoken = current_token.replace(' ',  '')  # strip whitespace from current token
                    if len(cleantoken) > 0:  # check if whitespace removed token is not empty
                        returnlist.append(cleantoken)  # add it then

                    current_token = ""      # Reset token
                    is_quoted = True        # Start parsing as a string
                    outer_quote_char = char # mark whether the string starts and ends with a ' or "
                # not opening to string
                else:
                    #check if a special character such as an operator or comment
                    if char in specialchars:
                        cleantoken = current_token.replace(' ',  '')  #  strip whitespace from current token
                        if len(cleantoken) > 0:  #  check if whitespace removed token is not empty
                            returnlist.append(cleantoken)  #  add it then
                            current_token = ''
                        # if start of comment
                        if char == comment_char:
                            break  # comment started; stop tokenizing
                        else:
                            returnlist.append(char) #add special character to token list
                    else:
                        current_token += char

        # check if open quote
        if is_quoted:
            print 'open quote!'

        if len(current_token) > 0:
            returnlist.append(current_token)

        return returnlist

# # # DRIVER CODE# # #
import time

file = open('script.txt', 'r')
x = file.readlines()
for i in x:
#      # print Evaluator.tokenizeExpression(i.rstrip())
     Evaluator.evaluateExpression(i.rstrip())

#                      __
#         _______     /*_)-< HISS HISS
#   ___ /  _____  \__/ /
#  < ____ /     \____ /