defmodule TeetimesWeb.PageController do
  use TeetimesWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
