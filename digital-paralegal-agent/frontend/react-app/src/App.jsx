import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, AlertTriangle, CheckCircle, Activity, Loader2 } from 'lucide-react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }
    setError('');
    setLoading(true);
    setReport(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setReport(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dark app-container">
      <header className="header">
        <Activity className="icon-large primary-color" />
        <h1>Digital Paralegal Agent</h1>
        <p>AI-Powered Autonomous Legal Risk Analysis</p>
      </header>

      {!report && (
        <main className="upload-section card">
          <div className="upload-box">
            <Upload className="icon-xl text-muted" />
            <h2>Upload Legal Contract</h2>
            <p>Supported formats: PDF, DOCX</p>
            <input type="file" onChange={handleFileChange} accept=".pdf,.docx" className="file-input" />
            <div className="file-info">{file ? file.name : "No file selected"}</div>
            
            <button onClick={handleUpload} disabled={loading} className="btn-primary">
              {loading ? <><Loader2 className="spinner" /> Analyzing...</> : "Run Agent Analysis"}
            </button>
          </div>
          {error && <div className="error-message"><AlertTriangle /> {error}</div>}
        </main>
      )}

      {report && (
        <main className="dashboard">
          <button className="btn-outline back-btn" onClick={() => { setReport(null); setFile(null); }}>
             Upload Another Client
          </button>
          
          <div className="summary-cards">
            <div className="card stat-card">
              <h3>Overall Risk Score</h3>
              <div className={`score ${report.executive_summary.risk_grade.replace(' ', '-').toLowerCase()}`}>
                {report.executive_summary.overall_score}/100
              </div>
              <p>{report.executive_summary.risk_grade}</p>
            </div>
            
            <div className="card stat-card">
              <h3>Agent Metadata</h3>
              <p><strong>File:</strong> {file?.name}</p>
              <p><strong>Chunks Analyzed:</strong> {report.metadata.total_chunks}</p>
              <p><strong>Total Risks:</strong> {report.executive_summary.total_risks_found}</p>
            </div>
          </div>

          <div className="risks-container">
            <h2><AlertTriangle className="icon-medium" /> Detected Risks</h2>
            {report.identified_clauses.length === 0 ? (
              <div className="no-risk card">
                <CheckCircle className="icon-large success-color" />
                <p>No high or medium risks detected in standard categories.</p>
              </div>
            ) : (
              <div className="clause-list">
                {report.identified_clauses.map((clause, idx) => (
                  <div key={idx} className={`card clause-card risk-${clause.risk_level.toLowerCase()}`}>
                    <div className="clause-header">
                       <h4>{clause.clause_type} <span className="category-tag">({clause.searched_category})</span></h4>
                       <span className={`badge badge-${clause.risk_level.toLowerCase()}`}>{clause.risk_level} Risk</span>
                    </div>
                    <p className="explanation">{clause.explanation}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="agent-trace card">
            <h2><Activity className="icon-medium text-muted"/> Agent Reasoning Trace</h2>
            <ul className="trace-list">
              {report.agent_trace.map((trace, idx) => (
                <li key={idx}><strong>{trace.action}:</strong> {trace.result}</li>
              ))}
            </ul>
          </div>
        </main>
      )}
    </div>
  );
}

export default App;
