"""
Quest Description:
Create and fund a Stellar account. In this challenge your task is to create
and fund a brand new Stellar account with 5000 XLM on the testnet. Include the
SHA256 hash of the string 'Stellar Quest Series 2' as the MEMO_HASH in the
transaction memo field. You will be required to use the createAccount
operation, so don't just rely on friendbot.
"""

# 1. Import Libraries
print("Importing Libraries...")

import requests
from stellar_sdk import Server, Keypair, TransactionBuilder, Network
import hashlib

# 2. Load Stellar Quest Keypair
print("Loading Stellar Quest Keypair...")

server = Server("https://horizon-testnet.stellar.org")
QUEST_KEYPAIR = Keypair.from_secret("Enter Your Stellar Quest Secret Key")
QUEST_PK = QUEST_KEYPAIR.public_key
QUEST_SK = QUEST_KEYPAIR.secret

# 3. Generate a Random Keypair
print("Generating Random Keypair...")

RANDOM_KEYPAIR = Keypair.random()
RANDOM_PK = RANDOM_KEYPAIR.public_key
RANDOM_SK = RANDOM_KEYPAIR.secret

# 4. Fund the Random Account via FriendBot
print("Funding Random Account...")

FRIENDBOT_URL = "https://friendbot.stellar.org"
response = requests.get(FRIENDBOT_URL, params={'addr': RANDOM_PK})
print(f"FriendBot responded with {response}")

# 5. Generate SHA-256 Hash for Transaction Memo
print("Generating SHA-256 Hash...")

hash_object = hashlib.sha256(b'Stellar Quest Series 2')
hex_digest = hash_object.hexdigest()

print(f"SHA-256 Hash: {hex_digest}")

# 6. Fund Stellar Quest Account via Random Account
print("Building Transaction...")

transaction = (
    TransactionBuilder (
        source_account = server.load_account(account_id = RANDOM_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .add_hash_memo(hex_digest)
    .append_create_account_op (
        destination = QUEST_PK,
        starting_balance = "5000",
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(RANDOM_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
