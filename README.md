# quickstart-smart-contract-tests 🧪🚀

[![CI](https://github.com/xian-network/quickstart-smart-contract-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/xian-network/quickstart-smart-contract-tests/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Try the Xian demo contracts & **run the full unit-test suite in under a minute**—locally *or* in the cloud.

> **Requires Python 3.11** (matches the `environment.yml` and CI matrix).

| One-click playgrounds | |
|-----------------------|-----------------------------------------------------------|
| Colab | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xian-network/quickstart-smart-contract-tests/blob/main/quickstart_tests.ipynb) |
| Binder | [![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/xian-network/quickstart-smart-contract-tests/HEAD?labpath=quickstart_tests.ipynb) |
| Replit | [![Run on Replit](https://replit.com/badge?v=1)](https://replit.com/new/github/xian-network/quickstart-smart-contract-tests) |

---

## What’s inside?

```
quickstart-smart-contract-tests/
├─ contracts/               ← demo smart-contracts
│   ├─ currency.py
│   └─ con_quickstart.py
├─ tests/                   ← pre-written PyTest/Unittest spec
│   └─ test_con_quickstart.py
├─ quickstart_tests.ipynb   ← notebook that shows & runs the tests
├─ environment.yml          ← Binder / Replit Python-3.11 env
└─ .github/workflows/tests.yml  ← CI: runs pytest on every push/PR
```

---

## 🚀 Quick start

### 1  One-click (no local install)

| Platform | Action |
|----------|--------|
| **Colab** | Click the badge above, then **Runtime → Run all**. |
| **Binder** | Click the badge & wait ~30 s; notebook opens automatically. |
| **Replit** | Click badge, hit **Fork → Run**. |

You’ll see green `pytest` dots:

```
tests/test_con_quickstart.py ...                                   [100%]
3 passed in 0.84s
```

### 2  Local clone (Python 3.11 required)

```bash
git clone https://github.com/xian-network/quickstart-smart-contract-tests.git
cd quickstart-smart-contract-tests

# create a Python 3.11 venv
python3.11 -m venv .venv && source .venv/bin/activate

pip install git+https://github.com/xian-network/xian-contracting pytest
pytest -q
```

---

## ✍️ Writing your own tests

1. Create a file under `tests/`, e.g. `test_my_feature.py`.  
2. Copy the `ContractingClient` setup shown in the existing test.  
3. `pytest -q` again—your new assertions run alongside ours.

---

## 📜 License

[MIT](LICENSE) — do what you like, just keep the notice.

> **Made with ❤️ by the Xian community.** PRs, issues & stars welcome!
