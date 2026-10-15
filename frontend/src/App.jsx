
import { useEffect, useState } from "react";
import "./App.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [selectedFilename, setSelectedFilename] = useState("");

  async function loadHistory() {
    setHistoryLoading(true);

    try {
      const response = await fetch(`${API}/api/history`);

      if (!response.ok) {
        throw new Error("Could not load analysis history.");
      }

      const data = await response.json();
      setHistory(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setHistoryLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      setError("Please select a PDF resume.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError("The PDF must be smaller than 5 MB.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");
    setResults([]);
    setSelectedFilename("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API}/api/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Resume analysis failed.");
      }

      if (!Array.isArray(data.results)) {
        throw new Error("The server returned unexpected results.");
      }

      setResults(data.results);
      setSelectedFilename(file.name);
      setMessage("Resume analyzed successfully.");

      await loadHistory();

      document.getElementById("results-section")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  function viewResults(item) {
    if (!Array.isArray(item.results)) {
      setError(
        "Saved results are missing or invalid. Please analyze this resume again."
      );
      setMessage("");
      return;
    }

    setResults(item.results);
    setSelectedFilename(item.filename || "Saved analysis");
    setError("");
    setMessage(`Showing saved results for ${item.filename || "this resume"}.`);

    setTimeout(() => {
      document.getElementById("results-section")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }, 50);
  }

  return (
    <main className="container">
      <header className="hero">
        <p className="eyebrow">AI-POWERED CAREER TOOL</p>
        <h1>Resume Intelligence</h1>
        <p>
          Discover matching jobs, identify skill gaps, and plan
          your next learning steps.
        </p>
      </header>

      <section className="panel">
        <h2>Analyze your resume</h2>
        <p>Upload a text-based PDF resume (maximum 5 MB).</p>

        <form onSubmit={handleSubmit}>
          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(event) => {
              setFile(event.target.files?.[0] || null);
              setError("");
              setMessage("");
            }}
          />

          <button type="submit" disabled={loading}>
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </form>

        {loading && (
          <p className="muted">
            Analyzing your resume. The first run may take longer
            while the AI model loads.
          </p>
        )}

        {error && <p className="error">{error}</p>}
        {message && <p className="success">{message}</p>}
      </section>

      <section id="results-section">
        {results.length > 0 && (
          <>
            <h2>Ranked job matches</h2>

            {selectedFilename && (
              <p className="muted">Results for: {selectedFilename}</p>
            )}

            <p className="muted">
              Similarity scores compare resume text with job descriptions.
              They are indicators, not probabilities of getting hired.
            </p>

            {results.map((job, index) => (
              <article
                className="job-card"
                key={`${job.job_id ?? job.title}-${index}`}
              >
                <div className="job-heading">
                  <div>
                    <h3>{job.title}</h3>
                    <p>{job.company} · {job.location}</p>
                  </div>

                  <div className="score">
                    {Number(job.similarity_score ?? 0).toFixed(1)}%
                    <small>Similarity</small>
                  </div>
                </div>

                <div>
                  <strong>Matched skills</strong>
                  <div className="tags">
                    {(job.matched_skills || []).length ? (
                      job.matched_skills.map((skill) => (
                        <span className="tag matched" key={skill}>
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="muted">No matched skills detected</span>
                    )}
                  </div>
                </div>

                <div>
                  <strong>Missing or unmentioned skills</strong>
                  <div className="tags">
                    {(job.missing_skills || []).length ? (
                      job.missing_skills.map((skill) => (
                        <span className="tag missing" key={skill}>
                          {skill}
                        </span>
                      ))
                    ) : (
                      <span className="muted">
                        No missing skills detected by the current checker
                      </span>
                    )}
                  </div>
                </div>

                <div className="recommendations">
                  <strong>Recommended next steps</strong>

                  {(job.recommendations || []).length ? (
                    job.recommendations.map((item) => (
                      <div className="recommendation-item" key={item.skill}>
                        <p>
                          <strong>{item.skill}</strong>{" "}
                          <span className="priority">
                            {item.priority} priority
                          </span>
                        </p>
                        <p>{item.action}</p>
                        <p>
                          <strong>Practice project:</strong> {item.project}
                        </p>
                      </div>
                    ))
                  ) : (
                    <p className="muted">
                      No additional recommendations for this result.
                      Older saved analyses may not include recommendations.
                    </p>
                  )}
                </div>

                <details>
                  <summary>View all detected skills</summary>
                  <p>
                    <strong>Resume skills:</strong>{" "}
                    {(job.resume_skills || []).join(", ") || "None detected"}
                  </p>
                  <p>
                    <strong>Required skills:</strong>{" "}
                    {(job.required_skills || []).join(", ") || "None detected"}
                  </p>
                </details>
              </article>
            ))}
          </>
        )}
      </section>

      <section className="panel">
        <h2>Recent analysis history</h2>

        {historyLoading ? (
          <p className="muted">Loading analysis history...</p>
        ) : history.length === 0 ? (
          <p className="muted">
            No analyses yet. Upload a resume to begin.
          </p>
        ) : (
          history.map((item) => (
            <div className="history-item" key={item.id}>
              <div>
                <strong>{item.filename}</strong>
                <p className="muted">
                  {item.created_at
                    ? new Date(item.created_at).toLocaleString()
                    : "Date unavailable"}
                </p>
              </div>

              <button
                type="button"
                className="secondary"
                onClick={() => viewResults(item)}
              >
                View results
              </button>
            </div>
          ))
        )}
      </section>

      <footer>
        Resume Intelligence · Built with React, FastAPI and NLP
      </footer>
    </main>
  );
}

export default App;
