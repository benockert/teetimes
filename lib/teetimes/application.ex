defmodule Teetimes.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  def start(_type, _args) do
    children = [
      # add our Python Server
      Teetimes.PythonServer,
      # Start the Telemetry supervisor
      TeetimesWeb.Telemetry,
      # Start the PubSub system
      {Phoenix.PubSub, name: Teetimes.PubSub},
      # Start the Endpoint (http/https)
      TeetimesWeb.Endpoint
      # Start a worker by calling: Teetimes.Worker.start_link(arg)
      # {Teetimes.Worker, arg}
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Teetimes.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  def config_change(changed, _new, removed) do
    TeetimesWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
