import { useState, useEffect } from "react";
import "./App.css";
import Layout from "./components/mock_interview/Layout";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import DifficultySelection from "./components/setup/DifficultySelection";
import io from "socket.io-client";
import Score from "./components/interview_analysis/Score";
import LoginButton from "./components/auth/LoginButton";
import LogoutButton from "./components/auth/LogoutButton";
import Profile from "./components/profile/Profile";
import LandingPage from "./components/landing_page/LandingPage";
import Dashboard from "./components/dashboard/Dashboard";
import { createTheme, ThemeProvider } from "@mui/material";
import ProtectedRoute from "./components/auth/ProtectedRoute";

const theme = createTheme({
  palette: {
    primary: {
      main: "#f4a261", // Main orange color
    },
    secondary: {
      //main: "#FFFFFF",
      main: "#ff5722", // Custom secondary color (orange)
    },
    background: {
      default: "#FFFFFF",
      //default: "#f2f2f2", // Light gray background
    },
    text: {
      default: "#FFFFFF", //white
    },
  },
  typography: {
    fontFamily: ["JetBrains Mono", "monospace"].join(","),

    h1: {
      fontSize: "0.9rem",
    },
    body1: {
      fontSize: "0.9rem",
    },
  },
});

function App() {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = io("http://localhost:5001");
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <LoginButton />
        <LogoutButton />
        <Routes>
          {/* Public Route */}
          <Route path="/" element={<LandingPage />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={<ProtectedRoute element={<Dashboard />} />}
          />
          <Route
            path="/selection"
            element={
              <ProtectedRoute
                element={<DifficultySelection socket={socket} />}
              />
            }
          />
          <Route
            path="/main"
            element={<ProtectedRoute element={<Layout socket={socket} />} />}
          />
          <Route
            path="/score"
            element={<ProtectedRoute element={<Score socket={socket} />} />}
          />
          <Route
            path="/profile"
            element={<ProtectedRoute element={<Profile />} />}
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
