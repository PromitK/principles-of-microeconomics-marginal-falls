# Validation and publication status

Checked on 2 October 2026.

- All 17 PDFs were uploaded to the new Drive folder. Readback verified each file's ID, MIME type, size, destination folder, and link.
- The 17 PDFs bundled in this repository match the supplied originals byte for byte, using SHA-256 comparison.
- The site has one course homepage and 16 module pages. All 333 internal file and fragment references were checked; none were broken.
- All 13 linked game entry pages at marginalfalls.com returned HTTP 200. Complete multiplayer sessions were not tested.
- Course metadata was checked for valid act assignments, consecutive module numbering, and valid activity references.
- The Python generator and JavaScript source were checked for syntax errors.
- The GitHub Pages workflow follows the official publishing workflow structure, but has not run in a live GitHub repository.

The CSS includes desktop and mobile layouts. Browser-based visual review and interaction testing could not be completed because a browser executable could not be made available in this environment. Review the rendered site before publication.

The repository was prepared locally. GitHub was not connected at the end of this run, so no remote GitHub repository or public Pages URL has been created. Drive copies currently have owner-only access; the bundled PDFs provide the primary slide links for the future published site.
