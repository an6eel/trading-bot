import {createSlice} from '@reduxjs/toolkit';
import _ from 'lodash'

export const stocksSlice = createSlice({
    name: 'stocks',
    initialState: {
        byId: {
            1: {
                id: 1,
                name: 'Stock 1',
                money: '$'
            }
        },
    },
    reducers: {
        addStocks: (state, action ) => {
            const stocks = action.payload
            stocks.forEach(s => state.byId[s.id] = s)
        },
    },
});

export const { addStocks } = stocksSlice.actions;

export const getStocks = () => dispatch => {
    setTimeout(() => {
        dispatch(addStocks([{
            id: 3,
            name: 'Stock 3',
            money: '$'
        }]));
    }, 1000);
};

export const selectStocks = (state) => _.values(state.stocks.byId);
export const selectStockById = (state, id) => state.stocks.byId[id];

export default stocksSlice.reducer;