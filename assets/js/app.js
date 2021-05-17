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
  //form inputs
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");

  //alerts
  const [msg, setMsg] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  //block
  const [block, setBlockId] = useState("");

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
           .receive("ok", (response) => {
             console.log("Received from server:", response.response);
             if (response.response.length > 20) {
               setError(response.response);
             } else {
               setSuccess("Successfully reserved tee time. You can now choose when to remove the hold on your tee time.");
               setBlockId(response.response);
             }
           });
  }

  function remove_block(u, p, b) {
    let d = $('#date').val();
    let t = $('#time').val();
    console.log("Removing block " + b);
    let send = "Removing lock " + b + " for tee time " + t + "on" + d + ".";
    setMsg(send);

    let channel = get_channel();
    channel.push("unblock", {username: u, password: p, date: d, time: t, block_id: b})
           .receive("ok", (response) => {
             console.log("Received from server:", response);
             setSuccess("Successfully removed the lock on your tee time. You can now go in and manually reserve it.");
           });
  }

  return (
    <div>
      {msg !== "" &&
        <div className="alert alert-info">
          <span className="closebtn" onClick={() => setMsg("")}>&times;</span>
          {msg}
        </div>
      }
      {success !== "" &&
        <div className="alert">
          <span className="closebtn" onClick={() => setSuccess("")}>&times;</span>
          {success}
        </div>
      }
      {error !== "" &&
        <div className="alert alert-danger">
          <span className="closebtn" onClick={() => setError("")}>&times;</span>
          {error}
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
            dateFormat='YYYY-MM-DD'
            timeFormat={false}
            closeOnSelect={true}
          />
          <DateTime
            inputProps={{ id:'time' }}
            dateFormat={false}
            timeFormat='HH:mm:00'
          />
          {block == "" &&
            <button className="reserve-btn button" onClick={() => reserve(username, password)}>
              Reserve
            </button>
          }
          {block !== "" &&
            <button id="remove-lock-btn" className="button remove-lock" onClick={() => remove_block(username, password, block)}>
              Remove Lock
            </button>
          }
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

$(document).ready(function() {
  $('.reserve-btn').click(function(e) {
    e.preventDefault();
    $('#form').find("input").each(function() {
      $(this).attr("disabled", true);
    });
  });
});

ReactDOM.render(
  <React.StrictMode>
    <TeeTimes />
  </React.StrictMode>,
  document.getElementById('root')
);
