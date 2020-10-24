/*
Basic:
  - index  <- GET all stocks
  - single <- GET single stocks by id
  - create <- POST an stocks
  - update <- PUT data to an stocks
  - remove <- DELETE an stocks

Specific:
  - singleBySomething
  - removeAll
 */

export const Stocks = {
  index: () => [`/stocks`],
  // Response: { "iso_date": close_value }
  single: (symbol) => [`/stocks/${symbol}`],
  // Response: { trained: boolean }
  train: (symbol, { lookBack = 5, forwardDays = 5 }) => [`/stocks/${symbol}/train`, {
    look_back: lookBack, forward_days: forwardDays
  }],
  // Response Format: { "iso_date": close_value }
  predictions: (symbol, { lookBack = 5, forwardDays = 5 }) => [`/stocks/${symbol}/predictions`, {
    look_back: lookBack, forward_days: forwardDays
  }],
}

export const Bot = {
  // Response: { "iso_date": action (SELL | BUY) }
  singleStockAction: (symbol, { lookBack = 5, forwardDays = 5 }) => [`/bot/${symbol}/actions`, {
    look_back: lookBack, forward_days: forwardDays
  }],
}