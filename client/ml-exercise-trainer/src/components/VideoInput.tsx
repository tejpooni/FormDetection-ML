import axios from "axios";
import React, { useRef, useState, ChangeEvent } from "react";
import '../../src/spinner.css' //css for loading animation

interface VideoInputProps {
  width?: number;
  height: number;
}

const VideoInput: React.FC<VideoInputProps> = (props) => {

  const inputRef = useRef<HTMLInputElement>(null);

  const [source, setSource] = useState<string | undefined>(); //video player
  const [loading, setLoading] = useState<boolean>(false); //loading state inits to false
  const [datafb, setData] = useState(""); //data for feedback

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setLoading(true); //start loading when file selected
    const url = URL.createObjectURL(file);
    setSource(url); //set video player to have video uploaded

    if (file != null) {
      const data = new FormData();
      data.append("file_uploaded", file);

      let response = await fetch("/send_file", {
        method: "POST",
        body: data,
      });
      let res = await response.json();
      if (res.status !== 1) {
        alert("Error uploading file");
        setLoading(false); //reset loading on error
      } else {
        setLoading(false); //reset loading on success
        axios
          .get("/get_vid", {
            headers: {
              "Content-Type": "video/mp4",
            },
            responseType: "blob",
          })
          .then((response) => {
            console.log(response.data);
            const videoURL = URL.createObjectURL(response.data);
            setSource(videoURL);
          }); //get the processed video and set player to have this

        let res_fb = await fetch("/get_feedback"); //get feedback
      
        if (!res_fb.ok) {
          throw new Error("Failed to fetch feedback");
        }
        //display the feedback for the user
        const responseData = await res_fb.json();
        console.log(responseData.feedback)
        setData(responseData.feedback);
      }
    }
  };

  const handleChoose = () => {
    inputRef.current?.click();
  };

  return (
    <>  
    <div>
      <h2 style={{ fontFamily: "Roboto, sans-serif" }}>Feedback:</h2>
      <h3 className="http">{datafb}</h3>
    </div>
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        border: "1px solid #ddd",
      }}
    >
      <input
        ref={inputRef}
        style={{ display: "none" }}
        type="file"
        onChange={handleFileChange}
        accept=".mov,.mp4,.pdf"
      />
      {!source && <button onClick={handleChoose}>Choose</button>}
      {source && (
        <video
          style={{ display: "block", margin: 0 }}
          width={"500px"}
          height={"300px"}
          controls
          src={source}
        />
      )}
      {loading && <div className="spinner"></div>} {/* Display loading indicator when processing */}
      {loading && <div>Please Wait</div>} {/* message while loading animation going */}
    </div>
  </>
  );
};

export default VideoInput;
