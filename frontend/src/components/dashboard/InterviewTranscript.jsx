import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { solarizedlight } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Box, Typography, Paper } from "@mui/material";

// Interview transcript, feedback, final code
const InterviewTranscript = () => {
  const { interviewId } = useParams();
  const [interview, setInterview] = useState([]);
  const { user, getAccessTokenSilently } = useAuth0();
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
      <Typography variant="h4" gutterBottom>
        Interview Transcript
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        Transcript for interview ID: {interviewId}
      </Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Transcript</Typography>
        {interview.transcript}
      </Paper>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6">Final Code</Typography>
        <SyntaxHighlighter language={interview.language} style={solarizedlight}>
          {interview.final_submission}
        </SyntaxHighlighter>
      </Paper>
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
    </Box>
  );
};

export default InterviewTranscript;
