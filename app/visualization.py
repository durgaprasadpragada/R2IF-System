import matplotlib.pyplot as plt


def plot_r2if(r2if):
    plt.figure()
    plt.plot(r2if['date'], r2if['severity'])
    plt.title("R2IF Over Time")
    plt.show()


def plot_r2if_vs_price(df):
    plt.figure()
    plt.scatter(df['price'], df['severity'])
    plt.title("R2IF vs Price")
    plt.show()


def plot_forecast(actual, forecast):
    plt.figure()
    plt.plot(actual)
    plt.plot(range(len(actual), len(actual)+len(forecast)), forecast)
    plt.title("Forecast vs Actual")
    plt.show()
