import _ from 'lodash'
import { mainAPIBase } from '../../environment'

const base = mainAPIBase
const addEndpoint = route => ({
  ...route,
  endpoint: base + route.path
})
const fillEndpoint = (endpoint, params) => _.template(endpoint)(params)

const stocksRoutes = {
  index: {
    type: 'STOCKS',
    path: '/stocks',
  },
  single: {
    type: 'SINGLE_STOCK',
    path: '/stocks/${ symbol }'
  },
  train: {
    type: 'TRAIN_STOCK',
    path: '/stocks/${ symbol }/train'
  },
  singlePredictions: {
    type: 'SINGLE_PREDICTIONS_STOCK',
    path: '/stocks/${ symbol }/predictions'
  }
}
const stocksEndpoints = _.mapValues(stocksRoutes, addEndpoint)

export const Stocks = {
  index: () => stocksEndpoints.index,
  // Response: { "iso_date": close_value }
  single: (symbol) => ({
    ...stocksEndpoints.single,
    endpoint: fillEndpoint(stocksEndpoints.single.endpoint, { symbol })
  }),
  // Response: { trained: boolean }
  train: (symbol, { lookBack = 5, forwardDays = 5 }) => ({
    ...stocksEndpoints.train,
    endpoint: fillEndpoint(stocksEndpoints.train.endpoint, { symbol }),
    params: {
      look_back: lookBack, forward_days: forwardDays
    }
  }),
  // Response Format: { "iso_date": close_value }
  singlePredictions: (symbol, { lookBack = 5, forwardDays = 5 }) => ({
    ...stocksEndpoints.single,
    endpoint: fillEndpoint(stocksEndpoints.singlePredictions.endpoint, { symbol }),
    params: {
      look_back: lookBack, forward_days: forwardDays
    }
  })
}

const botRoutes = {
  singleStockAction: {
    type: 'SINGLE_STOCK_ACTION',
    path: '/bot/${ symbol }/actions'
  },
}
const botEndpoints = _.mapValues(botRoutes, addEndpoint)

export const Bot = {
  // Response: { "iso_date": action (SELL | BUY) }
  singleStockAction: (symbol, { lookBack = 5, forwardDays = 5 }) => ({
    ...botEndpoints.singleStockAction,
    endpoint: fillEndpoint(botEndpoints.singleStockAction.endpoint, { symbol }),
    params: {
      look_back: lookBack, forward_days: forwardDays
    }
  })
}