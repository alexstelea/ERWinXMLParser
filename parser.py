from toposort import toposort
import xml.etree.ElementTree as ET
import json


tree = ET.parse('EDWSTDIC_orders_PHYSICAL.xml')
root = tree.getroot()
adjMap = {}

def makeEntities():
    for child in root:
        if "element" in child.tag:
            childName = child.attrib["name"]
            dependencies = set()
            for subChild in child:
                subChildTag = subChild.tag
                if "keyref" in subChildTag:
                    for keyRefChild in subChild:
                        if "selector" in keyRefChild.tag:
                            dependencies.add(keyRefChild.attrib["xpath"][3:])
            adjMap[childName] = dependencies

def dfs(graph):
    jsonGraph = {}
    jsonGraph["name"] = "root";
    jsonGraph["children"] = []
    visited = set()
    for vertex in adjMap:
        if vertex not in visited:
            jsonGraph["children"].append(explore(vertex, visited))
    return json.dumps(jsonGraph)

def explore(parentName, visited):
    parentDict = {}
    parentDict["name"] = parentName
    visited.add(parentName)
    leaf = True
    if parentName in adjMap:
        for child in adjMap[parentName]:
            if child not in visited:
                leaf = False
                if "children" not in parentDict:
                    parentDict["children"] = []
                parentDict["children"].append(explore(child,visited))
    if leaf:
        parentDict["size"] = 1994
    return parentDict

def topologicalSort(graph):
    topoList = list(toposort(graph))
    dfs(topoList)

def main():
    makeEntities()
    #topologicalSort(adjMap)
    jsonGraph = dfs(adjMap)
    print jsonGraph
    with open("edw.json","w") as f:
        f.write(jsonGraph)

if __name__ == "__main__":
    main()