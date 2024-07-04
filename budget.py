stocks = [
    {"id": 1183441, "price": 4058.00, "actual_percentage": 24.79, "desirable_percentage": 30},
    {"id": 1159235, "price": 320.10, "actual_percentage": 14.67, "desirable_percentage": 15},
    {"id": 1159243, "price": 4308.00, "actual_percentage": 13.16, "desirable_percentage": 15},
    {"id": 1159169, "price": 130.80, "actual_percentage": 4.8, "desirable_percentage": 5},
    {"id": 1159094, "price": 322.00, "actual_percentage": 4.92, "desirable_percentage": 5},
    {"id": 5113022, "price": 129.9, "actual_percentage": 13.77, "desirable_percentage": 15},
    {"id": 5113329, "price": 117.57, "actual_percentage": 13.67, "desirable_percentage": 15},
    # Add more stocks as needed
]

max_budget = 3300  # Example budget
top_k = 5  # Number of top combinations to show


def get_combinations(stocks, budget, current_combination=[], index=0):
    if budget < 0:
        return []

    if index == len(stocks):
        return [current_combination]

    combinations = []

    stock = stocks[index]
    max_units = budget // stock['price']

    for units in range(int(max_units) + 1):
        new_combination = current_combination + [
            {"id": stock["id"], "price": stock["price"], "units": units, "total_cost": units * stock["price"]}]
        remaining_budget = budget - units * stock["price"]
        combinations += get_combinations(stocks, remaining_budget, new_combination, index + 1)

    return combinations


# Calculate the difference between desirable and actual percentages
for stock in stocks:
    stock['percentage_diff'] = stock['desirable_percentage'] - stock['actual_percentage']

# Sort stocks based on the percentage difference and price (higher difference and lower price first)
stocks.sort(key=lambda x: (-x['percentage_diff'], x['price']))

combinations = get_combinations(stocks, max_budget)

# Filter out empty combinations and those that exceed the budget
valid_combinations = [
    comb for comb in combinations
    if sum(item['total_cost'] for item in comb) <= max_budget and any(item['units'] > 0 for item in comb)
]

# Sort combinations by remaining budget (ascending order)
valid_combinations.sort(key=lambda comb: max_budget - sum(item['total_cost'] for item in comb))

# Get the top K combinations
top_combinations = valid_combinations[:top_k]

# Print results
print(f"Top {top_k} combinations of stocks to buy within budget:")
for i, combination in enumerate(top_combinations):
    print(f"Combination {i + 1}:")
    for stock in combination:
        if stock["units"] > 0:
            print(
                f"  ID: {stock['id']}, Price: {stock['price']}, Units: {stock['units']}, Total Cost: {stock['total_cost']}")
    total_cost = sum(stock['total_cost'] for stock in combination)
    remaining_budget = max_budget - total_cost
    print(f"  Total Cost: {total_cost}, Remaining Budget: {remaining_budget}\n")