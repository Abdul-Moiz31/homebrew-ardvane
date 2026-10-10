class Ardvane < Formula
  desc "Protects developers from malware that spreads through code"
  homepage "https://github.com/Abdul-Moiz31/ardvane"
  url "https://github.com/Abdul-Moiz31/ardvane/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "549e06b6ef8f010091d79b067e731ad7ad0c37b25990bde5c17a82f3a261c8b4"
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
