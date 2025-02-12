import React, { useState } from "react";
import Split from "react-split";
import { useLocation } from "react-router-dom";
import { Box } from "@mui/material";
import CodeEditor from "./code_editor/CodeEditor";
import AIChat from "./ai_chat/AIChat";

const Layout = ({ auth0UserId }) => {
  const location = useLocation();
  const { difficulty } = location.state || { difficulty: "not selected" };
  const [code, setCode] = useState("");

  return (
    <Box sx={{ height: "100vh", width: "100%" }}>
      <Split className="split" sizes={[35, 65]} minSize={100} gutterSize={4} direction="horizontal">
        <Box sx={{ height: "100%", overflow: "auto" }}>
          <AIChat difficulty={difficulty} code={code} auth0UserId={auth0UserId} />
        </Box>
        <Box sx={{ height: "100%", overflow: "auto" }}>
          <CodeEditor difficulty={difficulty} code={code} setCode={setCode} auth0UserId={auth0UserId} />
        </Box>
      </Split>
    </Box>
  );
};

export default Layout;
