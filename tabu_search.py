import random
import math
from collections import deque
import os
import matplotlib.pyplot as plt

plt.ion()
cities = [(60, 200), (180, 200), (100, 180), (140, 180), (20, 160), (80, 160), (200, 160), (140, 140), (40, 120), (120, 120), (180, 100), (60, 80), (100, 80), (180, 60), (20, 40), (100, 40), (200, 40), (20, 20), (60, 20), (160, 20)]
iter = 2500     # počet iterácií
gengap = 10     # každých 'gengap' generácií sa uvoľní najstarší tabu ťah
tabu_queue = deque()   # poradie posledných ťahov (max 10)
tabu_set   = set()
gen= 0

def euclid(a, b):  # euklidovská vzdialenosť
    x1, y1 = a
    x2, y2 = b
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

n = len(cities)
D = [[0.0]*n for _ in range(n)]   # pripravime maticu n x n, dalo by sa ju zosekat kedze je redundantná ale privela pamata nam aj tak nezoberie tak to nechame tak:) 

    
for i in range(n):
    for j in range(n):
        D[i][j] = euclid(cities[i], cities[j])


def total_distance(tour, D):    # spočíta celkovú dĺžku trasy
    n = len(tour)
    if n < 2:
        return 0.0
    tour_distance = 0.0
    for i in range(n):
        x = tour[i]
        y = tour[(i + 1) % n]   # návrat na začiatok    
        tour_distance += D[x][y]
    return tour_distance
# skuska nejakej trasy
gut_tour = [0, 5, 12, 7, 18, 2, 9, 14, 3, 16, 11, 8, 19, 1, 10, 6, 4, 17, 15, 13]
bad_tour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # zle lebo chyba 
def is_valid_tour(tour, n): # kontrola platnosti trasy
    if len(tour) != n:
        print("Invalid tour length")
        return False
    if set(tour) != set(range(n)):
        print("Invalid tour content (duplicate or missing city)")
        return False
    return True # len by to malo vyhodit ak je nieco zle vypocitam si tu rovno aj velkost trasy


def make_initial_tour(n):
    return random.sample(range(n), n)

def two_opt_apply(tour, i, j):
    # otočí segment [i..j]
    return tour[:i] + list(reversed(tour[i:j+1])) + tour[j+1:]


def best_2opt_move(curr, D):       # vráti najlepší 2-opt ťah a zlepšenie
    global gen, tabu_queue, tabu_set, gengap
    n = len(curr)
    thebest_cost = float('inf')
    thebest_pair = None
    curr_cost = total_distance(curr, D)
    best_worse = float('inf')
    best_cost = curr_cost
    best_pair = None
    if gen>gengap:
        p = tabu_queue.popleft()
        tabu_set.remove(p)
    curr_cost_now = total_distance(curr, D)
    if gen % 200 == 0:                     # každá 200. generácia
        draw_tour(cities, curr, gen, curr_cost_now) # naživo do okna
    for i in range(1, n-1):          
        for j in range(i+1, n):# j > i
            p = (min(i, j), max(i, j))
            if p in tabu_set:
                continue
            cand = curr[:i] + list(reversed(curr[i:j+1])) + curr[j+1:]
            cand_cost = total_distance(cand, D)
            if cand_cost < best_cost:
                best_cost = cand_cost
                best_pair = (i, j)
            if cand_cost > best_cost:
                if cand_cost < best_worse:
                    best_worse = cand_cost
                    best_pair = (i, j)
            if cand_cost < thebest_cost:
                thebest_cost = cand_cost
                thebest_pair = (i, j)
    if best_pair is not None:
        p_best = best_pair if best_pair[0] < best_pair[1] else (best_pair[1], best_pair[0])
        tabu_queue.append(p_best)
        tabu_set.add(p_best)
    gen += 1
    if curr_cost == best_cost:
        return best_pair, (best_worse - curr_cost)
    else:
        return best_pair, (best_cost - curr_cost)
        
        
# štart
def draw_tour(cities, tour, gen, cost, save_dir=None):
    xs = [cities[i][0] for i in tour] + [cities[tour[0]][0]]
    ys = [cities[i][1] for i in tour] + [cities[tour[0]][1]]

    plt.clf()
    ax = plt.gca()
    ax.plot(xs, ys, marker='o')            # hrana + uzly
    ax.scatter(xs[0], ys[0], s=80)         
    ax.set_aspect('equal', 'box')
    ax.set_title(f"Gen {gen} | cost = {cost:.2f}")
    ax.set_xlabel("x"); ax.set_ylabel("y")      
    plt.tight_layout()
    plt.pause(0.001)                       

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        plt.savefig(os.path.join(save_dir, f"tour_gen_{gen:05d}.png"))

curr = make_initial_tour(n)
best_global_tour = curr[:]                          
best_global_cost = total_distance(curr, D)
draw_tour(cities, curr, gen, total_distance(curr, D))
print("start:", total_distance(curr, D))

best_progress = [best_global_cost]   # y: best-so-far; prvý bod = štart
curr_progress = [best_global_cost]   # y: current; prvý bod = štart
iters_done = 0                       # x: koľko krokov sme reálne vykonali


for q in range(iter):
    pair, d = best_2opt_move(curr, D)
    i, j = pair
    curr = two_opt_apply(curr, i, j)

    # ← NEW: prepočítaj aktuálnu cenu a prípadne zlepši globálny best
    curr_cost_now = total_distance(curr, D)
    if curr_cost_now < best_global_cost:     # malá epsilon pre float
        best_global_cost = curr_cost_now
        best_global_tour = curr[:]

    # voliteľné kreslenie priebehu
    if gen % 200 == 0:
        draw_tour(cities, curr, gen, curr_cost_now)

    curr_progress.append(curr_cost_now)
    best_progress.append(best_global_cost)
    iters_done += 1

print("najlepsia dlzka", best_global_cost)
print("dlzka tabu:", len(tabu_set))
draw_tour(cities, curr, gen, total_distance(curr, D))
draw_tour(cities, best_global_tour, gen, best_global_cost)

plt.figure(figsize=(10, 5))
x = list(range(iters_done + 1))      
plt.plot(x, best_progress, label="Best-so-far")
plt.plot(x, curr_progress, label="Current")
plt.title("Tabu Search – konvergencia")
plt.xlabel("Iterácia (krok 0 = štart)")
plt.ylabel("Dĺžka okruhu")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.ioff()
plt.show()
