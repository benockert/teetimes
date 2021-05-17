defmodule TeetimesWeb.GolfChannel do
  use TeetimesWeb, :channel

  alias Teetimes.PythonServer

  @impl true
  def join("golf:lobby", payload, socket) do
    {:ok, socket}
  end

  # Channels can be used in a request/response fashion
  # by sending replies to requests from the client
  @impl true
  def handle_in("reserve", %{"username" => uname,
                "password" => pass, "date" => date,
                "time" => time}, socket) do
    resp = PythonServer.call_function(:teetime, :tee_bot, [uname, pass, date, time])

    {:reply, {:ok, %{response: resp }}, socket}
  end

  @impl true
  def handle_in("unblock", %{"username" => uname,
                "password" => pass, "date" => date,
                "time" => time, "block_id" => id}, socket) do
    IO.inspect("Block ID")
    IO.inspect(id)
    resp = PythonServer.call_function(:removelock, :remove_lock, [uname, pass, date, time, id])

    {:reply, {:ok, %{response: resp }}, socket}
  end

end
