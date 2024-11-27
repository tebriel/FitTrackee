{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  # env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  # https://devenv.sh/languages/
  languages.typescript = {
    enable = true;
  };
  languages.python = {
    enable = true;
    manylinux.enable = false;
    poetry = {
      enable = true;
      activate.enable = true;
      install = {
        enable = true;
        allExtras = true;
        groups = [
          "dev"
        ];
        installRootPackage = true;
      };
    };
  };

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  services.postgres = {
    enable = true;
    package = pkgs.postgresql_16;
    initialDatabases = [{
      name = "fittrackee";
    }];
    port = 5433;
  };

  services.redis = {
    port = 6391;
  };

  # https://devenv.sh/scripts/
  # scripts.hello.exec = ''
  #   echo hello from $GREET
  # '';

  # enterShell = ''
  #   hello
  #   git --version
  # '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  # enterTest = ''
  #   echo "Running tests"
  #   git --version | grep --color=auto "${pkgs.git.version}"
  # '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.ruff = {
  #   enable = true;
  #   entry = "${lib.getExe pkgs.ruff} check --config pyproject.toml --fix";
  #   files = ".";
  # };
  # pre-commit.hooks.ruff-format = {
  #   enable = true;
  #   entry = "${lib.getExe pkgs.ruff} format --config pyproject.toml";
  #   files = ".";
  # };
  # pre-commit.hooks.bandit = {
  #   enable = true;
  #   name = "bandit";
  #   entry = "bandit -c pyproject.toml -r";
  #   files = ".";
  #   language = "python";
  # };

  # See full reference at https://devenv.sh/reference/options/
}
