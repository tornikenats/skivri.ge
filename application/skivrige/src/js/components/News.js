import React, { Component } from 'react'

import { get_news } from 'shared/api'

class News extends Component {
    constructor() {
        super()
        this.state = {}

        this.updateNewsList = this.updateNewsList.bind(this)
    }

    componentDidMount() {
        get_news(this.updateNewsList)
    }

    updateNewsList(json) {
        this.setState({ news: json })
    }

    render() {
        const { news } = this.state
        if(this.state.news){
            return (
                <div className="section news-list">
                    {news.map((item, index) => 
                        <div key={index} className="news-item">
                            <a href={item.link}>{item.title}</a>
                            <span className="source"> ({item.source})</span>
                        </div>
                    )}
                </div>
            )
        }else{
            return <div>Loading...</div>
        }
    }
}

export default News


// author
// category
// date_add
// date_pub
// description
// id
// lang
// link
// num
// score
// source
// title