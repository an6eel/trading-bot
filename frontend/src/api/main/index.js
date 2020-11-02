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
  index:  {
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
  train: {
    ...stocksRoutes.singleTrain,
    create: (symbol, { lookBack = 5, forwardDays = 5 }) => ({
      path: fillTemplate(stocksRoutes.train.path, { symbol }),
      params: {
        look_back: lookBack, forward_days: forwardDays
      }
    })
  },
  // Response Format: { "iso_date": close_value }
  singlePredictions: {
    ...stocksRoutes.singlePredictions,
    create: (symbol, { lookBack = 5, forwardDays = 5 }) => ({
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
    path: '/api/bot/${ symbol }/actions'
  },
}

export const Bot = {
  // Response: { "iso_date": action (SELL | BUY) }
  singleStockAction: {
    ...botRoutes.singleStockAction,
    create: (symbol, { lookBack = 5, forwardDays = 5 }) => ({
      path: fillTemplate(botRoutes.singleStockAction.path, { symbol }),
      params: {
        look_back: lookBack, forward_days: forwardDays
      }
    })
  }
}