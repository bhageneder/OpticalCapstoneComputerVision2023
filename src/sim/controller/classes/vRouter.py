
#### Router Class ####

# Routing Table (Very Rudementary) Format:
# dictionary = {
#     "10.0.0.10": [("10.0.0.11", 1), ("10.0.0.12", 2)],
#     "sourceIP": [("destIP", numHops), ...]
# }

class vRouter():
    def __init__(self):
        self.__table = dict()

    # Efficiently update the key-value pair
    def updateRoute(self, sourceIP, routeArray):
        self.__table.update({sourceIP: routeArray})

    # Inefficiently search the table for the best route
    def findRoute(self, destIP):
        bestRoute = (None, 65535)
        
        for key in self.__table.keys():
            possibleRoutes = self.__table.get(key)
            
            for tuple in possibleRoutes:
                if (tuple[0] == destIP and tuple[1] < bestRoute[1]):
                    bestRoute = tuple

                    # Stop if route length is 1
                    if (bestRoute[1] == 1):
                        return bestRoute[0]

        return bestRoute[0]