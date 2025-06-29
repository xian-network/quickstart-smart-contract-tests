balances = Hash(default_value=0)
metadata = Hash()
TransferEvent = LogEvent(
    event="Transfer",
    params={
        "from": {"type": str, "idx": True},
        "to": {"type": str, "idx": True},
        "amount": {"type": (int, float, decimal)},
    },
)
ApproveEvent = LogEvent(
    event="Approve",
    params={
        "from": {"type": str, "idx": True},
        "to": {"type": str, "idx": True},
        "amount": {"type": (int, float, decimal)},
    },
)

@construct
def seed():
    balances["user"] = 1_000_000_000
    balances["user1"] = 111_111_111
    balances["user2"] = 888_888_888
    metadata['token_name'] = 'XIAN'
    metadata['token_symbol'] = 'XIAN'
    metadata['token_logo_url'] = 'https://xian.org/assets/img/logo.svg'
    metadata['token_website'] = 'https://xian.org'
    metadata['total_supply'] = 1_999_999_999
    metadata['operator'] = 'user'
    


@export
def change_metadata(key: str, value: Any):
    assert ctx.caller == metadata['operator'], 'Only operator can set metadata.'
    metadata[key] = value


@export
def transfer(amount: float, to: str):
    assert amount > 0, 'Cannot send negative balances.'
    assert balances[ctx.caller] >= amount, 'Not enough coins to send.'
    balances[ctx.caller] -= amount
    balances[to] += amount
    TransferEvent({'from': ctx.caller, 'to': to, 'amount': amount})


@export
def approve(amount: float, to: str):
    assert amount >= 0, 'Cannot approve negative balances.'
    balances[ctx.caller, to] = amount
    ApproveEvent({'from': ctx.caller, 'to': to, 'amount': amount})


@export
def transfer_from(amount: float, to: str, main_account: str):
    assert amount > 0, 'Cannot send negative balances.'
    assert balances[main_account, ctx.caller] >= amount, f"Not enough coins approved to send. You have {balances[main_account, ctx.caller]} approved and are trying to spend {amount}"
    assert balances[main_account] >= amount, 'Not enough coins to send.'
    balances[main_account, ctx.caller] -= amount
    balances[main_account] -= amount
    balances[to] += amount
    TransferEvent({'from': main_account, 'to': to, 'amount': amount})


@export
def balance_of(address: str):
    return balances[address]
