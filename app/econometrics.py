from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt
import statsmodels.api as sm
from pmdarima import auto_arima
import numpy as np


def run_adf(series):
    result = adfuller(series)
    print("ADF Test:", result)
    return result


def run_regression(df):
    df = df.dropna()

    X = sm.add_constant(df['price'])
    y = df['severity']

    model = sm.OLS(y, X).fit()
    print(model.summary())
    return model


def run_granger(df):
    """Run Granger causality test and extract p-value"""
    try:
        result = grangercausalitytests(
            df[['severity', 'price']], maxlag=2, verbose=False)
        # Extract p-value from maxlag result (maxlag=2)
        if result:
            p_value = result[2][0][1][0]  # Get p-value from maxlag=2
            return p_value
    except Exception as e:
        print(f"Granger test error: {e}")
        return None


def run_arima(series):
    import numpy as np
    print(f"ARIMA input series length: {len(series)}")

    # For very small datasets, use exponential smoothing with trend
    if len(series) < 20:
        print("WARNING: Series too small for reliable ARIMA, using Holt's linear trend")
        try:
            # Fit Holt's linear trend model
            model = Holt(series)
            model_fit = model.fit()
            forecast = model_fit.forecast(5)
            forecast_values = [float(val) for val in forecast]
            print("Holt's linear trend forecast values:", forecast_values)
            return np.array(forecast_values)
        except Exception as e:
            print(f"Holt's method failed: {e}, using linear regression trend")
            # Fallback to simple linear trend
            x = np.arange(len(series))
            slope = np.polyfit(x, series, 1)[0]
            last_value = series.iloc[-1] if hasattr(
                series, 'iloc') else series[-1]
            forecast = [last_value + slope * (i + 1) for i in range(5)]
            forecast_values = [float(val) for val in forecast]
            print("Linear regression trend forecast values:", forecast_values)
            return np.array(forecast_values)

    try:
        # Use auto_arima to find the best ARIMA model
        print("Finding optimal ARIMA model...")
        model = auto_arima(series,
                           start_p=0, start_q=0,
                           max_p=5, max_q=5,
                           max_d=2,
                           seasonal=False,
                           trace=False,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)

        print(f"Selected ARIMA order: {model.order}")

        # Fit the model and forecast
        forecast = model.predict(n_periods=5)
        forecast_values = [float(val) for val in forecast]
        print("Forecast values:", forecast_values)
        return np.array(forecast_values)

    except Exception as e:
        print(f"Auto ARIMA failed: {e}, falling back to manual ARIMA")
        try:
            # Fallback to manual ARIMA with different orders
            best_aic = float('inf')
            best_model = None
            best_order = None

            for p in range(0, 3):
                for d in range(0, 2):
                    for q in range(0, 3):
                        try:
                            model = ARIMA(series, order=(p, d, q))
                            model_fit = model.fit()
                            if model_fit.aic < best_aic:
                                best_aic = model_fit.aic
                                best_model = model_fit
                                best_order = (p, d, q)
                        except:
                            continue

            if best_model is not None:
                print(
                    f"Best manual ARIMA order: {best_order} (AIC: {best_aic})")
                forecast = best_model.forecast(steps=5)
                forecast_values = [float(val) for val in forecast]
                print("Forecast values:", forecast_values)
                return np.array(forecast_values)
            else:
                raise Exception("No suitable ARIMA model found")

        except Exception as e2:
            print(
                f"All ARIMA attempts failed: {e2}, using Holt's linear trend")
            try:
                model = Holt(series)
                model_fit = model.fit()
                forecast = model_fit.forecast(5)
                forecast_values = [float(val) for val in forecast]
                return np.array(forecast_values)
            except:
                # Final fallback to linear trend
                x = np.arange(len(series))
                slope = np.polyfit(x, series, 1)[0]
                last_value = series.iloc[-1] if hasattr(
                    series, 'iloc') else series[-1]
                forecast = [last_value + slope * (i + 1) for i in range(5)]
                forecast_values = [float(val) for val in forecast]
                return np.array(forecast_values)
