import math

def choose(n, r):
    assert n >= 0
    assert 0 <= r <= n
    c = 1
    for num, denom in zip(range(n, n-r, -1), range(1, r+1, 1)):
        c = (c * num) // denom
    return c

def probability_of_failure_in_year(num_data_shards, num_parity_shards, afr, rebuild_time):
    yr = 365.25 * 24.0  # hours per year
    p_failure = 0
    for r in range(num_parity_shards + 1, num_data_shards + num_parity_shards + 1):
        pr_year = choose(num_data_shards + num_parity_shards, r) * (afr**r) * ((1-afr)**(num_data_shards + num_parity_shards - r))
        pr_rebuild = pr_year * (rebuild_time/yr)**(r-1)
        p_failure += pr_rebuild

    return p_failure

def calculate_durability(num_data_shards, num_parity_shards, afr, rebuild_time):
    probability_of_loss = probability_of_failure_in_year(num_data_shards, num_parity_shards, afr, rebuild_time)
    durability = 1 - probability_of_loss
    return durability

# Prompt user for input
num_data_shards = int(input("Enter number of data shards: "))
num_parity_shards = int(input("Enter number of parity shards: "))
afr = float(input("Enter annual failure rate (in %): ")) / 100  # Convert to fraction
rebuild_time = float(input("Enter rebuild time (in hours): "))

# Calculate and print durability
durability = calculate_durability(num_data_shards, num_parity_shards, afr, rebuild_time)
print(f"The calculated durability is: {durability*100:.15f}%")

# Calculate and print number of nines
num_failures_per_year = 1 - durability
if num_failures_per_year == 0:
    num_nines = "Infinite"
else:
    num_nines = abs(math.log10(num_failures_per_year))
print(f"The number of nines in the durability is: {num_nines}")
