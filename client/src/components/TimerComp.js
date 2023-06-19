import React, { useState, useEffect } from "react";

import "./TimerComp.css";

function TimerComp({ endTime, office_hours_id }) {
    const [timeLeft, setTimeLeft] = useState(getTimeLeft());

    useEffect(() => {
        const interval = setInterval(() => {
            setTimeLeft(getTimeLeft());
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    function getTimeLeft() {
        const endTimeMillis = Date.parse(endTime);
        const nowMillis = Date.now();
        const diff = endTimeMillis - nowMillis;
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff / (1000 * 60)) % 60);
        const seconds = Math.floor((diff / 1000) % 60);
        return { hours, minutes, seconds };
    }

    function formatTime(num) {
        return num.toString().padStart(2, "0");
    }

    return (
        <div className="timeArea">
            <div className="remainingTime">
                Remaining time: {timeLeft.hours}:{formatTime(timeLeft.minutes)}:
                {formatTime(timeLeft.seconds)}
            </div>
            <div className="averageTime">
                Average time: {timeLeft.hours}:{formatTime(timeLeft.minutes)}:
                {formatTime(timeLeft.seconds)}
            </div>
            <div className="turnEstimate">
                Turn Estimate: {timeLeft.hours}:{formatTime(timeLeft.minutes)}:
                {formatTime(timeLeft.seconds)}
            </div>
        </div>
    );
}

export default TimerComp;
