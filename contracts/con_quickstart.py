bank = Hash(default_value=0)

@export
def deposit(amount: float):
    token = importlib.import_module('currency')
    token.transfer_from(
        amount=amount,
        to=ctx.this,
        main_account=ctx.caller
    )
    bank[ctx.caller] += amount

@export
def withdraw(amount: float):
    assert bank[ctx.caller] >= amount, 'insufficient funds'
    token = importlib.import_module('currency')
    token.transfer(amount=amount, to=ctx.caller)
    bank[ctx.caller] -= amount