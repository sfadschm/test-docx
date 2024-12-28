#!/bin/bash

# Setup script error handling
set -euo pipefail

# Get directory link
thisdir=$(dirname $(readlink -f "$0"))

# Enable pandoc for .docx diffs
echo "Adding local configuration for diffing with pandoc ..."
git config --local diff.docx.textconv "tools/pandoc --from=docx --to=markdown --track-changes=all"
git config --local diff.docx.prompt "false"
git config --local diff.docx.binary "true"

# Enable pptx2md for .pptx diffs
echo "Add local configuration for diffing with pptx2md ..."
git config --local diff.pptx.textconv "sh -c 'tools/pptx2md --disable-image --disable-wmf \"\$0\" -o ~/.cache/git/presentation.md >/dev/null && cat ~/.cache/git/presentation.md'"
git config --local diff.pptx.cachetextconv "true"
git config --local diff.pptx.prompt "false"
git config --local diff.pptx.binary "true"

# Enable pdftotxt for .pdf diffs
echo "Add local configuration for diffing with pdftotxt ..."
git config --local diff.pdf.textconv "sh -c 'tools/pdftotext -simple -enc UTF-8 \"\$0\" -'"
git config --local diff.pdf.cachetextconv "true"
git config --local diff.pdf.prompt "false"
git config --local diff.pdf.binary "true"

# Rebase the hook lookup directory
echo "Relink the git hook lookup path ..."
git config --local core.hooksPath "tools/hooks"

# Exit on user confirmation
echo
read -p "Press enter to close."
exit 0
