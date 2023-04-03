import React, { useState, useEffect } from "react";
import { API_BASE_URL } from "../config";
import {
    Button
}  from "@mui/material";

function NotificationTurn({message}) {
    const [turnNotificationState, setTurnNotificationState] = React.useState(false);

    return (
        <div>
            <Button variant="contained" color={turnNotificationState? "primary" : "success"} onClick={() => {
                    setTurnNotificationState(!turnNotificationState);
                    alert(message);
                }}>
                    {
                        turnNotificationState ? "On" : "Off"
                    }
            </Button>
        </div>
    )
}

export default NotificationTurn