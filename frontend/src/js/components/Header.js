import React from 'react'
import {
  Link
} from 'react-router-dom'

const Header = () => (
    <header className="section">
        <div className="logo">
            <Link to="/" className="inverted">სკივრი</Link>
        </div>
        <ul>
            <li><Link className="inverted" to="/about">about</Link></li>
            <li><a href="mailto:tornikenatsvlishilideveloper@gmail.com" className="inverted">contact</a></li>
        </ul>
    </header>
)

export default Header