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
    return await instance.get(Stocks.singlePredictions.create(symbol).path)
  }
)

export const stocksSlice = createSlice({
  name: 'stocks',
  initialState: {
    bySymbol: {},
    valuesBySymbol: {},
    predictionsBySymbol: {},
    training: false,
    trained: false
  },
  reducers: {},
  extraReducers: {
    [getStocks.pending]: (state, action) => {
      state.training = false
      state.trained = false
      return state
    },
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
      state.training = true
      return state
    },
    [getSingleTrain.rejected]: (state, action) => {
      console.log(action)
      state.training = false
      return state
    },
    [getSingleTrain.fulfilled]: (state, action) => {
      const { data } = action.payload
      state.training = false
      state.trained = data.trained
      return state
    },
    [getSinglePredictions.fulfilled]: (state, action) => {
      const { arg: symbol } = action.meta
      const { data } = action.payload
      state.predictionsBySymbol[symbol] = data
      return state
    }
  }
})

export const { addAction } = stocksSlice.actions

export const selectStocks = (state) => _.values(state.stocks.bySymbol)
export const selectStockBySymbol = (state, symbol) => state.stocks.bySymbol[symbol]
export const selectStockValuesBySymbol = (state, symbol) => state.stocks.valuesBySymbol[symbol]
export const selectStockPredictionsBySymbol = (state, symbol) => state.stocks.predictionsBySymbol[symbol]
export const selectTraining = (state) => state.training
export const selectTrained = (state) => state.trained

export default stocksSlice.reducer