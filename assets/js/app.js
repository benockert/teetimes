//Add styling and phoenix stuff
import "../css/app.scss"
import "react-datetime/css/react-datetime.css";
import "phoenix_html"

//Add React component
import React, { useState, useEffect } from 'react';
import DateTime from 'react-datetime';
import ReactDOM from 'react-dom';

//Add socket functions
import { get_channel } from "./socket.js";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");

  const [resp, setResponse] = useState("Awaiting response...");

  function reserve(u, p, d, t) {
    let channel = get_channel();
    channel.push("reserve", {username: u, password: p, date: d, time: t})
           .receive("ok", (response) => setResponse(response.response));
  }

  return (
    <div>
      <div>
        <p>Enter username:</p>
        <input
        type="text"
        value={username}
        onChange={(u) => setUsername(u.target.value)}
        />
        <br/>
        <p>Enter password:</p>
        <input
        type="password"
        value={password}
        onChange={(p) => setPassword(p.target.value)}
        />
        <br/>
        <p>Enter target date:</p>
        <DateTime
          dateFormat='MM-DD-YYYY'
          timeFormat={false}
        />
        <br/>
        <p>Enter target time:</p>
        <DateTime
          dateFormat={false}
          timeFormat='HH:mm:00'
        />
        <br/>
        <button className="button" onClick={() => reserve(username,
                                                          password,
                                                          date,
                                                          time)}>
        Reserve
        </button>
        <br/>
        <br/>
        <h3>Response:</h3>
        <p>If the response is <i>200</i>, the tee time has been
        successfully blocked, so manually login and you will be able
        to book your time right at 8:05.</p>
        <p>Server response: <b>{ resp }</b></p>
      </div>
    </div>
  );

}


function TeeTimes() {

  let body = <App />

  return (
    <div className="container">
      {body}
    </div>
  );
}


ReactDOM.render(
  <React.StrictMode>
  <TeeTimes />
  </React.StrictMode>,
  document.getElementById('root')
);
