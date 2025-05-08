import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = dict()
    for link in corpus[page]:
        distribution[link] = damping_factor / len(corpus[page])
    for link in corpus:
        if link not in corpus[page]:
            distribution[link] = (1 - damping_factor) / len(corpus)
    return distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pageRank = {page: 0 for page in corpus}

    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pageRank[page] += 1 / n

        distribution = transition_model(corpus, page, damping_factor)

        # Sample the next page based on the transition model
        page = random.choices(
            population=list(distribution.keys()),
            weights=list(distribution.values()),
            k=1
        )[0]
    total = sum(pageRank.values())
    for page in pageRank:
        pageRank[page] /= total
    return pageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    epsilon = 0.001
    pageRank = {page: 1/N for page in corpus}

    while True:
        newPageRank = {}
        for page in corpus:

            rank = (1 - damping_factor) / N

            for i in corpus:
                if page in corpus[i]:
                    rank += damping_factor * (pageRank[i] / len(corpus[i]))

            if len(corpus[i]) == 0:
                rank += damping_factor * (pageRank[i] / N)

            newPageRank[page] = rank

        if all(abs(newPageRank[page] - pageRank[page]) < epsilon for page in pageRank):
            break


        pageRank = newPageRank


    total = sum(pageRank.values())
    for page in pageRank:
        pageRank[page] /= total

    return pageRank


if __name__ == "__main__":
    main()
