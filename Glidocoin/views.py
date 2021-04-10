from django.shortcuts import render
from django.http import HttpResponse
from Glidocoin.Modules.Blockchain import Blockchain
from Glidocoin.Modules.Block import Block
from Glidocoin.Modules.Wallet import Wallet
from Glidocoin.Modules.Transaction import Transaction
from .Modules.Glidocoin import Glidocoin
import hashlib, ecdsa, json, datetime, random
from django.views.decorators.csrf import csrf_exempt


blockchain = None

def init(req):
    global Glidocoin
    global blockchain
    Glidocoin.status = "running"
    Glidocoin.blockchain = Blockchain()
    blockchain = Glidocoin.blockchain
    blockchain.createGenesisBlock()
    Glidocoin.wallets = blockchain.getWallets()
    Glidocoin.wallets.createWallet("Abel Akponine", "17/04/2021", "kingabel", "1234")
    Glidocoin.myWallet = Glidocoin.wallets.findWallet("kingabel", "1234")
    return HttpResponse(Glidocoin.status)

# Create your views here.
def home(req):
    
    for block in blockchain.getChains():
        block.index = blockchain.getChains().index(block)
        blockchain.miningReward = blockchain.chain[(len(blockchain.getChains()) -1)].miningReward
        blockchain.myWallet = Glidocoin.myWallet
        blockchain.myBalance = blockchain.getBalanceOf(blockchain.myWallet['walletAddress'])
        blockchain.totalUsers = len(blockchain.getWallets().wallets)

    dict = {
        "Glidocoin": blockchain
    }
    return render(req, 'index.html', dict)

def startMainer(req, wallet_addr):

    myWallet = Glidocoin.myWallet
    
    if (wallet_addr == myWallet['walletAddress']):
        blockchain.startMainer(myWallet)
    else:
        print("Error starting miner")
    return HttpResponse(myWallet['status'])

def stopMainer(req, wallet_addr):

    myWallet = Glidocoin.myWallet

    if (wallet_addr == myWallet['walletAddress']):
        myWallet['status'] = "active"
    else:
        print("Error stopping miner")
    return HttpResponse(myWallet['status'])

def getBalanceOf(req, wallet_addr):

    myWallet = Glidocoin.myWallet

    if (wallet_addr == myWallet['walletAddress']):
        balance = blockchain.getBalanceOf(myWallet['walletAddress'])
        return HttpResponse("data:{:.6f}".format(balance)+"\n\n", content_type='text/event-stream')
    else:
        print("Invalid Wallet")
    return HttpResponse("data:0", content_type='text/event-stream')

@csrf_exempt
def getWallet(req):
    cred = json.loads(req.body.decode())
    wallet = Glidocoin.wallets.findWallet(cred['username'], cred['password'])
    myWallet = wallet.copy()
    if ('signature' in myWallet):
        del myWallet['signature']
    if ('password' in myWallet):
        del myWallet['password']

    return HttpResponse(json.dumps(myWallet))
