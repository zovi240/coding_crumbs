def rank_candidates(candidate_results):
    """
    Sort candidates by final score in descending order.
    """

    ranked = sorted(
        candidate_results,
        key=lambda x: x["final_score"],
        reverse=True
    )

    for index, candidate in enumerate(ranked):
        candidate["rank"] = index + 1

    return ranked


def top_candidate(candidate_results):
    """
    Return the highest-ranked candidate.
    """

    if not candidate_results:
        return None

    ranked = rank_candidates(candidate_results)

    return ranked[0]


def filter_candidates(candidate_results, minimum_score=70):
    """
    Return candidates above the given score.
    """

    return [
        candidate
        for candidate in candidate_results
        if candidate["final_score"] >= minimum_score
    ]