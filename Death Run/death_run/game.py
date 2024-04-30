import json
import random
import networkx as nx
from graph import generate_graph, edge_list_to_nx
from criminal import *
from student import *

jsonify = lambda d: {str(k): v for k, v in d.items() if v}


def play(
    edge_list: list[tuple[int, int, int]],
    begin: int,
    ends: list[int],
    criminals: list[tuple[str, BaseCriminal]],
    students: list[tuple[str, BaseStudent]],
):
    """Plays a game of Death Run 2."""
    criminals = [
        (criminal_name, criminal(edge_list, begin, ends))
        for (criminal_name, criminal) in criminals
    ]
    students = [
        (student_name, student(edge_list, begin, ends))
        for (student_name, student) in students
    ]

    edge_belong = {
        (u, v): {i: 0 for i in range(len(criminals))} for (u, v, _) in edge_list
    }  # Who weights belong to (for scoreboard reasons)
    edge_weights = {(u, v): w for (u, v, w) in edge_list}  # Edge weights as a dict
    edge_updates = {
        (u, v): 0 for (u, v, _) in edge_list
    }  # Previous round's edge updates (to pass to criminals)

    criminal_budgets = {i: 100 for i in range(len(criminals))}  # Criminal budget

    student_pos = {
        i: begin for i in range(len(students))
    }  # Each of the students' positions
    max_vertex = max(x for (_, x, _) in edge_list)
    vertex_count = {i: 0 for i in range(max_vertex + 1)}
    vertex_count[begin] = len(students)

    # Scoreboards
    criminal_scores = {i: 0 for i in range(len(criminals))}
    student_scores = {i: 0 for i in range(len(students))}

    # JSON Match Data
    criminal_match_data = {name: [] for name, _ in criminals}
    student_match_data = {name: [] for name, _ in students}

    sum_ends = lambda: sum(vertex_count[end] for end in ends)

    while sum_ends() < len(students):
        # Criminals turn
        next_edge_updates = {(u, v): 0 for (u, v, _) in edge_list}
        for i, (name, criminal) in enumerate(criminals):
            (u, v, w) = criminal.strategy(
                edge_updates, vertex_count, criminal_budgets[i]
            )
            criminal_match_data[name].append(
                (
                    (
                        jsonify(edge_updates),
                        jsonify(vertex_count),
                        criminal_budgets[i],
                    ),
                    (u, v, w),
                )
            )

            # Check weight in range and edge exists, o.w. do nothing
            if 0 <= w and w <= criminal_budgets[i] and (u, v) in edge_updates:
                criminal_budgets[i] -= w
                edge_belong[(u, v)][i] += w
                edge_weights[(u, v)] += w
                next_edge_updates[(u, v)] += w

            # print([(edge_belong[(u,v)][i], (u,v)) for (u,v) in edge_belong.keys() if edge_belong[(u,v)][i] > 0])

        # Students turn
        for i, (name, student) in enumerate(students):
            v = student.strategy(next_edge_updates, vertex_count, student_pos[i])
            student_match_data[name].append(
                (
                    (
                        jsonify(next_edge_updates),
                        jsonify(vertex_count),
                        student_pos[i],
                    ),
                    v,
                )
            )

            # Check that edge exists, o.w. take random out-edge
            if (student_pos[i], v) not in edge_updates:
                v = random.choice(
                    [
                        x
                        for (_, x, _) in filter(
                            lambda z: z[0] == student_pos[i], edge_list
                        )
                    ]
                )

            vertex_count[student_pos[i]] -= 1
            vertex_count[v] += 1

            for criminal_idx, contribution in edge_belong[(student_pos[i], v)].items():
                # print(criminal_idx, contribution)
                criminal_scores[criminal_idx] += contribution
            # print()
            student_scores[i] += edge_weights[(student_pos[i], v)]

            student_pos[i] = v

        edge_updates = next_edge_updates

    criminal_scores = {criminals[k][0]: v for k, v in criminal_scores.items()}
    student_scores = {students[k][0]: v for k, v in student_scores.items()}

    return criminal_scores, student_scores


# Edit the below
if __name__ == "__main__":
    NUM_TESTS = 10
    TOTAL_WINS = 0
    for test in range(NUM_TESTS):
        print(test)
        edge_list, begin, ends = generate_graph((15, 8), (1, 10), path="game.png")
        # edge_list, begin, ends = generate_graph((3, 3), (1, 10), path="game.png")

        criminals = [("Hybrid Criminal #1", HybridBetweenEvilAngryConstrainingRobinHoodCriminalAndAngryConstrainingRobinHoodCriminal), ("Evil Criminal #1", AngryConstrainingRobinHoodCriminal)]#("Angry Constraining Robin-Hood Criminal #1", AngryConstrainingRobinHoodCriminal), ("Robin-Hood Criminal #1", RobinHoodCriminal), ("Constraining Criminal #1", ConstrainingCriminal), ("Hot-Headed Criminal #1", HotHeadedCriminal), ("Miffed Criminal #1", MiffedCriminal), ("Crowd Criminal #1", CrowdCriminal), ("Cooldown Criminal #1", CooldownCriminal)]
        students = [("Random Greedy Student #1", RandomGreedyStudent), ("Random Greedy Student #2", RandomGreedyStudent), ("Random Greedy Student #3", RandomGreedyStudent), ("Greedy Student #4", GreedyStudent), ("Random Greedy Student #4", RandomGreedyStudent), ("Cautious Greedy Student #1", SimpleGreedyStudent), ("Random Greedy Student #5", RandomGreedyStudent), ("Cautious Avoidant Greedy Student #1", CautiousAvoidantGreedyStudent)]

        criminal_scores, student_scores = play(edge_list, begin, ends, criminals, students)

        G = edge_list_to_nx(edge_list)

        criminal_scores = {
            k: v
            for k, v in sorted(
                criminal_scores.items(), key=lambda item: item[1], reverse=True
            )
        }
        student_scores = {
            k: v for k, v in sorted(student_scores.items(), key=lambda item: item[1])
        }
        print("Student Leaderboard")
        for student, score in student_scores.items():
            print(f"{student}: {score}")
        print("Criminal Leaderboard")
        for criminal, score in criminal_scores.items():
            print(f"{criminal}: {score}")
        if criminal_scores["Hybrid Criminal #1"] < criminal_scores["Evil Criminal #1"]:
            TOTAL_WINS += 1
        print()
    print(TOTAL_WINS, TOTAL_WINS/NUM_TESTS)
