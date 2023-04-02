import React, { useEffect } from "react";
import ZoomMtgEmbedded from "@zoomus/websdk/embedded";
import { useParams } from "react-router-dom";

const MeetingPage = () => {
    const client = ZoomMtgEmbedded.createClient();
    let meetingSDKElement = document.getElementById("meetingSDKElement");
    client.init({ zoomAppRoot: meetingSDKElement, language: "en-US" });

    client.join({
        sdkKey: "34lXC9oHRd21RUeUcVu5FA",
        signature: signature, // role in SDK signature needs to be 1
        meetingNumber: meetingNumber,
        password: password,
        userName: userName,
        zak: zakToken, // the host's zak token
    });

    const { meetingId } = useParams();

    useEffect(() => {
        // Initialize the Zoom Web SDK
        ZoomMtg.setZoomJSLib("https://source.zoom.us/1.9.1/lib", "/av");
        ZoomMtg.preLoadWasm();
        ZoomMtg.prepareJssdk();

        // Join the Zoom meeting
        const joinMeeting = async () => {
            try {
                const signature = "your-signature"; // Generate a signature for the meeting
                const apiKey = "your-api-key"; // Your Zoom API key
                const userName = "your-name"; // Your name
                const userEmail = "your-email"; // Your email
                const passWord = "your-password"; // Meeting password

                await ZoomMtg.init({
                    leaveUrl: "https://yourapp.com/meeting-end-page",
                    isSupportAV: true,
                    success: () => {
                        ZoomMtg.join({
                            meetingNumber: meetingId,
                            userName,
                            signature,
                            apiKey,
                            userEmail,
                            passWord,
                            success: (res) => {
                                console.log("join meeting success");
                            },
                            error: (res) => {
                                console.log("join meeting error", res);
                            },
                        });
                    },
                    error: (res) => {
                        console.log("init error", res);
                    },
                });
            } catch (error) {
                console.log(error);
            }
        };

        joinMeeting();

        return () => {
            // Leave the Zoom meeting when the component unmounts
            ZoomMtg.leaveMeeting({});
            ZoomMtg.cleanCache();
            console.log("meeting left");
        };
    }, [meetingId]);

    return (
        <div id="meetingSDKElement">
            {/* Meeting SDK renders here when a user starts or joins a Zoom meeting */}
        </div>
    );
};

export default MeetingPage;
