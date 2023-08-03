import Button from '@mui/material/Button';
import './App.css';
import { ApiRequest } from './controllers/api';
import * as React from 'react'

export default class App extends React.Component {
  state = {
    data: null,
    gen: null,
  }
  componentDidMount = async () => {
    let data = await (await ApiRequest('/')).json();
    console.log(data);
    this.setState({data: data});

    // This section outputs the entire hell oworld
    
    let gen = []
    for (let key in data) {
      gen.push(
        <h1> {key} : {data[key]} </h1>
      )
    }
    this.setState({gen: gen})
  }

  render = () => {
    return (
      <div className="App">
        <h1> {this.state.data?.poop} test </h1> {/* This looks at k,v pair and returns v. Doing ?. is conditional 
        chanining, look it up*/}
        <Button variant="contained">Hello World</Button>
        {this.state.gen}
      </div>
    )
  }
}

