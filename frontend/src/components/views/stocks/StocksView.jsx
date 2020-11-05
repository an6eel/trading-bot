import React, { useCallback, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import {
  selectStocks,
  getStocks,
} from '../../../features/stocksSlice'
import { MainLayout } from '../../layouts/MainLayout'
import { StocksList } from '../../lists/stocks/StocksList'
import styled from 'styled-components'

const ContentContainer = styled.div`
  margin: 0 auto !important;
  max-width: 900px;
`

export const StocksView = ({ history }) => {
  const stocks = useSelector(selectStocks)
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(getStocks())
  }, [])

  const openStock = useCallback((stock) => {
    const { symbol } = stock
    history.push(`/stockdetails/${symbol}`)
  }, [])

  const content = (
    <ContentContainer>
      <StocksList stocks={stocks} onOpenStock={openStock}/>
    </ContentContainer>
  )
  return (
    <MainLayout content={content}/>
  )
}