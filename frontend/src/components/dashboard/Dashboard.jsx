import { useState, useEffect } from "react";
import Profile from "../profile/Profile";
import { useNavigate } from "react-router-dom";
import { Box, Button, Typography, Paper, Grid2, IconButton } from "@mui/material";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import Interview from "./Interview";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

const Dashboard = () => {
  const { user, getAccessTokenSilently } = useAuth0();
  const [interviews, setInterviews] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalInterviews, setTotalInterviews] = useState(0);
  const [interviewStats, setInterviewStats] = useState({
    success_rate: 0,
    easy_successes: 0,
    medium_successes: 0,
    hard_successes: 0,
  });
  const navigate = useNavigate();
  const interviewsPerPage = 15;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = await getAccessTokenSilently();
        // Fetch paginated interviews
        const interviewsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/interview/get-interviews`, {
          params: {
            auth0_user_id: user.sub,
            page: currentPage,
            limit: interviewsPerPage,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setInterviews(interviewsResponse.data.interviews);
        setTotalInterviews(interviewsResponse.data.total);
        // Fetch stats
        const statsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/interview/get-interview-stats`, {
          params: { auth0_user_id: user.sub },
          headers: { Authorization: `Bearer ${token}` },
        });
        setInterviewStats(statsResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [user, getAccessTokenSilently, currentPage]);

  const onClick = () => {
    navigate("/selection");
  };

  const handleNextPage = () => {
    setCurrentPage((prevPage) => prevPage + 1);
  };

  const handlePreviousPage = () => {
    setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
  };

  return (
    <Grid2 container spacing={2} p={2}>
      {/* TOP BOX */}
      <Grid2
        className="dashboard-container"
        bgcolor="white"
        size={4}
        display="flex"
        justifyContent="center"
        alignItems="center">
        <Button variant="contained" onClick={onClick}>
          Start Interview
        </Button>
      </Grid2>
      <Grid2
        container
        size={8}
        sx={{ border: "2px solid white" }}
        p={1}
        color="black"
        bgcolor="white"
        className="dashboard-container">
        <Grid2 size={3}>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              height: "100%",
              justifyContent: "center",
            }}>
            <Typography
              variant="h5"
              sx={{
                fontWeight: "bold",
              }}>
              {Math.round(interviewStats.success_rate * 100)}%
            </Typography>
            <Typography sx={{ mt: 0.5 }}>Success Rate</Typography>
          </Box>
        </Grid2>
        <Grid2
          size={3}
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}>
          <Typography>{interviewStats.easy_successes}</Typography>
          <Typography color="#4caf50" sx={{ fontWeight: "bold" }}>
            Easy
          </Typography>
        </Grid2>
        <Grid2
          size={3}
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}>
          <Typography>{interviewStats.medium_successes}</Typography>
          <Typography color="#ffa000" sx={{ fontWeight: "bold" }}>
            Medium
          </Typography>
        </Grid2>
        <Grid2
          size={3}
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}>
          <Typography>{interviewStats.hard_successes}</Typography>
          <Typography color="#f44336" sx={{ fontWeight: "bold" }}>
            Hard
          </Typography>
        </Grid2>
      </Grid2>

      {/* BOTTOM BOX */}
      <Grid2 size={4} color="black">
        <Box alignContent="center" sx={{ p: 2 }} className="dashboard-container" bgcolor="white">
          <Profile />
        </Box>
      </Grid2>
      <Grid2 size={8} sx={{ border: "2px solid white" }} className="dashboard-container" p={1} bgcolor="white">
        <Paper sx={{ boxShadow: "none" }}>
          <Box>
            {/* Header row for the interview list */}
            <Grid2 container alignItems="center" spacing={0} p={2} sx={{ borderBottom: "1px solid #ccc" }}>
              <Grid2 size={4}>
                <Typography variant="body2" sx={{ fontWeight: "bold" }}>
                  Title
                </Typography>
              </Grid2>
              <Grid2 size={3}>
                <Typography variant="body2" sx={{ fontWeight: "bold" }}>
                  Difficulty
                </Typography>
              </Grid2>
              <Grid2 size={3}>
                <Typography variant="body2" sx={{ fontWeight: "bold" }}>
                  Score
                </Typography>
              </Grid2>
              <Grid2 size={2}>
                <Typography variant="body2" sx={{ fontWeight: "bold" }}>
                  Date
                </Typography>
              </Grid2>
            </Grid2>

            {/* Map over interviews */}
            {[...interviews].map((interview, index) => (
              <Interview
                key={interview.id}
                interview={interview}
                index={index}
                sx={{
                  backgroundColor: index % 2 === 0 ? "#f5f5f5" : "white",
                }}
              />
            ))}
          </Box>
          <Box sx={{ display: "flex", justifyContent: "space-between", mt: 2 }}>
            <IconButton onClick={handlePreviousPage} disabled={currentPage === 1}>
              <ArrowBackIcon />
            </IconButton>
            <Typography variant="body2">
              Page {currentPage} of {Math.ceil(totalInterviews / interviewsPerPage)}
            </Typography>
            <IconButton onClick={handleNextPage} disabled={currentPage * interviewsPerPage >= totalInterviews}>
              <ArrowForwardIcon />
            </IconButton>
          </Box>
        </Paper>
      </Grid2>
    </Grid2>
  );
};

export default Dashboard;
