import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import "./App.css";
import ClassInfo from "./components/ClassInfo";
import ZoomPage from "./components/ZoomPage";

function App() {
    return (
        <div className="App">
            <header className="App-header"></header>
            <Router>
                <Routes>
                    <Route exact path="/" element={ClassInfo} />
                    <Route path="/zoom" element={ZoomPage} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
