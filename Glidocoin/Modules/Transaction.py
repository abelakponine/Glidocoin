import hashlib, ecdsa, datetime

class Transaction():

    def __init__(self, fromAddress = None, toAddress = None, amount = 0, timestamp = datetime.datetime.now().strftime("%d/%m/%Y - %I:%M %p")):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.timestamp = timestamp
        self.hash = None
        self.signature = None
        self.calculate_hash()

    def calculate_hash(self):
        self.hash = hashlib.sha256((str(self.fromAddress)+" "+str(self.toAddress)+" "+str(self.amount)).encode()).hexdigest()+" "+self.timestamp

    def getTransactionHash(self):
        return self.hash

    def signTransaction(self, prvKey):
        self.signature = prvKey.sign(self.getTransactionHash().encode())
        return True
    
    def getSignature(self):
        return self.signature

    def isTransactionValid(self, pubKey):
        if (self.fromAddress == None):
            return True
        if (not self.signature or self.signature == None):
            return False
        
        return pubKey.verify(self.signature, self.hash.encode())