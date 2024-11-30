from flask_socketio import SocketIO, emit
from app import socketio
from flask import request
import random
import pprint
from app.chatbot_manager import ChatbotManager
import re
import json
  
user_sessions = {}
chatbot_manager = ChatbotManager()


"""
KEY = Session ID for user   VALUE = Object containing:
- conversation: List of conversation messages: [{role: "user", "content": [{"type": "text", "text": convo message}] }, {}, {}]
- difficulty: String (Easy, Medium, Hard)
- question: String (LeetCode-style problem statement)
"""
questions = {
    "Easy": [
        {
            "id": 9, 
            "topics": ["Math"],
            "question": "Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise."
        },
        {
            "id": 206,
            "topics": ["Linked List", "Recursion"],
            "question": "Given the head of a singly linked list, reverse the list, and return the reversed list."
        },
        {
            "id": 344,
            "topics": ["Two Pointers", "String"],
            "question": "Write a function that reverses a string. The input string is given as an array of characters `s`.\n\nYou must do this by modifying the input array in-place with O(1) extra memory."
        },
        {
            "id": 20,
            "topics": ["String", "Stack"],
            "question": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n\n- Open brackets must be closed by the same type of brackets.\n- Open brackets must be closed in the correct order.\n- Every close bracket has a corresponding open bracket of the same type."
        },
        {
            "id": 509,
            "topics": ["Math", "Dynamic Programming", "Recursion", "Memoization"],
            "question": "The Fibonacci numbers, commonly denoted `F(n)`, form a sequence, called the Fibonacci sequence, such that each number is the sum of the two preceding ones, starting from `0` and `1`. That is:\n\n`F(0) = 0`, `F(1) = 1`\n`F(n) = F(n - 1) + F(n - 2)`, for `n > 1`.\n\nGiven `n`, calculate `F(n)`."
        }

    ],
    "Medium": [
        {
            "id": 2,
            "topics": ["Linked List", "Recursion", "Math"],
            "question": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\nYou may assume the two numbers do not contain any leading zero, except the number `0` itself."
        },
        {
            "id": 873,
            "topics": ["Array", "Hash Table", "Dynamic Programming"],
            "question": "A sequence `x1, x2, ..., xn` is Fibonacci-like if:\n\n- `n >= 3`\n- `xi + xi+1 == xi+2` for all `i + 2 <= n`\n\nGiven a strictly increasing array `arr` of positive integers forming a sequence, return the length of the longest Fibonacci-like subsequence of `arr`. If one does not exist, return `0`.\n\nA subsequence is derived from another sequence `arr` by deleting any number of elements (including none) from `arr`, without changing the order of the remaining elements. For example, `[3, 5, 8]` is a subsequence of `[3, 4, 5, 6, 7, 8]`."
        },
        {
            "id": 74,
            "topics": ["Array", "Binary Search", "Matrix"],
            "question": "You are given an m x n integer matrix `matrix` with the following two properties:\n\n- Each row is sorted in non-decreasing order.\n- The first integer of each row is greater than the last integer of the previous row.\n\nGiven an integer `target`, return `true` if `target` is in matrix or `false` otherwise.\n\nYou must write a solution in `O(log(m * n))` time complexity."
        },
        {
            "id": 75,
            "topics": ["Array", "Two Pointer", "String"],
            "question": "Given an array `nums` with `n` objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.\n\nWe will use the integers `0`, `1`, and `2` to represent the color red, white, and blue, respectively.\n\nYou must solve this problem without using the library's sort function."
        },      

    ],
    "Hard": [
        {
            "id": 4,
            "topics": ["Array", "Binary Search", "Divide and Conquer"],
            "question": "Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.\n\nThe overall run time complexity should be `O(log (m+n))`."
        },
        {
            "id": 30,
            "topics": ["Hash Table", "String", "Sliding Window"],
            "question": "You are given a string `s` and an array of strings `words`. All the strings in `words` are of the same length.\n\nA concatenated string is a string that exactly contains all the strings of any permutation of `words` concatenated.\n\nFor example, if `words = [\"ab\",\"cd\",\"ef\"]`, then \"abcdef\", \"abefcd\", \"cdabef\", \"cdefab\", \"efabcd\", and \"efcdab\" are all concatenated strings. \"acdbef\" is not a concatenated string because it is not the concatenation of any permutation of `words`.\n\nReturn an array of the starting indices of all the concatenated substrings in `s`. You can return the answer in any order."

        },
        {
            "id": 42,
            "topics":["Array", "Two Pointers", "Dynamic Programming", "Stack", "Monotonic Stack"],
            "question": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining."
        },
        {
            "id": 51,
            "topics": ["Array", "Backtracking"],
            "question": "The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.\n\nGiven an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.\n\nEach solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively."
        },
        {
            "id": 124,
            "topics": ["Dynamic Programming", "Tree", "Depth-First Search", "Binary Tree"],
            "question": "A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.\n\nThe path sum of a path is the sum of the node's values in the path.\n\nGiven the root of a binary tree, return the maximum path sum of any non-empty path."
        }
    ],
}

pp = pprint.PrettyPrinter(width=1000, compact=False)

@socketio.on('connect') #listening for an event
def handle_connect():
    sid = request.sid
    user_sessions[sid] = {
        'conversation': []
    }  # append a client identifier (if needed )
    print("Client connected")
    emit('message', {'data': 'Welcome to the WebSocket server!'}) #emitting an event (client would have to listen for message)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    removed_session = user_sessions.pop(sid, None)
    
    if removed_session:
        print(f"Session for {sid} removed.")
    else:
        print(f"No session found for {sid}.")
    
    print("Client disconnected")


