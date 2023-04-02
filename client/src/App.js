import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import "./App.css";
import ClassInfo from "./components/ClassInfo";
import ZoomPage from "./components/ZoomPage";

function App() {
    return (
        <div className="App">
            <header className="App-header"></header>
            <Router>
                <Switch>
                    <Route exact path="/" component={ClassInfo} />
                    <Route path="/zoom" component={ZoomPage} />
                </Switch>
            </Router>
        </div>
    );
}

export default App;
