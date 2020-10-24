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
    <Layout>
      {header && <Header>{header}</Header>}
      <Layout>
        {content && <Content>{content}</Content>}
      </Layout>
      {footer && <Footer>{footer}</Footer>}
    </Layout>
  )
})