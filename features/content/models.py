from django.db import models  # noqa: F401

# PRD requirements for this slice:
# - Types: article, poem, literature (§5.1)
# - Fields: title, author byline, category, cover image, image credit, body, status, publish date (§5.1)
# - Poem/literature bodies keep line breaks and spacing exactly (§5.1)
# - featured flag, set by executives (§5.1)
# - Status flow: draft -> submitted -> published, or sent back (§5.2)
# - Only executives publish/delete; delete is a soft delete (§5.2)
# - Open question: can journalists edit others' posts? Default: own drafts only (§3)
