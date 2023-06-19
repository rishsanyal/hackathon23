import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import "./App.css";
import ClassInfo from "./components/ClassInfo";
import ZoomPage from "./components/ZoomPage";

import { CookiesProvider } from "react-cookie";

function App() {

    return (
        <div className="App">

            <CookiesProvider>
                {/* <header className="App-header"> */}
                <Router>
                    <Routes>
                        <Route path="/" element={<ClassInfo />} />
                        <Route path="/zoom/:ohId" element={<ZoomPage />} />
                    </Routes>
                </Router>
            </CookiesProvider>
            {/* </header> */}
        </div>
    );
}

export default App;
