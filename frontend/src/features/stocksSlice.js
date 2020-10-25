import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import _ from 'lodash'
import axios from 'axios'
import { Stocks } from '../api/main'

const { type, endpoint } = Stocks.index()
export const getStocks = createAsyncThunk(
  type,
  async (userId, thunkAPI) => {
    console.log('sssss')
    const response = await axios.get(endpoint)
    return response
  }
)

export const stocksSlice = createSlice({
  name: 'stocks',
  initialState: {
    bySymbol: {},
    valuesBySymbol: {
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
    predictionsBySymbol: {}
  },
  reducers: {
    addStocks: (state, action) => {
      const stocks = action.payload
      stocks.forEach(s => state.bySymbol[s.id] = s)
    },
  },
  extraReducers: {
    [getStocks.fulfilled]: (state, action) => {
      const { data } = action.payload
      const bySymbol = _.reduce(data, function(result, symbol, name) {
        result[symbol] = { name }
        return result
      }, {})
      _.forEach(bySymbol, (stock, symbol) => state.bySymbol[symbol] = stock )
      return state
    }
  }
})

export const { addStocks } = stocksSlice.actions

export const selectStocks = (state) => _.values(state.stocks.bySymbol)
export const selectStockById = (state, symbol) => state.stocks.bySymbol[symbol]

export default stocksSlice.reducer