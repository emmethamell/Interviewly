import { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneLight, oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { Box, Typography, Paper, IconButton, Tooltip } from "@mui/material";
import Grid2 from "@mui/material/Grid2";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import ReactSpeedometer from "react-d3-speedometer";
import confetti from "canvas-confetti";
import ReactMarkdown from "react-markdown";

// Interview transcript, feedback, final code
const InterviewTranscript = () => {
  const { interviewId } = useParams();
  const [interview, setInterview] = useState([]);
  const [displayMode, setDisplayMode] = useState("light");
  const { user, getAccessTokenSilently } = useAuth0();

  const handleDisplayModeChange = (mode) => {
    setDisplayMode(mode);
  };

  const fetchInterviews = useCallback(async () => {
    try {
      const token = await getAccessTokenSilently();
      const response = await axios.get("http://localhost:5001/interview/get-single-interview", {
        params: {
          interviewId,
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setInterview(response.data);
    } catch (error) {
      console.error("Error fetching interviews:", error);
    }
  }, [getAccessTokenSilently, interviewId]);

  useEffect(() => {
    fetchInterviews();
  }, [user, getAccessTokenSilently, fetchInterviews]);

  // Confetti
  useEffect(() => {
    if (interview.score === "Strong Hire") {
      // First burst
      confetti({
        particleCount: 200,
        spread: 90,
        origin: { y: 0.6, x: 0.4 },
        colors: ["#22c55e", "#15803d", "#84cc16", "#facc15"],
        gravity: 2,
        decay: 0.94,
      });

      // Second burst after a small delay
      setTimeout(() => {
        confetti({
          particleCount: 200,
          spread: 100,
          origin: { y: 0.6, x: 0.6 },
          colors: ["#22c55e", "#15803d", "#84cc16", "#facc15"],
          gravity: 2,
          decay: 0.94,
        });
      }, 200);

      // Third burst back to center
      setTimeout(() => {
        confetti({
          particleCount: 200,
          spread: 100,
          origin: { y: 0.6, x: 0.5 },
          colors: ["#22c55e", "#15803d", "#84cc16", "#facc15"],
          gravity: 2,
          decay: 0.94,
        });
      }, 400);
    }
  }, [interview.score]);

  const scoreToValue = (score) => {
    switch (score) {
      case "Strong No Hire":
        return 10; //0–20
      case "No Hire":
        return 27.5; //20–35
      case "Lean No Hire":
        return 42.5; //35–50
      case "Lean Hire":
        return 57.5; //50–65
      case "Hire":
        return 72.5; //65–80
      case "Strong Hire":
        return 90; //80–100
      default:
        return 10; // N/A
    }
  };

  return (
    <Box sx={{ pl: 5, pr: 5, pt: 2 }}>
      <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
        <Box>
          <Tooltip 
            title={
              <ReactMarkdown className="score-card-code">{interview.question_content}</ReactMarkdown>
            }
            arrow
            placement="right-start"
            componentsProps={{
              tooltip: {
                sx: {
                  bgcolor: 'background.paper',
                  color: 'text.primary',
                  border: '1px solid',
                  borderColor: 'divider',
                  p: 2,
                  maxWidth: '600px',
                  fontSize: '1rem',
                  boxShadow: 1,
                  '& p': { 
                    m: 0,
                    whiteSpace: 'pre-wrap',
                    wordWrap: 'break-word',
                    overflowWrap: 'break-word',
                  }
                }
              }
            }}
          >
            <Typography 
              variant="h6" 
              color="#60a5fa" 
              sx={{ 
                cursor: 'help',
                display: 'inline-block' 
              }}
            >
              {interview.question_name}
            </Typography>
          </Tooltip>
          <Typography variant="h4" sx={{ flexGrow: 1, p: 1 }}>
            Interview Report
          </Typography>
        </Box>
      </Box>

      {/* Two separate Papers side by side */}
      <Box sx={{ display: "flex", gap: 2, alignItems: "stretch", mb: 2 }}>
        {/* Left Paper (Gauge) */}
        <Paper
          sx={{
            width: "30%",
            pt: 4,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}>
          <ReactSpeedometer
            customSegmentStops={[0, 20, 35, 50, 65, 80, 100]}
            segmentColors={["#ef4444", "#f97316", "#facc15", "#84cc16", "#22c55e", "#15803d"]}
            customSegmentLabels={[
              { text: "SNH", position: "OUTSIDE", color: "#555", fontSize: "12px" },
              { text: "NH", position: "OUTSIDE", color: "#555", fontSize: "12px" },
              { text: "LNH", position: "OUTSIDE", color: "#555", fontSize: "12px" },
              { text: "LH", position: "OUTSIDE", color: "#555", fontSize: "12px" },
              { text: "H", position: "OUTSIDE", color: "#555", fontSize: "12px" },
              { text: "SH", position: "OUTSIDE", color: "#555", fontSize: "12px" },
            ]}
            value={scoreToValue(interview.score)}
            minValue={0}
            maxValue={100}
            currentValueText={interview.score}
            height={180}
            width={250}
            needleColor="#334155"
            textColor="#000000"
            ringWidth={25}
            labelFontSize="0"
            valueTextFontSize="20px"
          />
        </Paper>

        {/* Right Paper (Summary) */}
        <Paper sx={{ width: "70%", p: 2 }}>
          <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
            <Typography variant="h6">Summary</Typography>
          </Box>
          <Typography variant="body1" sx={{ fontSize: "1.0rem" }}>
            {interview.summary}
          </Typography>
        </Paper>
      </Box>

      {/* Final Code */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
          <Typography variant="h6">Final Code</Typography>
          <IconButton
            onClick={() => handleDisplayModeChange(displayMode === "light" ? "dark" : "light")}
            sx={{ ml: 1 }}>
            {displayMode === "light" ? <Brightness4Icon /> : <Brightness7Icon />}
          </IconButton>
        </Box>
        <SyntaxHighlighter
          language={interview.language}
          style={displayMode === "light" ? oneLight : oneDark}
          showLineNumbers>
          {interview.final_submission}
        </SyntaxHighlighter>
      </Paper>
    </Box>
  );
};

export default InterviewTranscript;
