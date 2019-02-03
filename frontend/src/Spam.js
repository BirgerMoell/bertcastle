import React, { Component } from 'react'
import logo from './bert.jpg'
import './App.css'
import { postJson } from './utils'

class Spam extends Component {
  constructor (props) {
    super(props)
    this.state = {
      value: '',
      spam: false,
   }
  }

  handleChange = async (event) => {
    this.setState({ value: event.target.value })
    const url= "http://localhost:5000/model"
    const body = {
      text: event.target.value
    }
    const response = await postJson(url, body)
  }

  render () {
    return (
      <div className='App'>
        <header className='App-header'>
          <img src={logo} className='App-logo' alt='logo' />
          <p>
            Bert Model
          </p>
          <label>Ham or Spam
            <br />
            <input type='text' value={this.state.value} onChange={(e) => this.handleChange(e)}
            />
          </label>

          <p>{this.state.value}</p>

         { this.state.spam ? <p>Spam</p> : <p>Ham</p>}

        </header>
      </div>
    )
  }
}

export default Spam
