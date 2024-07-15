import React, { useState } from 'react';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleJobDescriptionChange = (event) => {
    setJobDescription(event.target.value);
  };

  const handleResumeChange = (event) => {
    setResumeFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!resumeFile) {
      setError('Please select a resume file.');
      return;
    }

    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('resume', resumeFile);

    try {
      const res = await fetch('/process_resume', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await res.json();
      setResponse(data);
      setError(null);
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while processing your request.');
    }
  };

  return (
    <div className="App">
      <h1>Resume Analyzer</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Job Description:
            <textarea value={jobDescription} onChange={handleJobDescriptionChange} />
          </label>
        </div>
        <div>
          <label>
            Resume:
            <input type="file" onChange={handleResumeChange} />
          </label>
        </div>
        <button type="submit">Submit</button>
      </form>
      {error && (
        <div className="error">
          <p>{error}</p>
        </div>
      )}
      {response && (
        <div>
          <h2>Response</h2>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
