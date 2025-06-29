# tests/test_con_quickstart.py
import unittest, os, sys
from pathlib import Path
from contracting.client import ContractingClient

# ──────────────────────────────────────────────────────────
#  locate repo root & contracts dir
# ──────────────────────────────────────────────────────────
THIS_FILE     = Path(__file__).resolve()
ROOT_DIR      = THIS_FILE.parent.parent          # quickstart-smart-contracts/
CONTRACTS_DIR = ROOT_DIR / 'contracts'

# keep CWD at repo root so any relative imports inside contracts work
os.chdir(ROOT_DIR)

TOKEN       = 'currency'          # contracts/currency.py
QUICKSTART  = 'con_quickstart'    # contracts/con_quickstart.py
SUBMISSION  = 'submission'        # contracts/submission.s.py  (helper, optional)


class TestQuickstartBank(unittest.TestCase):

    # ──────────────────────────────────────────────────────
    #  scaffolding
    # ──────────────────────────────────────────────────────
    def setUp(self):
        self.c = ContractingClient()
        self.c.raw_driver.flush_full()

        # optional helper contract (ignore if absent)
        sub_file = CONTRACTS_DIR / 'submission.s.py'
        if sub_file.exists():
            with open(sub_file) as f:
                self.c.raw_driver.set_contract(name=SUBMISSION, code=f.read())

        # 1. submit base currency
        with open(CONTRACTS_DIR / 'currency.py') as f:
            self.c.submit(f.read(),
                          name=TOKEN)
        self.cur = self.c.get_contract(TOKEN)

        # 2. submit quick-start bank contract
        with open(CONTRACTS_DIR / 'con_quickstart.py') as f:
            self.c.submit(f.read(), name=QUICKSTART, signer='sys')
        self.qk = self.c.get_contract(QUICKSTART)

    # handy alias
    def _bank(self, who): return self.qk.bank[who]

    # ──────────────────────────────────────────────────────
    #  deposit should credit bank + move tokens
    # ──────────────────────────────────────────────────────
    def test_deposit_updates_state_and_balances(self):
        amt = 150

        bal_user_before   = self.cur.balance_of(address="user")
        bal_contract_before = self.cur.balance_of(address=QUICKSTART)

        # approve tokens for transfer by the contract
        self.cur.approve(amount=amt, to=QUICKSTART, signer="user")
        # deposit tokens into bank
        self.qk.deposit(amount=amt, signer="user")

        self.assertEqual(self._bank("user"), amt)                  # mapping
        self.assertEqual(self.cur.balance_of(address="user"),
                         bal_user_before - amt)                       # user balance
        self.assertEqual(self.cur.balance_of(address=QUICKSTART),
                         bal_contract_before + amt)                   # contract balance

    # ──────────────────────────────────────────────────────
    #  withdraw returns tokens & debits bank
    # ──────────────────────────────────────────────────────
    def test_withdraw_updates_state_and_balances(self):
        dep, wd = 200, 80
        # approve tokens for transfer by the contract
        self.cur.approve(amount=dep, to=QUICKSTART, signer="user")
        # deposit tokens into bank
        self.qk.deposit(amount=dep, signer="user")

        bal_user_before     = self.cur.balance_of(address="user")
        bal_contract_before = self.cur.balance_of(address=QUICKSTART)

        self.qk.withdraw(amount=wd, signer="user")

        self.assertEqual(self._bank("user"), dep - wd)
        self.assertEqual(self.cur.balance_of(address="user"),
                         bal_user_before + wd)
        self.assertEqual(self.cur.balance_of(address=QUICKSTART),
                         bal_contract_before - wd)

    # ──────────────────────────────────────────────────────
    #  cannot withdraw more than balance
    # ──────────────────────────────────────────────────────
    def test_withdraw_insufficient_funds_fails(self):
        # approve tokens for transfer by the contract
        self.cur.approve(amount=50, to=QUICKSTART, signer="user")
        self.qk.deposit(amount=50, signer="user")
        with self.assertRaises(AssertionError):
            self.qk.withdraw(amount=100, signer="user")


if __name__ == '__main__':
    unittest.main()
