import React, { useState, useEffect } from "react";
import { Typography } from "@mui/material";
import { useLocation } from "react-router-dom";

const Score = () => {
  const location = useLocation();
  const { analysis } = location.state || { analysis: [] };

  return (
    <>
      <Typography color={"white"}>
        SCORE WILL BE HERE
        <div>
          <h2>Final Analysis:</h2>
          <pre>{JSON.stringify(analysis, null, 2)}</pre>
        </div>
      </Typography>
    </>
  );
};

export default Score;
