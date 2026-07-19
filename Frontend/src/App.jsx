import { useEffect, useState } from "react";

function App() {
  const [documents, setDocuments] = useState([]);

  // useEffect(() => {
  //   fetch("http://127.0.0.1:5000/hello")
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setMessage(data.message);
  //     });
  // }, []);

  useEffect(() => {
  async function getData() {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/documents`);
      const data = await response.json();
      setDocuments(data);
    } catch (error) {
      console.error("Failed to fetch documents:", error);
    }
  }

  getData();
}, []);

  return (
    <div>
      <h1>Documents</h1>
      <ul>
        {documents.map((doc) => (
          <li key={doc.id}>{doc.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;