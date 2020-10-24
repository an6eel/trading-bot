
### /stocks/{symbol} get response

Format:

{
    "iso_date": close_value
}

Example:

{
    "2000-01-03T00:00:00": 0.9994419813156128,
    "2000-01-04T00:00:00": 0.9151785969734192,
    "2000-01-05T00:00:00": 0.9285714030265808,
    ...
    "2020-10-19T00:00:00": 115.9800033569336,
    "2020-10-20T00:00:00": 117.51000213623047,
    "2020-10-21T00:00:00": 116.87000274658203,
    "2020-10-22T00:00:00": 115.75,
    "2020-10-23T00:00:00": 115.04000091552734
}

### /stocks/{symbol}/train post response

Params:

- look_back: int -> Número de dias que se mira hacia atrás
- forward_days: int -> Numero de dias que se intenta predecir

Response:

{
    trained: boolean
}

### /stocks/{symbol}/predictions

Params:

- look_back: int -> Número de dias que se mira hacia atrás
- forward_days: int -> Numero de dias que se intenta predecir

Format:

{
    "iso_date": close_value
}

Example:

{
    "2020-10-24T00:00:00": 110.40219116210938,
    "2020-10-25T00:00:00": 112.23725128173828,
    "2020-10-26T00:00:00": 113.28914642333984,
    "2020-10-27T00:00:00": 110.17041778564453,
    "2020-10-28T00:00:00": 111.63607025146484,
    ...
    "2020-11-08T00:00:00": 114.66622161865234,
    "2020-11-09T00:00:00": 113.96394348144531,
    "2020-11-10T00:00:00": 116.13938903808594,
    "2020-11-11T00:00:00": 114.99710083007812,
    "2020-11-12T00:00:00": 113.87833404541016
}

### /agent/{symbol}/actions get response

Params:

- look_back: int -> Número de dias que se mira hacia atrás
- forward_days: int -> Numero de dias que se intenta predecir

Format:

{
    "iso_date": action (SELL | BUY)
}


Example:

{
    "2020-10-26T00:00:00": SELL,
    "2020-10-27T00:00:00": BUY,
    "2020-10-30T00:00:00": SELL,
    "2020-11-01T00:00:00": BUY,
    "2020-11-05T00:00:00": SELL,
    "2020-11-08T00:00:00": BUY,
    "2020-11-09T00:00:00": SELL,
    "2020-11-10T00:00:00": BUY,
}



