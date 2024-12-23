import { useState, useEffect } from "react";
import "./App.css";
import Layout from "./components/mock_interview/Layout";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import DifficultySelection from "./components/setup/DifficultySelection";
import io from "socket.io-client";
import Score from "./components/interview_analysis/Score";
import Profile from "./components/profile/Profile";
import LandingPage from "./components/landing_page/LandingPage";
import Dashboard from "./components/dashboard/Dashboard";
import { createTheme, ThemeProvider } from "@mui/material";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import axios from "axios";
import ConditionalNavbar from "./components/navbar/ConditionalNavbar";

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
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = io("http://localhost:5001");
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  useEffect(() => {
    if (isAuthenticated && user) {
      const storeUser = async () => {
        const token = await getAccessTokenSilently();
        const auth0_user_id = user.sub;
        const name = user.name;
        const email = user.email;

        axios
          .post(
            "http://localhost:5001/auth/signup",
            { auth0_user_id, name, email },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            },
          )
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.error(error);
          });
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
          {/* Public Route */}
          <Route path="/" element={<LandingPage className="landing-page" />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute
                element={<Dashboard className="dashboard-page" />}
              />
            }
          />
          <Route
            path="/selection"
            element={
              <ProtectedRoute
                element={
                  <DifficultySelection
                    className="difficult-selection-page"
                    socket={socket}
                  />
                }
              />
            }
          />
          <Route
            path="/main"
            element={
              <ProtectedRoute
                element={<Layout className="layout-page" socket={socket} />}
              />
            }
          />
          <Route
            path="/score"
            element={
              <ProtectedRoute
                element={<Score className="score-page" socket={socket} />}
              />
            }
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
