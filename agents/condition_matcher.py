class ConditionMatcherAgent:
    def match(self, symptoms):
        # Dummy mapping
        symptom_map = {
            "fever": ["flu", "dengue"],
            "cough": ["cold", "flu"],
            "headache": ["migraine", "flu"]
        }
        return {"flu": 0.85, "cold": 0.65}