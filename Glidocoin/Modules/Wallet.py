import hashlib, json, ecdsa

# this class represents a set of user wallets used to store currency and wallet information
class Wallet():

    def __init__(self):
        self.wallets = []
        self.walletId = 1000
        self.fullname = None
        self.dob = None
        self.username = None
        self.password = None
        self.hash = None
        self.walletAddress = None
        self.status = "dormant" # dormant, active, mining

    # create new wallet
    def createWallet(self, fullname, dob, username, password):
        self.fullname = fullname
        self.dob = dob
        self.username = str(username)
        self.password = str(hashlib.sha256(str(password).encode()).hexdigest())
        self.status = "active"

        # hash wallet
        self.hash = hashlib.sha256((self.fullname+" "+self.dob+" "+self.username+" "+self.password).encode()).hexdigest()

        # generate wallet address (public key)
        prvKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

        # save private key
        f = open("Glidocoin/secrets/"+str(self.hash)+".pem", "w+")
        f.write(prvKey.to_pem().decode())

        # sign wallet
        self.signature = prvKey.sign(self.hash.encode())

        # assign wallet address
        self.walletAddress = hashlib.sha1(prvKey.verifying_key.to_pem()).hexdigest()
        myWallet = self.getLastWalletInfo()
        self.wallets.append(myWallet)
        self.walletId += 1
        return True

    # check if wallet is valid
    def isWalletValid(self, pubKey, wallet):
        try:
            return pubKey.verify(wallet['signature'], wallet['hash'].encode())
        except:
            return False

    # load public key
    def loadPrvKey(self, hash):
        f = open("Glidocoin/secrets/"+str(hash)+".pem", "r")
        prvKey = ecdsa.SigningKey.from_pem(f.read())
        return prvKey

    # find wallet by Id or wallet Address
    def findWallet(self, username, password):
        wallet = None
        for w in self.getWallets():
            if (w['username'] == str(username) or w['password'] == str(hashlib.sha256(str(password).encode()).hexdigest())):
                wallet = w
        return wallet

    # get wallet index
    def getWalletIndex(self, wallet):
        return self.getWallets().index(wallet)

    # get list of all created wallets
    def getWallets(self):
        return self.wallets

    # get last wallet info
    def getLastWalletInfo(self):
        walletInfo = {
            "walletId" : self.walletId,
            "fullname" : self.fullname,
            "walletAddress" : self.walletAddress,
            "hash" : self.hash,
            "signature" : self.signature,
            "username" : self.username,
            "password" : self.password,
            "status" : self.status
        }
        return walletInfo