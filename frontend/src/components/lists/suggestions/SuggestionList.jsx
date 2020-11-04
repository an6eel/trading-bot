import React, { useCallback } from 'react'
import { List } from 'antd'
import { SuggestionRow } from './SuggestionRow'

export const SuggestionList = ({ suggestions, ...rest }) => {

  console.log(suggestions)
  const renderSuggestion = useCallback((action) => {
    return (
      <SuggestionRow item={action}/>
    )
  }, [])

  return (
    <List dataSource={suggestions} renderItem={renderSuggestion} {...rest}/>
  )
}