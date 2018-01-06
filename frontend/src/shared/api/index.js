
export const get_news = cb => {
    fetch('http://localhost:5000/api/v1/news')
    .then(resp => resp.json())
    .then(json => cb(json))
}