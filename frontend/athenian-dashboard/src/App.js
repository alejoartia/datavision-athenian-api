import { useState, useEffect } from "react";
import "./App.css";
import BarChart from "./Charts/BarChart";
import LineChart from "./Charts/LineChart";
import PieChart from "./Charts/PieChart";

function App() {
  const [userDataOneMean, setUserDataOneMean] = useState({
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

    const [userDataOneMedian, setDataOneMedian] = useState({
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

    const [userDataOneMode, setDataOneMode] = useState({
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

    const [userDataTwoMean, setUserDataTwoMean] = useState({
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

    const [userDataTwoMedian, setUserDataTwoMedian] = useState({
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

    const [userDataTwoMode, setUserDataTwoMode] = useState({
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

  const [fileListDataAnalysis, setFileListDataAnalysis] = useState([]);


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
  const handleSaveAnalysis = (event) => {
    event.preventDefault();

  fetch("http://0.0.0.0:8000/app/v1/save_analysis?file=" + selectedFile)
    .then((response) => response.json())
    .then((data) => {
      console.log("File download successful: ", data);
    })
    .catch((error) => {
      console.error("Error downloading file: ", error);
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
    fetch("http://0.0.0.0:8000/app/v1/review_stats")
      .then((response) => response.json())
      .then((data) => {
        setUserDataOneMean({
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

    fetch("http://0.0.0.0:8000/app/v1/review_stats")
      .then((response) => response.json())
      .then((data) => {
        setDataOneMedian({
          labels: data.map((data) => data.name),
          datasets: [
            {
              label: "repos Insights",
              data: data.map((data) => data.median_review_time),
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

    fetch("http://0.0.0.0:8000/app/v1/review_stats")
      .then((response) => response.json())
      .then((data) => {
        setDataOneMode({
          labels: data.map((data) => data.name),
          datasets: [
            {
              label: "repos Insights",
              data: data.map((data) => data.mode_review_time),
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

        fetch("http://0.0.0.0:8000/app/v1/review_stats")
      .then((response) => response.json())
      .then((data) => {
        setUserDataTwoMean({
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

        fetch("http://0.0.0.0:8000/app/v1/review_stats")
      .then((response) => response.json())
      .then((data) => {
        setUserDataTwoMedian({
          labels: data.map((data) => data.name),
          datasets: [
            {
              label: "repos Insights",
              data: data.map((data) => data.median_merge_time),
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

        fetch("http://0.0.0.0:8000/app/v1/review_stats")
      .then((response) => response.json())
      .then((data) => {
        setUserDataTwoMode({
          labels: data.map((data) => data.name),
          datasets: [
            {
              label: "repos Insights",
              data: data.map((data) => data.mode_merge_time),
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

    fetch("http://0.0.0.0:8000/app/v1/file_list")
      .then((response) => response.json())
      .then((data) => {
        setFileListData(data);
      })
      .catch((error) => {
        console.error("Error fetching file list data: ", error);
      });

    fetch("http://0.0.0.0:8000/app/v1/saved_analysis_list")
      .then((response) => response.json())
      .then((data) => {
        setFileListDataAnalysis(data);
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

<div style={{ display: "flex", flexDirection: "row" }}>

          <table style={{ border: "1px solid black", borderCollapse: "collapse", margin: "20px" }}>


          <thead>
          <h3 style={{margin: "10px" }}> CSV uploaded </h3>
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

        <table style={{ border: "1px solid black", borderCollapse: "collapse", margin: "20px" }}>


          <thead>
          <h3 style={{margin: "10px" }}> Analysis Saved </h3>
            <tr>
              <th style={{ border: "1px solid black", padding: "0.5rem" }}>Number</th>
              <th style={{ border: "1px solid black", padding: "0.5rem" }}>Date</th>
              <th style={{ border: "1px solid black", padding: "0.5rem" }}></th>
            </tr>
          </thead>
          <tbody>
            {fileListDataAnalysis.map((file) => (
              <tr key={file.id}>
                <td style={{ border: "1px solid black", padding: "0.5rem" }}>{file.query_number}</td>
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
        <form
        onSubmit={handleSaveAnalysis}
        style={{ display: "flex", flexDirection: "column", alignItems: "center", margin: "10px" }}
      >
        <button
          type="submit"
          style={{
            backgroundColor: "#2c4c9b",
            color: "white",
            padding: "1rem 1rem",
            borderRadius: "5px",
            border: "none",
            cursor: "pointer",
          }}
        >
          CLICK HERE TO SAVE THE CURRENT ANALYSIS
        </button>
      </form>

      </div>
    <h2 style={{ border: "1px solid black", borderCollapse: "collapse", margin: "20px" }} >Data-Vision Review Time</h2>
        <h3>MEAN</h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userDataOneMean} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userDataOneMean} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userDataOneMean} />
      </div>
      </div>
              <h3>MEDIAN </h3>

        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userDataOneMedian} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userDataOneMedian} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userDataOneMedian} />
      </div>
      </div>

      <h3>MODE </h3>

        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <LineChart chartData={userDataOneMode} />
      </div>
      </div>


    <h2 style={{ border: "1px solid black", borderCollapse: "collapse", margin: "20px" }} >Data-Vision Merge Time</h2>
    <h3>MEAN </h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userDataTwoMean} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userDataTwoMean} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userDataTwoMean} />
      </div>
      </div>

          <h3>MEDIAN </h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>

      <div style={{ width: 400 }}>
        <BarChart chartData={userDataTwoMedian} />
      </div>
      <div style={{ width: 400 }}>
        <LineChart chartData={userDataTwoMedian} />
      </div>
      <div style={{ width: 250 }}>
        <PieChart chartData={userDataTwoMedian} />
      </div>
      </div>

          <h3>MODE </h3>
        <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>


      <div style={{ width: 400 }}>
        <LineChart chartData={userDataTwoMode} />
      </div>

      </div>


    </div>
  );
}

export default App;