import React, { useRef, useEffect, useState } from "react";
import MonacoEditor from "react-monaco-editor";
import * as monaco from "monaco-editor";
import { Box, Button, Menu, MenuItem } from "@mui/material";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const CodeEditor = () => {
  const [language, setLanguage] = useState('javascript');
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const languages = [
    { label: 'JavaScript', value: 'javascript' },
    { label: 'Python', value: 'python' },
    { label: 'Java', value: 'java' },
    { label: 'C++', value: 'cpp' },
    { label: 'TypeScript', value: 'typescript' }
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
    <Box display="flex" flexDirection="column" height="100%" bgcolor="#1e1e1e" >
      <Box
        sx={{
          bgcolor: "#1e1e1e",
          display: "flex",
          alignItems: "center",
          gap: 1,
          p: 2, // Match AIChat padding
          minHeight: "25px", // Match AIChat height
          flexShrink: 0 
        }}
      >
        {/* Add buttons here */}
        
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

      {/* Bottom Panel */}
      <Box
        sx={{
          borderTop: "2px solid black",
          bgcolor: "#1e1e1e",
          display: "flex",
          alignItems: "center",
          gap: 1,
          p: 2, // Match AIChat padding
          minHeight: "20px", // Match AIChat height
          flexShrink: 0
        }}
      >
        <Button
          onClick={handleClick}
          endIcon={<KeyboardArrowDownIcon />}
          sx={{ 
            color: 'white',
            bgcolor: '#333',
            '&:hover': { bgcolor: '#444' },
            
          }}
        >
          {languages.find(l => l.value === language)?.label || 'Select Language'}
        </Button>
        <Menu
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
        >
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
        
      </Box>
    </Box>
  );
};

export default CodeEditor;
