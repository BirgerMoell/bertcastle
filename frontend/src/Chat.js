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
    const url= "http://localhost:5000/model"
    const body = {
      text: newMessage
    }
    const response = await postJson(url, body)
    return response
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