import React, { useState, useEffect } from "react";
import Profile from "../profile/Profile";
import { useNavigate } from "react-router-dom";
import { Box, Button, Typography, Paper, Grid2 } from "@mui/material";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import Interview from "./Interview";
import GitHubCalendar from "react-github-calendar";

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, getAccessTokenSilently } = useAuth0();
  const [interviews, setInterviews] = useState([]);

  useEffect(() => {
    const fetchInterviews = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await axios.get(
          "http://localhost:5001/routes/get-interviews",
          {
            params: {
              auth0_user_id: user.sub,
            },
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
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

  const getSuccessRate = (interviews) => {
    const total = interviews.length;
    const totalSuccess = interviews.reduce((acc, cur) => {
      if (cur.score == "Hire" || cur.score == "Strong Hire") {
        return acc + 1;
      }
      return acc;
    }, 0);
    return Math.ceil((totalSuccess / total) * 100) + "%";
  };


  return (
    <Grid2 container spacing={2} p={2}>
      {/* TOP BOX */}
      <Grid2 className="dashboard-container" bgcolor="white" size={4} display="flex" justifyContent="center" alignItems="center">
        <Button variant="contained" onClick={onClick}>
          Start Interview
        </Button>
      </Grid2>

      <Grid2 container size={8} sx={{ border: "2px solid white"}} p={1} color="black" bgcolor="white" className="dashboard-container">
      <Grid2 size={3}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Typography>SUCCESS RATE</Typography>
          <Typography>{getSuccessRate(interviews)}</Typography>
        </Box>
      </Grid2>
      <Grid2
        size={3}
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",

        }}
      >
        <Typography color="#4caf50">Easy</Typography>
        <Typography>
          {interviews.reduce(
            (acc, cur) => (cur.question_difficulty == "Easy" ? acc + 1 : acc),
            0,
          )}
        </Typography>
      </Grid2>
      <Grid2
        size={3}
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
        
      >
        <Typography color="#ffeb3b">Medium</Typography>
        <Typography>
          {interviews.reduce(
            (acc, cur) => (cur.question_difficulty == "Medium" ? acc + 1 : acc),
            0,
          )}
        </Typography>
      </Grid2>
      <Grid2
        size={3}
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography color="#f44336">Hard</Typography>
        <Typography>
          {interviews.reduce(
            (acc, cur) => (cur.question_difficulty == "Hard" ? acc + 1 : acc),
            0,
          )}
        </Typography>
      </Grid2>
      </Grid2>
  
      {/* BOTTOM */}
      <Grid2 size={4} color="black">
        <Box alignContent="center" sx={{ p: 2 }} className="dashboard-container" bgcolor="white">
          <Profile />
        </Box>
      </Grid2>
      <Grid2 size={8} sx={{border: "2px solid white"}} className="dashboard-container" p={1} bgcolor="white">
        <Paper sx={{boxShadow: "none"}}>
            <Box>
              {[... interviews].reverse().map((interview, index) => (
                <Interview
                  key={interview.id}
                  interview={interview}
                  sx={{
                    backgroundColor: index % 2 === 0 ? "#f5f5f5" : "white",
                  }}
                />
              ))}
          </Box>
        </Paper>
      </Grid2>
      <Grid2></Grid2>
    </Grid2>
  );
};

export default Dashboard;
