
from fbprophet import Prophet
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from datetime import timedelta
import pandas as pd


def get_predictions_prophet(df, days):
    df['ds'] = df.index
    df['y'] = df['Close']
    model = Prophet(daily_seasonality=True)
    model.fit(df)

    days_df = model.make_future_dataframe(periods=days)
    forecast = model.predict(days_df)

    response = []

    date = pd.to_datetime(df.index[-1]) + timedelta(days=1)

    predictions = forecast['yhat']

    for forecast in predictions[-days:].values:
        response.append(
            {
                'date': date.strftime("%Y-%m-%d"),
                'value': float(forecast)
            }
        )
        date += timedelta(days=1)

    return response


def evaluate_model(data, days):
    train = data.drop(data.index[-90:])
    model = Prophet(daily_seasonality=True)
    # fit the model
    model.fit(train)
    days_df = model.make_future_dataframe(periods=90)
    forecast = model.predict(days_df)
    predicted_dates = data['ds'][-90:].values
    predicted_forecast = forecast[forecast['ds'].isin(predicted_dates)]
    y_true = data['y'][-predicted_forecast.shape[0]:].values
    print(y_true.shape)
    y_pred = predicted_forecast['yhat'].values
    print(y_pred.shape)
    mae = mean_absolute_error(y_true, y_pred)
    print('MAE: %.3f' % mae)
    # plot expected vs actual
    plt.plot(y_true, label='Actual')
    plt.plot(y_pred, label='Predicted')
    plt.legend()
    plt.show()
