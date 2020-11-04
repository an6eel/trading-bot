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

  const onTrain = useCallback(() => {
    setTraining(true)
    dispatch(getSingleTrain(symbol))
    setTraining(false)
  }, [symbol])

  const onPredictions = useCallback(() => {
    setLoadingPredictions(true)
    dispatch(getSinglePredictions(symbol))
    setLoadingPredictions(false)
  }, [])

  if (!values) {
    return 'Loading...'
  }

  if (loadingPredictions) {
    return 'Loading predictions...'
  }

  const content = (
    <ContentContainer>
      <div>
        <StockChart symbol={symbol} values={values} predictions={trained ? predictions : null}/>
      </div>
      <Footer>
        <Button type="primary" onClick={onTrain} disabled={training}>
          Train
        </Button>
        {trained && !loadingPredictions &&
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