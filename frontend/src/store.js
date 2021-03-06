import { configureStore, combineReducers, getDefaultMiddleware } from '@reduxjs/toolkit'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import stocksReducer from './features/stocksSlice'

const reducers = combineReducers({
  stocks: stocksReducer,
})

const middleware = [...getDefaultMiddleware({
  serializableCheck: false,
})]

const persistConfig = {
  key: 'root',
  storage,
  whitelist: []
}

const persistedReducer = persistReducer(persistConfig, reducers)

export const store = configureStore({
  reducer: persistedReducer,
  middleware: middleware
})
export const persistor = persistStore(store)