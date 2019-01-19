import React, { Component } from 'react'
import logo from './bert.jpg'
import './App.css'
import { postJson } from './utils'

class App extends Component {
  constructor (props) {
    super(props)
    this.state = {
      value: '',
      spam: false,
   }
  }

  handleChange = async (event) => {
    this.setState({ value: event.target.value })
    const url= "http://localhost:5000/api"
    const data = {
      text: event.target.value
    }
    //const response = await postJson(url, data)

    const response = await fetch(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json"
      },
    })

    // const response = await fetch("http://localhost:5000/api", {
    //     body: "{\"text\":\"win money today!!\", \"key2\":\"value2\"}",
    //     headers: {
    //       "Content-Type": "application/json"
    //     },
    //     method: "POST"
    //   })

    const responseJson = await response.json()

    console.log("the response is", responseJson)

    if(responseJson > 0.10) {
      this.setState({
        spam: true
      })
    }
      else {
        this.setState({
          spam: false
        })
      }


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

export default App
