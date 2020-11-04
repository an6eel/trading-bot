import React, { memo } from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom';

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
  const history = useHistory()
  const goHome = () => history.push('/')
  return (
    <Container>
      <Icon onClick={goHome} style={{ cursor: 'pointer'}}/>
      <Title onClick={goHome} style={{ cursor: 'pointer'}}>Trading Bot</Title>
    </Container>
  )
})