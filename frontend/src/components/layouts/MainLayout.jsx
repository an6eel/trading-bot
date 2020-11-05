import React, { memo } from 'react'
import { Layout } from 'antd'
import { MainHeader } from './headers/MainHeader'

const { Header, Footer, Content } = Layout

export const MainLayout = memo((
  {
    header = <MainHeader/>,
    content,
    footer
  }) => {
  return (
    <Layout style={{ height: "100vh" }}>
      {header && <Header>{header}</Header>}
      <Layout style={{ backgroundColor: 'white'}}>
        {content && <Content>{content}</Content>}
      </Layout>
      {footer && <Footer>{footer}</Footer>}
    </Layout>
  )
})