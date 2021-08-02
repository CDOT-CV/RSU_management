import React, { Component } from 'react';

class Header extends Component {
  render() {
    return (
      <header style={style}>
        <h1>CDOT RSU Manager</h1>
      </header>
    )
  }
}

const style = {
  background: '#333',
  color: 'white',
  textAlign: 'left',
  padding: '10px'
}

export default Header;