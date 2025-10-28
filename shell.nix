{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    clang
    gcc
    llvmPackages.libcxx
  ];
  packages = with pkgs; [
    black
    clang-tools
    (pkgs.python312.withPackages (
      ppkgs: with ppkgs; [
        pip
        python-lsp-server
        black
        flake8
      ]
    ))
  ];

  shellHook = # sh
    ''
      export name="nix:boj-cli"
      export CPLUS_INCLUDE_PATH="$HOME/.config/assets/clang/include";
      export CLANGD_FLAGS="--header-insertion=never";
    '';
}
