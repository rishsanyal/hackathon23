import React, { useState, useEffect } from "react";
import { API_BASE_URL } from "../config";

import {
    Button,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    Select,
    MenuItem,
    Link,
} from "@mui/material";
import NotificationTurn from "./NotificationTurn";

function ClassInfo() {
    // const [classData, setClassData] = useState(null);
    const [selectedOption, setSelectedOption] = useState("");
    const [classData, setClassData] = useState({
        options: [],
        title: "",
        office_hours_info: [
            {
                // join: false,
                // date: "Bharat Day",
                // time: "Jay Time",
                // zoom_link: "Olga Link",
                // notify: true,
                // notify_turn: false
            },
        ],
    });
    const [notificationState, setNotificationState] = useState(false);
    // const [turnNotificationState, setTurnNotificationState] = useState(false);

    const [officeHoursInfo, setOfficeHoursInfo] = useState([]);

    useEffect(() => {
        fetch(`${API_BASE_URL}/office_hours_info`)
            .then((response) => response.json())
            .then((data) => {
                // setClassData({
                //     ...classData,
                //     office_hours_info: data.office_hours_info,
                // });
                setOfficeHoursInfo(data.office_hours_info);
            })
            .catch((error) => {
                console.log("Error fetching class info:", error);
                // Handle the error here, such as showing an error message to the user
            });
    }, []);
    useEffect(() => {
        fetch(`${API_BASE_URL}/class_info`)
            .then((response) => response.json())
            .then((data) => {
                setSelectedOption(data.class_info[0].class_name); // Select first option by default
                // setClassData({
                //     ...classData,
                //     options: data.class_info.names,
                // });
                setClassData((prevClassData) => ({
                    ...prevClassData,
                    options: data.class_info.names,
                }));
            })
            .catch((error) => {
                console.log("Error fetching class info:", error);
                // Handle the error here, such as showing an error message to the user
            });
    }, []);

    // useEffect(() => {
    //     Promise.all([
    //       fetch(`${API_BASE_URL}/class_info`),
    //       fetch(`${API_BASE_URL}/students`)
    //     ])
    //     .then(([classesResponse, studentsResponse]) => Promise.all([classesResponse.json(), studentsResponse.json()]))
    //     .then(([classesData, studentsData]) => {
    //       setClassData(classesData);
    //       setStudentData(studentsData);
    //     })
    //     .catch((error) => console.error(error));
    //   }, []);

    if (!classData) {
        return <div>Loading...</div>;
    }

    function handleOptionChange(event) {
        setSelectedOption(event.target.value);
        setClassData({
            ...classData,
            title: event.target.value,
        });
    }

    function formatTime(dateString, timeString) {
        const date = new Date(`${dateString}T${timeString}Z`);
        const time = date.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
            hour12: true,
        });
        // perform some formatting on the text
        return time;
    }

    // const updateOfficeHours = (newOfficeHours) => {
    //     setClassData({ ...classData, office_hours_info: newOfficeHours });
    // };
    function goToExternalLink(link) {
        // open link in new tab
        window.open(link, "_blank");
    }

    return (
        <div className="rootNode" style={
            {
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }
        }>
            {/* <h1>
                <Select
                    value={selectedOption}
                    onChange={handleOptionChange}
                    label="Class info"
                >
                    {classData.options.map((option) => (
                        <MenuItem key={option} value={option}>
                            {option}
                        </MenuItem>
                    ))}
                </Select>
            </h1> */}
            <div className="office-hours" style={
                {
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    height: "100%",
                    width: "80%",
                }
            }>

            <h2 style={
                {
                    margin: "3%"
                }
            }>
                Office Hours
            </h2>
            {/* Add table with columns Join, Date Time, Notify, Notify Turn */}
                <TableContainer component={Paper}>
                    <Table sx={{ }} aria-label="simple table">
                        <TableHead>
                            <TableRow key={0}>
                                <TableCell aling="center">Join</TableCell>
                                <TableCell align="center">Date</TableCell>
                                <TableCell align="center">Time</TableCell>
                                <TableCell align="center">Notify</TableCell>
                                {/* <TableCell align="center">Notify Turn</TableCell> */}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {officeHoursInfo.map((row) => (
                                <TableRow
                                    key={row.id}
                                    sx={{
                                        "&:last-child td, &:last-child th": {
                                            // border: 0,
                                        },
                                    }}
                                >
                                    {/* <TableCell component="th" scope="row">
                                        {row.instructor}
                                    </TableCell> */}
                                    <TableCell>
                                        {/* Add a button that redirects to a link */}
                                        <Button
                                            variant="contained"
                                            color="primary"
                                            onClick={() =>
                                                goToExternalLink(row.zoom)
                                            }
                                        >
                                            {" "}
                                            Join{" "}
                                        </Button>
                                    </TableCell>
                                    <TableCell align="center">{row.date}</TableCell>
                                    <TableCell align="center">
                                        {formatTime(row.date, row.time)}
                                    </TableCell>
                                    <TableCell align="center">
                                    <NotificationTurn  message={"You will be notified when your office hours start!"}></NotificationTurn>
                                    </TableCell>
                                    {/* <TableCell align="center">
                                        <NotificationTurn message={"You will be notified when your estimated turn comes up!"}></NotificationTurn>
                                    </TableCell> */}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div>
    );
}

export default ClassInfo;
