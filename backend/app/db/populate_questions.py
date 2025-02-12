from app import create_app, db
from app.models.question import Question, DifficultyLevel
from app.models.tag import Tag

questions = {
    "Easy": [
        {
            "id": 509,
            "topics": ["Math", "Dynamic Programming", "Recursion", "Memoization"],
            "question": "The Fibonacci numbers, commonly denoted `F(n)`, form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from `0` and `1`.\n\nGiven `n`, calculate `F(n)`.",
            "name": "Fibonacci Number"
        }

    ],
    "Medium": [
        {
            "id": 873,
            "topics": ["Array", "Hash Table", "Dynamic Programming"],
            "question": "A sequence `x1, x2, ..., xn` is Fibonacci-like if:\n\n- `n >= 3`\n- `xi + xi+1 == xi+2` for all `i + 2 <= n`\n\nGiven a strictly increasing array `arr` of positive integers forming a sequence, return the length of the longest Fibonacci-like subsequence of `arr`. If one does not exist, return `0`.",
            "name": "Longest Fibonacci-Like Sequence"
        }
    ],
    "Hard": [
        {
            "id": 124,
            "topics": ["Dynamic Programming", "Tree", "Depth-First Search", "Binary Tree"],
            "question": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.\n\nThe path sum of a path is the sum of the node's values in the path.\n\nGiven the root of a binary tree, return the maximum path sum of any non-empty path.",
            "name": "Binary Tree Maximum Path Sum"
        }
    ]
}

def populate_db():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()

        # Recreate all tables with new schema
        db.create_all()

        existing_tags = {t.name: t for t in Tag.query.all()}

        for difficulty_str, questions_list in questions.items():
            difficulty_enum = DifficultyLevel[difficulty_str.upper()]

            for q_data in questions_list:
                q_id = q_data["id"]
                q_content = q_data["question"]
                q_topics = q_data["topics"]
                q_name = q_data["name"]  

                new_question = Question(
                    id=q_id,
                    content=q_content,
                    difficulty=difficulty_enum,
                    name=q_name
                )

                for topic in q_topics:
                    if topic not in existing_tags:
                        new_tag = Tag(name=topic)
                        db.session.add(new_tag)
                        db.session.flush()  
                        existing_tags[topic] = new_tag
                    new_question.tags.append(existing_tags[topic])

                db.session.add(new_question)

        db.session.commit()
        print("Database has been dropped, recreated, and populated successfully!")

if __name__ == "__main__":
    populate_db()