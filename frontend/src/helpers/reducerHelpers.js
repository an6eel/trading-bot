import _ from 'lodash'
import { APIById } from '../api'

export const apiEventByType = {
  start: 'START',
  success: 'SUCCESS',
  error: 'ERROR',
}
const eventTypes = _.values(apiEventByType)

export const actionTypeSeparator = '-'
export const createActionTypeString = (api, resource, event) =>
  api + actionTypeSeparator + resource + actionTypeSeparator + event
export const createActionType = (api, resource, event) => ({ api, resource, event })

const createActionTypeWithMeta = (api, resource, event, meta) => ({
  type: createActionTypeString(api, resource, event),
  meta,
})

export const createActionTypesForRequest = (api, resource, meta) =>
  _.map(eventTypes, _.partial(createActionTypeWithMeta, api, resource, _, meta))

export const createActionTypesOfMainAPI = _.partial(createActionTypesForRequest, APIById.main)

export const parseAPIActionType = type => {
  if (!_.isString(type)) {
    throw new Error('Action should be a String')
  }
  const pieces = type.split(actionTypeSeparator)
  if (pieces.length !== 3) {
    return void 0
  }
  return createActionType(...pieces)
}