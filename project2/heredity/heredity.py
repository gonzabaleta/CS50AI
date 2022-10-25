import csv
import itertools
import sys


PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that """

    joint_probability = 0

    # everyone in set `one_gene` has one copy of the gene, and=
    # everyone in set `two_genes` has two copies of the gene, and
    # everyone not in `one_gene` or `two_gene` does not have the gene, and
    # everyone in set `have_trait` has the trait, and
    # everyone not in set` have_trait` does not have the trait.

    # for all people
    for person in people:
        probability = 0
        has_parents = people[person]['mother'] and people[person]['father']

        if has_parents:
            father = people[person]['father']
            mother = people[person]['mother']

            father_genes = 1 if father in one_gene else 2 if father in two_genes else 0
            mother_genes = 1 if mother in one_gene else 2 if mother in two_genes else 0

            # calculate the probability of the person geting the gene from either of their parents
            got_from = {
                'father': father_genes / 2,
                'mother': mother_genes / 2
            }

            for parent in got_from:
                if got_from[parent] == 0:
                    got_from[parent] = PROBS['mutation']
                elif got_from[parent] == 1:
                    got_from[parent] = 1 - PROBS['mutation']

        # Calculate the probability of the person having one gene
        if person in one_gene:
            # If the person has no parents, then get the unconditional probability of one_gene
            if not has_parents:
                probability = PROBS['gene'][1]
            else:
                # a person has one gene if they got it either from the father and not from the mother OR from the mother and not the father
                # probability of getting it from the father and not from the mother
                probability = got_from['father'] * (1 - got_from['mother'])
                # add probability of getting it from the mother and not from the father
                probability += got_from['mother'] * (1 - got_from['father'])

        # calculate the probability of the person having two genes
        elif person in two_genes:
            # If the person has no parents, then get the unconditional probability of one_gene
            if not has_parents:
                probability = PROBS['gene'][2]
            else:
                # a person has two genes only if both parents transmit the virus
                probability = got_from['father'] * got_from['mother']

        # calculate the probability of the person having no genes
        else:
            if not has_parents:
                probability = PROBS['gene'][0]
            else:
                # a person has no genes if neither of the parents pass the gene
                probability = (1 - got_from['father']) * \
                    (1 - got_from['mother'])

        # calculate the probability of the person having the trait
        if person in have_trait:
            if person in one_gene:
                probability *= PROBS['trait'][1][True]
            elif person in two_genes:
                probability *= PROBS['trait'][2][True]
            else:
                probability *= PROBS['trait'][0][True]

        # calculate the probability of the person NOT having the trait
        else:
            if person in one_gene:
                probability *= PROBS['trait'][1][False]
            elif person in two_genes:
                probability *= PROBS['trait'][2][False]
            else:
                probability *= PROBS['trait'][0][False]

        if (joint_probability == 0):
            joint_probability = probability
        else:
            joint_probability *= probability

    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p

        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # normalize genes
        gene_sum = 0
        for gene_prob in probabilities[person]['gene'].values():
            gene_sum += gene_prob

        normalizer = 1 / gene_sum

        for gene in probabilities[person]['gene']:
            probabilities[person]['gene'][gene] *= normalizer

        # normalize trait
        trait_sum = probabilities[person]['trait'][True] + \
            probabilities[person]['trait'][False]

        normalizer = 1 / trait_sum

        probabilities[person]['trait'][True] *= normalizer
        probabilities[person]['trait'][False] *= normalizer


if __name__ == "__main__":
    main()
