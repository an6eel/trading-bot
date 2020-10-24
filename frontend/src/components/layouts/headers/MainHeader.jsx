import React, { memo } from 'react'
import styled from 'styled-components'

const Container = styled.div`
  display: flex;
  align-items: center;
`

const Icon = styled.img.attrs({
  src: '/icon.svg'
})`
  height: 40px;
`

const Title = styled.div`
  color: white;
  font-size: 2em;
  margin-left: 0.5em;
`

export const MainHeader = memo((props) => {
  return (
    <Container>
      <Icon/>
      <Title>Trading Bot</Title>
    </Container>
  )
})