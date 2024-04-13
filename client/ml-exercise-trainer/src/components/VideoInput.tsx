import axios from "axios";
import React, { useRef, useState, ChangeEvent } from "react";

interface VideoInputProps {
  width?: number;
  height: number;
}

const VideoInput: React.FC<VideoInputProps> = (props) => {
  const { height } = props;

  const inputRef = useRef<HTMLInputElement>(null);

  const [source, setSource] = useState<string | undefined>();

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    setSource(url);

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
      }else {
        // const processedVideoUrl = new URL(res.video_url, window.location.origin).href;
        // axios.get('/get_feedback', {
        //   headers:{
        //     "Content-Type": "video/mp4"
        //   },
        //   responseType: "blob",
        // }).then((response) => {
        //   console.log(response);
        //   const videoURL = URL.createObjectURL(response.data);
        //   setSource(videoURL)
        // })
        
    }
    }
  };

  const handleChoose = () => {
    inputRef.current?.click();
  };

  return (
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
      {/* <div>{source ? <a href={source} target="_blank">Download Processed Video</a> : "Nothing selected"}</div> */}
      <div>{source || "Nothing selected"}</div>
    </div>
  );
};

export default VideoInput;
