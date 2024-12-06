from app.data_models import db, Question, Tag, DifficultyLevel
from app import create_app

questions = {
    "Easy": [
        {
            "id": 9, 
            "topics": ["Math"],
            "question": "Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.",
            "name": "Palindrome Number"
        },
        {
            "id": 206,
            "topics": ["Linked List", "Recursion"],
            "question": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
            "name": "Reverse Linked List"
        },
        {
            "id": 344,
            "topics": ["Two Pointers", "String"],
            "question": "Write a function that reverses a string. The input string is given as an array of characters `s`.\n\nYou must do this by modifying the input array in-place with O(1) extra memory.",
            "name": "Reverse String"
        },
        {
            "id": 20,
            "topics": ["String", "Stack"],
            "question": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n\n- Open brackets must be closed by the same type of brackets.\n- Open brackets must be closed in the correct order.\n- Every close bracket has a corresponding open bracket of the same type.",
            "name": "Valid Parentheses"
        },
        {
            "id": 509,
            "topics": ["Math", "Dynamic Programming", "Recursion", "Memoization"],
            "question": "The Fibonacci numbers, commonly denoted `F(n)`, form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from `0` and `1`.\n\nGiven `n`, calculate `F(n)`.",
            "name": "Fibonacci Number"
        }

    ],
    "Medium": [
        {
            "id": 2,
            "topics": ["Linked List", "Recursion", "Math"],
            "question": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\nYou may assume the two numbers do not contain any leading zero, except the number `0` itself.",
            "name": "Add Two Numbers"
        },
        {
            "id": 873,
            "topics": ["Array", "Hash Table", "Dynamic Programming"],
            "question": "A sequence `x1, x2, ..., xn` is Fibonacci-like if:\n\n- `n >= 3`\n- `xi + xi+1 == xi+2` for all `i + 2 <= n`\n\nGiven a strictly increasing array `arr` of positive integers forming a sequence, return the length of the longest Fibonacci-like subsequence of `arr`. If one does not exist, return `0`.",
            "name": "Longest Fibonacci-Like Sequence"
        },
        {
            "id": 74,
            "topics": ["Array", "Binary Search", "Matrix"],
            "question": "You are given an m x n integer matrix `matrix` with the following two properties:\n\n- Each row is sorted in non-decreasing order.\n- The first integer of each row is greater than the last integer of the previous row.\n\nGiven an integer `target`, return `true` if `target` is in matrix or `false` otherwise.\n\nYou must write a solution in `O(log(m * n))` time complexity.",
            "name": "Search a 2D Matrix"
        },
        {
            "id": 75,
            "topics": ["Array", "Two Pointer", "String"],
            "question": "Given an array `nums` with `n` objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.\n\nWe will use the integers `0`, `1`, and `2` to represent the color red, white, and blue, respectively.\n\nYou must solve this problem without using the library's sort function.",
            "name": "Sort Colors"
        }
    ],
    "Hard": [
        {
            "id": 4,
            "topics": ["Array", "Binary Search", "Divide and Conquer"],
            "question": "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.\n\nThe overall run time complexity should be `O(log (m+n))`.",
            "name": "Median of Two Sorted Arrays"
        },
        {
            "id": 30,
            "topics": ["Hash Table", "String", "Sliding Window"],
            "question": "You are given a string `s` and an array of strings `words`. All the strings in `words` are of the same length.\n\nA concatenated string is a string that exactly contains all the strings of any permutation of `words` concatenated.\n\nFor example, if `words = [\"ab\",\"cd\",\"ef\"]`, then \"abcdef\", \"abefcd\", \"cdabef\", \"cdefab\", \"efabcd\", and \"efcdab\" are all concatenated strings. \"acdbef\" is not a concatenated string because it is not the concatenation of any permutation of `words`.\n\nReturn an array of the starting indices of all the concatenated substrings in `s`. You can return the answer in any order.",
            "name": "Substring with Concatenation of All Words"
        },
        {
            "id": 42,
            "topics":["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
            "question": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
            "name": "Trapping Rain Water"
        },
        {
            "id": 51,
            "topics": ["Array", "Backtracking"],
            "question": "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.\n\nGiven an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.\n\nEach solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively.",
            "name": "N-Queens"
        },
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