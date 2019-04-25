import React, { Component } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';
import logo from './bert.jpg'
import './App.css'
import 'react-chat-widget/lib/styles.css';
import { postJson } from './utils'

class Chat extends Component {
  componentDidMount() {
    addResponseMessage("Welcome to this awesome chat!");
  }

  handleNewUserMessage = async (newMessage) => {
    console.log(`New message incomig! ${newMessage}`);
    // Now send the message throught the backend API
    //addResponseMessage(response);
    let response = await this.getResponse(newMessage)
    addResponseMessage(response);
  }

  getResponse = async (newMessage) => {
    const url= "http://localhost:5000/nearest"
    const body = {
      text: newMessage
    }
    const response = await fetch("http://localhost:5050/nearest",
    { body: JSON.stringify(body), headers: { "Content-Type": "application/json" }, method: "POST" })
    console.log(response)
    let responseJson = await response.json()
    console.log("the response json is", responseJson)
    return responseJson
  }

  render() {
    return (
      <div className="App">

      <header className='App-header'>
          <h2>Bert Chat</h2>
          <img src={logo} className='App-logo' alt='logo' />

        </header>


        <Widget
          handleNewUserMessage={this.handleNewUserMessage}
        />
      </div>
    );
  }
}

export default Chat;
