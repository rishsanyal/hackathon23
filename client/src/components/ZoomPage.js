// import React, { useEffect } from "react";
import React, {useEffect, useState} from 'react';
import { useParams } from 'react-router-dom';


import ZoomCall from "./ZoomCall";
import TimerComp from "./TimerComp";


function ZoomPage() {

    // const [cookies, setCookie] = useCookies(["user"]);
    const { ohId } = useParams();
    const endTime = "2023-04-03T08:44:18Z"; // UTC timestring

    // console.log("cookies", cookies.user_id);

    useEffect(() => {
        const handleTabClose = event => {
          event.preventDefault();

          console.log('beforeunload event triggered');

          return (event.returnValue =
            'Are you sure you want to exit?');
        };

        window.addEventListener('beforeunload', handleTabClose);

        return () => {
          window.removeEventListener('beforeunload', handleTabClose);
        };
      }, []);

    console.log("Updated");


    return (
        <div className="ZoomPage" style={
            {
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
            }
        }>

            <h3>Networks Programming - Prof. Vahab P</h3>
            <div>
                <ZoomCall office_hours_id={ohId} />
            </div>
            <TimerComp endTime={endTime} office_hours_id={ohId} />
        </div>
    );
}

export default ZoomPage;
