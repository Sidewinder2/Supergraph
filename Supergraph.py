class Configurations:
    config_values = {}  # dictionary containing all configs
    DEFAULT_CONFIG_FNAME = "config.json" # default congig filename

    @staticmethod
    def setRuntimeConfigs(filename = DEFAULT_CONFIG_FNAME):
        # sets all hardcoded values in DEFAULT_CONFIG_VALUES
        # if the designated config file is not detected, create one
        # and populate with default configs
        # If it exists, read from it

        Configurations.config_values["runtimescript"] = "script.txt"
        Configurations.loadConfigFile(filename)
        Configurations.writeConfigFile(filename)

    @staticmethod
    def loadConfigFile(filename = DEFAULT_CONFIG_FNAME):
        # loads configs from given file, if it exists
        import os.path
        if os.path.exists(filename):
            with open(filename, 'r') as infile:
                Configurations.config_values = json.load(infile)


    @staticmethod
    def writeConfigFile(filename=DEFAULT_CONFIG_FNAME):
        # writes current configs to given file
        with open(filename, 'w') as outfile:
            json.dump(Configurations.config_values, outfile, indent=4, sort_keys=True)

class KeyGenerator:
    # Generator class that keeps track of automatic namings
    # For instance, creates "Connection1","Connection2".... given "Connection" as a starting string
    name_to_count = {}  # keeps track of autonumber for each name

    @staticmethod
    def getNextName(generatorname = "", existing_keys = []):
        # Generates next key name in sequence that does not exist within existing key list
        # If sequence does not exist, create one
        return_string = ""
        while True:
            if generatorname not in KeyGenerator.name_to_count.keys(): # create new sequence
                KeyGenerator.name_to_count[generatorname] = 0
            possible_name = generatorname + str(KeyGenerator.name_to_count[generatorname])
            if possible_name not in existing_keys:
                return possible_name
            else:
                KeyGenerator.name_to_count[generatorname] = KeyGenerator.name_to_count[generatorname] + 1

