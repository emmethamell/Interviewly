import React, { useState, useEffect } from "react";
import Profile from "../profile/Profile";
import { useNavigate } from "react-router-dom";
import { Box, Button, Typography } from "@mui/material";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, getAccessTokenSilently } = useAuth0();
  const [interviews, setInterviews] = useState([]);

  useEffect(() => {
    const fetchInterviews = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await axios.get('http://localhost:5001/routes/get-interviews', {
          params: {
            auth0_user_id: user.sub,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setInterviews(response.data.interviews);
      } catch (error) {
        console.error("Error fetching interviews:", error);
      }
    };

    fetchInterviews();
  }, [user, getAccessTokenSilently]);
  
  const onClick = () => {
    navigate("/selection");
  };
  return (
    <Box className="dashboard">
      <Profile />
      <Box>
        PAST INTERVIEWS:
        <Box>
        {interviews.map((interview) => (
            <Box key={interview.id} mb={2}>
              <Typography variant="body1">Question ID: {interview.question_id}</Typography>
              <Typography variant="body1">Transcript: {interview.transcript}</Typography>
              <Typography variant="body1">Score: {interview.score}</Typography>
              <Typography variant="body1">Question: {interview.question_name}</Typography>
              <Typography variant="body1">Difficulty: {interview.question_difficulty}</Typography>
            </Box>
          ))}
        </Box>
      </Box>
      <Button variant="contained" onClick={onClick}>
        Start Interview
      </Button>
    </Box>
  );
};

export default Dashboard;
