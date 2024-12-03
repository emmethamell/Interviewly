import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import Layout from "./components/Layout";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import DifficultySelection from "./components/DifficultySelection";
import io from "socket.io-client";
import Score from "./components/Score";
import LoginButton from "./components/LoginButton";
import LogoutButton from "./components/LogoutButton";
import Profile from "./components/Profile";

import {
  createTheme,
  ThemeProvider,
  CssBaseline,
  Button,
  Grid2,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Box,
  Stack,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

const theme = createTheme({
  palette: {
    primary: {
      main: "#f4a261", // Custom primary color (orange)
    },
    secondary: {
      main: "#ff5722", // Custom secondary color (orange)
    },
    background: {
      default: "#f2f2f2", // Light gray background
    },
    text: {
      primary: "#333333", // Custom text color
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
    const newSocket = io("http://localhost:5001"); // Adjust the URL as needed
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);
  
  /*
  const { isLoading, isAuthenticated, loginWithRedirect } = useAuth0();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    loginWithRedirect();
    return <div>Redirecting...</div>;
  }
    */

  return (
    <ThemeProvider theme={theme}>
      <Router>
      <LoginButton  />
      <LogoutButton />
        <Routes>
          <Route path="/" element={<DifficultySelection socket={socket} />} />
          <Route path="/main" element={<Layout socket={socket} />} />
          <Route path="/score" element={<Score socket={socket} />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>

      </Router>
    </ThemeProvider>
  );
}

export default App;
