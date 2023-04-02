import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";

import "./App.css";
import ClassInfo from "./components/ClassInfo";
import ZoomPage from "./components/ZoomPage";

function App() {
    return (
        <div className="App">
            <header className="App-header"></header>
            <Router>
                <nav>
                    <ul>
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        <li>
                            <Link to="/zoom">Zoom</Link>
                        </li>
                    </ul>
                </nav>
                <Routes>
                    <Route path="/" element={<ClassInfo />} />
                    <Route path="/zoom" element={<ZoomPage />} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
