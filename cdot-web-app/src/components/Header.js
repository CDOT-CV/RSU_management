import React, { Component } from 'react';
import logo from '../images/cdot_logo.png';

import Grid from '@material-ui/core/Grid';

class Header extends Component {
  render() {
    return (
      <header style={style}>
        <Grid container style={gridStyle} alignItems="center">
          <img src={logo} style={logoStyle} alt="Logo" />
          <h1 style={headerStyle}>CDOT RSU Manager</h1>
        </Grid>
      </header>
    )
  }
}

const style = {
  background: '#333',
  color: 'white',
  textAlign: 'left',
  padding: '10px',
  position: 'relative',
  zIndex: '100'
}

const gridStyle = {
  alightnment: "center"
}

const logoStyle = {
  padding: '5px',
  marginLeft: '20px',
  alignment: 'center'
}

const headerStyle = {
  padding: '5px',
  marginLeft: '10px',
  alignment: 'center'
}

export default Header;