@socketio.on('select_difficulty')
def handle_select_difficulty(data):
    sid = request.sid
    difficulty = data.get('difficulty')
    
    if difficulty not in questions:
        emit('bot_message', {'message': 'Invalid difficulty selected. Please choose Easy, Medium, or Hard.'})
        return

    question = getQuestion(difficulty)
    
    # Create session with difficulty and question, populate the conversation field with the system prompt and initial interview question
    user_sessions[sid] = {
        'conversation': [
            {
                "role": "system", 
                "content": [{"type": "text", "text": "You are a technical interviewer at a top FAANG company. Your role is to assess a candidate's problem-solving skills through structured guidance and follow-up questions. Follow these rules to ensure a smooth and logical flow of conversation:\
              \
              1. **DO NOT analyze their code every time**:\
                 - The candidate sends their current code implementation with every follow up, sometimes its empty, other times its not.\
                 - Only analyze the code when explicitly asked, or when the candidate has updated their implementation.\
                 - You should primarily focus on the user input to guide the conversation\
              2. **DO NOT give the candidate answers**:\
                 - The goal of the interview is to get a sense of the candidates problem solving skills. Let them solve the question by themselves, do not give them answers. \
                 - Do not point out small errors in the users code. For example, do not point out syntax errors.\
              3. **Acknowledge and Progress**:\
                 - When the user provides an answer, acknowledge it and as the next follow up question. Flow of conversation should be as follows.\
                  1. Start by asking the technical question. Answer any simple questions about the question. For example, you are allowed to clarify data types.\
                  2. Guide them to offer you a solution in Code if they haven't.\
                  3. Analyze their code based on the rules in number one. Ask them what the time complexity is.\
                  4. If their solution is not optimal for time complexity, ask them if there is a way to optimize it further, but do not give them the answer as to how. Also, only ask them to optimize if there is a real substantial difference that can be made. For example if its possible to go from O(n^2) to O(n).\
                  5. Ask them what the space complexity is. \
                  6. If either their solution is correct, or if the candidate struggles and can't get anywhere without answers, then thank the candidate for their time and kindly ask them to submit their solution. \
              4. **Never Repeat the Same Phrase**:\
                 - Use varied phrasing and ask different types of questions to avoid redundancy.\
              5. **Limit Depth of Exploration**:\
                 - Spend no more than two follow-up questions exploring a single topic (e.g., time complexity).\
                 - Try to limit it to one follow-up question if possible"}]
            },
                {
                "role": "assistant", 
                "content": [{"type": "text", "text": f"Hello my name is Cody, I'll be your interviewer. Let's get started with your question:\n\n {question}" }]
            }
        ]

    }
    
    # emit the bot_message for the frontend
    bot_message = f"Hello my name is Cody, I'll be your interviewer. Let's get started with your question:\n\n {question}"
    emit('bot_message', {'message': bot_message})
    print(f"Session updated for {sid}: {user_sessions[sid]}")


@socketio.on('user_message')
def handle_user_message(data):
    sid = request.sid

    user_message = data.get('message', '')
    code = data.get('code', '')
    session = user_sessions.get(sid)

    if session:

        # Save user message in convo (and code if then sent some)
        session['conversation'].append({'role': 'user', 'content': [{"type": "text", "text": user_message}]})
        if code != '':
            session['conversation'][-1]['content'].append({"type": "text", "text": code})
        
        print(f"Updated conversation for {sid}:")
        pp.pprint(session["conversation"])

        print(f"PRINTING OUT THE WHOLE OBJECT IN USER_SESSIONS FOR GIVEN SID:")
        pp.pprint(user_sessions[sid])

        # GENERATE THE BOT RESPONSE
        # We pass in the entire conversation to the api
        bot_reply = chatbot_manager.generate_response(session['conversation'])

        # Save bot reply
        session['conversation'].append({'role': 'assistant', 'content': [{'type': 'text', 'text': bot_reply}]})
        pp.pprint(f"Bot reply added to conversation for {sid}: {bot_reply}")
        emit('bot_message', {'message': bot_reply})
    else:
        emit('bot_message', {'message': 'Please select a difficulty to start the interview.'})
        print(f"No session found for {sid}. Prompting user to select difficulty.")


@socketio.on('submit_solution')
def handle_submit_solution():
    sid = request.sid
    session = user_sessions.get(sid)

    if session:
        # TODO: Store the convo in a database
        
        # get final analysis
        final_analysis = chatbot_manager.generate_final_analysis(session['conversation'])

        # gpt returns markdown formatting of json, so remove before sending to frontend
        final_analysis = re.sub(r'```json|```', '', final_analysis).strip()
    
        # make sure that the json is valid
        try:
            final_analysis = json.loads(final_analysis)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format after cleaning.")
        print("FINAL ANALYSIS PARSED JSON: " + str(final_analysis))

        # emit final analysis for frontend
        emit('final_analysis', {'analysis': final_analysis})
    else:
        emit('error', {'message': 'No session found. Please start the interview first.'})


def getQuestion(difficulty):
    """
    qs = questions[difficulty]
    for q in qs:
        if q["id"] == 30:
            return q["question"]
    return "idk"
    """

    if difficulty not in questions:
        return "Invalid difficulty"

    qs = questions[difficulty]

    random_question = random.choice(qs)
    
    return random_question["question"]