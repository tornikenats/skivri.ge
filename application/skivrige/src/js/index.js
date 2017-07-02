require('../style/screen.scss')

import React from 'react'
import { render } from 'react-dom'
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom'

import Header from './components/Header'
import Footer from './components/Footer'
import News from './components/News'

const App = () => (
    <div className="app">
        <Header />
        <Router>
            <Route path="/" component={News} />
        </Router>
        <Footer />
    </div>
)


render(<App />, document.getElementById('root'));


