//Add styling and phoenix stuff
import "../css/app.scss";
import "react-datetime/css/react-datetime.css";
import "phoenix_html";
import $ from 'jquery';

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

  const [msg, setMsg] = useState("");

  function reserve(u, p) {
    let d = $('#date').val();
    let t = $('#time').val();
    console.log("Making reservation", u, p, d, t);
    let send = "Reserving tee time for user ";
    send += username;
    send += " on " + d;
    send += " at " + t + ".";
    setMsg(send);

    let channel = get_channel();
    channel.push("reserve", {username: u, password: p, date: d, time: t})
           .receive("ok", (response) => console.log("Received from server:", response));
  }

  return (
    <div>
      {msg !== "" &&
        <div className="alert">
          <span className="closebtn" onClick={() => setMsg("")}>&times;</span>
          {msg}
        </div>
      }
      <div id="form">
        <h2 className="title">Tee Time Bot</h2>
        <div>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(u) => setUsername(u.target.value)}
          />
          <input
            type="password"
            value={password}
            onChange={(p) => setPassword(p.target.value)}
          />
          <DateTime
            inputProps={{ id:'date' }}
            dateFormat='MM-DD-YYYY'
            timeFormat={false}
            closeOnSelect={true}
          />
          <DateTime
            inputProps={{ id:'time' }}
            dateFormat={false}
            timeFormat='HH:mm:00'
          />
          <button className="button" onClick={() => reserve(username, password)}>
            Reserve
          </button>
        </div>
      </div>
    </div>
  );

}


function TeeTimes() {

  let body = <App />

  return (
    <div>
      <img className="logo" src='/images/logo.svg' alt="Alt" />
      <div className="tee-form">
        {body}
      </div>
    </div>
  );
}

//sets input field placeholder values
$(document).ready(function() {
  $('#form').find("input[id=username], textarea").each(function(ev) {
    if(!$(this).val()) {
      $(this).attr("placeholder", "Enter your ACC username");
    }
  });
});

$(document).ready(function() {
  $('#form').find("input[type=password], textarea").each(function(ev) {
    if(!$(this).val()) {
      $(this).attr("placeholder", "Enter your ACC password");
    }
  });
});

$(document).ready(function() {
  $('#form').find("input[id=date], textarea").each(function(ev) {
    if(!$(this).val()) {
      $(this).attr("placeholder", "Select your target date (MM-DD-YYYY)");
    }
  });
});

$(document).ready(function() {
  $('#form').find("input[id=time], textarea").each(function(ev) {
    if(!$(this).val()) {
      $(this).attr("placeholder", "Select your target time (HH:mm:00)");
    }
  });
});

ReactDOM.render(
  <React.StrictMode>
    <TeeTimes />
  </React.StrictMode>,
  document.getElementById('root')
);
