import React, { useCallback, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
  getSinglePredictions,
  getSingleStock,
  getSingleTrain, selectStockPredictionsBySymbol,
  selectStockValuesBySymbol, selectTrainedBySymbol,
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
  
  margin: 0 auto !important;
  max-width: 900px;
`

const ChartContainer = styled.div`
  width: 100%;
  flex: 0 0 auto; 
`

const Footer = styled.div`
   display: flex;
   align-items: center;
   padding-top: 12px
`

const TrainButton = styled(Button).attrs({
  type: 'primary'
})`
  
`

const PredictionsButton = styled(Button).attrs({
  type: 'primary'
})`
  margin-left: 12px;
`

export const StockDetailsView = ({ match }) => {
  const dispatch = useDispatch()
  const { symbol } = match.params
  const values = useSelector(state => selectStockValuesBySymbol(state, symbol))
  const [training, setTraining] = useState(false)

  const trained = useSelector(state => selectTrainedBySymbol(state, symbol))
  const predictions = useSelector(state => selectStockPredictionsBySymbol(state, symbol))
  const [loadingPredictions, setLoadingPredictions] = useState(false)

  useEffect(() => {
    if (!symbol) {
      return
    }
    dispatch(getSingleStock(symbol))
  }, [symbol])

  const onTrain = useCallback(async () => {
    setTraining(true)
    await dispatch(getSingleTrain(symbol))
    setTraining(false)
  }, [symbol])

  const onPredictions = useCallback(async () => {
    setLoadingPredictions(true)
    await dispatch(getSinglePredictions(symbol))
    setLoadingPredictions(false)
  }, [])

  if (!values) {
    return 'Loading...'
  }

  const content = (
    <ContentContainer>
      <ChartContainer>
        <StockChart symbol={symbol} values={values} predictions={trained ? predictions : null}/>
      </ChartContainer>
      <Footer>
        <TrainButton onClick={onTrain} disabled={training}>
          Train
        </TrainButton>
        {trained && !loadingPredictions &&
        <PredictionsButton onClick={onPredictions}>
          Get Predictions
        </PredictionsButton>
        }
        {loadingPredictions && 'Loading predictions...'}
      </Footer>
    </ContentContainer>
  )
  return (
    <MainLayout content={content}/>
  )
}