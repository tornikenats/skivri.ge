import { hostname } from '../constants'

export const get_news = cb => {
    fetch(`${hostname}/api/v1/news`)
        .then(resp => resp.json())
        .then(json => cb(json))
}