import { useEffect, useState } from "react";

export default function HttpCall() {
  const [data, setData] = useState("");

  useEffect(() => {
    fetch("/get_feedback", {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((responseData) => {
        setData(responseData.feedback);
      });
  });
  return (
    <>
      <h2 style={{ fontFamily: "Roboto, sans-serif" }}>Feedback:</h2>
      <h3 className="http">{data}</h3>
    </>
  );
}
