import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import _ from 'lodash'
import { getSingleStock, selectStockValuesBySymbol } from '../../../features/stocksSlice'

export const StockDetailsView = ({ match }) => {
  const dispatch = useDispatch()
  const { symbol } = match.params

  const values = useSelector(state => selectStockValuesBySymbol(state, symbol) || {})
  console.log(values)
  useEffect(() => {
    if (!symbol) {
      return
    }
    dispatch(getSingleStock(symbol))
  }, [symbol])

  return (
    <div>
      {_.values(values).map(v => <div key={2}>{v}</div>)}
    </div>
  )
}