import { useState } from "react";
import axios from "axios";
import {
  CircularProgressbar,
  buildStyles,
} from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

function UploadResume() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [jobDescription, setJobDescription] = useState("");

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF.");
      return;
    }

    if (!jobDescription.trim()) {
  alert("Please paste the Job Description.");
  return;
}

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Backend connection failed.");
    } finally {
      setLoading(false);
    }
  };

  // Inline styling object for a modern UI
  const styles = {
    container: {
      fontFamily: "'Segoe UI', Roboto, sans-serif",
      backgroundColor: "#0f172a",
      color: "#f8fafc",
      minHeight: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      padding: "20px",
    },
    card: {
      backgroundColor: "#1e293b",
      borderRadius: "16px",
      boxShadow: "0 10px 25px rgba(0,0,0,0.3)",
      width: "100%",
      maxWidth: "950px",
      padding: "32px",
      textAlign: "center",
      border: "1px solid #334155",
    },
    title: {
      fontSize: "24px",
      fontWeight: "700",
      marginBottom: "8px",
      color: "#f8fafc",
    },
    subtitle: {
      fontSize: "14px",
      color: "#94a3b8",
      marginBottom: "24px",
    },
    dropzone: {
      border: "2px dashed #3b82f6",
      borderRadius: "12px",
      padding: "30px 20px",
      backgroundColor: "#1e293b",
      cursor: "pointer",
      transition: "all 0.3s ease",
      position: "relative",
      marginBottom: "20px",
    },
    fileInput: {
      position: "absolute",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      opacity: 0,
      cursor: "pointer",
    },
    button: {
      width: "100%",
      padding: "12px",
      backgroundColor: loading ? "#64748b" : "#2563eb",
      color: "#fff",
      border: "none",
      borderRadius: "8px",
      fontSize: "16px",
      fontWeight: "600",
      cursor: loading ? "not-allowed" : "pointer",
      transition: "background 0.2s",
    },
    resultContainer: {
      marginTop: "32px",
      textAlign: "left",
      borderTop: "1px solid #334155",
      paddingTop: "24px",
    },
    scoreWrapper: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      backgroundColor: "#0f172a",
      padding: "16px",
      borderRadius: "8px",
      marginBottom: "20px",
    },
    scoreBadge: {
      fontSize: "24px",
      fontWeight: "800",
      color: "#10b981",
    },
    skillsGrid: {
      display: "flex",
      flexWrap: "wrap",
      gap: "8px",
      padding: 0,
      listStyle: "none",
    },
    skillTag: {
      backgroundColor: "#334155",
      color: "#e2e8f0",
      padding: "6px 12px",
      borderRadius: "20px",
      fontSize: "13px",
      fontWeight: "500",
    },
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>AI Resume Analyzer</h1>
        <p style={styles.subtitle}>Upload your PDF resume to check your ATS compatibility</p>

        {/* Custom File Upload Box */}
        <div style={styles.dropzone}>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            style={styles.fileInput}
          />
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{marginBottom: '10px'}}>
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          <p style={{ margin: "5px 0 0 0", fontSize: "14px", fontWeight: "500" }}>
            {file ? file.name : "Click or drag PDF here"}
          </p>
        </div>

       {/* Job Description */}
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the Job Description here..."
          rows={8}
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "20px",
            borderRadius: "10px",
            border: "1px solid #334155",
            background: "#0f172a",
            color: "#fff",
            fontSize: "14px",
            resize: "vertical",
            outline: "none",
            boxSizing: "border-box",
          }}
        />

        <button 
          onClick={handleUpload} 
          disabled={loading}
          style={styles.button}
        >
          {loading ? "Analyzing Profile..." : "Analyze Resume"}
        </button>

        {/* Output Section */}
        {result && (
          <div style={styles.resultContainer}>
          <div
  style={{
    display: "flex",
    alignItems: "center",
    gap: "30px",
    marginBottom: "30px",
  }}
>
  <div
  style={{
  display: "flex",
  alignItems: "center",
  gap: "30px",
  background: "#0f172a",
  padding: "25px",
  borderRadius: "15px",
  marginBottom: "30px",
  border: "1px solid #334155",
}}
>
    <CircularProgressbar
      value={result["ATS Score"]}
      text={`${result["ATS Score"]}%`}
      styles={buildStyles({
        textColor: "#ffffff",
        pathColor:
          result["ATS Score"] >= 80
            ? "#22c55e"
            : result["ATS Score"] >= 60
            ? "#f59e0b"
            : "#ef4444",
        trailColor: "#334155",
        textSize: "16px",
      })}
    />
  </div>

  <div>
    <h2
      style={{
        margin: 0,
        color: "#ffffff",
      }}
    >
      ATS Analysis
    </h2>

    <p
      style={{
        color: "#94a3b8",
        marginTop: "10px",
      }}
    >
      Resume Match Score
    </p>

    <h1
      style={{
        fontSize: "40px",
        margin: 0,
        color:
          result["ATS Score"] >= 80
            ? "#22c55e"
            : result["ATS Score"] >= 60
            ? "#f59e0b"
            : "#ef4444",
      }}
    >
      {result["ATS Score"]}%
    </h1>
  </div>
</div>

            <h3 style={{ fontSize: "16px", marginBottom: "12px", color: "#94a3b8" }}>Matched Skills</h3>
            <ul style={styles.skillsGrid}>
              {result["Matched Skills"] && result["Matched Skills"].length > 0 ? (
                result["Matched Skills"].map((skill, index) => (
                  <li key={index} style={styles.skillTag}>
                    {skill}
                  </li>
                ))
              ) : (
                <span style={{ fontSize: "14px", color: "#64748b" }}>No direct matches found.</span>
              )}
            </ul>
            <h3 style={{ fontSize: "16px", marginTop: "20px", marginBottom: "12px", color: "#94a3b8" }}>
  Missing Skills
</h3>

<ul style={styles.skillsGrid}>
  {result["Missing Skills"]?.length > 0 ? (
    result["Missing Skills"].map((skill, index) => (
      <li
        key={index}
        style={{
          ...styles.skillTag,
          backgroundColor: "#7f1d1d",
        }}
      >
        {skill}
      </li>
    ))
  ) : (
    <span>No missing skills 🎉</span>
  )}
</ul>

<h3 style={{ fontSize: "16px", marginTop: "20px", marginBottom: "12px", color: "#94a3b8" }}>
  AI Feedback
</h3>

<div
  style={{
    background: "#0f172a",
    padding: "15px",
    borderRadius: "10px",
    whiteSpace: "pre-wrap",
    lineHeight: "1.6",
  }}
>
  {result["AI Feedback"]}
</div>

<h3 style={{ fontSize: "16px", marginTop: "20px", marginBottom: "12px", color: "#94a3b8" }}>
  Resume Preview
</h3>

<pre
  style={{
    background: "#0f172a",
    padding: "15px",
    borderRadius: "10px",
    color: "#e2e8f0",
    overflowX: "auto",
    whiteSpace: "pre-wrap",
  }}
>
  {result["Preview"]}
</pre>

         </div>
        )}
          
      </div>
    </div>
  );
}

export default UploadResume;