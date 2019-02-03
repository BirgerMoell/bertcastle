import React, { Component } from 'react'
import './App.css'
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import Chat from './Chat'
import Spam from './Spam'

class App extends Component {
  render () {
    return (
      <div className='App'>
        <Router>
          <div>

            <Route exact path='/' component={Spam} />
            <Route path='/spam' component={Spam} />
            <Route path='/chat' component={Chat} />
          </div>
        </Router>
      </div>
    )
  }
}

export default App
