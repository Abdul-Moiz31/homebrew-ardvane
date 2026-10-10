class Ardvane < Formula
  desc "Protects developers from malware that spreads through code"
  homepage "https://github.com/Abdul-Moiz31/ardvane"
  url "https://github.com/Abdul-Moiz31/ardvane/archive/refs/tags/v0.2.2.tar.gz"
  sha256 "dd9a4a145c00ab242334ba5316705dfc6946a06231f6eb1345682276acee7b9c"
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
