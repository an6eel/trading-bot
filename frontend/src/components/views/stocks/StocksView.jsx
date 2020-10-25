import React, { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import _ from 'lodash'
import {
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

  const content = _.map(stocks, s => s.name)

  return (
    <MainLayout content={content}>
    </MainLayout>
  )
}