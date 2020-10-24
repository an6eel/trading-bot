import { createSlice } from '@reduxjs/toolkit'
import _ from 'lodash'
import { createAction } from 'redux-api-middleware'
import { Stocks } from '../api/main'
import { createActionTypesOfMainAPI } from '../helpers/reducerHelpers'

export const stocksSlice = createSlice({
  name: 'stocks',
  initialState: {
    byId: {
      1: {
        id: 1,
        symbol: 'APPL',
        name: 'Apple',
        money: '$'
      }
    },
    valuesById: {
      1: {
        '2000-01-03T00:00:00': 0.99,
        '2000-01-04T00:00:00': 0.91,
        '2000-01-05T00:00:00': 0.92,
        '2020-10-19T00:00:00': 115.98,
        '2020-10-20T00:00:00': 117.51,
        '2020-10-21T00:00:00': 116.87,
        '2020-10-22T00:00:00': 115.75,
        '2020-10-23T00:00:00': 115.04
      }
    },
    predictionsById: {}

  },
  reducers: {
    addStocks: (state, action) => {
      const stocks = action.payload
      stocks.forEach(s => state.byId[s.id] = s)
    },
  },
})

export const { addStocks } = stocksSlice.actions

export const addStockAsync = () => dispatch => {
  setTimeout(() => {
    dispatch(addStocks([{
      id: 3,
      name: 'Stock 3',
      money: '$'
    }]))
  }, 1000)
}

export const getStocks = () => {
  const { type, endpoint } = Stocks.index()
  return createAction({
    endpoint,
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    types: createActionTypesOfMainAPI(type)
  })
}

export const selectStocks = (state) => _.values(state.stocks.byId)
export const selectStockById = (state, id) => state.stocks.byId[id]

export default stocksSlice.reducer