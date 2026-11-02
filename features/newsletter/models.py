from django.db import models  # noqa: F401

# PRD requirements for this slice:
# - Subscriber: email (required, unique), name (optional) (§5.5)
# - Handle duplicate/invalid emails; return a confirmation message (§5.5)
# - Unsubscribe path and consent statement (§5.5, NDPA §6)
# - Executives can export the list (§5.5)
# - Rate limit signup: throttle_scope = "newsletter" (§6)