class Supergraph:
    keylist = []          # list of keys. Prevents a connection, graph and a node having the same name
    graphlist = {}        # dictionary maintaining a graph name to graph pointer conversion
    nodelist = {}         # dictionary maintaining a node name to node pointer conversion
    connectionlist = {}   # dictionary maintaining a connection name to connection pointer conversion
    nodeconnectionlist = {}    # maintains a dictionary of nodes to Sets of connection keys

    supergraphdata = {}   # dictionary maintaining a variable name to variable data conversion

    @staticmethod
    def getNodeConnectionList():
        return Supergraph.nodeconnectionlist

    @staticmethod
    def getKeyList():
        return Supergraph.keylist

    @staticmethod
    def verifyKeys(keylist):
        # Will remove any names from list that don't point to anything
        returnlist = []
        for key in keylist:
            if key in Supergraph.keylist:
                returnlist.append(key)  # add valid name to list
        return returnlist

    @staticmethod
    def getPointerData(pointers = [], this = ""):
        # Pulls data from supergraph when given a pointer such as NODE.DATA
        if len(pointers) == 1:
            if pointers[0] == "THIS":
                if this == "":
                    raise Exception("Keyword THIS does not currently reference something")
                reference = this
            else:
                reference = pointers[0]
            
            if reference in Supergraph.nodelist.keys():
                return reference
            elif reference in Supergraph.connectionlist.keys():
                return reference
            elif reference in Supergraph.graphlist.keys():
                return reference
        elif len(pointers) == 2:
            if pointers[0] == "THIS":
                if this == "":
                    raise Exception("Keyword THIS does not currently reference something")
                reference = this
            else:
                reference = pointers[0]
            if reference in Supergraph.nodelist.keys():
                data = Supergraph.getNodeData([reference], pointers[1])
                if len(data) == 0:
                    return None
                else:
                    return data[0]
            if reference in Supergraph.connectionlist.keys():
                data = Supergraph.getConnectionData([reference], pointers[1])
                if len(data) == 0:
                    return None
                else:
                    return data[0]
            # elif reference in Supergraph.connectionlist.keys():
            #     return Supergraph.getConnectionData([reference], pointers[1])
            # elif reference in Supergraph.graphlist.keys():
            #     return Supergraph.getGraphData([reference], pointers[1])
        return None

    @staticmethod
    def addData( varname,  vardata):
        if (varname not in Supergraph.supergraphdata) and varname != "name":
            Supergraph.supergraphdata[varname] = vardata

    @staticmethod
    def getData( varname):
        # gets type and value of requested variable,  none if it doesn't exist
        if varname in Supergraph.supergraphdata:
            # print "RETURNING " + Supergraph.name + ": "+str([Supergraph.nodedatatype[varname], Supergraph.nodedata[varname]])
            return Supergraph.supergraphdata[varname]
        return None

    @staticmethod
    def removeData( varname):
        if varname in Supergraph.supergraphdata:
            del Supergraph.supergraphdata[varname]
            del Supergraph.supergraphdatatype[varname]

    @staticmethod
    def addGraph( graphname,  nodekeys = [],  connectionkeys = []):
        # Adds a graph to the database
        if graphname not in Supergraph.graphlist and graphname not in Supergraph.keylist:
            Supergraph.graphlist[graphname] = Graph( graphname,  nodekeys,  connectionkeys)
            Supergraph.keylist.append(graphname)

    @staticmethod
    def removeGraphs( graphnames):
        verifiedgraphs = Supergraph.verifyGraphNames(graphnames)     # get list of graphs from keys
        for graphname in verifiedgraphs:
            del Supergraph.graphlist[graphname]
            Supergraph.keylist.remove(graphname)

    @staticmethod
    def getAllGraphKeys():
        #  Lists names of all existing graphs
        return Supergraph.graphlist.keys()

    @staticmethod
    def printGraphList():
        #  Lists names of all existing graphs
        print Supergraph.graphlist.keys()

    @staticmethod
    def verifyGraphNames( graphnames = []):
        # Will remove any names from list that don't point to anything
        returnlist = []
        for name in graphnames:
            if name in Supergraph.graphlist.keys():
                returnlist.append(name) # add valid name to list
        return returnlist

    @staticmethod
    def namesToGraphs( graphnames = []):
        # Converts a list of a keys to graph pointers
        returnlist = []
        for i in graphnames:
            if graphnames[i] in Supergraph.graphlist:
                returnlist.append(Supergraph.graphlist[graphnames[i]])
        return returnlist

    @staticmethod
    def addNode(nodename, nodedata = {}):
        assert type(nodename) is str
        assert type(nodedata) is dict

        #  Adds a node to the database. Returns True if successful
        if nodename not in Supergraph.nodelist and nodename not in Supergraph.keylist:
            Supergraph.nodelist[nodename] = Node(nodename)
            Supergraph.nodeconnectionlist[nodename] = set()
            Supergraph.keylist.append(nodename)
            return True
        else:
            return False

    @staticmethod
    def addNodes(nodenames = [], nodedata={}):
        assert type(nodenames) is list
        assert type(nodedata) is dict

        for nodename in nodenames:
            Supergraph.addNode(nodename,nodedata)

    @staticmethod
    def removeNodes( nodenames):
        # Removes a list of nodes from the database
        verifiednodes = Supergraph.verifyNodeNames(nodenames)     # get list of nodes from keys
        for nodename in verifiednodes:
            del Supergraph.nodelist[nodename]
            del Supergraph.nodeconnectionlist[nodename]
            Supergraph.keylist.remove(nodename)

    @staticmethod
    def getAllNodeKeys():
        # lists the node keys
        return Supergraph.nodelist.keys()

    @staticmethod
    def printNodeList():
        # lists the node keys
        print Supergraph.nodelist.keys()

    @staticmethod
    def verifyNodeNames( nodenames = []):
        # Will remove any names from list that don't point to anything
        returnlist = []
        for name in nodenames:
            if name in Supergraph.nodelist.keys():
                returnlist.append(name) # add valid name to list
        return returnlist

    @staticmethod
    def namesToNodes( nodenames = []):
        # Converts a list of a keys to node pointers
        #  Will remove any names from list that don't point to anything
        returnlist = []
        names = Supergraph.verifyNodeNames(nodenames)
        for i in names:
            returnlist.append(Supergraph.nodelist[i]) # get pointer from node list
        return returnlist

    @staticmethod
    def getNodeNeighbors(nodekeys = []):
        # Get neighbors directly connected to a list of nodes
        return_list = set()
        for node in nodekeys:
            for connection in Supergraph.namesToConnections(Supergraph.nodeconnectionlist[node]):
                neighbor = Connection.getEndPoint(connection,node)
                if neighbor is not None:
                    return_list.add(neighbor)

        return list(return_list)

    @staticmethod
    def addNodeData( nodenames,  varname,  vardata):
        #  Adds data to a list of nodes
        nodes = Supergraph.namesToNodes(nodenames)  #  get list of nodes from keys
        for i in nodes:
            Node.addNodeData(i,  varname,  vardata)

    @staticmethod
    def getNodeDegrees(nodenames = [], degree = "in"):
        # Returns the degrees or indegrees for a list of node keys
        assert degree in ["in","out"], AttributeError
        verified_nodes = Supergraph.namesToNodes(nodenames)  # get list of nodes from keys
        returnlist = []
        for node in verified_nodes:
            returnlist.append(Node.getNodeDegree(node,degree))
        return returnlist


    @staticmethod
    def getNodeData( nodenames,  varname):
        # Gets requested variable from a list of nodes.
        # Returns a list containing the values
        # Won't append data if it doesn't exist for that node
        nodes = Supergraph.namesToNodes(nodenames)  #  get list of nodes from keys
        returnlist = []
        for i in nodes:
            value = Node.getNodeData(i,  varname)   # get the array containing the type and value of the data
            if value is not None:
                returnlist.append(value)
        return returnlist

    @staticmethod
    def removeNodeData( nodenames,  varname):
        #  Removes data from a list of nodes
        nodes = Supergraph.namesToNodes(nodenames)  #  get list of nodes from keys
        for node in nodes:
            Node.removeNodeData(nodes[node],  varname)

    @staticmethod
    def addConnection( connectionname,  leftname,  rightname, direction = "both"):
        # creates a connection in the database. Returns true if successful, false if not

        assert type(connectionname) is str
        assert type(leftname) is str
        assert type(rightname) is str

        # Check if left and right keys in database, otherwise it fails
        if leftname not in Supergraph.nodelist.keys():
            return False
        if rightname not in Supergraph.nodelist.keys():
            return False

        if connectionname not in Supergraph.connectionlist:
            Supergraph.connectionlist[connectionname] = Connection(connectionname, leftname,  rightname, direction)
            Supergraph.nodeconnectionlist[leftname].add(connectionname)
            Supergraph.nodeconnectionlist[rightname].add(connectionname)
            Supergraph.keylist.append(connectionname)
            return True
        return False

    @staticmethod
    def addConnections( leftnames,  rightnames, direction = 'both', generator = "Connection"):
        # Adds connections to the database
        # Will connect every node from left side to right side,  resulting in L * R connections
        assert direction in ["both","right"]

        verifiedleftnames = Supergraph.verifyNodeNames(leftnames)
        verifiedrightnames = Supergraph.verifyNodeNames(rightnames)
        for left in verifiedleftnames:
            for right in verifiedrightnames:
                connectionname = KeyGenerator.getNextName(generator, Supergraph.getAllConnectionKeys())
                Supergraph.addConnection(connectionname, left, right, direction)

    @staticmethod
    def removeConnections(connectionnames):
        # removes the specified connections,  if they exist
        for connectionkey in connectionnames:
            if connectionkey in Supergraph.connectionlist.keys():
                # remove references to this connection for the left and right nodes it connects
                c = Supergraph.connectionlist[connectionkey]
                leftkey = Connection.getConnectionData(c,"leftkey")
                rightkey = Connection.getConnectionData(c,"rightkey")
                if leftkey in Supergraph.nodeconnectionlist:
                    if connectionkey in Supergraph.nodeconnectionlist[leftkey]:
                        Supergraph.nodeconnectionlist[leftkey].remove(connectionkey)
                if rightkey in Supergraph.nodeconnectionlist:
                    if connectionkey in Supergraph.nodeconnectionlist[rightkey]:
                        Supergraph.nodeconnectionlist[rightkey].remove(connectionkey)
                # remove connection
                del Supergraph.connectionlist[connectionkey]
                Supergraph.keylist.remove(connectionkey)

    @staticmethod
    def getAllConnectionKeys():
        # lists the node keys
        return Supergraph.connectionlist.keys()

    @staticmethod
    def printConnectionList():
        # lists the node keys
        print Supergraph.connectionlist.keys()

    @staticmethod
    def getNextConnectionName():
        # Used for automatically naming connections
        # Will update id counter to make it as up to date as possible
        connectname = Supergraph.connectionidprefix + str(Supergraph.connectionidsuffix)
        while (connectname in Supergraph.connectionlist) or (connectname in Supergraph.keylist):
            Supergraph.connectionidsuffix += 1
            connectname = Supergraph.connectionidprefix + str(Supergraph.connectionidsuffix)
        return connectname

    @staticmethod
    def verifyConnectionNames( connectionnames = []):
        # Will remove any names from list that don't point to anything
        returnlist = []
        for name in connectionnames:
            if name in Supergraph.connectionlist.keys():
                returnlist.append(name) #append valid name to list
        return returnlist

    @staticmethod
    def namesToConnections( connectionnames = []):
        # Converts a list of a keys to connection pointers
        #  Will remove any names from list that don't point to anything
        returnlist = []
        verifiednames = Supergraph.verifyConnectionNames(connectionnames)
        for name in verifiednames:
            returnlist.append(Supergraph.connectionlist[name]) # get pointer from node list
        return returnlist

    @staticmethod
    def addConnectionData( connectionnames,  varname,  vardata):
        #  Adds data to a list of connections
        connections = Supergraph.namesToConnections(connectionnames)  #  get list of connections from keys
        for i in connections:
            Connection.addConnectionData(i,  varname,  vardata)

    @staticmethod
    def getConnectionData( connectionnames,  varname):
        # Gets requested variable from a list of nodes.
        # Returns a list containing the values
        # Won't append data if it doesn't exist for that node
        connections = Supergraph.namesToConnections(connectionnames)  # get list of nodes from keys
        returnlist = []
        for i in connections:
            value = Connection.getConnectionData(i, varname)  # get the array containing the type and value of the data
            if value is not None:
                returnlist.append(value)
        return returnlist

    @staticmethod
    def removeConnectionData( connectionnames,  varname):
        #  Removes data from a list of connections
        connections = Supergraph.namesToConnections(connectionnames)  #  get list of connections from keys
        for connection in connections:
            Connection.removeConnectionData(connections[connection],  varname)

    @staticmethod
    def showAllConnections():
        # prints all connections, and their left and right keys
        for connect in Supergraph.connectionlist.values():
            print connect.name, ": ",connect.leftkey,", ",connect.rightkey

    @staticmethod
    def getNodeConnections(nodekeys=[],connectionkeys = []):
        # gets all connection keys that belong to the given list of nodes
        # Will restrain the search to a list of connections
        # maintains direction of connections

        returnlist = set() # is a set to restrict duplicate connections. Converted to list at end
        connections = Supergraph.namesToConnections(connectionkeys)
        for connect in connections:
            leftkey = connect.leftkey
            rightkey = connect.rightkey
            direction = connect.direction
            # check if an endpoint is in given node list, and destination lines up
            if (leftkey in nodekeys) and (direction in ['right','both']):
                returnlist.add(connect.name)
            if (rightkey in nodekeys) and (direction in ['left','both']):
                returnlist.add(connect.name)

        return list(returnlist)

