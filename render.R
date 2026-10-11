# Canonical renderer for the interactive network.
#
# Keeping responsive UI behavior as a render include means the project source
# owns the mobile controls directly. GitHub Actions and local renders use the
# same render entry point; no generated HTML is patched after rendering.

# Verify the bundled snapshot before any cached tables or browser output are used.
python_command <- Sys.getenv('CONGRESS_PYTHON',unset='')
if (!nzchar(python_command)) {
  candidates <- Sys.which(c('python3','python'))
  candidates <- candidates[nzchar(candidates)]
  if (!length(candidates)) stop('Python 3 is required to verify bundled 2025 inputs.')
  python_command <- unname(candidates[1])
}
if (system2(python_command,'scripts/verify_2025_inputs.py') != 0) {
  stop('Bundled 2025 inputs failed verification; rendering stopped.')
}

rmarkdown::render(
  "2025_Congressional_Stock_Network.Rmd",
  output_file = "index.html",
  output_options = list(
    includes = rmarkdown::includes(
      after_body = c("performance-ui.html", "mobile-network-controls.html", "v1-ui.html")
    )
  ),
  quiet = FALSE
)
