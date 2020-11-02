import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import _ from 'lodash'
import axios from 'axios'
import { Stocks } from '../api/main'
import { mainAPIBase } from '../environment'

const instance = axios.create({
  baseURL: mainAPIBase,
})

export const getStocks = createAsyncThunk(
  Stocks.index.type,
  async (nothing, thunkAPI) => {
    return await instance.get(Stocks.index.create().path)
  }
)

export const getSingleStock = createAsyncThunk(
  Stocks.single.type,
  async (symbol, thunkAPI) => {
    return await instance.get(Stocks.single.create(symbol).path)
  }
)

export const stocksSlice = createSlice({
  name: 'stocks',
  initialState: {
    bySymbol: {},
    valuesBySymbol: {},
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
        result[symbol] = { symbol, name }
        return result
      }, {})
      _.forEach(bySymbol, (stock, symbol) => state.bySymbol[symbol] = stock)
      return state
    },
    [getSingleStock.fulfilled]: (state, action) => {
      const { arg: symbol } = action.meta
      const { data } = action.payload
      state.valuesBySymbol[symbol] = data
      return state
    }
  }
})

export const { addStocks } = stocksSlice.actions

export const selectStocks = (state) => _.values(state.stocks.bySymbol)
export const selectStockBySymbol = (state, symbol) => state.stocks.bySymbol[symbol]
export const selectStockValuesBySymbol = (state, symbol) => state.stocks.valuesBySymbol[symbol]

export default stocksSlice.reducer