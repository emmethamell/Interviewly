import React, { useState, useEffect } from "react";
import Profile from "../profile/Profile";
import { useNavigate } from "react-router-dom";
import { Box, Button, Typography } from "@mui/material";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import Interview from "./Interview";

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
    <Box className="dashboard" sx={{p: 3}}>
      <Profile />
      <Button variant="contained" onClick={onClick}>
        Start Interview
      </Button>
      <Box sx={{mt: 3}}>
        PAST INTERVIEWS:
        <Box>
          {interviews.map((interview) => (
            <Interview key={interview.id} interview={interview} />
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
