import React, { Component } from 'react'
import ReactGA from 'react-ga';
import { get_news } from '../shared/api'

class Home extends Component {
    constructor() {
        super()
        this.state = {
            news: []
        }
    }

    componentDidMount() {
        get_news(json => this.setState({ news: json }))
    }

    onArticleClick(e) {
        let title = e.target.innerText
        ReactGA.pageview(window.location.pathname + window.location.search);
    }

    render() {
        const { news } = this.state
        return (
            <div className="container">
                <div className="section news">
                    <div className="title-container">
                        <div className="title">
                            აგრირებული სტატიები
                        </div>
                        <div className="title-options">
                            <span className="active">eng</span>
                            <span>ქარ</span>
                        </div>
                    </div>
                    <NewsGroup newsItems={news} />
                </div>
            </div>
        )
    }
}

const NewsGroup = ({ newsItems }) => (
    <div className="news-group">
        {newsItems && newsItems.map((item, index) =>
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
        {!newsItems && <div className="section news-section">Loading...</div>}
    </div>
)

export default Home