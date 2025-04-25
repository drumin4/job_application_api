import React, { useState } from 'react';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [matchResults, setMatchResults] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://localhost:8000/upload_resume", {
      method: "POST",
      body: formData,
    });

    const response = await fetch("http://localhost:8000/match_job", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jobDescription }),
    });

    const data = await response.json();
    setMatchResults(data);
  };

  return (
    <form onSubmit={handleUpload}>
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} required />
      <textarea
        placeholder="Paste job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        required
      />
      <button type="submit">Match Resume</button>

      {matchResults && (
        <div>
          <h3>Match Results</h3>
          <pre>{JSON.stringify(matchResults, null, 2)}</pre>
        </div>
      )}
    </form>
  );
}

export default UploadForm;
