import json
import matplotlib.pyplot as plt
import time

def plot_portfolio_value():
    try:
        with open('portfolio_values.json', 'r') as f:
            portfolio_values = json.load(f)
    except FileNotFoundError:
        print("Portfolio values file not found.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(portfolio_values, label="Portfolio Value")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Portfolio Value (USD)")
    plt.title("Portfolio Value Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    while True:
        plot_portfolio_value()
        time.sleep(60)  # update the plot every 60 seconds