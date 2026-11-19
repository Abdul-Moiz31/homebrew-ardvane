class Ardvane < Formula
  desc "Protects developers from malware that spreads through code"
  homepage "https://github.com/Abdul-Moiz31/ardvane"
  url "https://github.com/Abdul-Moiz31/ardvane/releases/download/v0.10.0/ardvane-0.10.0.tar.gz"
  sha256 "6393001a4131b77dd922531733214a5fb45c7d394d98620a64977b62d4c05563"
  license "MIT"

  depends_on "python@3.14"

  def install
    libexec.install Dir["*"]
    python = Formula["python@3.14"].opt_bin/"python3.14"
    (bin/"ardvane").write <<~SH
      #!/bin/bash
      export ARDVANE_KIT="#{opt_libexec}"
      export ARDVANE_INSTALLED=1
      exec "#{python}" "#{opt_libexec}/app/dashboard.py" "$@"
    SH
  end

  def caveats
    <<~EOS
      Open the dashboard:   ardvane
      Scan this computer:   ardvane scan
      All commands:         ardvane --help
    EOS
  end

  test do
    assert_match "Ardvane", shell_output("#{bin}/ardvane --version")
  end
end
