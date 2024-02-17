class Test():
    def __init__(self):
        self.selfVar = None

    def firstMethod(self):
        aLocalVar = 'aLocalVar'
        print(aLocalVar)

    def secondMethod(self):
        aLocalVar = 'localVarModified' + aLocalVar
        print(aLocalVar)

aTest = Test()
aTest.firstMethod()
aTest.secondMethod()