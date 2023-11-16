import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from arch import arch_model
from scipy.stats import norm
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Function to download data from Yahoo Finance
def download_yahoo_finance_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Function to calculate Black-Scholes option price
def black_scholes(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# Function to perform Monte Carlo simulation
def monte_carlo_simulation(S, r, sigma, T, n_simulations):
    dt = T / n_simulations
    price_paths = np.zeros((n_simulations, n_simulations+1))
    price_paths[:, 0] = S

    for i in range(1, n_simulations+1):
        Z = np.random.normal(0, 1, n_simulations)
        price_paths[:, i] = price_paths[:, i-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

    return price_paths

# Stock symbol and date range
symbol = 'AAPL'
start_date = '2020-01-01'
end_date = '2023-01-01'

# Download data from Yahoo Finance
stock_data = download_yahoo_finance_data(symbol, start_date, end_date)

# Extract 'Adj Close' prices for time series analysis
time_series = stock_data['Adj Close']

# Daily Returns
daily_returns = time_series.pct_change().dropna()

# 1) Descriptive Statistics
print("1) Descriptive Statistics (based on daily returns):")
print("   Mean:", np.mean(daily_returns))
print("   Median:", np.median(daily_returns))
print("   Standard Deviation:", np.std(daily_returns))
print("   Skewness:", daily_returns.skew())
print()

# 2) Time Series Analysis
print("2) Time Series Analysis:")
# 2.1) Plot Time Series
plt.figure(figsize=(12, 6))
plt.plot(time_series, label='AAPL Adj Close Prices')
plt.title('AAPL Adj Close Prices (2020-2023)')
plt.xlabel('Date')
plt.ylabel('Adj Close Price')
plt.legend()
plt.show()
# 2.2) AutoCorrelation Function and Partial AutoCorrelation Function
# Create subplots
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
# Plot AutoCorrelation Function (ACF)
plot_acf(time_series, lags=20, ax=ax[0])
ax[0].set_title('Autocorrelation Function (ACF)')
# Plot Partial AutoCorrelation Function (PACF)
plot_pacf(time_series, lags=20, ax=ax[1])
ax[1].set_title('Partial Autocorrelation Function (PACF)')
# Adjust layout for better spacing
plt.tight_layout()
# Show the merged plot
plt.show()
# 2.3) Exponential Moving Average
# Calculate 20-day exponential moving average
ema = time_series.ewm(span=20, adjust=False).mean()
# Plot the exponential moving average
plt.figure(figsize=(12, 6))
plt.plot(time_series, label='AAPL Adj Close Prices')
plt.plot(ema, label='20-day EMA', linestyle='--', color='red')
plt.title('AAPL Adj Close Prices with 20-day EMA (2020-2023)')
plt.xlabel('Date')
plt.ylabel('Adj Close Price')
plt.legend()
plt.show()
# 2.4) ARIMA Model
# Check for stationarity using Augmented Dickey-Fuller test
result_adf = sm.tsa.adfuller(daily_returns)
print("ARIMA Model:")
print("   ADF Statistic:", result_adf[0])
print("   p-value:", result_adf[1])
# Differencing to achieve stationarity
diff_returns = daily_returns.diff().dropna()
# Check for stationarity using Augmented Dickey-Fuller test on the differenced time series
result_adf_diff = sm.tsa.adfuller(diff_returns)
print("   ADF Statistic (Differenced):", result_adf_diff[0])
print("   p-value (Differenced):", result_adf_diff[1])
# Fit ARIMA model on the original time series
order_original = (1, 1, 1)  # Example order, replace with values based on ACF and PACF analysis
model_arima_original = sm.tsa.ARIMA(time_series, order=order_original)
results_arima_original = model_arima_original.fit()
# Print ARIMA model summary for the original time series
print()
print('ARIMA original result summary:')
print(results_arima_original.summary())
print()
# Fit ARIMA model on the differenced time series
order_diff = (1, 0, 1)  # Example order, replace with values based on ACF and PACF analysis
model_arima_diff = sm.tsa.ARIMA(diff_returns, order=order_diff)
results_arima_diff = model_arima_diff.fit()
# Print ARIMA model summary for the differenced time series
print()
print('ARIMA differenced result summary:')
print(results_arima_diff.summary())

# 3) Volatility Model - GARCH
# 3.1) Fit GARCH(1, 1) model
# Rescale the returns
returns_rescaled = diff_returns * 10
model_garch = arch_model(returns_rescaled, vol='Garch', p=1, q=1)
results_garch = model_garch.fit()
# 3.2) Display GARCH model summary
print()
print("3) GARCH Volatility Model:")
print(results_garch.summary())
print()
# 3.3) Plot GARCH volatility
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(results_garch.conditional_volatility, label='GARCH Volatility')
ax.set_title('GARCH Volatility Model')
ax.set_xlabel('Date')
ax.set_ylabel('Volatility')
plt.legend()
plt.show()

# 4) Regression Analysis
# Prepare data for regression
X = sm.add_constant(np.arange(len(time_series)))
y = time_series.values
# Fit linear regression model
results_regression = sm.OLS(y, X).fit()
# Display regression results
print("4) Regression Analysis:")
print(results_regression.summary())
print()
# Plot the regression line
plt.figure(figsize=(12, 6))
plt.scatter(np.arange(len(time_series)), time_series, label='AAPL Adj Close Prices')
plt.plot(np.arange(len(time_series)), results_regression.predict(X), label='Regression Line', color='red')
plt.title('Regression Analysis of AAPL Adj Close Prices (2020-2023)')
plt.xlabel('Date')
plt.ylabel('Adj Close Price')
plt.legend()
plt.show()

# 5) Correlation Analysis
# Calculate correlation matrix
correlation_matrix = stock_data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].corr()
# Display correlation matrix
print("5) Correlation Analysis:")
print(correlation_matrix)
print()

# 6) Machine Learning Models - Linear Regression and SVM
# Prepare data for machine learning
X_ml = np.arange(len(time_series)).reshape(-1, 1)
y_ml = time_series.values
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_ml, y_ml, test_size=0.2, random_state=42)
# 6.1) Linear Regression
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
y_pred_lr = model_lr.predict(X_test)
# 6.2) Support Vector Machine (SVM)
model_svm = SVR()
model_svm.fit(X_train, y_train)
y_pred_svm = model_svm.predict(X_test)
# Evaluate the models
mse_lr = mean_squared_error(y_test, y_pred_lr)
mse_svm = mean_squared_error(y_test, y_pred_svm)
mae_lr = mean_absolute_error(y_test, y_pred_lr)
mae_svm = mean_absolute_error(y_test, y_pred_svm)
print("6) Machine Learning Models:")
print("   Linear Regression Mean Squared Error:", mse_lr)
print("   SVM Mean Squared Error:", mse_svm)
print("   Linear Regression Mean Absolute Error:", mae_lr)
print("   SVM Mean Absolute Error:", mae_svm)
print()

