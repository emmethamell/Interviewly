import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { solarizedlight } from "react-syntax-highlighter/dist/esm/styles/prism";

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
          "http://localhost:5001/routes/get-single-interview",
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
    <div>
      <h1>Interview Transcript</h1>
      <p>Transcript for interview ID: {interviewId}</p>
      <p>{interview.transcript}</p>
      <p>SCORE: {interview.score}</p>
      <SyntaxHighlighter language={interview.language} style={solarizedlight}>
        {interview.final_submission}
      </SyntaxHighlighter>
      <p> LANGUAGE: {interview.language}</p>
      <p>Tech abil: {interview.technical_ability}</p>
      <p>Prob solve: {interview.problem_solving_score}</p>
      <p>Summary: {interview.summary}</p>
    </div>
  );
};

export default InterviewTranscript;
