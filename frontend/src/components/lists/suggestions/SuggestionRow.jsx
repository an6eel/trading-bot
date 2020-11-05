import { Button } from 'antd'
import React from 'react'
import styled from 'styled-components'
import * as moment from 'moment'

const Container = styled.div`
  display: flex;
  padding: 8px;
`

const Title = styled.div`
  flex: 1
 
`

export const SuggestionRow = ({ item }) => {
  const { date, action } = item
  return (
    <Container>
      <Title>
        {moment(new Date(date), 'DD-MM-YYYY').format('DD-MM-YYYY')}
      </Title>
      <Button type="primary" disabled style={{ backgroundColor: action === "SELL" ? 'green' : 'red', color: 'white'}}>
        {action}
      </Button>
    </Container>
  )
}