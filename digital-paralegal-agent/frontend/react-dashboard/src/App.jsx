import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Activity, ShieldAlert, CheckCircle, Database, FileText, Loader2 } from 'lucide-react';
import './index.css';

function App() {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [systemState, setSystemState] = useState('idle'); // idle -> analyzing -> complete
  
  // Streams & States
  const [traceLog, setTraceLog] = useState([]);
  const [activeStreamCategory, setActiveStreamCategory] = useState(null);
  const [streamBuffer, setStreamBuffer] = useState('');
  const [finalReport, setFinalReport] = useState(null);
  const [memoryStats, setMemoryStats] = useState(null);

  const scrollRef = useRef(null);

  // Auto-scroll trace log
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [traceLog, streamBuffer]);

  // Fetch memory stats on load
  useEffect(() => {
    fetch('http://127.0.0.1:8000/memory/status')
      .then(res => res.json())
      .then(data => setMemoryStats(data))
      .catch(() => setMemoryStats({ status: 'error', chunks_in_memory: 0 }));
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    
    setIsProcessing(true);
    setSystemState('analyzing');
    setTraceLog([]);
    setFinalReport(null);
    setStreamBuffer('');
    setActiveStreamCategory(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      // Connect to SSE Endpoint
      const response = await fetch('http://127.0.0.1:8000/analyze/stream', {
        method: 'POST',
        body: formData,
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // keep the last partial line in buffer

        for (const line of lines) {
          if (line.trim() === '') continue;
          
          if (line.startsWith('data: ')) {
            const dataStr = line.replace('data: ', '').trim();
            if (dataStr === '[DONE]') {
               setSystemState('complete');
               setIsProcessing(false);
               break;
            }

            try {
              const parsed = JSON.parse(dataStr);

              // 1. Planner Trace Events
              if (parsed.type === 'trace') {
                setTraceLog(prev => [...prev, parsed]);
              }
              // 2. LLM Stream Start
              else if (parsed.type === 'stream_start') {
                setActiveStreamCategory(parsed.category);
                setStreamBuffer('');
              }
              // 3. Raw Token
              else if (parsed.token) {
                setStreamBuffer(prev => prev + parsed.token);
              }
              // 4. LLM Stream End
              else if (parsed.type === 'stream_end') {
                setActiveStreamCategory(null);
              }
              // 5. Final Report
              else if (parsed.type === 'final_report') {
                setFinalReport(parsed.report);
              }
            } catch (e) {
               console.warn("SSE Parse Error:", dataStr);
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setTraceLog(prev => [...prev, { agent: 'System', action: 'Error', result: 'Connection failed.' }]);
      setIsProcessing(false);
    }
  };

  return (
    <div className="dark app-container">
      {/* HEADER */}
      <motion.header 
        initial={{ y: -50, opacity: 0 }} 
        animate={{ y: 0, opacity: 1 }}
        className="header"
      >
        <div className="title-area">
           <Activity className="icon-large primary-color" />
           <div>
             <h1>Autonomous Digital Paralegal</h1>
             <p className="text-muted">Multi-Agent Planner & Streaming RAG Framework</p>
           </div>
        </div>
        
        {memoryStats && (
            <div className="memory-badge">
               <Database className="icon-small" />
               ChromaDB: {memoryStats.chunks_in_memory} Vectors Ready
            </div>
        )}
      </motion.header>

      {/* UPLOAD PANEL */}
      <AnimatePresence>
        {systemState === 'idle' && (
          <motion.main 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0, height: 0 }}
            className="upload-panel card"
          >
            <Upload className="icon-xl text-muted" />
            <h2>Initialize Autonomous Review</h2>
            <p>Upload a PDF or DOCX to trigger the agent swarm.</p>
            
            <input 
              type="file" 
              onChange={(e) => setFile(e.target.files[0])} 
              accept=".pdf,.docx" 
              className="file-input" 
            />
            
            <button 
              onClick={handleUpload} 
              disabled={!file || isProcessing} 
              className="btn-primary"
            >
              Launch Core Agents
            </button>
          </motion.main>
        )}
      </AnimatePresence>

      {/* ACTIVE ANALYZER PANEL */}
      {(systemState === 'analyzing' || systemState === 'complete') && (
        <main className="dashboard-grid">
          
          {/* Agent Reasoning Stream */}
          <motion.div 
            initial={{ x: -20, opacity: 0 }} 
            animate={{ x: 0, opacity: 1 }}
            className="card reasoning-card"
          >
            <h2><Activity className="icon-medium text-muted"/> Agent Planner Trace</h2>
            <div className="trace-scroll-area" ref={scrollRef}>
               <AnimatePresence>
                 {traceLog.map((trace, idx) => (
                   <motion.div 
                     key={idx}
                     initial={{ opacity: 0, y: 10 }}
                     animate={{ opacity: 1, y: 0 }}
                     className={`trace-item agent-${trace.agent.toLowerCase()}`}
                   >
                     <span className="agent-tag">[{trace.agent}]</span>
                     <span className="action-tag">{trace.action}:</span>
                     <span className="trace-result">{trace.result}</span>
                   </motion.div>
                 ))}
                 
                 {/* Live Streaming LLM Render */}
                 {activeStreamCategory && (
                    <motion.div 
                       initial={{ opacity: 0 }}
                       animate={{ opacity: 1 }}
                       className="live-llm-stream"
                    >
                       <span className="streaming-badge">
                          <Loader2 className="spinner icon-small" /> Streaming Analysis: {activeStreamCategory}
                       </span>
                       <div className="stream-buffer-view">
                          {streamBuffer}
                          <span className="cursor-blink">|</span>
                       </div>
                    </motion.div>
                 )}
               </AnimatePresence>
            </div>
          </motion.div>

          {/* Final Results Panel */}
          <motion.div 
            initial={{ x: 20, opacity: 0 }} 
            animate={{ x: 0, opacity: 1 }}
            className={`card results-card ${systemState === 'analyzing' ? 'blur-overlay' : ''}`}
          >
             <h2><ShieldAlert className="icon-medium primary-color" /> Intelligence Report</h2>
             
             {!finalReport ? (
                 <div className="processing-state">
                   <Loader2 className="spinner icon-xl text-muted" />
                   <p>Awaiting Consensus from Swarm...</p>
                 </div>
             ) : (
                 <div className="final-report-view">
                    <div className="score-header">
                       <div className="score-box">
                         <span className="score-val">{finalReport.executive_summary.overall_risk_score}</span>
                         <span className="score-lbl">Risk Index</span>
                       </div>
                       <div className="grade-box">
                          {finalReport.executive_summary.risk_grade}
                       </div>
                    </div>
                    
                    <h3 className="section-title">Flagged Clauses</h3>
                    <div className="clauses-list">
                       {finalReport.clause_analysis.map((clause, idx) => (
                          <motion.div 
                            initial={{ scale: 0.95, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ delay: idx * 0.1 }}
                            key={idx} className={`clause-highlight risk-${clause.risk_level.toLowerCase()}`}
                          >
                             <div className="c-head">
                                <strong>{clause.clause_type}</strong>
                                <span className={`badge badge-${clause.risk_level.toLowerCase()}`}>{clause.risk_level}</span>
                             </div>
                             <p className="c-reasoning">{clause.explanation}</p>
                          </motion.div>
                       ))}
                       {finalReport.clause_analysis.length === 0 && (
                          <p className="no-risks-found"><CheckCircle/> No critical vulnerabilities detected.</p>
                       )}
                    </div>
                    
                    <button className="btn-outline mt-2" onClick={() => window.location.reload()}>
                       Reset Swarm
                    </button>
                 </div>
             )}
          </motion.div>
          
        </main>
      )}
    </div>
  );
}

export default App;
