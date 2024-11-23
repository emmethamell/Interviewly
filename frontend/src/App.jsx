import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import Layout from "./components/Layout";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DifficultySelection from "./components/DifficultySelection";
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
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/" element={<DifficultySelection />} />
          <Route path="/main" element={<Layout />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
