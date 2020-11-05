import _ from 'lodash'
import { Line } from 'react-chartjs-2'
import React, { useMemo } from 'react'

const mapStockValues = values => {
  const byDate = _.mapKeys(values, (v, key) => new Date(key))
  return _.map(byDate, (v, key) => ({ t: key, y: v }))
}

export const StockChart = ({ symbol, values, predictions }) => {
  const options = useMemo(() => {
    return {
      scales: {
        xAxes: [{
          type: 'time'
        }]
      }
    }
  }, [])

  const data = useMemo(() => {
    const data = {
      //labels: [minDate, maxDate],
      datasets: []
    }

    const { datasets } = data
    if (values) {
      datasets.push({
        label: `${symbol} Values`,
        data: mapStockValues(values),
        borderColor: 'black'
      })
    }

    if (predictions) {
      datasets.push({
        label: `${symbol} Predictions`,
        data: mapStockValues(predictions),
        borderColor: 'red'
      })
    }

    return data
  }, [values, predictions])

  return (
    <Line data={data} options={options}/>
  )
}