class Graph:
    def __init__(self, name, nodekeys, connectionkeys):
        self.name = name                           # name uniquely identifying the graph
        self.nodekeys = nodekeys                   # list of node keys used in this graph
        self.connectionkeys = connectionkeys       # list of connection keys used in this graph

    # def addConnections(self,connections):
    #     for connection in connections:
    #         if connection in self.connectionkeys:
    #             self.connectionkeys.remove(connection)
    #
    # def getConnections(self):
    #     return self.connectionkeys
    #
    # def removeConnections(self,connections):
    #     for connection in connections:
    #         if connection not in self.connectionkeys:
    #             self.connectionkeys.append(connection)
    #
    # def addNodes(self, nodes):
    #     for node in nodes:
    #         if node not in self.nodekeys:
    #             self.nodekeys.append(node)
    #
    # def getNodes(self):
    #     return self.nodekeys
    #
    # def removeNodes(self,nodes):
    #     for node in nodes:
    #         if node in self.nodekeys:
    #             self.nodekeys.remove(node)

class Node:
    def __init__(self, name):
        self.name = name
        self.nodedata = {}

    def addNodeData(self,  varname,  vardata):
        if varname.lower() != "name":
            self.nodedata[varname] = vardata

    def getNodeData(self,  varname):
        # gets type and value of requested variable,  none if it doesn't exist
        if varname in self.nodedata:
            # print "RETURNING " + self.name + ": "+str([self.nodedatatype[varname], self.nodedata[varname]])
            return self.nodedata[varname]
        if varname.lower() == "name":
            return self.name
        return None

    def removeNodeData(self,  varname):
        if varname in self.nodedata:
            del self.nodedata[varname]

    def getNodeDegree(self,degree = "in"):
        # Counts either the indegree or outdegree of the node

        assert degree in ["in","out"], AttributeError

        degree_count = 0    # count of degree for the node
        c_list = Supergraph.nodeconnectionlist[self.name] # get list of connection keys
        for connectionkey in c_list:
            conn = Supergraph.connectionlist[connectionkey]
            leftkey = Connection.getConnectionData(conn,"leftkey")
            rightkey = Connection.getConnectionData(conn, "rightkey")
            direction = Connection.getConnectionData(conn, "direction")

            # Bidirectional edges count either way for in or outdegree
            if direction == "both":
                degree_count += 1
                continue

            if degree == "in":
                if self.name == rightkey and direction == "right":
                    degree_count += 1
            else:
                if self.name == leftkey and direction == "right":
                    degree_count += 1

        return degree_count


class Connection:
    def __init__(self, name, leftkey, rightkey,
                 direction = "both"): # The endpoint of the connection. Either right for directed, or both for undirected.
        self.name = name   # unique name of the connection used as a key
        assert direction in ['right','both']
        self.connectiondata = {"leftkey": leftkey, "rightkey":rightkey,"direction":direction}  # maintains information about the connection

    def addConnectionData(self,  varname,  vardata):
        if varname.lower() not in ["name","leftkey","rightkey","direction"]:
            self.connectiondata[varname] = vardata

    def getConnectionData(self,  varname):
        # gets type and value of requested variable,  none if it doesn't exist
        if varname in self.connectiondata:
            return self.connectiondata[varname]
        if varname.lower() == "name":
            return self.name
        return None

    def removeConnectionData(self,  varname):
        if varname in self.connectiondata:
            del self.connectiondata[varname]

    def getEndPoint(self,startpoint):
        # Used to traverse a connection, given the start point
        # If you attempt to go the opposite way from a directed edge, it returns None
        assert startpoint in [self.connectiondata["leftkey"],self.connectiondata["rightkey"]]
        if self.connectiondata["direction"] == "both":
            if startpoint == self.connectiondata["leftkey"]:
                return self.connectiondata["rightkey"]
            else:
                return self.connectiondata["leftkey"]
        else:
            if startpoint == self.connectiondata["leftkey"]:
                return self.connectiondata["rightkey"]
            else:
                return None

