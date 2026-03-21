import matplotlib.pyplot as plt
import numpy as np

# Data Simulation for 2026 Beef Cow-Calf Operations
herd_sizes = np.array([50, 150, 300, 500, 1000])
acres = herd_sizes * 2.5 # Assuming 2.5 acres per cow-calf pair

# Cash Net Income (Revenue minus only direct bills like feed/vet)
cash_net_per_acre = np.array([280, 310, 356, 380, 410])

# Hidden Costs (Opportunity cost of land, unpaid labor, depreciation)
# These drop per acre as you scale because you spread them over more land/cows
hidden_costs_per_acre = np.array([320, 280, 240, 210, 190])

# Clean Income (The actual economic profit)
clean_income_per_acre = cash_net_per_acre - hidden_costs_per_acre

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(herd_sizes, cash_net_per_acre, label='Cash Net Income (Before Hidden Costs)', marker='o', color='blue', linestyle='--')
plt.plot(herd_sizes, clean_income_per_acre, label='True "Clean" Income (Economic Profit)', marker='s', color='green', linewidth=3)
plt.axhline(0, color='red', linewidth=1, label='Break-Even Point')

plt.title('2026 Ranch Profitability: Scaling to "Clean" Income', fontsize=14)
plt.xlabel('Herd Size (Number of Cows)', fontsize=12)
plt.ylabel('Income Per Acre ($USD)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

# Highlight the "Wealth Gap"
plt.fill_between(herd_sizes, cash_net_per_acre, clean_income_per_acre, color='gray', alpha=0.1, label='The Wealth Gap (Hidden Costs)')

plt.show()