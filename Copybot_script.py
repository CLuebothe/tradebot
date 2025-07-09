
from eth_utils import from_wei
from web3 import Web3
import time
import requests

# Telegram setup
bot_token = '7967898034:AAGuTmptiuMkMe9-jlsKuSYZNdEEvQnc0g0'
chat_id = '6676913889'

def send_telegram(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    print(f"[Telegram] Status: {response.status_code}, Message: {message}")

# Blockchain setup
infura_url = 'https://mainnet.infura.io/v3/9a6ac04b4430495f8c588c631e7e17d8'
web3 = Web3(Web3.HTTPProvider(infura_url))

wallets = [
    '0xB80D90fcf2Ed0e4FeBE02d2a209109Bf1F62DF95',
    '0xB3A4B86499eb64d2159205967BBcfe0dE365C028',
    '0xbdfa4f4492dd7b7cf211209c4791af8d52bf5c50',
    '0x7bfee91193d9df2ac0bfe90191d40f23c773c060',
    '0x564286362092D8e7936f0549571a803B203aAceD'
]

def check_new_block():
    try:
        block = web3.eth.get_block('latest', full_transactions=True)
        print(f"[Block] Block number: {block.number}")
        for tx in block.transactions:
            from_addr = tx['from']
            to_addr = tx['to']
            eth_value = from_wei(tx['value'], 'ether')
            tx_hash = tx['hash'].hex()

            if from_addr.lower() in [w.lower() for w in wallets]:
                print(f"\n🟢 Trade Detected!")
                print(f"From: {from_addr}")
                print(f"To: {to_addr}")
                print(f"ETH Sent: {eth_value} ETH")
                print(f"Tx Hash: {tx_hash}")

                msg = f"🟢 New Trade!\nFrom: {from_addr}\nTo: {to_addr}\nETH: {eth_value}\nTx: {tx_hash}"
                send_telegram(msg)
    except Exception as e:
        print(f"[Error] {e}")

# ✅ Confirm bot is alive
print("[Info] Bot is starting...")
send_telegram("✅ Bot is running and connected!")

# 🌀 Start monitoring
while True:
    check_new_block()
    time.sleep(5)
