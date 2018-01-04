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

    onArticleClick(e){
        let title = e.target.innerText
        ga('send', 'event', 'article', 'click', title)
    }

    render() {
        const { news } = this.state
        if(this.state.news){
            return (
                <div className="section news-section">
                    {news.map((item, index) => 
                        <div key={index} className="news-item">
                            <div className="mainline">
                                <a href={item.link} onClick={this.onArticleClick}>{item.title}</a>
                                <span className="source"> ({item.source})</span>
                            </div>
                            <div className="byline">
                                {item.time_since}
                            </div>
                        </div>
                    )}
                </div>
            )
        }else{
            return <div className="section news-section">Loading...</div>
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