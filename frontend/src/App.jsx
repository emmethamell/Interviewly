import { useState, useEffect } from "react";
import "./App.css";
import Layout from "./components/mock_interview/Layout";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import DifficultySelection from "./components/setup/DifficultySelection";
import Profile from "./components/profile/Profile";
import LandingPage from "./components/landing_page/LandingPage";
import Dashboard from "./components/dashboard/Dashboard";
import { createTheme, ThemeProvider } from "@mui/material";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import axios from "axios";
import ConditionalNavbar from "./components/navbar/ConditionalNavbar";
import InterviewTranscript from "./components/dashboard/InterviewTranscript";

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
    fontFamily: ["Roboto"].join(","),

    h1: {
      fontSize: "0.9rem",
    },
    body1: {
      fontSize: "0.9rem",
    },
  },
});

function ScrollHandler() {
  const location = useLocation();

  useEffect(() => {
    // Add or remove `layout-active` based on the current route
    if (location.pathname === "/main") {
      document.documentElement.classList.add("layout-active");
    } else {
      document.documentElement.classList.remove("layout-active");
    }
  }, [location.pathname]);

  return null;
}

function App() {
  const { isAuthenticated, user, getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    if (isAuthenticated && user) {
      const storeUser = async () => {
        try {
          const token = await getAccessTokenSilently();
          const auth0_user_id = user.sub;
          const name = user.name;
          const email = user.email;

          await axios.post(
            `${import.meta.env.VITE_API_URL}/auth/signup`,
            { auth0_user_id, name, email },
            {
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
              },
            },
          );
        } catch (error) {
          console.error(error);
        }
      };

      storeUser();
    }
  }, [isAuthenticated, user, getAccessTokenSilently]);

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <ScrollHandler />
        <ConditionalNavbar />
        <Routes>
          <Route path="/" element={<LandingPage className="landing-page" />} />
          <Route path="/dashboard" element={<ProtectedRoute element={<Dashboard className="dashboard-page" />} />} />
          <Route
            path="/selection"
            element={<ProtectedRoute element={<DifficultySelection className="difficulty-selection-page" />} />}
          />
          <Route
            path="/main"
            element={<ProtectedRoute element={<Layout className="layout-page" auth0UserId={user?.sub} />} />}
          />
          <Route path="/profile" element={<ProtectedRoute element={<Profile />} />} />
          <Route path="/transcript/:interviewId" element={<ProtectedRoute element={<InterviewTranscript />} />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
