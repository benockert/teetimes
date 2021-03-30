defmodule Teetimes.PythonServer do
  use GenServer

  alias Teetimes.PythonHelper

  def start_link(_args) do
    GenServer.start_link(__MODULE__, nil, name: __MODULE__)
  end

  # priv/python_sripts
  def init(_) do
    path = Application.app_dir(:teetimes, "priv/python_scripts")
    |> to_charlist()
    |> PythonHelper.start_instance('python3')
  end

  def call_function(module, function, args) do
    GenServer.call(__MODULE__, {:call_function, module, function, args})
  end


  # module = :filename
  # function = :function_name within filename
  # args = ["list", "of", "arguments"] for the function
  def handle_call({:call_function, module, function, args}, _from, pid) do
    IO.inspect("Got here");
    result = PythonHelper.call_instance(pid, module, function, args)
    {:reply, result, pid}
  end
end
