import React, { useState } from "react";
import Profile from "../profile/Profile";
import { useNavigate } from "react-router-dom";
import { Box, Button } from "@mui/material";

const Dashboard = () => {
    const navigate = useNavigate();
    const onClick = () => {
        navigate("/selection");
    }
    return(
        <Box className="dashboard">
            <Profile />
            <Button variant="contained" onClick={onClick}>Start Interview</Button>
        </Box>
    );
}

export default Dashboard;