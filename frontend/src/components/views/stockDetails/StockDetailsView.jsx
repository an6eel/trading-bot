import React, { useCallback, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
  getSinglePredictions,
  getSingleStock,
  getSingleTrain, selectStockPredictionsBySymbol,
  selectStockValuesBySymbol,
  selectTrained,
  selectTraining
} from '../../../features/stocksSlice'
import { MainLayout } from '../../layouts/MainLayout'
import styled from 'styled-components'
import { Button } from 'antd'
import { StockChart } from '../../charts/StockChart'

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
  const training = useSelector(selectTraining)
  const trained = useSelector(selectTrained)

  const predictions = useSelector(state => selectStockPredictionsBySymbol(state, symbol))
  const loadingPredictions = trained && !predictions

  useEffect(() => {
    if (!symbol) {
      return
    }
    dispatch(getSingleStock(symbol))
  }, [symbol])

  const onTrain = useCallback(() => {
    console.log('onTrain')
    dispatch(getSingleTrain(symbol))
  }, [symbol])

  const onPredictions = useCallback(() => {
    dispatch(getSinglePredictions(symbol))
  }, [])

  if (!values) {
    return 'Loading...'
  }

  const content = (
    <ContentContainer>
      <div>
        <StockChart symbol={symbol} values={values} predictions={predictions}/>
      </div>
      <Footer>
        <Button type="primary" onClick={onTrain} disabled={training || trained || loadingPredictions}>
          Train
        </Button>
        {trained &&
        <Button type="primary" onClick={onPredictions}>
          Get Predictions
        </Button>
        }
      </Footer>
    </ContentContainer>
  )
  return (
    <MainLayout content={content}/>
  )
}