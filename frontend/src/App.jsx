import UploadResume from "./components/UploadResume";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>AI Resume Analyzer</h1>
        <p>AI-Powered ATS Resume Screening System</p>
      </header>

      <UploadResume />
    </div>
  );
}

export default App;
