import { Button } from 'antd'
import React from 'react'
import styled from 'styled-components'

const Container = styled.div`
  display: flex;
  padding: 8px;
`

const Title = styled.div`
  flex: 1
 
`

export const StockRow = ({ stock, onOpen }) => {
  const { name } = stock
  return (
    <Container>
      <Title>
        {name}
      </Title>
      <Button type="primary" onClick={onOpen}>
        Open
      </Button>
    </Container>
  )
}