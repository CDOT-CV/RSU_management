import React, { Component } from 'react';
import Header from './components/Header';
import Map from './components/Map';

import './App.css'

const axios = require('axios').default;

class App extends Component {

  state = {
    rsuData: []
  }

  constructor(props) {
    super(props);
    this.getRsuData();
  }

  async getRsuData() {
    try {
      let response = await axios.get('https://rsu-manager-apigateway-5xm3e3o5.uc.gateway.dev/rsuinfo');
      this.setState({'rsuData': response.data.rsuList});
    } catch (error) {
      console.log(error);
    }
  }

  render() {
    return (
      <div>
        <Header/>
        <Map rsuData={this.state.rsuData}/>
      </div>
    );
  }
}

export default App;
