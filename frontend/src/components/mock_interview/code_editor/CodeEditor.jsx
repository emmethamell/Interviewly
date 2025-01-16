import { useRef, useEffect, useState } from "react";
import MonacoEditor from "react-monaco-editor";
import { Box, Button, Menu, MenuItem } from "@mui/material";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import { Timer } from "./Timer";
import { useNavigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import * as monaco from "monaco-editor";

const CodeEditor = ({ difficulty, code, setCode, socket }) => {
  const [language, setLanguage] = useState("javascript");
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const navigate = useNavigate();
  const { user } = useAuth0();
  const userId = user?.sub;

  const languages = [
    { label: "JavaScript", value: "javascript" },
    { label: "Python", value: "python" },
    { label: "Java", value: "java" },
    { label: "C++", value: "cpp" },
    { label: "TypeScript", value: "typescript" },
  ];

  useEffect(() => {
    if (socket) {
      socket.on("final_analysis", (data) => {
        navigate("/score", {
          state: { analysis: data.analysis, loading: false },
        });
      });

      return () => {
        socket.off("final_analysis");
      };
    }
  }, [socket, navigate]);

  const handleSubmit = () => {
    if (socket) {
      socket.emit("submit_solution", { userId, code, language });
      navigate("/score", { state: { loading: true } });
    }
  };

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLanguageSelect = (value) => {
    setLanguage(value);
    handleClose();
  };

  const editorContainerRef = useRef(null);
  const [dimensions, setDimensions] = useState({
    width: 0,
    height: 0,
  });

  // Editor resizing
  useEffect(() => {
    const resizeObserver = new ResizeObserver(() => {
      if (editorContainerRef.current) {
        setDimensions({
          width: editorContainerRef.current.offsetWidth,
          height: editorContainerRef.current.offsetHeight,
        });
      }
    });
    resizeObserver.observe(editorContainerRef.current);

    return () => resizeObserver.disconnect();
  }, []);

  const getTimerDuration = (difficulty) => {
    switch (difficulty) {
      case "Easy":
        return 30;
      case "Medium":
        return 45;
      case "Hard":
        return 60;
      default:
        return 30;
    }
  };

  return (
    <Box display="flex" flexDirection="column" height="100%" bgcolor="#1e1e1e">
      {/* Top panel */}
      <Box
        sx={{
          bgcolor: "#F5F5F5",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 1,
          p: 2,
          minHeight: "25px",
          flexShrink: 0,
          borderBottom: "2px solid black",
        }}
      >
        <Button
          onClick={handleClick}
          endIcon={<KeyboardArrowDownIcon />}
          size="small"
          sx={{
            color: "black",
            width: "120px",
            border: "1px solid #BDBDBD",
            bgcolor: "#E0E0E0",
            "&:hover": { bgcolor: "#D6D6D6" },
          }}
        >
          {languages.find((l) => l.value === language)?.label ||
            "Select Language"}
        </Button>
        <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
          {languages.map((lang) => (
            <MenuItem
              key={lang.value}
              onClick={() => handleLanguageSelect(lang.value)}
              selected={language === lang.value}
            >
              {lang.label}
            </MenuItem>
          ))}
        </Menu>
        {/* Submit Button (Right) */}
        <Timer minutes={getTimerDuration(difficulty)} onTimeUp={handleSubmit} />
        <Button
          variant="outlined"
          size="small"
          sx={{
            backgroundColor: "#f4a261",
            border: "1px solid #e76f51",
            color: "white",
            "&:hover": {
              backgroundColor: "#e08e57",
            },
          }}
          onClick={() => handleSubmit()}
        >
          Submit Solution
        </Button>
      </Box>

      <Box flex={1} position="relative" minHeight="200px">
        <div
          ref={editorContainerRef}
          style={{
            width: "100%",
            height: "100%",
          }}
        >
          <MonacoEditor
            width={dimensions.width}
            height={dimensions.height}
            language={language}
            theme="v5"
            value={code}
            options={{
              fontSize: 16,
              fontFamily: "Fira Code, Consolas, monospace",
              lineNumbers: "on",
              wordWrap: "on",
              automaticLayout: true,
              padding: {
                top: 20,
              },
              minimap: {
                enabled: false,
              },
            }}
            onChange={(newValue) => setCode(newValue)}
          />
        </div>
      </Box>
    </Box>
  );
};

export default CodeEditor;
