# AI Ops Assistant – Order Intelligence System

This project implements a working AI Ops decision system that processes incoming orders, checks inventory and daily production capacity, and generates operational decisions with clear reasoning.

---

## How to Run

### Requirements
- Python 3.9+
- pip

### Setup
```bash
pip install -r requirements.txt
```

### Run
```bash
python main.py
```

---

## What the System Does

- Automatically reads orders and inventory from CSV files
- Enforces a fixed daily production capacity (200 units/day)
- Prioritizes urgent orders over normal orders per day
- Prevents negative inventory and capacity violations
- Generates one decision per order:
  - Approve
  - Split
  - Delay
  - Escalate
- Produces clear, human-readable reasons for each decision

---

## Output

- Console log showing order decisions with order date
- `decision_output.csv` generated for audit and review

---

## Notes

- Production capacity resets daily
- Inventory is carried across days
- Split decisions are only made when partial fulfillment is possible within capacity
- Orders are delayed when capacity is exhausted and escalated when inventory is unavailable

