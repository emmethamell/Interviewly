import React, { useState, useEffect, useRef } from "react";
import SplitPane from "react-split-pane";
import { useLocation } from "react-router-dom";
import { Box } from "@mui/material";
import CodeEditor from "./code_editor/CodeEditor";
import AIChat from "./ai_chat/AIChat";

const Layout = ({ socket }) => {
  const location = useLocation();
  const { difficulty } = location.state || { difficulty: "not selected" };

  const [code, setCode] = useState("");

  const hasEmittedRef = useRef(false);

  useEffect(() => {
    if (socket && !hasEmittedRef.current) {
      socket.emit("select_difficulty", { difficulty });
      hasEmittedRef.current = true;
    }
  }, [socket, difficulty, hasEmittedRef]);

  return (
    <Box
      sx={{
        height: "100%",
        overflow: "hidden",
        bgcolor: "#1e1e1e",
      }}>
      <SplitPane
        split="vertical"
        minSize={200}
        defaultSize="35%"
        className="custom-split-pane"
        style={{
          width: "100%",
          height: "100%",
        }}>
        {/* Left Pane */}
        <Box sx={{ height: "100%", overflow: "auto" }}>
          <AIChat difficulty={difficulty} socket={socket} code={code} />
        </Box>

        {/* Right Pane */}
        <Box sx={{ height: "100%", overflow: "auto" }}>
          <CodeEditor difficulty={difficulty} code={code} setCode={setCode} socket={socket} />
        </Box>
      </SplitPane>
    </Box>
  );
};

export default Layout;
