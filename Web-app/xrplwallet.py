from xrpl.account import get_balance
from xrpl.clients import JsonRpcClient
from xrpl.models import Payment, Tx
from xrpl.transaction import submit_and_wait
from xrpl.wallet import generate_faucet_wallet
from xrpl.wallet import Wallet

# Create a client to connect to the test network
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

def getseedToWallet(seed):
    test_wallet = Wallet.from_seed(seed)
    print(test_wallet)
    return test_wallet


def getbalance(address):
    balance = get_balance(address, client)
    return balance

def createwallet():
    # Create two wallets to send money between on the test network
    wallet1 = generate_faucet_wallet(client, debug=True)
    print(wallet1)
    walletaddress = wallet1.address
    seed = wallet1.seed
    balance = getbalance(walletaddress)
    
    return walletaddress, seed, balance

def xrpTransfer(wallet1,wallet1address,wallet2address,amount):
    
    # Create a Payment transaction from wallet1 to wallet2
    payment_tx = Payment(
        account=wallet1address,
        amount="1000",
        destination=wallet2address,
    )

    # Submit the payment to the network and wait to see a response
    #   Behind the scenes, this fills in fields which can be looked up automatically like the fee.
    #   It also signs the transaction with wallet1 to prove you own the account you're paying from.
    payment_response = submit_and_wait(payment_tx, client, wallet1)
    print("Transaction was submitted")

    # Create a "Tx" request to look up the transaction on the ledger
    tx_response = client.request(Tx(transaction=payment_response.result["hash"]))

    # Check whether the transaction was actually validated on ledger
    print("Validated:", tx_response.result["validated"])

    # Check balances after 1000 drops (.001 XRP) was sent from wallet1 to wallet2
    print("Balances of wallets after Payment tx:")
    print(get_balance(wallet1address, client))
    print(get_balance(wallet2address, client))
