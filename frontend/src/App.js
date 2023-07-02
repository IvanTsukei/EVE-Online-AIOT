import logo from './logo.svg';
import './App.css';
import { ApiRequest } from './controllers/api';
import * as React from 'react'

export default class App extends React.Component {
  state = {
    poop: null
  }
  componentDidMount = async () => {
    let data = await (await ApiRequest('/')).json();
    console.log(data);
    this.setState(data);
  }

  render = () => {
    return (
      <div className="App">
        <h1> {this.state.poop} poop </h1>
      </div>
    )
  }
}

