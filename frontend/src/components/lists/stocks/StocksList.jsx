import React, { useCallback } from 'react'
import { List } from 'antd'
import { StockRow } from './StockRow'

export const StocksList = ({ stocks, onOpenStock, ...rest }) => {

  const renderStock = useCallback((stock) => {
    const onOpen = () => {
      onOpenStock(stock)
    }
    return (
      <StockRow stock={stock} onOpen={onOpen}/>
    )
  }, [onOpenStock])

  return (
    <List dataSource={stocks} renderItem={renderStock} {...rest}/>
  )
}