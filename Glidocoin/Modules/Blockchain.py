# Project: Glidocoin Blockcchain
# Developer: Abel Akponine
# Description: This is a blockchain application developed in Python
#   It is still in a early stage but almost completed
#   It is designed to simplify mining process, CPU friendly, without compromizing the blockchain security
#   It was developed on Python v3 environment
# Contacts: 
#   Instagram: @kingabel.a
#   Github: https://gihub.com/abelakponine

from Glidocoin.Modules.Wallet import Wallet
from Glidocoin.Modules.Transaction import Transaction
from Glidocoin.Modules.Block import Block
from decimal import Decimal as decimal
import hashlib, datetime, time, math

class Blockchain():

    def __init__(self):
        self.currencyName = "Glidocoin"
        self.username = "Abel"
        self.password = "Akponine"
        self.dateCreated = "31/03/2021 - 3:27 PM"
        self.wallet = None
        self.genesisAddress = None
        self.wallets = Wallet()
        self.transactions = []
        self.pendingBlocks = []
        self.chain = []
        self.decimal = 1000000 # 1 million okies
        self.totalSupply = 100000000 * self.decimal # 100 million Glidocoin = 1 Trillion okies

    def createTransaction(self, transaction, pubKey):
        balance = self.getBalanceOf(transaction.fromAddress) # get current balance of sender and validate
        if (self.isTransactionValid(balance, transaction)):    
            if (transaction.isTransactionValid(pubKey)):
                self.transactions.append(transaction)
                return True
            else:
                return False
        else:
            return False
    
    def isTransactionValid(self, balance, transaction):
        # check for double spending
        txnBalance = balance # current wallet balance
        isValid = False
        
        if (transaction.fromAddress == None): # means it's a genesis block (allowed)
            isValid = True
        elif (len(self.transactions) > 0): # current balance must be validated if the sender has any existing transactions
                                            # neccessary to prevent double spending
            for txn in self.transactions:
                if (txn.fromAddress == transaction.fromAddress and (balance >= transaction.amount and transaction not in self.transactions)):
                    txnBalance -= txn.amount
                    return (txnBalance >= transaction.amount)
        else: # current balance is valid, if there are no pending transactions
            isValid = True

        return isValid

    def addTransactionBlock(self, block):
        # add block to pending block list
        self.pendingBlocks.append(block)

    def createGenesisBlock(self):
        # create Glidocoin exchanger wallet
        wallets = self.wallets
        wallets.createWallet(self.currencyName, self.dateCreated, self.username, self.password)
        gWallet = wallets.findWallet(self.username, self.password)
        self.genesisAddress = gWallet['walletAddress']
        self.wallet = gWallet
        # instantiate genesis transaction
        txn = Transaction(None, gWallet['walletAddress'], self.totalSupply, self.dateCreated)
        # load keypair
        prvKey = wallets.loadPrvKey(gWallet['hash'])
        pubKey = prvKey.verifying_key
        # sign transaction
        txn.signTransaction(prvKey)
        # create genesis transaction and mine genesis block
        if (self.createTransaction(txn,pubKey)):
            self.minePendingBlocks(self.wallet)
            self.transactions = [] # clear transaction list
        else:
            return False

        # print("Genesis Block created:")
        # print("\tIndex: \t\t"+str(self.transactions.index(self.transactions[0])))
        # print("\tFrom: \t\t"+str(self.transactions[0].fromAddress))
        # print("\tTo: \t\t"+str(self.transactions[0].toAddress))
        # print("\tAmount: \t"+str(self.transactions[0].amount)
        #     +' ('+self.fromOkies(self.transactions[0].amount)+' GCN)')
        # print("\tTimestamp: \t"+str(self.transactions[0].timestamp))
        # print("\tMined on: \t"+str(self.transactions[0].mined)+"\r\n")
        # print("Pending: "+str(self.pendingBlocks))

        return True

    def createBlock(self):
        # if (len(self.transactions) > 0):
        storedTxns = self.transactions.copy()
        self.transactions = []
        block = Block(storedTxns, datetime.datetime.now().strftime("%d/%m/%Y - %I:%M %p"), str(self.getPreviousHash())).getBlock()
        block.calculate_hash()
        block.miningReward = (((block.miningReward/5)*10)/60)

        # add block to pending block list
        self.addTransactionBlock(block)
        print("\r\n\033[1;92mNew block created!\033[0m\r\n")

        # delay block creation for 10 seconds
        print("\r\033[1;92mPreparing to create block in "+str(block.miningDuration)+" seconds, please wait...\033[0m")
        
        miningDuration = int(block.miningDuration/30)
        
        # if (len(self.chain) == 0):
        for timer in range(0, miningDuration):
            
            if ((miningDuration - timer) > 60):
                print("\033[1;92mTimer: "+str(miningDuration - timer)+" ("+str(math.ceil((block.miningDuration - timer)/60))+" minutes)", end="\r")
            elif ((miningDuration - timer) > 1):
                print("\033[1;92mTimer: "+str(miningDuration - timer)+" seconds ", end="\r")
            else:
                print("\033[1;92mTimer: "+str(miningDuration - timer)+" second ", end="\r")
            time.sleep(1)
            
        # add block to pending block list
        self.addTransactionBlock(block)
        print("\r\n\033[1;92mNew block created!\033[0m\r\n")

    def minePendingBlocks(self, wallet):

        self.createBlock() # create new pending block

        if (len(self.pendingBlocks) > 0):
            pendingBlocks = self.pendingBlocks.copy()
            self.pendingBlocks = [] # clear pending block list after mining
            self.validateBlocks(pendingBlocks)

            for block in pendingBlocks:
                walletLength = len(self.getWallets().wallets)
                block.setMiningReward(walletLength)
                block.setDifficulty(walletLength)

                # miner's reward transaction
                global_wallet = self.getWallets()
                mTxn = Transaction(self.genesisAddress, wallet['walletAddress'], block.miningReward, block.timestamp)
                prvKey = global_wallet.loadPrvKey(wallet['hash'])
                pubKey = prvKey.verifying_key
                mTxn.signTransaction(prvKey)

                # add miner's transaction to block
                block.addTransaction(mTxn)
                block.calculate_hash()
                
                if (block.mine()):
                    try:
                        if (block in pendingBlocks and block not in self.chain):
                            self.chain.append(block)
                            pendingBlocks.remove(block)
                            print("\033[1;96mBlock mined!\033[0m")
                            print("\033[1;96mCurrent balance: \033[1;93m"+"{:.6f}".format(self.getBalanceOf(wallet['walletAddress']))+" GCN\033[0m ("+str(self.to_okies(self.getBalanceOf(wallet['walletAddress'])))+" Okies)")
                            print("\033[1;96mSystem balance: \033[1;93m"+"{:.6f}".format(self.getBalanceOf(self.genesisAddress))+" GCN\033[0m ("+str(self.to_okies(self.getBalanceOf(wallet['walletAddress'])))+" Okies)\r\n")
                            print(self.genesisAddress)

                        elif (block in pendingBlocks and block in self.chain):
                            self.pendingBlocks.remove(block)
                        else:
                            print("Oops! block is gone")

                    except ValueError:
                        print(ValueError)

                # update mined timestamp
                for txn in block.transactions:
                    txn.mined = datetime.datetime.now().strftime("%d/%m/%Y - %I:%M %p")
        else:
            print("\033[93mNo pending transaction available at the moment.\033[0m\r\n")
            

    def getPreviousHash(self):
        if (len(self.chain) < 1):
            return None
        else:
            return self.chain[(len(self.chain) - 1)].hash

    def to_GCN(self, amount):
        return int(str(round(amount / self.decimal)))

    def to_okies(self, amount):
        return int(str(round(amount * self.decimal)))

    def getAddress(self):
        return self.wallet['walletAddress']
    
    def getWallets(self):
        return self.wallets

    def getTransactions(self):
        return self.transactions

    def getPendingBlocks(self):
        return self.pendingBlocks

    def getChains(self):
        return self.chain
    
    def validateBlocks(self, pendingBlocks):
        for block in pendingBlocks:
            data = str(block.transactions)+' '+str(block.getPreviousHash())+' '+block.timestamp
            hash = hashlib.sha256(data.encode()).hexdigest()
            if (block.hash != hash):
                self.removeBlockFromPending(block)
            else:
                return True

    def removeBlockFromPending(self, block):
        self.getPendingBlocks().remove(block)
        return True

    def getBalanceOf(self, walletAddress):
        global balance
        balance = 0
        if (len(self.getChains()) > 0):
            for block in self.getChains():
                for txn in block.getTransactions():
                    if (txn.fromAddress == walletAddress):
                        balance = (decimal(balance) - decimal(txn.amount))
                    elif (txn.toAddress == walletAddress):
                        balance += decimal(txn.amount)
        return balance
    
    def startMainer(self, wallet):
        wallet['status'] = "mining"
        while (True):
            global_wallet = self.getWallets()
            # initialize wallet
            myWallet = global_wallet.findWallet(wallet['username'], wallet["password"])
            self.minePendingBlocks(myWallet)
            time.sleep(1)
            print(self.getBalanceOf(self.genesisAddress))

            if (wallet['status'] != "mining"):
                break