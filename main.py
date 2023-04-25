import json

# exports.reece.sh/juno
auth_file = "7980000_auth.json"
bank_file = "7980000_bank.json"

accounts_to_ignore = [
    # They moved funds to new wallet 30 days ago
    "juno1ws8d7f234jtnda3ea22hhejzx5qsfu3dl50shx"
]

normal_acc_len = len("juno1qqq9txnw4c77sdvzx0tkedsafl5s3vk7hn53fn")

empty_accounts = {}
with open(auth_file) as f:
    accs = json.load(f)
    for acc in accs["accounts"]:
        # Only get normal accounts
        if acc["@type"] != "/cosmos.auth.v1beta1.BaseAccount":
            continue

        if "sequence" not in acc:
            # print(acc)
            continue

        if int(acc["sequence"]) == 0:
            empty_accounts[acc["address"]] = acc["sequence"]


# open bank file and get all accounts which are in empty accounts
with open(bank_file) as f:
    bank = json.load(f)

all_juno = {}
for b in bank["balances"]:
    addr = b["address"]

    if addr in accounts_to_ignore:
        continue

    if addr in empty_accounts:
        if len(addr) != normal_acc_len:
            continue

        if len(b["coins"]) > 1:
            # If they have IBC denoms other tokens, then they are active
            continue

        for coin in b["coins"]:
            if coin["denom"] == "ujuno":
                amount = int(coin["amount"])
                if amount > 50000_000_000:
                    print(addr, amount)
                all_juno[addr] = amount

print(f"{len(all_juno.keys()):,} accounts")

# get all accounts with 50k
whales = {k: v for k, v in all_juno.items() if v == 50000_000_000}

print(len(whales.keys()), "50k JUNO whales")
amt_of_whales = sum(whales.values())
print(f"{amt_of_whales/1_000_000:,} JUNO")

summation = sum(all_juno.values())
print(f"{round(summation/1_000_000, 0):,} JUNO")

# save all_juno to a file
reverse_sort_all_juno = {
    k: v for k, v in sorted(all_juno.items(), key=lambda item: item[1], reverse=True)
}
with open("all_juno.json", "w") as f:
    json.dump(reverse_sort_all_juno, f, indent=4)
