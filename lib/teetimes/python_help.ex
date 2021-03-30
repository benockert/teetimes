defmodule Teetimes.PythonHelper do

  # Starts a Python instance
  # path -- project path to Python files
  # version -- python instance version (defaults to python3)
  def start_instance(path, version \\ 'python3') do
    :python.start([{:python_path, path}, {:python, version}])
  end

  # calls the create Python instance
  # *args should be in list of arguments for a Python function*
  def call_instance(pid, module, function, args \\ []) do
    IO.inspect(pid)
    IO.inspect(module)
    IO.inspect(function)
    IO.inspect(args)
    :python.call(pid, module, function, args)
  end

  # stops the Python instance
  def stop_instance(pid) do
    :python.stop(pid)
  end


end
