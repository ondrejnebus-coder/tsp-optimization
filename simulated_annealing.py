import random
import math
from collections import deque
import os
import matplotlib.pyplot as plt

cities = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
T = 10000.0      # počiatočná teplota 
alpha = 0.995   # chladenie
iter = 2500     # počet sweepov

plt.ion()

def euclid(a, b):
    x1, y1 = a
    x2, y2 = b
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# matica vzdialeností
n = len(cities)
D = [[0.0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        D[i][j] = euclid(cities[i], cities[j])

def total_distance(tour, D):
    n = len(tour)
    if n < 2:
        return 0.0
    tour_distance = 0.0
    for i in range(n):
        x = tour[i]
        y = tour[(i + 1) % n]
        tour_distance += D[x][y]
    return tour_distance

def shuffling(tour, i ,j):
    seg = tour[i:j+1][:]
    random.shuffle(seg)
    return tour[:i] + seg + tour[j+1:]

def neighbr_shuffle(tour, T, D, best_tour, best_cost):
    n = len(tour)
    curr = tour[:]
    curr_cost = total_distance(curr, D)

    for i in range(1, n-1):
        for j in range(i+1, n):
            cand = shuffling(curr, i, j)
            cand_cost = total_distance(cand, D)
            delta = cand_cost - curr_cost

            # Metropolis akceptácia
            if delta <= 0 or random.random() < math.exp(-delta / T):
                curr = cand
                curr_cost = cand_cost
                if curr_cost < best_cost:
                    best_cost = curr_cost
                    best_tour = curr[:]

    return curr, curr_cost, best_tour, best_cost

def draw_tour(cities, tour, gen, cost, save_dir=None):
    xs = [cities[i][0] for i in tour] + [cities[tour[0]][0]]
    ys = [cities[i][1] for i in tour] + [cities[tour[0]][1]]

    plt.clf()
    ax = plt.gca()
    ax.plot(xs, ys, marker='o')
    ax.scatter(xs[0], ys[0], s=80)
    ax.set_aspect('equal', 'box')
    ax.set_title(f"Gen {gen} | cost = {cost:.2f}")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    plt.tight_layout()
    plt.pause(0.1)

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        plt.savefig(os.path.join(save_dir, f"tour_gen_{gen:05d}.png"))

# --- štart ---
init = list(range(n))
random.shuffle(init)
print("Initial distance:", total_distance(init, D))
curr = init[:]
best_tour = curr[:]
best_cost = total_distance(curr, D)

# LOGY NA GRAF + počítadlo iterácií
best_progress = [best_cost]      # y: best-so-far (bod 0 = štart)
curr_progress = [best_cost]      # y: current (bod 0 = štart)
iters_done = 0                   # x: koľko sweepov prebehlo

for ep in range(1, iter+1):
    curr, curr_cost, best_tour, best_cost = neighbr_shuffle(curr, T, D, best_tour, best_cost)

    # priebežné kreslenie
    if ep % 100 == 0:
        draw_tour(cities, curr, ep, curr_cost); plt.pause(0.001)

    # logovanie priebehu
    curr_progress.append(curr_cost)
    best_progress.append(best_cost)
    iters_done += 1

    T *= alpha

print("SA best:", best_cost)

# --- KONVERGENČNÝ GRAF: vývoj dĺžky okruhu v čase ---
plt.figure(figsize=(10, 5))
x = list(range(iters_done + 1))   # osi X = iterácie

# priebeh najlepšej doterajšej a aktuálnej hodnoty
plt.plot(x, best_progress, label="Najlepšie doteraz (best-so-far)", linewidth=2)
plt.plot(x, curr_progress, label="Aktuálne riešenie (current)", linestyle="--")

# popisy a formátovanie
plt.title("Simulated Annealing – konvergencia riešenia")
plt.xlabel("Iterácia (počet sweepov)")
plt.ylabel("Celková dĺžka trasy")
plt.legend()
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.show()

plt.ioff()
plt.show()
