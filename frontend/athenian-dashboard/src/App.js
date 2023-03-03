import { useState, useEffect } from "react";
import "./App.css";
import BarChart from "./Charts/BarChart";
import LineChart from "./Charts/LineChart";
import PieChart from "./Charts/PieChart";

function App() {
  const [userData, setUserData] = useState({
    labels: [],
    datasets: [
      {
        label: "repos Insights",
        data: [],
        backgroundColor: [
          "rgba(75,192,192,1)",
          "#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0",
        ],
        borderColor: "black",
        borderWidth: 2,
      },
    ],
  });

    const [userDataOne, setUserDataOne] = useState({
    labels: [],
    datasets: [
      {
        label: "repos Insights",
        data: [],
        backgroundColor: [
          "rgba(75,192,192,1)",
          "#ecf0f1",
          "#50AF95",
          "#f3ba2f",
          "#2a71d0",
        ],
        borderColor: "black",
        borderWidth: 2,
      },
    ],
  });




  const [fileListData, setFileListData] = useState([]);

  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = (event) => {
    event.preventDefault();

    if (!selectedFile) {
      console.error("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://0.0.0.0:8000/app/v1/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("File upload successful: ", data);
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
  };

const handleAnalysisFile = (id) => {
  fetch(`http://0.0.0.0:8000/app/v1/analysis_file/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Analysis file successful: ", data);
    })
    .catch((error) => {
      console.error("Error analyzing file: ", error);
    });
};

  useEffect(() => {
    fetch("http://0.0.0.0:8000/app/v1/review-stats")
      .then((response) => response.json())
      .then((data) => {
        setUserData({
          labels: data.map((data) => data.name),
          datasets: [
            {
              label: "repos Insights",
              data: data.map((data) => data.mean_review_time),
              backgroundColor: [
                "rgba(75,192,192,1)",
                "#ecf0f1",
                "#50AF95",
                "#f3ba2f",
                "#2a71d0",
              ],
              borderColor: "black",
              borderWidth: 2,
            },
          ],
        });
      })
      .catch((error) => {
        console.error("Error fetching user data: ", error);
      });



        fetch("http://0.0.0.0:8000/app/v1/review-stats")
      .then((response) => response.json())
      .then((data) => {
        setUserDataOne({
          labels: data.map((data) => data.name),
          datasets: [
            {
              label: "repos Insights",
              data: data.map((data) => data.mean_merge_time),
              backgroundColor: [
                "rgb(0,175,63)",
                "#ecf0f1",
                "#9eef7b",
                "#f3ba2f",
                "#f33f2f",
              ],
              borderColor: "black",
              borderWidth: 2,
            },
          ],
        });
      })
      .catch((error) => {
        console.error("Error fetching user data: ", error);
      });




    fetch("http://0.0.0.0:8000/app/v1/filelist")
      .then((response) => response.json())
      .then((data) => {
        setFileListData(data);
      })
      .catch((error) => {
        console.error("Error fetching file list data: ", error);
      });
  }, []);

  // IF YOU SEE THIS COMMENT: I HAVE GOOD EYESIGHT


return (
    <div className="App">
      <h1>Data-Vision Athenian Dashboard </h1>
      <form
        onSubmit={handleFileUpload}
        style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
      >
        <div style={{ marginBottom: "1rem" }}>
          <input
            type="file"
            onChange={handleFileSelect}
            style={{ display: "none" }}
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            style={{
              backgroundColor: "#2a71d0",
              color: "white",
              padding: "0.5rem 1rem",
              borderRadius: "5px",
              cursor: "pointer",
            }}
          >
            Choose a file
          </label>
        </div>
        <button
          type="submit"
          style={{
            backgroundColor: "#50AF95",
            color: "white",
            padding: "0.5rem 1rem",
            borderRadius: "5px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Upload
        </button>
      </form>
        <div style={{ width: 700 }}>
        <table style={{ border: "1px solid black", borderCollapse: "collapse", margin: "20px" }}>
          <thead>
            <tr>
              <th style={{ border: "1px solid black", padding: "0.5rem" }}>ID</th>
              <th style={{ border: "1px solid black", padding: "0.5rem" }}>Date</th>
              <th style={{ border: "1px solid black", padding: "0.5rem" }}></th>
            </tr>
          </thead>
          <tbody>
            {fileListData.map((file) => (
              <tr key={file.id}>
                <td style={{ border: "1px solid black", padding: "0.5rem" }}>{file.id}</td>
                <td style={{ border: "1px solid black", padding: "0.5rem" }}>{file.date}</td>
                <td style={{ border: "1px solid black", padding: "0.5rem" }}>
                  <button
                    onClick={() => handleAnalysisFile(file.id)}
                    style={{
                      backgroundColor: "#f3ba2f",
                      color: "white",
                      padding: "0.5rem 1rem",
                      borderRadius: "5px",
                      border: "none",
                      cursor: "pointer",
                    }}
                  >
                    Analyze
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    <h2 style={{ border: "1px solid black", borderCollapse: "collapse", margin: "20px" }} >Data-Vision Review Time</h2>
        <h3>MEAN</h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userData} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userData} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userData} />
      </div>
      </div>
              <h3>MEDIAN </h3>

        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userData} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userData} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userData} />
      </div>
      </div>

      <h3>MODE </h3>

        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userData} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userData} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userData} />
      </div>
      </div>
    <h2 style={{ border: "1px solid black", borderCollapse: "collapse", margin: "20px" }} >Data-Vision Merge Time</h2>
    <h3>MEAN </h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userDataOne} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userDataOne} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userDataOne} />
      </div>
      </div>

          <h3>MEDIAN </h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userDataOne} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userDataOne} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userDataOne} />
      </div>
      </div>

          <h3>MODE </h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userDataOne} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userDataOne} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userDataOne} />
      </div>
      </div>


    </div>
  );
}

export default App;