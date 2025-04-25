import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

""" 
The credit goes to Paul Coster.

Profile link : https://github.com/PLCoster

I took so many hints from his code. 
due to some reasons i haven't code for a pretty lone time, so i decided to took 
some hints from his code for faster comeback. 
Thank you Paul Coster. 
"""
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):  # Not forget to replace with directory
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Initialization of probability distribution
    prob_distro = {page_name: 0 for page_name in corpus}

    # if the page has no links then all the pages in corpus gets equal probability
    if len(corpus[page]) == 0:
        equal_prob = 1 / len(corpus)
        for page_name in prob_distro:
            prob_distro[page_name] = equal_prob
        return prob_distro

    # Probability for picking page at random from curpus
    random_prob = (1 - damping_factor) / len(corpus)

    # probability for picking link from the page
    link_prob = damping_factor / len(corpus[page])

    # adding probabilities to the distro
    for page_name in prob_distro:
        prob_distro[page_name] += random_prob

        if page_name in corpus[page]:
            prob_distro[page_name] += link_prob

    return prob_distro


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    visits = {page_name: 0 for page_name in corpus}

    page = random.choice(list(visits))
    visits[page] += 1

    for i in range(0, n - 1):
        tr_model = transition_model(corpus, page, damping_factor)

        rand_value = random.random()
        cumulative_prob = 0

        for page_name, probability in tr_model.items():
            cumulative_prob += probability

            if rand_value <= cumulative_prob:
                page = page_name
                break

        visits[page] += 1

    # Converting Visits to Probabilities
    ranks = {page_name: (visit_num / n) for page_name, visit_num in visits.items()}

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # defining some constants
    N = len(corpus)
    init_rank = 1 / N
    add_rank = (1 - damping_factor) / N
    threshold = init_rank
    iteration = 0

    # Giving every page a initial probability of (1 / total pages)
    page_ranks = {page: init_rank for page in corpus}
    new_ranks = {page: None for page in corpus}

    while threshold > 0.001:
        iteration += 1
        threshold = 0

        for page in corpus:
            summation = 0
            for link in corpus:
                if len(corpus[link]) == 0:
                    summation += page_ranks[link] * init_rank
                elif page in corpus[link]:
                    summation += page_ranks[link] / len(corpus[link])
            new_rank = add_rank + (damping_factor * summation)
            new_ranks[page] = new_rank

        # Normalizing the rankings
        norm_fact = sum(new_ranks.values())
        new_ranks = {page: (rank / norm_fact) for page, rank in new_ranks.items()}

        for page in corpus:
            rank_change = abs(page_ranks[page] - new_ranks[page])
            if rank_change > threshold:
                threshold = rank_change
        page_ranks = new_ranks.copy()

    return page_ranks


if __name__ == "__main__":
    main()
