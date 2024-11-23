import React, { useRef, useEffect, useState } from "react";
import MonacoEditor from "react-monaco-editor";
import * as monaco from "monaco-editor";
import { Box, Button, Menu, MenuItem } from "@mui/material";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import { Timer } from "./Timer";
const CodeEditor = ({ difficulty }) => {
  const [language, setLanguage] = useState("javascript");
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);


  const languages = [
    { label: "JavaScript", value: "javascript" },
    { label: "Python", value: "python" },
    { label: "Java", value: "java" },
    { label: "C++", value: "cpp" },
    { label: "TypeScript", value: "typescript" },
  ];

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

  const editorRef = useRef(null);
  const handleEditorDidMount = (editor) => {
    editorRef.current = editor; // Store the editor instance
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
      case 'Easy':
        return 30;
      case 'Medium':
        return 45;
      case 'Hard':
        return 60;
      default:
        return 30;
    }
  };

  monaco.editor.defineTheme("custom-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [{ token: "comment", foreground: "666666" }],
    colors: {
      "editor.background": "#1e1e1e",
      "editor.foreground": "#d4d4d4",
      "editorLineNumber.foreground": "#858585",
      "editor.selectionBackground": "#264f78",
      "editor.inactiveSelectionBackground": "#3a3d41",
    },
  });

  return (
    <Box display="flex" flexDirection="column" height="100%" bgcolor="#1e1e1e">
      {/* Top panel */}
      <Box
        sx={{
          bgcolor: "#1e1e1e",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 1,
          p: 2, // Match AIChat padding
          minHeight: "25px", // Match AIChat height
          flexShrink: 0,
          borderBottom: "2px solid black",
        }}
      >
        <Button
          onClick={handleClick}
          endIcon={<KeyboardArrowDownIcon />}
          size="small"
          sx={{
            color: "white",
            bgcolor: "#333",
            "&:hover": { bgcolor: "#444" },
            // minWidth: "100px",    // Add minimum width
            //  height: "30px"
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
        {/* Add buttons here */}
        {/* Submit Button (Right) */}
        <Timer minutes={getTimerDuration(difficulty)} />
        <Button
          variant="contained"
          size="small"
          sx={{
            bgcolor: "#f4a261",
            "&:hover": { bgcolor: "#e76f51" },
            color: "white",
          }}
          onClick={() => {
            // Handle submit logic here
            console.log("Submitting solution");
          }}
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
            theme="custom-dark"
            value="// Write your code here"
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
          />
        </div>
      </Box>
    </Box>
  );
};

export default CodeEditor;