class ArtPointsFinder:
    # Todo: Implement ArtPointsFinder

    @staticmethod
    def getArtPoints(nodes = [], connections = {}):
        assert type(nodes) is list
        assert type(connections) is dict
        assert len(nodes) > 0
        assert len(connections.keys()) > 0

        print ("Current nodes: ",nodes)
        # Returns articulated points, given a list of node and connection keys
        unvisited_nodes = list(nodes)  # maintains list of previously visited nodes
        unvisited_connections = connections.keys()
        node_to_parent = {}             # maintains parent heirarchy in DFS
        node_to_index = {}              # maintains index of given node
        node_to_low = {}                # maintains low value of given node
        counter = 1

        node_stack = list(nodes)
        current_node_key = ""

        # remove all connections that point somewhere not in the subgraph
        for conn in unvisited_connections:
            if connections[conn].leftkey not in unvisited_nodes or connections[conn].rightkey not in unvisited_nodes:
                unvisited_connections.remove(conn)


        while len(node_stack) > 0:
            # pop item from stack to create a DFS
            current_node_key = node_stack.pop(0)
            print("Current node: ", current_node_key)

            if current_node_key in unvisited_nodes:
                # new node found. Assign values
                unvisited_nodes.remove(current_node_key)                 # node has now been visited
                node_to_index[current_node_key] = counter           # its index is current counter
                node_to_parent[current_node_key] = ""                 # its parent is the last enountered node

                node_to_low[current_node_key] = counter
                counter += 1  # increment counter

            # iterate through all connections for the current node
            for conn in unvisited_connections:
                leftkey = connections[conn].leftkey
                rightkey = connections[conn].rightkey

                # from left to right
                if leftkey == current_node_key:
                    print("Current connection: ", conn, "left:", leftkey, "right: ", rightkey)
                    unvisited_connections.remove(conn)

                    if rightkey in unvisited_nodes:
                        print("unvisited",unvisited_nodes)
                        # new node found. Assign values
                        node_stack.insert(0,rightkey)
                        unvisited_nodes.remove(rightkey)  # node has now been visited
                        node_to_index[rightkey] = counter  # its index is current counter
                        node_to_parent[rightkey] = leftkey  # its parent is the last enountered node
                        node_to_low[rightkey] = counter
                        counter += 1  # increment counter
                        print("Current counter: ", counter)
                    elif node_to_low[leftkey] > node_to_low[rightkey]:
                        print("\tWAT",leftkey,rightkey)
                        temp_value = node_to_index[rightkey]
                        child_key = leftkey
                        node_to_low[leftkey] = temp_value
                        while child_key != "":
                            print ("\t" + child_key)
                            if node_to_parent[child_key] != "":
                                if node_to_low[node_to_parent[child_key]] > node_to_low[child_key]:
                                    node_to_low[child_key] = temp_value
                            child_key = node_to_parent[child_key]

        # at the end print all nodes and data about them
        for nodekey in node_to_parent.keys():
            print(nodekey, "parent:",node_to_parent[nodekey])
            print("index:",node_to_index[nodekey])
            print("low:",node_to_low[nodekey])

        for conn in connections.keys():
            leftkey = connections[conn].leftkey
            rightkey = connections[conn].rightkey
            if node_to_low[rightkey] < node_to_index[leftkey]:
                print(leftkey + " is art point")

