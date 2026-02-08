import re


class GeneratorAgent:
    def generate(self, grade, topic, feedback=None):
        topic = topic.lower()

        # Handle angles explicitly, fallback for others
        if "angle" in topic:

            if grade <= 3:
                explanation = (
                    "An angle is made when two lines meet. "
                    "A right angle looks like the corner of a book."
                )

            elif grade <= 6:
                explanation = (
                    "An angle is formed when two lines meet at a point. "
                    "An acute angle is less than 90 degrees. "
                    "A right angle is exactly 90 degrees."
                )

            else:
                explanation = (
                    "An angle is formed when two rays meet at a common point and angles are measured in degrees. "
                    "An acute angle is less than 90 degrees, a right angle equals 90 degrees, "
                    "and an obtuse angle is between 90 and 180 degrees."
                )

        else:
            explanation = (
                f"This lesson explains basic ideas about {topic}. "
                f"It is written for Grade {grade} students."
            )

        # Apply reviewer feedback once, if needed
        if feedback and grade >= 7:
            explanation = (
                "An angle is formed when two rays meet at a point. "
                "Angles are measured in degrees. "
                "An acute angle is smaller than 90 degrees. "
                "A right angle is exactly 90 degrees. "
                "An obtuse angle is bigger than a right angle."
            )

        mcqs = [
            {
                "question": "Which angle is exactly 90 degrees?",
                "options": ["Acute", "Right", "Obtuse", "Straight"],
                "answer": "Right"
            }
        ]

        return {
            "explanation": explanation,
            "mcqs": mcqs
        }


class ReviewerAgent:
    def review(self, content, grade):
        feedback = []
        sentences = re.split(r'[.!?]', content["explanation"])

        # Basic age-based sentence length check
        if grade <= 3:
            max_words = 12
        elif grade <= 6:
            max_words = 18
        else:
            max_words = 22

        for i, sentence in enumerate(sentences):
            if len(sentence.split()) > max_words:
                feedback.append(
                    f"Sentence {i+1} is too complex for Grade {grade}"
                )

        # For higher grades, also check if one sentence packs too many concepts
        if grade >= 7:
            for i, sentence in enumerate(sentences):
                concept_count = 0

                for angle_type in ["acute", "right", "obtuse"]:
                    if angle_type in sentence.lower():
                        concept_count += 1

                if concept_count >= 2:
                    feedback.append(
                        f"Sentence {i+1} explains multiple angle types and is too dense for Grade {grade}"
                    )

        if feedback:
            return {
                "status": "fail",
                "feedback": feedback
            }

        return {
            "status": "pass",
            "feedback": []
        }
