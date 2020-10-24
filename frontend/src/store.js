import { configureStore, combineReducers, getDefaultMiddleware } from '@reduxjs/toolkit'
import { createMiddleware as createApiMiddeleware } from 'redux-api-middleware';
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import stocksReducer from './features/stocksSlice'

const reducers = combineReducers({
  stocks: stocksReducer,
})

const apiMiddleware = createApiMiddeleware()
const middleware = [...getDefaultMiddleware({
  serializableCheck: false,
}), apiMiddleware]

const persistConfig = {
  key: 'root',
  storage,
}

const persistedReducer = persistReducer(persistConfig, reducers)

export const store = configureStore({
  reducer: persistedReducer,
  middleware: middleware
})
export const persistor = persistStore(store)