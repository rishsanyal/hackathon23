import React from "react";

import "./ZoomCall.css";
import ZoomMtgEmbedded from "@zoomus/websdk/embedded";

function ZoomCall() {
    var link =
        "https://us04web.zoom.us/j/71945271375?pwd=0VWTn6dkUj1UwLCEq626eD9nF0pa4g.1";
    const client = ZoomMtgEmbedded.createClient();

    const regexMeetingNumber = /j\/(\d+)/;
    const regexMeetingPassword = /\?pwd=(\w+)/;
    var authEndpoint = "https://meetingsdk-auth-learnly.herokuapp.com";
    var sdkKey = "34lXC9oHRd21RUeUcVu5FA";
    var meetingNumber = link.match(regexMeetingNumber)[1];
    var passWord = link.match(regexMeetingPassword)[1];
    var userName = "John Doe";
    var role = 0;
    var userEmail = "johndoe232@gmail.com";

    function getSignature(e) {
        e.preventDefault();

        fetch(authEndpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                meetingNumber: meetingNumber,
                role: role,
            }),
        })
            .then((res) => res.json())
            .then((response) => {
                startMeeting(response.signature);
            })
            .catch((error) => {
                console.error(error);
            });
    }

    // function toString(strTypeObj) {
    //     return Object.prototype.toString.call(strTypeObj);
    // }

    function startMeeting(signature) {
        let meetingSDKElement = document.getElementById("meetingSDKElement");

        client.init({
            debug: true,
            zoomAppRoot: meetingSDKElement,
            language: "en-US",
            customize: {
                meetingInfo: [
                    "topic",
                    "host",
                    "mn",
                    "pwd",
                    "telPwd",
                    "invite",
                    "participant",
                    "dc",
                    "enctype",
                ],
                toolbar: {
                    buttons: [
                        {
                            text: "Custom Button",
                            className: "CustomButton",
                            onClick: () => {
                                console.log("custom button");
                            },
                        },
                    ],
                },
                video: {
                    isResizable: true,
                    viewSizes: {
                        default: {
                            width: 1000,
                            height: 600,
                        },
                        ribbon: {
                            width: 300,
                            height: 700,
                        },
                    },
                },
            },
        });

        client.join({
            signature: signature,
            sdkKey: sdkKey,
            meetingNumber: meetingNumber,
            password: passWord,
            userName: userName,
            userEmail: userEmail,
            success: (success) => {
                console.log(success);

                // Your success callback code here
            },
        });

        client.on("join", () => {
            console.log("Joined the meeting");
        });

        client.on("onShareContentStarted", () => {
            client.setVideoViewSize({ width: 1000, height: 600 });
            client.setActiveSpeakerViewOptions({ noRemoteVideo: true });
            client.setGalleryViewActive(false);
        });
        client.on("onShareContentStopped", () => {
            client.setVideoViewSize({ width: 1000, height: 600 });
            client.setActiveSpeakerViewOptions({ noRemoteVideo: false });
            client.setGalleryViewActive(true);
        });

        client.on("leave", () => {
            console.log("Left the meeting");
        });
    }

    return (
        <div className="zoomCall">
            <main>
                <h3>Networks Programming - Prof. Vahab P</h3>
                <div>
                    <div id="meetingSDKElement">
                        {/* Zoom Meeting SDK Component View Rendered Here */}
                    </div>
                    <button onClick={getSignature}>Join Meeting</button>
                </div>
            </main>
        </div>
    );
}

export default ZoomCall;
