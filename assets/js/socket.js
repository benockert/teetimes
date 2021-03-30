import {Socket} from "phoenix"

let socket = new Socket("/socket", {params: {token: ""}});

socket.connect();

let channel = socket.channel("golf:lobby", {});
channel.join()
       .receive("ok", resp => {console.log("Successfully connected to channel", resp)})
       .receive("error", resp => {console.log("Unable to connect to channel", resp)});

export function get_channel() {
  return channel;
}
