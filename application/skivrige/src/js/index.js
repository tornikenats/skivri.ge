require('../style/screen.scss')

import React from 'react'
import { render } from 'react-dom'
import {
    BrowserRouter as Router,
    Route, Link, Switch
} from 'react-router-dom'

import Header from './components/Header'
import Footer from './components/Footer'
import News from './components/News'
import About from './components/About'

const App = () => (
    <Router>
        <div className="app">
            <Header />
            <Switch>
                <Route path="/about" component={About} />
                <Route path="/" component={News} />
            </Switch>
            <Footer />
        </div>
    </Router>
)


render(<App />, document.getElementById('root'));


