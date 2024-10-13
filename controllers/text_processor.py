from models.keyword_search.keyword_identification import insertCluster, matchKeywords

class TextProcessor:
    def __init__(self, cluster_name, keywords=None):
        self.cluster_name = cluster_name
        
        # Insert keywords into the cluster if provided
        if keywords:
            insertCluster(keywords, self.cluster_name)

    def process(self, text):
        num_matches, matched_keywords, match_dict = matchKeywords(text, self.cluster_name)
        return {
            'message': text,
            'matches': num_matches,
            'matched_keywords': matched_keywords,
            'match_dict': match_dict
        }
