import React, { Component } from 'react';
import OfficeHours from "./components/OfficeHour"

import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <OfficeHours slotNum={5}> </OfficeHours>
        </header>
      </div>
    );
  }
}

export default App;
