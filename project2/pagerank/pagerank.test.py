from pagerank import transition_model, DAMPING, SAMPLES, sample_pagerank

SAMPLE_CORPUS = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

print("--- TRANSITION MODEL ---")
print(transition_model(SAMPLE_CORPUS, "1.html", DAMPING))

print("\n --- SAMPLE PAGERANK ---")
print(sample_pagerank(SAMPLE_CORPUS, DAMPING, SAMPLES))