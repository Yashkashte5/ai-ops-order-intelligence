import pandas as pd

MAX_DAILY_CAPACITY = 200

def load_data():
    orders = pd.read_csv("orders.csv")
    inventory_df = pd.read_csv("inventory.csv")
    inventory = dict(zip(inventory_df.ProductCode, inventory_df.AvailableStock))
    orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])
    return orders, inventory

def process_orders(orders, inventory):
    # Urgent orders > then Normal > per day
    orders["PriorityRank"] = orders["Priority"].map({"Urgent": 0, "Normal": 1})
    orders = orders.sort_values(by=["OrderDate", "PriorityRank"])

    daily_capacity = {}
    results = []

    for _, order in orders.iterrows():
        order_id = order["OrderID"]
        product = order["ProductCode"]
        qty = order["Quantity"]
        date = order["OrderDate"].date()

        daily_capacity.setdefault(date, MAX_DAILY_CAPACITY)

        available_stock = inventory.get(product, 0)
        remaining_capacity = daily_capacity[date]

        # HARD STOP no capacity left today
        if remaining_capacity == 0:
            results.append({
                "OrderID": order_id,
                "OrderDate": date,
                "Decision": "Delay",
                "Reason": "Daily production capacity exhausted"
            })
            continue

        # HARD STOP no inventory
        if available_stock == 0:
            results.append({
                "OrderID": order_id,
                "OrderDate": date,
                "Decision": "Escalate",
                "Reason": "No inventory available"
            })
            continue

        # FULL APPROVAL
        if qty <= available_stock and qty <= remaining_capacity:
            inventory[product] -= qty
            daily_capacity[date] -= qty

            results.append({
                "OrderID": order_id,
                "OrderDate": date,
                "Decision": "Approve",
                "Reason": "Sufficient inventory and capacity"
            })
            continue

        # PARTIAL FULFILLMENT
        fulfillable_qty = min(available_stock, remaining_capacity)

        if fulfillable_qty > 0:
            inventory[product] -= fulfillable_qty
            daily_capacity[date] -= fulfillable_qty

            results.append({
                "OrderID": order_id,
                "OrderDate": date,
                "Decision": "Split",
                "Reason": f"Only {fulfillable_qty} units can be fulfilled today"
            })
        else:
            results.append({
                "OrderID": order_id,
                "OrderDate": date,
                "Decision": "Delay",
                "Reason": "Inventory available but no production capacity today"
            })

    return pd.DataFrame(results)

def main():
    orders, inventory = load_data()
    output = process_orders(orders, inventory)

    print("\n  AI OPS ORDER DECISIONS \n")
    print(output.to_string(index=False))

    output.to_csv("decision_output.csv", index=False)

if __name__ == "__main__":
    main()
