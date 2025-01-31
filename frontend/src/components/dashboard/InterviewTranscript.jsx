import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneLight, oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Box, Typography, Paper, IconButton } from "@mui/material";
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

// Interview transcript, feedback, final code
const InterviewTranscript = () => {
  const { interviewId } = useParams();
  const [interview, setInterview] = useState([]);
  const [displayMode, setDisplayMode] = useState("light");
  const { user, getAccessTokenSilently } = useAuth0();
  
  const handleDisplayModeChange = (mode) => {
    setDisplayMode(mode);
  };

  useEffect(() => {
    const fetchInterviews = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await axios.get(
          "http://localhost:5001/interview/get-single-interview",
          {
            params: {
              interviewId,
            },
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
        setInterview(response.data);
      } catch (error) {
        console.error("Error fetching interviews:", error);
      }
    };

    fetchInterviews();
  }, [user, getAccessTokenSilently]);

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
          Interview Report
        </Typography>
      </Box>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Details</Typography>
        <Typography variant="body1">Score: {interview.score}</Typography>
        <Typography variant="body1">Language: {interview.language}</Typography>
        <Typography variant="body1">
          Technical Ability: {interview.technical_ability}
        </Typography>
        <Typography variant="body1">
          Problem Solving: {interview.problem_solving_score}
        </Typography>
        <Typography variant="body1">Summary: {interview.summary}</Typography>
      </Paper>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">Final Code</Typography> 
          <IconButton onClick={() => handleDisplayModeChange(displayMode === 'light' ? 'dark' : 'light')}>
            {displayMode === 'light' ? <Brightness4Icon /> : <Brightness7Icon />}
          </IconButton>
        </Box>
        <SyntaxHighlighter 
          language={interview.language} 
          style={displayMode === "light" ? oneLight : oneDark}
          showLineNumbers={true}
        >
          {interview.final_submission}
        </SyntaxHighlighter>
      </Paper>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Transcript</Typography>
        {interview.transcript}
      </Paper>
    </Box>
  );
};

export default InterviewTranscript;
