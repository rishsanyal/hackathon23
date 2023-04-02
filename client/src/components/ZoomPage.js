import React from "react";
import ZoomCall from "./ZoomCall";
import TimerComp from "./TimerComp";

function ZoomPage() {
    const endTime = "2023-04-02T08:44:18Z"; // UTC timestring
    return (
        <div className="ZoomPage">
            <ZoomCall />
            <TimerComp endTime={endTime} />
        </div>
    );
}

export default ZoomPage;
