
export const get_news = (cb) => {
    fetch('/api/news')
    .then((resp) => resp.json())
    .then((json) => cb(json))
}