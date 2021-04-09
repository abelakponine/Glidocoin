import hashlib, ecdsa, time, random, math

''' This Class represents a block that can be added to a blockchain network '''
class Block():

    def __init__(self, transactions, timestamp, previousHash = None):
        self.transactions = transactions
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.hash = None
        self.mined = None
        self.minerLimit = 500000000 # mining will stop when total users reach this amount (500 millio users)
        self.endMiner = 0 # value to be assigned at the end of mining
        self.decimal = 1000000 # 1 million okies
        self.difficulty = 0 # default mining dificulty 0 (total number of wallets * 5, eg: 10 wallets * 5 = 50)
                            # The difficulty ranges from 0 to maximum 
        self.maxDifficulty = 5000 # maximum mining dificulty 5000
        self.exponential = 5 # an increment of *5 on difficulty
        self.miningReward = 50000 / self.decimal # 0.05 Glidocoin => 50000 Okies every 5 minutes up to 0.6 per hour
        self.miningDuration = 5 * 60 # 5 minutes minimum, may take longer depend on guesses

    def getBlock(self):
        return self

    def getPreviousHash(self):
        return self.previousHash

    def getTransactions(self):
        return self.transactions

    def getAuthor(self):
        return self.author

    def getSignature(self):
        return self.signature

    def calculate_hash(self):
        data = str(self.transactions)+' '+str(self.previousHash)+' '+self.timestamp
        self.hash = hashlib.sha256(data.encode()).hexdigest()
        return self.hash

    def addTransaction(self, transaction):
        self.transactions.append(transaction)
        return True
        
    def mine(self):
        target = random.randint(0, self.difficulty)
        while(True): # 0 to maximum difficulty
            guess = random.randint(0, self.difficulty)
            print("\033[1;92mGuessing (POW = "+str(target)+"): "+str(guess)+" \033[0m", end="\r")
            if (guess == target):
                time.sleep(1)
                break

        print("\033[1;92mReward: "+str("{:.6f}".format(self.miningReward))+" GCN ("+str("{:.0f}".format(self.miningReward * self.decimal))+" Okies) \033[0m", end="\r")
        print("\r")
        return True

    def hasValidTransactions(self):
        for tx in self.transactions :
            if (not tx.isTransactionValid()):
                return False
        return True

    def setDifficulty(self, walletLength):
        if (self.difficulty < self.maxDifficulty):
            self.difficulty = walletLength*self.exponential
        else:
            self.difficulty = self.maxDifficulty

    def setMiningReward(self, walletLength):
        if (walletLength > self.minerLimit):
            self.miningReward = self.endMiner # stop mining when users exceeds 500 million (value = 0)
        elif ((walletLength % self.decimal) == 0):
            reward = ((self.minerLimit / self.decimal) * 0.0001)
            self.miningReward = reward - (0.0001 * (walletLength / self.decimal))
