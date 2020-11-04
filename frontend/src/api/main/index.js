import _ from 'lodash'

const fillTemplate = (string, params) => _.template(string)(params)

const stocksRoutes = {
  index: {
    type: 'stocks/index',
    path: '/api/stocks',
  },
  single: {
    type: 'stocks/single',
    path: '/api/stocks/${ symbol }'
  },
  singleTrain: {
    type: 'stocks/single_train',
    path: '/api/stocks/${ symbol }/train'
  },
  singlePredictions: {
    type: 'stocks/single_predictions',
    path: '/api/stocks/${ symbol }/predictions'
  }
}

export const Stocks = {
  index: {
    ...stocksRoutes.index,
    create: () => ({
      path: stocksRoutes.index.path
    })
  },
  // Response: { "iso_date": close_value }
  single: {
    ...stocksRoutes.single,
    create: (symbol) => ({
      path: fillTemplate(stocksRoutes.single.path, { symbol })
    })
  },
  // Response: { trained: boolean }
  singleTrain: {
    ...stocksRoutes.singleTrain,
    create: (symbol, lookBack = 90, forwardDays = 10) => ({
      path: fillTemplate(stocksRoutes.singleTrain.path, { symbol }),
      params: {
        look_back: lookBack, forward_days: forwardDays
      }
    })
  },
  // Response Format: { "iso_date": close_value }
  singlePredictions: {
    ...stocksRoutes.singlePredictions,
    create: (symbol, lookBack = 90, forwardDays = 10) => ({
      path: fillTemplate(stocksRoutes.singlePredictions.path, { symbol }),
      params: {
        look_back: lookBack, forward_days: forwardDays
      }
    })
  }
}

const botRoutes = {
  singleStockAction: {
    type: 'bot/single_stock_actions',
    path: '/api/agent/${ symbol }/actions'
  },
}

export const Bot = {
  // Response: { "iso_date": action (SELL | BUY) }
  singleStockAction: {
    ...botRoutes.singleStockAction,
    create: (symbol, lookBack = 90, forwardDays = 10) => ({
      path: fillTemplate(botRoutes.singleStockAction.path, { symbol }),
      params: {
        look_back: lookBack, forward_days: forwardDays
      }
    })
  }
}