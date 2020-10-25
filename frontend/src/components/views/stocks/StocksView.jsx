import React, { useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import _ from 'lodash'
import {
  addStocks,
  selectStocks,
  getStocks,
} from '../../../features/stocksSlice'
import { MainLayout } from '../../layouts/MainLayout'

export const StocksView = () => {
  const stocks = useSelector(selectStocks)
  const dispatch = useDispatch()

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
    <MainLayout>
      StocksView
      {_.map(stocks, s => s.name)}
      <button onClick={onAdd}>Add</button>
    </MainLayout>
  )
}