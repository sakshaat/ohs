import React, { Component } from 'react';
import Course from "./components/Course"
import { BrowserRouter as Router} from "react-router-dom";

import './App.css';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <nav>
            <div className="links">
              <div className="nav-item">
                OHS
              </div>
              <div className="nav-item">
                Logged In as Dr. Frankenstein 
              </div>
            </div>

          </nav>
          <header className="App-header">
            <Course />
          </header>
        </div>
      </Router>
    );
  }
}

export default App;
