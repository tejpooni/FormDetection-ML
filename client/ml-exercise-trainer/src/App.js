import "./App.css";
import VideoInput from "./components/VideoInput.tsx";

// Styles object for consistency and cleaner JSX
const styles = {
  app: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
    background:
      "linear-gradient(180deg, #0a192f 0%, #172a45 50%, #203a5c 100%)",
    color: "white",
    fontSize: "16px",
    fontFamily: "Roboto, sans-serif",
    textAlign: "center", // Center align text for all children
  },
  container: {
    width: "80%",
    maxWidth: "640px",
    padding: "20px",
    marginTop: "20px",
    borderRadius: "12px",
    boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.2)",
    backgroundColor: "rgba(255, 255, 255, 0.2)",
    border: "1px solid rgba(255, 255, 255, 0.3)",
  },
  instructions: {
    marginTop: "20px",
    padding: "20px",
    borderRadius: "10px",
    background: "rgba(0, 0, 0, 0.2)",
    boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.25)",
    width: "100%", // Use full width of the container for centering
    maxWidth: "640px",
    boxSizing: "border-box", // Include padding in width calculation
  },
  button: {
    marginTop: "20px",
    padding: "10px 30px",
    fontSize: "16px",
    fontFamily: "Roboto, sans-serif",
    color: "#fff",
    background: "#2962ff",
    border: "none",
    borderRadius: "50px",
    boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.3)",
    cursor: "pointer",
    transition: "background 0.3s",
    alignSelf: "center", // Align button itself to center within flex container
  },
  list: {
    textAlign: "left", // Align list items to the left for better readability
    listStylePosition: "inside", // Ensure bullets/numbers are inside the content flow
    paddingLeft: 100,
  },
};

function App() {
  //refresh button action
  const refreshPage = () => {
    window.location.reload();
  };

  return (
    <div className="App" style={styles.app}>
      <h1
        style={{
          fontFamily: "Roboto Mono, monospace",
          fontWeight: "bold",
          marginBottom: "40px",
        }}
      >
        A.I.thlete - Fitness Trainer
      </h1>
      <div style={styles.container}>
        <VideoInput onClick={VideoInput.handleFileChange} />
        <button onClick={refreshPage} style={styles.button}>
          Refresh for Next Upload
        </button>
        <div style={styles.instructions}>
          <p>Instructions:</p>
          <ul style={styles.list}>
            <li>Record yourself doing one of the following exercises:</li>
            <ul>
              <li>Pushups</li>
              <li>Squats</li>
              <li>Overhead Press</li>
            </ul>
            <li>Upload a .mp4 file</li>
            <li>Must have the entire body in the video frame</li>
            <li>Please wait for your video to be processed</li>
            <li>Click the refresh button before uploading the next video</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
