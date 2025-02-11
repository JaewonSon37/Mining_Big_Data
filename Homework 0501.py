# To run on 4 EMR nodes (master node created by default):
# python HW3_JaewonSon.py -r emr --num-core-instances=3 --movies=movies.dat --conf-path mrjob.conf ratings.dat

# To run on 8 EMR nodes (master node created by default):
# python HW3_JaewonSon.py -r emr --num-core-instances=7 --movies=movies.dat --conf-path mrjob.conf ratings.dat


from mrjob.job import MRJob
from mrjob.step import MRStep
from math import sqrt
from itertools import combinations


class MovieSimilarities(MRJob):


    # Method to configure the command-line arguments for the job
    def configure_args(self):

        super(MovieSimilarities, self).configure_args() # Call the parent class's configure_args method
        self.add_file_arg('--movies', help = 'Path to movies.dat') # Add a command-line argument


    # Method to load movie names from the movies.dat file
    def load_movie_names(self):
        
        self.movieNames = {}

        # Open the movies.dat file and read it line by line
        with open(self.options.movies, encoding = 'ascii', errors = 'ignore') as f:
            for line in f:
                fields = line.split("::")
                self.movieNames[int(fields[0])] = fields[1] # Store the movie ID and the movie name in the dictionary


    # Method to define the sequence of MapReduce steps for the job
    def steps(self):

        return [MRStep(mapper = self.mapper_parse_input,
                       reducer = self.reducer_ratings_by_user),
                MRStep(mapper = self.mapper_create_item_pairs,
                       reducer = self.reducer_compute_similarity),
                MRStep(mapper = self.mapper_sort_similarities,
                       mapper_init = self.load_movie_names,
                       reducer = self.reducer_output_similarities)]


    # Method to parse the input data (userID, movieID, rating, timestamp)
    def mapper_parse_input(self, key, line):

        (userID, movieID, rating, timestamp) = line.split('::')
        yield userID, (movieID, float(rating))


    # Method to group item ratings by user and prepare them for further processing
    def reducer_ratings_by_user(self, user_id, itemRatings):

        ratings = []

        for movieID, rating in itemRatings:
            ratings.append((movieID, rating))

        yield user_id, ratings


    # Method to create pairs of movies and their ratings from the user's ratings
    def mapper_create_item_pairs(self, user_id, itemRatings):

        for itemRating1, itemRating2 in combinations(itemRatings, 2):
            movieID1 = itemRating1[0]
            rating1 = itemRating1[1]
            movieID2 = itemRating2[0]
            rating2 = itemRating2[1]

            # Yield the movie pair and the reversed movie pair
            yield (movieID1, movieID2), (rating1, rating2)
            yield (movieID2, movieID1), (rating2, rating1)


    # Method to calculate the cosine similarity between two sets of ratings
    def cosine_similarity(self, ratingPairs):

        numPairs = 0
        sum_xx = sum_yy = sum_xy = 0

        for ratingX, ratingY in ratingPairs:
            sum_xx += ratingX * ratingX
            sum_yy += ratingY * ratingY
            sum_xy += ratingX * ratingY
            numPairs += 1

        numerator = sum_xy
        denominator = sqrt(sum_xx) * sqrt(sum_yy) # Calculate the denominator of the cosine similarity
        score = 0

        # If the denominator is non-zero, calculate the cosine similarity
        if denominator:
            score = numerator / float(denominator)

        return score, numPairs


    # Method to compute the similarity between movie pairs using the cosine similarity
    def reducer_compute_similarity(self, moviePair, ratingPairs):

        score, numPairs = self.cosine_similarity(ratingPairs)

        # Only yield results with more than 10 rating pairs and a similarity score above 0.95
        if (numPairs > 10 and score > 0.95):
            yield moviePair, (score, numPairs)


    # Method to sort movie similarities in descending order of similarity score
    def mapper_sort_similarities(self, moviePair, scores):

        score, n = scores
        movie1, movie2 = moviePair

        # Yield movie names with their corresponding similarity score and number of ratings
        yield (self.movieNames[int(movie1)], score), (self.movieNames[int(movie2)], n)


    # Method to output the final movie similarities after sorting
    def reducer_output_similarities(self, movieScore, similarN):

        movie1, score = movieScore

        # Yield the similarities between movies along with the number of ratings
        for movie2, n in similarN:
            yield movie1, (movie2, score, n)


if __name__ == '__main__':
    MovieSimilarities.run()
