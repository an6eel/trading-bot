import {configureStore, combineReducers} from '@reduxjs/toolkit';
import {persistStore, persistReducer} from 'redux-persist'
import storage from 'redux-persist/lib/storage'
import stocksReducer from './features/stocksSlice';

const reducers = combineReducers({
    stocks: stocksReducer,
})

const persistConfig = {
    key: 'root',
    storage,
}

const persistedReducer = persistReducer(persistConfig, reducers)

export const store = configureStore({reducer: persistedReducer})
export const persistor = persistStore(store)