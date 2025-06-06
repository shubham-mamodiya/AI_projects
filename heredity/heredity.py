import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
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
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def get_gen_count_and_prob(person, one_gene, two_genes):
    """
    Returns a Tuple (gene_count, probability)"""

    if person in one_gene:
        return (1, 0.5)
    elif person in two_genes:
        return (2, 0.99)
    return (0, 0.01)


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Total Probability
    joint_prob = 1

    # Going through the each person in the people
    for person in people:

        father = people[person]["father"]
        mother = people[person]["mother"]
        observed_trait = person in have_trait

        person_gene_count, _ = get_gen_count_and_prob(person, one_gene, two_genes)
        person_prob = 1

        # When child don't have parents the use the unconditional probability
        if not father and not mother:
            person_prob = PROBS["gene"][person_gene_count]
        # When there are parents then calculating the conditional probability
        else:
            _, mother_prob = get_gen_count_and_prob(mother, one_gene, two_genes)
            _, father_prob = get_gen_count_and_prob(father, one_gene, two_genes)

            match person_gene_count:
                case 2:
                    person_prob = mother_prob * father_prob
                case 1:
                    person_prob = (1 - father_prob) * mother_prob + (
                        1 - mother_prob
                    ) * father_prob
                case 0:
                    person_prob = (1 - father_prob) * (1 - mother_prob)

        person_prob *= PROBS["trait"][person_gene_count][observed_trait]

        joint_prob *= person_prob
        
    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        gen_count = None
        observed_trait = person in have_trait

        if person in one_gene:
            gen_count = 1
        elif person in two_genes:
            gen_count = 2
        else:
            gen_count = 0

        probabilities[person]["gene"][gen_count] += p
        probabilities[person]["trait"][observed_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_probs = probabilities[person]["gene"]
        trait_probs = probabilities[person]["trait"]
        gene_sum = sum(gene_probs.values())
        trait_sum = sum(trait_probs.values())

        for prob in gene_probs:
            gene_probs[prob] /= gene_sum
        for prob in trait_probs:
            trait_probs[prob] /= trait_sum
        probabilities[person]["gene"] = gene_probs
        probabilities[person]["trait"] = trait_probs


if __name__ == "__main__":
    main()
