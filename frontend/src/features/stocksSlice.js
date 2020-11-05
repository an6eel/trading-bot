import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import _ from 'lodash'
import axios from 'axios'
import { Stocks, Bot } from '../api/main'
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

export const getSingleTrain = createAsyncThunk(
  Stocks.singleTrain.type,
  async (symbol, thunkAPI) => {
    const { path, params } = Stocks.singleTrain.create(symbol)
    return await instance.post(path, null, { params })
  }
)

export const getSinglePredictions = createAsyncThunk(
  Stocks.singlePredictions.type,
  async (symbol, thunkAPI) => {
    const { path, params } = Stocks.singlePredictions.create(symbol)
    return await instance.get(path, { params })
  }
)

export const getSingleSuggestions = createAsyncThunk(
  Bot.singleStockAction.type,
  async (symbol, thunkAPI) => {
    const { path, params } = Bot.singleStockAction.create(symbol)//Stocks.singlePredictions.create(symbol)
    return await instance.get(path, { params })
  }
)

export const stocksSlice = createSlice({
  name: 'stocks',
  initialState: {
    bySymbol: {},
    valuesBySymbol: {},
    predictionsBySymbol: {},
    trainedBySymbol: {},
    suggestionsBySymbol: {}
  },
  reducers: {},
  extraReducers: {
    [getStocks.fulfilled]: (state, action) => {
      const { data } = action.payload
      const bySymbol = _.reduce(data, (result, symbol, name) => {
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
    },
    [getSingleTrain.pending]: (state, action) => {
      const { arg: symbol } = action.meta
      const obj = state.trainedBySymbol[symbol] || {}
      obj.trained = false
      state.trainedBySymbol[symbol] = obj
      return state
    },
    [getSingleTrain.fulfilled]: (state, action) => {
      const { arg: symbol } = action.meta
      const { data } = action.payload
      const obj = state.trainedBySymbol[symbol] || {}
      obj.trained = data.trained
      state.trainedBySymbol[symbol] = obj
      return state
    },
    [getSingleTrain.rejected]: (state, action) => {
      console.log(action)
      return state
    },
    [getSinglePredictions.fulfilled]: (state, action) => {
      const { arg: symbol } = action.meta
      const { data } = action.payload
      state.predictionsBySymbol[symbol] = data
      console.log(state)
      return state
    },
    [getSinglePredictions.rejected]: (state, action) => {
      console.log(action)
      return state
    },
    [getSingleSuggestions.fulfilled]: (state, action) => {
      const { arg: symbol } = action.meta
      const { data } = action.payload
      state.suggestionsBySymbol[symbol] = Object.entries(data).map(([date, action]) => ({ date, action}))
      return state
    },
    [getSingleSuggestions.rejected]: (state, action) => {
      console.log(action)
      return state
    },
  }
})


export const selectStocks = (state) => _.values(state.stocks.bySymbol)
export const selectStockBySymbol = (state, symbol) => state.stocks.bySymbol[symbol]
export const selectStockValuesBySymbol = (state, symbol) => state.stocks.valuesBySymbol[symbol]
export const selectStockPredictionsBySymbol = (state, symbol) => state.stocks.predictionsBySymbol[symbol]
export const selectStockSuggestionsBySymbol = (state, symbol) => state.stocks.suggestionsBySymbol[symbol]
export const selectTrainedBySymbol = (state, symbol) => state.stocks.trainedBySymbol[symbol]

export default stocksSlice.reducer