class Interpreter:
    S = Supergraph()
    function_names = ['PRINT','PRINTKEYS', 'GETTIME',
                      'SUM', 'SUBTRACT','MULTIPLY', 'DIVIDE',
                      'ABS', 'SQRT', 'SIZE',
                      'NOT', 'AND', 'OR', 'XOR', 'XNOR',
                      'EQ', 'GTEQ', 'LTEQ', 'NEQ', 'LT', 'GT',
                      'SORT',
                      'LOGBASE',
                      'ISNUMERIC', 'HAMMING', 'LEVEN', 'MIN',
                      'MAX', 'SMALLEST', 'LARGEST', 'CHOOSE',
                      'AVG',
                      'RANDOM', 'RANDOMINT',
                      'STRREPLACE',
                      'ADDDATA', 'REMOVEDATA',
                      'LISTNODES', 'ADDNODES', 'GETNODES', 'REMOVENODES',
                      'ADDNODEDATA', 'GETNODEDATA', 'REMOVENODEDATA',
                      'LISTCONNECTIONS','ADDCONNECTIONS','GETCONNECTIONS','REMOVECONNECTIONS',
                      'ADDCONNECTIONDATA', 'GETCONNECTIONDATA', 'REMOVECONNECTIONDATA',
                      'LISTGRAPHS', 'ADDGRAPHS', 'GETGRAPHS', 'REMOVEGRAPHS',
                      'QUERY']
    operators = ['<-->','-->','-', '+', '/', '*', '%', '==', '!=', '>', '<', '>=', '<=', '||', '&&']
    reserved_chars = ['(', ')', '#', '"', "'", '\\', '\t', ',']   # these characters cannot be used in an object name


    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def levenshtein(s1, s2):
        # returns levenshtein distance of two strings
        # code from https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
        if len(s1) < len(s2):
            return Interpreter.levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[
                                 j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1  # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @staticmethod
    def checkParenCount(expression):
        if expression.count('(') == expression.count(')'):
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
            Interpreter.function_names.append(keyword.rstrip())
        return False

    @staticmethod
    def categorizeToken(token):
        quote_chars = ["'", '"']
        bools = ['true','false']
        null = ["null"]

        if token == '(':
            return '('
        elif token == ')':
            return ')'
        elif token == ',':
            return ','
        elif token in Interpreter.function_names:
            return 'Fun'
        elif token in Interpreter.operators:
            return 'Op'
        elif token.lower() in null:
            return 'V'
        elif token.lower() in bools:
            return 'Boolean'
        elif (len(token) >= 2) and ((token[0] in quote_chars) and (token[len(token) - 1] in quote_chars)):
            return 'Str'
        elif Interpreter.is_number(token):
            return 'Num'
        elif token == '\t':
            return 'Tab'
        elif token == ', ':
            return 'Comma'
        elif token == 'ALL':
            return '*'
        else:
            return '?'     # unknown likely variable

    @staticmethod
    def checkAllTypes(parameters=[], validparamtypes=[]):
        # checks to see if all values in paramtypes match up with valid types
        for param in parameters:
            if type(param) not in validparamtypes:
                return False
        return True

    @staticmethod
    def evaluateFunction(function, parameters):
        # Performs a designated function with the given parameters

        if function == "PRINT":
            # Basic print; will unpack values if only 1 is given
            if len(parameters) == 1:
                print parameters[0]
            else:
                print parameters
            return None

        if function == "PRINTKEYS":
            # Prints all existing keys in the supergraph
            print Supergraph.getKeyList()
            return None

        if function == "GETTIME":
            # Gets the time in milliseconds from 1970
            if len(parameters) == 0:
                return time.time()
            else:
                raise Exception("Unexpected parameters given")


        if function in ["+", "SUM"]:
            # General sumation function.
            # if given 1 list will sum all items in that list
            # multiple lists will merge the lists into one
            # will concatenate Strings and add numbers
            if len(parameters) == 1 and isinstance(parameters[0],list):
                # add all the items in a single list together
                params = parameters[0]
                return Interpreter.evaluateFunction("SUM", params)
            if Interpreter.checkAllTypes(parameters, [list]):
                # merge multiple lists together
                returnlist = []
                for param in parameters:
                    returnlist.extend(param)
                return returnlist
            elif Interpreter.checkAllTypes(parameters, [int, float]):
                # Add numbers
                result = 0
                if len(parameters) >= 1:
                    for param in parameters:
                        result += param
                return result
            elif Interpreter.checkAllTypes(parameters, [int, float, str]):
                # A mix will produce a string
                result = ""
                if len(parameters) >= 1:
                    for param in parameters:
                        result += str(param)
                return result
            else:
                raise Exception("Unexpected parameters given")

        if function in ["-", "SUBTRACT"]:
            if len(parameters) == 2:
                if Interpreter.checkAllTypes(parameters, [int, float]):
                    return float(parameters[0]) - float(parameters[1])
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 Parameters expected")

        if function in ["*", "MULTIPLY"]:
            if len(parameters) == 2:
                if Interpreter.checkAllTypes(parameters, [int, float]):
                    return ["Num", float(parameters[0]) * float(parameters[1])]
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 Parameters expected")

        if function in ["/", "DIVIDE"]:
            if len(parameters) == 2:
                if Interpreter.checkAllTypes(parameters, [int, float]):
                    return float(parameters[0]) / float(parameters[1])
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 Parameters expected")

        if function in ["%", "MOD"]:
            if len(parameters) == 2:
                if Interpreter.checkAllTypes(parameters, [int, float]):
                    return float(parameters[0]) % float(parameters[1])
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 Parameters expected")

        if function in ["ABS"]:
            if len(parameters) == 1:
                if Interpreter.checkAllTypes(parameters, [int, float]):
                    return abs(float(parameters[0]))
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("1 Parameter expected")

        if function in ["SQRT"]:
            if len(parameters) == 1:
                if Interpreter.checkAllTypes(parameters, [int, float]):
                    result = parameters[0] ** (1.0 / 2) #raise the power of parameter to 1/2, giving square root
                    return result
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("1 Parameter expected")

        if function == "SIZE":
            if len(parameters) == 1:
                if isinstance(parameters[0],(list,str)):
                    return len(parameters[0])
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Too many parameters given")

        if function == "NOT":
            if len(parameters) == 1:
                if type(parameters[0]) is bool:
                    return (not parameters[0])
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Too many parameters given")

        if function in ["&&","AND"]:
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(parameters, [bool]):
                    for param in parameters:
                        if not param:
                            return False
                    return True
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function in ["||","OR"]:
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(parameters, [bool]):
                    for param in parameters:
                        if param:
                            return True
                    return False
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function == "XOR":
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(paramtypes, ['Boolean']):
                    truecount = 0
                    for param in parameters:
                        if param.lower() == 'true':
                            truecount += 1
                    if (truecount % 2) == 1:
                        return ["Boolean", 'true']
                    return ["Boolean", 'false']
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function == "XNOR":
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(paramtypes, ['Boolean']):
                    truecount = 0
                    for param in parameters:
                        if param.lower() == 'true':
                            truecount += 1
                    if (truecount % 2) == 0:
                        return ["Boolean", 'true']
                    return ["Boolean", 'false']
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function in ["==","EQ"]:
            # Equals function
            if len(parameters) >= 2:
                if not Interpreter.checkAllTypes(parameters, [list]):
                    for index in range(1,len(parameters)):
                        if parameters[index] != parameters[0]:
                            return False
                    return True
                else:
                    raise Exception("Cannot compare lists")
            else:
                raise Exception("2 or more parameters expected")

        if function in ["!=","NEQ"]:
            # Not Equals function. All items must by unique values to return true
            if len(parameters) >= 2:
                if not Interpreter.checkAllTypes(parameters, [list]):
                    itemset = []    #set of all unique items
                    for param in parameters:
                        if param in itemset:
                            return False
                        itemset.append(param)
                    return True
                else:
                    raise Exception("Cannot compare lists")
            else:
                raise Exception("2 or more parameters expected")

        if function in [">=","GTEQ"]:
            # Greater than. Will return false if items are not sorted in descending order
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(paramtypes, ['Num']):
                    for index in range(1,len(parameters)):
                        if parameters[index-1] <= parameters[index]:
                            return ["Boolean", 'false']
                    return ["Boolean", 'true']
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function in ["<=","LTEQ"]:
            # Greater than. Will return false if items are not sorted in descending order
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(paramtypes, ['Num']):
                    for index in range(1,len(parameters)):
                        if parameters[index-1] >= parameters[index]:
                            return ["Boolean", 'false']
                    return ["Boolean", 'true']
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function in [">","GT"]:
            # Greater than. Will return false if items are not sorted in descending order
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(paramtypes, ['Num']):
                    for index in range(1,len(parameters)):
                        if parameters[index-1] < parameters[index]:
                            return ["Boolean", 'false']
                    return ["Boolean", 'true']
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function in ["<","LT"]:
            # Greater than. Will return false if items are not sorted in descending order
            if len(parameters) >= 2:
                if Interpreter.checkAllTypes(parameters, [int, float]):
                    for index in range(1,len(parameters)):
                        if parameters[index-1] > parameters[index]:
                            return False
                    return True
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 or more parameters expected")

        if function in ["SORT"]:
            # Returns a sorted list
            if Interpreter.checkAllTypes(parameters, [str, int, float]):
                numlist = []
                strlist = []
                for index in range(0,len(parameters)):
                    if parameters[index] is str:
                        strlist.append(parameters[index])
                    else:
                        numlist.append(parameters[index])

                numlist.sort()
                strlist.sort()
                sortedlist = numlist+strlist
                print("sorted list: ", sortedlist)
                return sortedlist
            else:
                raise Exception("Unexpected parameters given")

        if function in ["LEVEN"]:
            if len(parameters) == 2:
                if Interpreter.checkAllTypes(parameters, [str]):
                    return Interpreter.levenshtein(parameters[0], parameters[1])
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("2 Parameters Expected")

        if function in ["AVG"]:
            if Interpreter.checkAllTypes(parameters, [int, float]):
                if len(parameters) > 0:
                    sum = 0
                    result = 0
                    for param in parameters:
                        sum += float(param)
                    result = sum / len(parameters)
                    return result
                else:
                    raise Exception("At least one parameter must be supplied")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["RANDOM"]:
            # Returns random float between 0 and x, or in range if two numbers given
            if Interpreter.checkAllTypes(parameters, [int, float]):
                if len(parameters) == 2:
                        return random.uniform(parameters[0],parameters[1])
                if len(parameters) == 1:
                        return random.uniform(0,parameters[0])
                raise Exception("1 or 2 numbers expected")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["RANDOMINT"]:
            # Returns random int between 0 and x, or in range if two numbers given
            if Interpreter.checkAllTypes(parameters, [int, float]):
                if len(parameters) == 2:
                    return int(random.uniform(parameters[0], parameters[1]))
                if len(parameters) == 1:
                    return int(random.uniform(0, parameters[0]))
                raise Exception("1 or 2 numbers expected")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["ADDDATA"]:
            if len(parameters) == 2:
                #  varname,  vardata
                if isinstance(parameters[0],str):
                    # print Supergraph.verifyNodeNames(parameters[0])
                    Supergraph.addData(parameters[0], parameters[1])
                    return None
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["REMOVEDATA"]:
            if len(parameters) == 1:
                #  varname,  vardata
                if isinstance(parameters[0],str):
                    # print Supergraph.verifyNodeNames(parameters[0])
                    Supergraph.removeData(parameters[0])
                    return None
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["LISTNODES"]:
            if len(parameters) > 0:
                raise Exception("Unexpected parameters given")
            Supergraph.printNodeList()
            return None

        if function in ["ADDNODES"]:
            if not Interpreter.checkAllTypes(parameters, [str]):
                raise Exception("Only strings can be added as node keys")
            for param in parameters:
                Supergraph.addNode(param)
            return Supergraph.verifyNodeNames(parameters)

        if function in ["GETNODES"]:
            # converts a list of names into a nodelist,  removing ones that don't exist in the supergraph
            if len(parameters) > 1:
                if Interpreter.checkAllTypes(parameters, [str]):
                    nodekeys = Supergraph.verifyNodeNames(parameters)
                    return nodekeys
                raise Exception("Unexpected parameters given")
            else:
                nodekeys = Supergraph.getAllNodeKeys()
                return nodekeys

        if function == "REMOVENODES":
            if len(parameters) > 1:
                if Interpreter.checkAllTypes(parameters, [str]):
                    Supergraph.removeNodes(Supergraph.verifyNodeNames(parameters))
                    return None
                raise Exception("Unexpected parameters given")
            elif len(parameters) == 1:
                if isinstance(parameters[0],str):
                    Supergraph.removeNodes(Supergraph.verifyNodeNames(parameters))
                    return None
                elif isinstance(parameters[0],list):
                        Supergraph.removeNodes(Supergraph.verifyNodeNames(parameters[0]))
                        return None
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["ADDNODEDATA"]:
            if len(parameters) == 3:
                # nodenames(L),  varname,  vardata
                if isinstance(parameters[0],list) and isinstance(parameters[1],str):
                    if Interpreter.checkAllTypes(parameters[0], [str]):
                        Supergraph.addNodeData(parameters[0], parameters[1], parameters[2])
                        return None
                    else:
                        raise Exception("Unexpected parameters given")
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["REMOVENODEDATA"]:
            if len(parameters) == 3:
                # nodenames,  varname
                if isinstance(parameters[0], list) and isinstance(parameters[1],str):
                    # print Supergraph.verifyNodeNames(parameters[0])
                    if Interpreter.checkAllTypes(parameters[0], [str]):
                        Supergraph.removeNodeData(parameters[0], parameters[1])
                        return None
                raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["GETNODEDATA"]:
            if len(parameters) == 2:
                # nodenames,  varname
                if isinstance(parameters[0], list) and isinstance(parameters[1], str):
                    if Interpreter.checkAllTypes(parameters[0], [str]):
                        returnlist = Supergraph.getNodeData(parameters[0], parameters[1])
                        return returnlist
                raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["LISTCONNECTIONS"]:
            if len(parameters) > 0:
                raise Exception("Unexpected parameters given")
            Supergraph.printConnectionList()
            return None

        if function in ['-->','<-->',"ADDCONNECTIONS"]:
            if len(parameters) in [2,3]:
                # ADDCONNECTIONS(leftnodes, rightnodes)
                # Get initial left and right keys
                # They're treated as lists even if they might be one item
                leftkeys = [parameters[0]]
                rightkeys = [parameters[1]]

                # if list type detected, unpack the list
                if isinstance(parameters[0],list):
                    leftkeys = parameters[0]
                if isinstance(parameters[1],list):
                    rightkeys = parameters[1]

                # get the direction of the connections
                con_direction = "both"
                if function == '-->':
                    con_direction = "right"
                if len(parameters) == 3:
                    con_direction = parameters[2]

                Supergraph.addConnections(leftkeys, rightkeys,con_direction)
                return None
            else:
                raise Exception("Unexpected parameters given")

            
        if function in ["GETCONNECTIONS"]:
            # converts a list of names into a connectionlist,  removing ones that don't exist in the supergraph
            if len(parameters) > 1:
                if Interpreter.checkAllTypes(parameters, [str]):
                    connectionkeys = Supergraph.verifyConnectionNames(parameters)
                    return connectionkeys
                raise Exception("Unexpected parameters given")
            else:
                connectionkeys = Supergraph.getAllConnectionKeys()
                return connectionkeys

        if function in ["REMOVECONNECTIONS"]:
            if len(parameters) == 1 and isinstance(parameters[0],list):
                if Interpreter.checkAllTypes(parameters[0], [str]):
                    Supergraph.removeConnections(Supergraph.verifyConnectionNames( parameters[0]))
                    return None
                raise Exception("Unexpected parameters given")
            elif len(parameters) >= 1:
                if Interpreter.checkAllTypes(parameters, [str]):
                    Supergraph.removeConnections(Supergraph.verifyConnectionNames( parameters))
                    return None
                raise Exception("Unexpected parameters given")
            elif len(parameters) == 0:
                Supergraph.removeConnections(Supergraph.getAllConnectionKeys())
                return None
            else:
                raise Exception("Unexpected parameters given")

        if function in ["ADDCONNECTIONDATA"]:
            if len(parameters) == 3:
                # connectionnames(L),  varname,  vardata
                if isinstance(parameters[0],list) and isinstance(parameters[1],str):
                    if Interpreter.checkAllTypes(parameters[0], [str]):
                        Supergraph.addConnectionData(parameters[0], parameters[1], parameters[2])
                        return None
                    else:
                        raise Exception("Unexpected parameters given")
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["REMOVECONNECTIONDATA"]:
            if len(parameters) == 2:
                # connectionnames,  varname
                if isinstance(parameters[0],list) and isinstance(parameters[1],str):
                    if Interpreter.checkAllTypes(parameters[0], [str]):
                        Supergraph.removeConnectionData(parameters[0], parameters[1])
                        return None
                raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["GETCONNECTIONDATA"]:
            if len(parameters) == 2:
                # connectionnames,  varname
                if isinstance(parameters[0], list) and isinstance(parameters[1], str):
                    if Interpreter.checkAllTypes(parameters[0], [str]):
                        return Supergraph.getConnectionData(parameters[0], parameters[1])
                raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        if function in ["LISTGRAPHS"]:
            if len(parameters) > 0:
                raise Exception("Unexpected parameters given")
            Supergraph.printGraphList()
            return None

        if function in ["ADDGRAPHS"]:
            if Interpreter.checkAllTypes(parameters, [str]):
                for param in parameters:
                    Supergraph.addGraph(param)
            else:
                raise Exception("Unexpected parameters given")
            return None
        
        if function in ["GETGRAPHS"]:
            # converts a list of names into a graphlist,  removing ones that don't exist in the supergraph
            if len(parameters) > 1:
                if Interpreter.checkAllTypes(parameters, [str]):
                    return Supergraph.verifyGraphNames(parameters)
                else:
                    raise Exception("Unexpected parameters given")
            else:
                return Supergraph.getAllGraphKeys()
        
        if function in ["REMOVEGRAPHS"]:
            if len(parameters) >= 1:
                if Interpreter.checkAllTypes(parameters, [str]):
                    Supergraph.removeGraphs(Supergraph.verifyGraphNames(parameters))
                    return None
                else:
                    raise Exception("Unexpected parameters given")
            else:
                Supergraph.removeGraphs(Supergraph.getAllGraphKeys())
                return None

        if function in ["QUERY"]:
            # Run a query on a selected group of objects, only giving the ones where the expression returns true
            # Keyword THIS is used for this function to refer to object being currently queried
            if len(parameters) == 2:
                # object list(L), query expression(Str)
                if isinstance(parameters[0], list) and isinstance(parameters[1], str):
                    if Interpreter.checkAllTypes(parameters[0], [str]):
                        returnlist = [] # Maintains list of keys that satisfied query
                        # iterate through items in key list
                        for queryitem in parameters[0]:
                            result = Interpreter.evaluateExpression(parameters[1], queryitem)
                            if result == [[True]]:
                                returnlist.append(queryitem)
                        return returnlist
                else:
                    raise Exception("Unexpected parameters given")
            else:
                raise Exception("Unexpected parameters given")

        # return error if no function defintion found
        raise Exception("Unknown function " + function)

    @staticmethod
    def evaluateExpression(expression, this = ""):
        # Evaluates an expression. Tokenizes it, then evaluates the tokens
        # this variables references what the keyword THIS references in the supergraph
        print "EXPRESSION: "+expression
        tokenlist = Interpreter.tokenizeExpression(expression)
        #print tokenlist
        return Interpreter.evaluateTokens(tokenlist, this)

    @staticmethod
    def evaluateTokens(tokenlist, this = ""):
        # parameter stacks
        paramStack = [[]]  # holds parameter lists
        paramHeights = [0] # Maintains the parenthesis depth of each list in paramStack
        # operation/function stacks
        opStack = []       # Actual operation/function name
        opHeight = []      # Parenthesis depth of function/operator
        opType = []        # Determines whether an operator or a function
        # height
        current_height = 0 # Used for keeping track of the current parenthesis depth

        data_pointer = "."  # Used for pointers that pull data from supergraph. NAME.DATA

        previous_category = None

        # tokenize the input expression

        # run through each token and evaluate expression
        for token in tokenlist:
            # get the category of the current token to determine what to do
            category = Interpreter.categorizeToken(token)
            # print category

            if category == '(':
                # increase the height
                current_height += 1
                # make a new parameter list at new height
                paramStack.append([])
                paramHeights.append(current_height)
            elif category == ',':
                # To prevent crosstalk between parameters in a function, new parameters are thrown onto the stack
                # vertically rather than horizontally
                # The height is kept the same, and when a function is being evaluated at ) they are compressed into one
                # before evaluation
                paramStack.append([])
                paramHeights.append(current_height)
            elif category == ')':

                #compress the parameters seperated by commas into one list
                while len(paramStack) > 1 and paramHeights[-2] == paramHeights[-1]:
                    paramStack[-2] = paramStack[-2] + paramStack[-1]
                    paramStack.pop()
                    paramHeights.pop()


                # set height to one less,  and update height of topmost parameters
                current_height -= 1
                paramHeights[-1] = current_height

                #  check for possible function call
                if (len(opStack) > 0) and opType[-1] == 'Fun':
                    # check if function and current parameter heights match up
                    if opHeight[-1] == paramHeights[-1]:
                        # Evaluate result of function call
                        result = Interpreter.evaluateFunction(opStack[-1], paramStack[-1])
                        #print("result: ", result)

                        # Add results to stacks
                        paramStack[-1] = [result]

                        # pop function from stack
                        opType.pop()
                        opHeight.pop()
                        opStack.pop()

                # merge the paramaters list within the parenthesis with ones "below" them
                # EX: 3, (4, 5) <-> [[3], [4, 5]] becomes  3, 4, 5 <-> [[3, 4, 5]]
                paramStack[-2] = paramStack[-2] + paramStack[-1]
                paramStack.pop()
                paramHeights.pop()

            elif category == "Fun" or category == "Op":
                # Add operation/function to operation stack
                opStack.append(token)
                opType.append(category)
                opHeight.append(current_height)

                # If two operations are at the same height there's a problem
                if len(opHeight) > 1:
                    if opHeight[-1] == opHeight[-2]:
                        if opType[-1] == opType[-2]:
                            raise Exception("Unsuccessful evaluation of operation "+opStack[-2])

            elif category == "Str":
                # Add new parameter to the list at the top of the stack
                paramStack[-1].append(token[1:-1]) # remove the " from start and end of string
            elif category == "Num":
                # Add new numeric parameter to the list at the top of the stack
                paramStack[-1].append(float(token))
            elif category in ["Boolean"]:
                # Add new boolean parameter to the list at the top of the stack
                paramStack[-1].append(token.lower() in ['true'])
            elif category in ["V"]:
                # Add new parameter to the list at the top of the stack
                paramStack[-1].append(None)
            elif category == "?":
                # Unknown category; search supergraph for data and inject it if possible
                data = Supergraph.getData(token)
                if data is not None:
                    paramStack[-1].append(data)
                else:
                    # Failed to find anything in supergraph; look in objects in supergraph
                    pointers = token.split(data_pointer)
                    data = Supergraph.getPointerData(pointers, this)
                    if data is not None:
                        paramStack[-1].append(data)
                    else:
                        paramStack[-1].append(None)
                        #raise Exception("Unable to find value of "+token)

            # At end,  check if a binary operation is possible.
            # Don't process operations immediately when encountered to prevent accidental postfix processing
            if len(opStack) > 0 and category not in ["Op","Fun"]:
                if opType[-1] == 'Op':
                    # check if 2 or more parameters in topmost list
                    if len(paramStack[-1]) > 1:
                        # check if height of top list and top operator match
                        if opHeight[-1] == paramHeights[-1]:
                            # get left and right values
                            rightparam = paramStack[-1].pop()
                            leftparam = paramStack[-1].pop()
                            # Evaluate the binary operator
                            result = Interpreter.evaluateFunction(opStack[-1], [leftparam, rightparam])
                            #print("result: ", result)

                            # put results in stacks
                            paramStack[-1].append(result)
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
                            # Negate the value
                            result = Interpreter.evaluateFunction(opStack[-1], [0, rightparam])

                            # put results in stacks
                            paramStack[-1].append(result)
                            # remove operator from top of stack
                            opType.pop()
                            opHeight.pop()
                            opStack.pop()
            previous_category = category

        #print 'END OF EVALUATION PARAMETERS: ',paramStack

        if len(paramStack) == 1:
            return paramStack

    @staticmethod
    def tokenizeExpression(expression):
        # Improved algorithm for tokenizing a math expression

        is_quoted = False
        is_escaped = False
        quote_chars = ["'", '"']
        outer_quote_char = None  # will be ' or " once a quote starts
        comment_substring = '#'
        tab = '\t'

        regstring = '(<-->|-->|\*|/|\+|\-|\(|\)|%|==|!=|>=|<=|>|<|&&|\\|\\||in|,|"|\'|#|\\\\'+"|"+tab+"|"+comment_substring + ")"
        initial_tokens = re.split(regstring, expression)    # tokenize the expression initially
        final_tokens = []   # final token list

        # print initial_tokens

        for token in initial_tokens:
            if not is_quoted:
                # not being parsed as a string
                if token == comment_substring:
                    # start of a comment; stop tokenizing
                    break
                elif token in quote_chars:
                    # start of a string
                    final_tokens.append(token)
                    is_quoted = True
                    outer_quote_char = token
                else:
                    # a normal token like an operator, parenthesis, function, or variable
                    cleantoken = token.replace(' ','')
                    if len(cleantoken) > 0:  #  strip whitespace from current token
                        final_tokens.append(cleantoken)
            else:
                # is quoted
                if token == "\\":
                    # at escape char
                    if is_escaped:
                        # add escape char as literal
                        final_tokens[-1] = final_tokens[-1] + "\\"
                        is_escaped = False
                    else:
                        # first escape character
                        is_escaped = True
                elif token == outer_quote_char:
                    # at quote char
                    if not is_escaped:
                        # Quote is not escaped; end quote mode
                        is_quoted = False
                    final_tokens[-1] = final_tokens[-1] + token
                    is_escaped = False
                else:
                    if len(token) > 0:
                        # merge any tokens into a single string token
                        # this is the body of the string
                        final_tokens[-1] = final_tokens[-1] + token
                        is_escaped = False

        return final_tokens

    @staticmethod
    def checkTokenLegality(token):
        # returns True if token is not a keyword used by database
        assert type(token) is str
        if token in Interpreter.function_names:
            return False
        if token in Interpreter.operators:
            return False
        for illegal_char in Interpreter.reserved_chars:
            if illegal_char in token:
                return False
        return True

class FileHandler:

    @staticmethod
    def writeGraphFileJSON(filename="", version_num=1.00,
                       nodekeys=[], connectionkeys=[], graphkeys=[]):

        json_dict = {}
        json_dict["Nodes"] = {}
        json_dict["Connections"] = {}
        json_dict["Graphs"] = {}

        nodes = Supergraph.namesToNodes(nodekeys)

        for node in nodes:
            json_dict["Nodes"][node.name] = node.nodedata

        connections = Supergraph.namesToConnections(connectionkeys)

        for conn in connections:
            json_dict["Connections"][conn.name] = conn.connectiondata

        graphs = Supergraph.namesToGraphs(graphkeys)

        for graph in graphs:
            json_dict["Graphs"][graph.name]["nodekeys"] = graph.nodekeys
            json_dict["Graphs"][graph.name]["connectionkeys"] = graph.connectionkeys

        with open(filename, 'w') as outfile:
            json.dump(json_dict, outfile, indent=4, sort_keys=True)

    @staticmethod
    def readGraphFile(filename=""):
        #TODO Implement reading file
        return


import time # used for getting unix time
import Queue    # used for priority queues
import re       # regex library
import random   # used for random functions
import json

Configurations.setRuntimeConfigs()

file = open(Configurations.config_values["runtimescript"], 'r')
x = file.readlines()
for i in x:
    Interpreter.evaluateExpression(i.rstrip())

print("writing to file")
FileHandler.writeGraphFileJSON("graphfile.json","1",Supergraph.nodelist.keys(),Supergraph.connectionlist.keys())


print(Supergraph.getAllNodeKeys())
#print "connections: ",Supergraph.getAllConnectionKeys()
Supergraph.addConnections(["NODE1"],["NODE2"],'right')
print("degrees",Supergraph.getNodeDegrees(nodenames = Supergraph.getAllNodeKeys(), degree = "in"))
Supergraph.removeNodes(Supergraph.getAllNodeKeys())
Supergraph.removeConnections(Supergraph.getAllConnectionKeys())

# testing in and out degrees more
nodelist = ["N1","N2","N3","N4"]
Supergraph.addNodes(nodelist)
Supergraph.addConnections(["N1","N2","N3"],["N4"],"both")
print("degrees",Supergraph.getNodeDegrees(nodenames = Supergraph.getAllNodeKeys(), degree = "in"))
print("degrees",Supergraph.getNodeDegrees(nodenames = Supergraph.getAllNodeKeys(), degree = "out"))

print("result:",Supergraph.getNodeNeighbors(["N1"]))
print("result:",Supergraph.getNodeNeighbors(Supergraph.getNodeNeighbors(["N1"])))



#ArtPointsFinder.getArtPoints(Supergraph.getAllNodeKeys(),Supergraph.connectionlist)

#                      __
#         _______     /*_)-< HISS HISS
#   ___ /  _____  \__/ /
#  <____ /      \____ /