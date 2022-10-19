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
    distribution = {}

    # If no links from page, all pages have equal probability
    if (not len(corpus[page])):
        probability = 1 / len(corpus)
        for link in corpus:
            distribution[link] = probability
        return distribution

    # Else:
    damping_plus = (1 - damping_factor) / len(corpus) # We set the damping additional to (1 - damping) / all pages
    probability = damping_factor / len(corpus[page])  # We set the probability to the damping factor divided by the amount of links

    # Fill the distributino dict with the values
    for link in corpus:
        distribution[link] = damping_plus
        if link in corpus[page]:
            distribution[link] += probability

    # Return dictionary
    return distribution
            



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize pagerank dict with all values set to 0
    pagerank = {}
    for link in corpus: 
        pagerank[link] = 0

    # get a random first page and set it to 1
    page = random.choices(list(corpus.keys()))[0]
    pagerank[page] += 1

    # iterate n times
    for _ in range(n - 1):
        # Get probability distributino from page
        distribution = transition_model(corpus, page, damping_factor)

        # Choose next page based on the probability distribution and add one to that page
        page = random.choices(list(distribution.keys()), weights=distribution.values(), k=1)[0]
        pagerank[page] += 1
    
    # Divide all values in pagerank by n
    for page in pagerank:
        pagerank[page] /= n
    
    return pagerank
        




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    distribution = {}
    for page in corpus:
        distribution[page] = 1 / len(corpus)


if __name__ == "__main__":
    main()
