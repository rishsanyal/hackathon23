import React, { useState, useEffect } from "react";
import { useCookies } from "react-cookie";

import {List, ListItem, ListItemButton, ListItemText } from '@mui/material'

function OHStudentTable({office_hours_id}) {

    const [cookies, setCookie, removeCookie] = useCookies(["user"]);

    let currUser = cookies.user_id;

    const [studentNames, setStudentNames] = useState([
        'Bharat',
        'Tanya']);

    useEffect(() => {
            fetch("http://localhost:5001/update_students_queue", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    office_hours_id: office_hours_id,
                    user_id: currUser
                })
            }).then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json()}
            ).then((data) => {
                console.log("data", data);
                setStudentNames(data);
            });
        }, []);



    // setStudentNames()

    // useEffect(() => {
    //     fetch("http://localhost:5000/office_hours_info")
    //         .then((response) => response.json())
    //         .then((data) => {
    //             setStudentNames(data.office_hours_info);
    //         })
    //         .catch((error) => {
    //             console.log("Error fetching class info:", error);
    //             // Handle the error here, such as showing an error message to the user
    //         });
    // }, []);


    return (
        <div className="StudentTable" style={
            {
                // width: "200px",
                // display: "flex",
                // flexDirection: "column",
                // justifyContent: "center",
                // alignItems: "center",
            }
        }>
            <List >
                <ListItem>
                    <ListItemButton>
                        <ListItemText primary="Students" />
                    </ListItemButton>
                </ListItem>

                <hr/>
                {
                    studentNames.map((studentName, index) => (
                        <ListItem disablePadding>
                            <ListItemButton selected={studentName=="Rishab" ? 1:0}>
                                <ListItemText primary={studentName} />
                            </ListItemButton>
                        </ListItem>
                    ))

                }
            </List>
        </div>
    )
}

export default OHStudentTable