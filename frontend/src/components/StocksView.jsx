import React, {useEffect, useState} from 'react';
import { useSelector, useDispatch } from 'react-redux';
import _ from 'lodash'
import {
    addStocks,
    selectStocks,
    selectStockById, getStocks,
} from '../features/stocksSlice';

export const StocksView = () => {
    const stocks = useSelector(selectStocks);
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(getStocks())
    }, [])

    const onAdd = () => {
        const stock = {
            id: 2,
            name: 'Stock 2',
            money: '$'
        }
        dispatch(addStocks([stock]))
    }

    return (
        <div>
            StocksView
            {_.map(stocks, s => s.name)}

            <button onClick={onAdd}>Add</button>
        </div>
    )
}