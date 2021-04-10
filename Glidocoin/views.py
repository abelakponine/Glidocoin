from django.shortcuts import render
from django.http import HttpResponse
from Glidocoin.Modules.Blockchain import Blockchain
from Glidocoin.Modules.Block import Block
from Glidocoin.Modules.Wallet import Wallet
from Glidocoin.Modules.Transaction import Transaction
from .Modules.Glidocoin import Glidocoin
import hashlib, ecdsa, json, datetime, random
from django.views.decorators.csrf import csrf_exempt

print(Glidocoin.status)

blockchain = None

def init(req):
    global Glidocoin
    global blockchain
    Glidocoin.status = "running"
    Glidocoin.blockchain = Blockchain()
    blockchain = Glidocoin.blockchain
    blockchain.createGenesisBlock()
    Glidocoin.wallets = blockchain.getWallets()
    Glidocoin.wallets.createWallet("Abel Akponine", "17/04/1993", "kingabel", "Exploxi2")
    Glidocoin.myWallet = Glidocoin.wallets.findWallet("kingabel", "Exploxi2")
    print("\r\n Checking...... \r\n")
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

    print("")
    print(blockchain)
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
        return HttpResponse("data:{:.2f}".format(balance)+"\n\n", content_type='text/event-stream')
    else:
        print("Invalid Wallet")
    return HttpResponse("data:0", content_type='text/event-stream')

@csrf_exempt
def getWallet(req):
    wallet = Glidocoin.wallets.findWallet("kingabel", "Exploxi2")
    if ('signature' in wallet):
        del wallet['signature']
    if ('password' in wallet):
        del wallet['password']
    return HttpResponse(json.dumps(wallet))