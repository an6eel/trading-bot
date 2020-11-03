import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import _ from 'lodash'
import { getSingleStock, selectStockValuesBySymbol } from '../../../features/stocksSlice'
import { MainLayout } from '../../layouts/MainLayout'
import { Line } from 'react-chartjs-2'
import styled from 'styled-components'
import { Button } from 'antd'

const ContentContainer = styled.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 24px;
`

const Footer = styled.div`
   height: 60px;
   display: flex;
   align-items: center;
`

export const StockDetailsView = ({ match }) => {
  const dispatch = useDispatch()
  const { symbol } = match.params

  const values = useSelector(state => selectStockValuesBySymbol(state, symbol))
  useEffect(() => {
    if (!symbol) {
      return
    }
    dispatch(getSingleStock(symbol))
  }, [symbol])

  if (!values) {
    return 'Loading...'
  }

  const byDate = _.mapKeys(values,(v, key) => new Date(key))
  const stockData = _.map(byDate, (v, key) => ({ t: key, y: v }))
  const dates = _.keys(byDate)
  const minDate = _.min(dates)
  const maxDate = _.max(dates)

  const options = {
    scales: {
      xAxes: [{
        type: 'time'
      }]
    }
  }

  const data = {
    labels: [minDate, maxDate],
    datasets: [{
      label: symbol,
      data: stockData
    }]
  }

  const content = (
    <ContentContainer>
      <div>
        <Line data={data} options={options}/>
      </div>
      <Footer>
        <Button type="primary">
          Train
        </Button>
      </Footer>
    </ContentContainer>
  )
  return (
    <MainLayout content={content}/>
  )
}