import React from "react";

import "./ZoomCall.css";
import ZoomMtgEmbedded from "@zoomus/websdk/embedded";
import OHStudentTable from "./OHStudentTable";

function ZoomCall({office_hours_id}) {
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

    const [meetingStarted, setMeetingStarted] = React.useState(false);

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
                setMeetingStarted(true);
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

                setMeetingStarted(true);
                // Your success callback code here
            },
        });

        client.on("join", () => {
            setMeetingStarted(true);
            console.debug("Joined the meeting");
        });

        client.on("onShareContentStarted", () => {
            client.setVideoViewSize({ width: 1000, height: 600 });
            client.setActiveSpeakerViewOptions({ noRemoteVideo: true });
            client.setGalleryViewActive(false);
            setMeetingStarted(true);
        });
        client.on("onShareContentStopped", () => {
            client.setVideoViewSize({ width: 1000, height: 600 });
            client.setActiveSpeakerViewOptions({ noRemoteVideo: false });
            client.setGalleryViewActive(true);
            setMeetingStarted(true);
        });

        client.on("leave", () => {
            setMeetingStarted(false);
            console.log("Left the meeting");
        });
    }

    return (
        <div className="zoomCall">
            <main>
                <div className="ZoomInteraction" style={
                    {
                        display: "flex",
                        // flexDirection: "row",
                        justifyContent: "center",
                        alignItems: "center",
                        border: "1px solid black",
                        height: "80vh",
                        // width: "80vw",
                    }
                }>
                        <div
                            id="zoomSpace"
                            style={
                                {
                                    // marginLeft: "10px",
                                    left: "0px",
                                    flex: "8",
                                    // position: "absolute",
                                    border: "1px solid black",
                                    height: "100%",
                                    width: "80%",

                                }
                            }
                        >
                            {/* Zoom Meeting SDK Component View Rendered Here */}
                        </div>
                        <div style={{
                            right: "0px",
                            flex: "2",
                            border: "1px solid black",
                            borderRadius: "5px",
                            height: "inherit",
                            width: "10vw",
                            overflow: "scroll",
                        }}>
                            <OHStudentTable office_hours_id={office_hours_id} />
                        </div>
                        {/* <div id="zoomButton" style={
                            {
                                display: {meetingStarted} ? "flex" : "none",
                                flexDirection: "column",
                                justifyContent: "center",
                                alignItems: "center",
                            }
                        }>
                                { !(meetingStarted) && <button onClick={getSignature} style={
                                    {
                                        height: "50px",
                                        width: "100px",
                                        margin: "10px",
                                        backgroundColor: "#007bff",
                                        color: "white",
                                        borderRadius: "5px",
                                        textAlign: "center"
                                    }
                                }>
                                    Join Success
                                </button>}

                        </div> */}
                </div>
            </main>
        </div>
    );
}

export default ZoomCall;
