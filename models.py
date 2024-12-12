import typing_extensions as typing
from typing import Union

class Filter(typing.TypedDict):
    field: str
    operator:str
    value: str
 
class ApiKeyManagement:
    def __init__(self,keys:list[str]):
        self.keys=keys
        self.currKey=0

    def nextKey(self):
        self.currKey=(self.currKey+1)%len(self.keys)
        return self.keys[self.currKey]
    
    def getKey(self):
        return self.keys[self.currKey]
# class DataManagement:
#     def __init__(self,keys)
    
class BinTreeNode:
    def __init__(self, key, data):
        self.key = key
        self.data=[data]
        self.leftChild = None
        self.rightChild = None

    def insert(self, data):
        self.data.append(data)

class BinTree:
    def __init__(self, head:BinTreeNode=None):
        self.head=head
        self.keys=[]

    def insert(self, key, data):
        if (self.head==None):
            self.head=BinTreeNode(key,data)

        elif (key==self.head.key):
            self.head.insert(data)

        elif (key<self.head.key):#less than condition
            if (self.head.leftChild==None):
                self.head.leftChild=BinTreeNode(key,data)
            else:
                self.__insertNode(self.head.leftChild, key, data)

        else:#greater than conditions
            if (self.head.rightChild==None):
                self.head.rightChild=BinTreeNode(key,data)
            else:
                self.__insertNode(self.head.rightChild, key, data)

    def __insertNode(self, currNode:BinTreeNode, key, data):
        #no None condition since already checked previously
        if (currNode.key==key):
            currNode.insert(data)

        elif (key<currNode.key):
            if (currNode.leftChild==None):
                currNode.leftChild=BinTreeNode(key,data)
            else:
                self.__insertNode(currNode.leftChild, key, data)

        else:#greater than conditions
            if (currNode.rightChild==None):
                currNode.rightChild=BinTreeNode(key,data)
            else:
                self.__insertNode(currNode.rightChild, key, data)

    def inorder(self, root:BinTreeNode=None):
        # if (root==None):
        #     if (self.head==None):
        #         print("None")
        #     else:
        #         if(self.head.leftChild!=None):
        #             self.inorder(self.head.leftChild)
        #         print(f'{self.head.key}({len(self.head.data)}): {self.head.data} ')
        #         if(self.head.rightChild!=None):
        #             self.inorder(self.head.rightChild)
        # else:
        if(root==None):
            return []
        res=[]
        if (root.leftChild!=None):
            res.extend(self.inorder(root.leftChild))
        # print(f'{root.key}({len(root.data)}): {root.data} ')
        res.extend(root.data)
        if (root.rightChild!=None):
            res.extend(self.inorder(root.rightChild))
        return res

    def search(self, key ,root:BinTreeNode=None):
        if (root==None):
            root=self.head
        if (root==None):
            return None
        data=[]
        
        if (root.key==key):
            return root.data
        elif (key<root.key):
            if(root.leftChild==None):
                return None
            return self.search(key,root.leftChild)
        else:
            if(root.rightChild==None):
                return None
            return self.search(key,root.rightChild)
        return data
    #add partial search
    def searchLess(self, key, lessThanEqual=False, root:BinTreeNode=None):
        if (root==None):#incase of head node
            root=self.head
            
        if (root==None):
            return []
            
        if (root.key==key):
            data=[]
            if(root.leftChild!=None):
                data=self.inorder(root.leftChild)
            if(lessThanEqual):
                data.extend(root.data)
            return data
        elif (key<root.key):
            if(root.leftChild!=None):
                return self.searchLess(key,lessThanEqual,root.leftChild)
        else:
            data=[]
            if(root.leftChild!=None):
                data=self.inorder(root.leftChild)
            data.extend(root.data)
            if(root.rightChild!=None):
                data.extend(self.searchLess(key,lessThanEqual,root.rightChild))
            return data
            
        return []
    
    def searchGreater(self, key, greaterThanEqual=False, root:BinTreeNode=None):
        if (root==None):
            root=self.head
        
        if (root==None):
            return []
        
        if (root.key==key):
            data=[]
            if (greaterThanEqual):
                data=root.data
            if (root.rightChild!=None):
                data.extend(self.inorder(root.rightChild))
            return data 
        elif (key<root.key):
            data=[]
            if (root.leftChild!=None):
                data=self.searchGreater(key,greaterThanEqual,root.leftChild)
            data.extend(root.data)
            if(root.rightChild!=None):
                data.extend(self.inorder(root.rightChild))
            return data
        else:
            if(root.rightChild!=None):
                return self.searchGreater(key,greaterThanEqual,root.rightChild)
        return []
    
    
class Hashmap:
    def __init__(self):
        self.map={}
        
    def insert(self, key, data):
        if (key not in self.map):
            self.map[key]=[data]
        else:
            self.map[key].append(data)
            
    def search(self, key):
        return (self.map.get(key))
    
    #add partial search
    
if __name__=='__main__':
    myTree=BinTree()
    myTree.insert(3,'3a')
    myTree.insert(3,'3b')
    myTree.insert(1,'1a')
    myTree.insert(2,'2a')
    myTree.insert(2,'2b')
    myTree.insert(0,'0a')
    res=myTree.inorder(myTree.head)
    # print(res)
    print(myTree.searchLess(3,1))
    print(myTree.searchGreater(0,True))
    
    # print(myTree.search(0))
    # print(myTree.search(3))
    # print(myTree.search(-1))

