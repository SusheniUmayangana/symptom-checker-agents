# agents/condition_matcher.py

class ConditionMatcherAgent:
    def __init__(self):
        print("Initialized ConditionMatcherAgent.")
        
        # Define the conditions and their associated symptoms
        self.condition_symptoms = {
            "common cold": ["cough", "sore throat", "runny nose"],
            "flu": ["fever", "cough", "sore throat", "body aches", "fatigue"],
            "migraine": ["headache", "nausea", "sensitivity to light"],
            "food poisoning": ["nausea", "vomiting", "diarrhea"]
        }

    def execute(self, symptoms: list) -> dict:
        """
        Matches detected symptoms to possible conditions.
        """
        scores = {}
        for condition, required_symptoms in self.condition_symptoms.items():
            # Calculate how many of the user's symptoms match the condition
            matched_symptoms = set(symptoms) & set(required_symptoms)
            score = len(matched_symptoms)
            if score > 0:
                scores[condition] = score
        
        # Sort conditions by how many symptoms matched
        sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        print(f"[ConditionMatcherAgent] Matched Conditions: {sorted_scores}")
        return sorted_scores