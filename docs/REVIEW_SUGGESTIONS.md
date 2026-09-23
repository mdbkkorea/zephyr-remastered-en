# Translation suggestions in Mac Safari

Open **Launch Review in Safari.command** inside the mounted NAS translation-review
folder. Safari opens the review at `http://127.0.0.1:8766/`. Keep the Terminal
window open and the NAS mounted while reviewing. Only this Mac can reach the
service; the existing Tailscale static review remains available for reading.

Each entry has **Translation suggestion**, **Explanation**, and **Save suggestion**.
The fields accept multiline text. Search and section/page navigation still work.
Typed drafts stay in this browser; only the **Saved to NAS** message confirms a
Markdown file was written. Saved fields return when the page is reopened.

Files are stored in the NAS review folder's **Suggestions** subfolder, with a
review ID and timestamp in each filename. Each save preserves the source text,
current English, suggestion, explanation and resource identity. Revisions create
new files; earlier submissions remain available. Stale concurrent saves are
rejected instead of silently overwriting another revision. Failed saves keep the
browser draft. Browser storage is a convenience, not a substitute for saving.

Suggestions are **pending**. They do not change translations or game files.
The assistant reads them and proposes/applies corrections only when the user
asks. If a requested replacement has a grammar issue or a better wording is
available, explain that before applying it as requested by the user.

The `.md` file's first HTML comment contains structured data for restoring the
form. Preserve it when moving files. The human-readable sections follow it.
The service has no delete or translation-update endpoint and serves only the
review page and its suggestion API, never arbitrary NAS files.

Implementation: `scripts/review/server.py`, `scripts/review/launch.py`,
`scripts/review/suggestions.js`, and `scripts/render_offline_review.py`.
After regenerating the HTML, restart the review server to load the new catalog.
Opening the HTML directly as a file, or via the static Tailscale page, permits
reading and browser drafts but cannot save to NAS; use the Mac launcher to save.