# 7) Black-Scholes Model
# Parameters for Black-Scholes
spot_price = time_series.iloc[-1]  # current stock price
strike_price = spot_price * 1.1  # arbitrary strike price
time_to_maturity = 1  # arbitrary time to maturity in years
risk_free_rate = 0.01  # arbitrary risk-free rate
volatility_bs = results_garch.conditional_volatility[-1]  # using GARCH volatility as a proxy for future volatility
# Calculate Black-Scholes option price
call_price_bs = black_scholes(spot_price, strike_price, time_to_maturity, risk_free_rate, volatility_bs)
print("7) Black-Scholes Model:")
print(f'Spot price is {spot_price}.')
print(f'Strike price is {strike_price}.')
print(f'TTM is {time_to_maturity}.')
print(f'Risk-free rate is {risk_free_rate}.')
print(f'Volatility is {volatility_bs}.')
print(f"   Black-Scholes Call Option Price: {call_price_bs:.2f}")
print()

# 8) Monte Carlo Simulation
# Parameters for Monte Carlo simulation
n_simulations = 1000
# Perform Monte Carlo simulation
simulated_prices = monte_carlo_simulation(spot_price, risk_free_rate, volatility_bs, time_to_maturity, n_simulations)
# Plot Monte Carlo simulation results
plt.figure(figsize=(12, 6))
plt.plot(simulated_prices.T, color='gray', alpha=0.1)
plt.title('Monte Carlo Simulation of AAPL Stock Prices')
plt.xlabel('Time Steps')
plt.ylabel('Stock Price')
plt.show()