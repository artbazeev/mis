from django.urls import NoReverseMatch, reverse


def r(candidates, fallback=None):
    """Try to reverse the first existing URL name from candidates.
    If none found and fallback is given, return the fallback raw path.
    """
    if isinstance(candidates, str):
        candidates = [candidates]
    for name in candidates:
        try:
            return reverse(name)
        except NoReverseMatch:
            continue
    if fallback:
        return fallback
    # As last resort, raise for the final candidate to show a clear error
    raise NoReverseMatch(f"None of these names exist: {candidates}")


def r_detail(candidates, pk, fallback=None):
    if isinstance(candidates, str):
        candidates = [candidates]
    for name in candidates:
        try:
            return reverse(name, args=[pk])
        except NoReverseMatch:
            continue
    if fallback:
        return fallback.rstrip("/") + f"/{pk}/"
    raise NoReverseMatch(f"None of these detail names exist: {candidates}")


def r_action(candidates, pk, action="set-status", fallback=None):
    if isinstance(candidates, str):
        candidates = [candidates]
    for name in candidates:
        try:
            return reverse(name, args=[pk])
        except NoReverseMatch:
            continue
    if fallback:
        # assume DRF action url like /.../<pk>/<action>/
        return fallback.rstrip("/") + f"/{pk}/{action}/"
    raise NoReverseMatch(f"None of these action names exist: {candidates}")
