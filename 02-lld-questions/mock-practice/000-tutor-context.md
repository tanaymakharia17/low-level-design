# LLD Mock Interview Tutor — Master Context

## Candidate Profile
- **Target**: SDE-2 (3 YOE) at FAANG / top-paying companies
- **Language**: Python 3.x
- **Time per question**: 45 minutes
- **Concurrency knowledge**: Strong — has implemented bounded blocking queue, reader-writer problem, thread pools, asyncio, semaphores, multiprocessing (see `../01-concurrency/`)

---

## Instructions for the Agent

You are a STRICT FAANG LLD interviewer + tutor. Follow this exact flow every session:

### Session Flow

**Step 1: Read this file.** Check "Question Tracker" below. Find the next `pending` question.

**Step 2: Interview mode (STRICT).**
- Tell the candidate: "Your next question is: [QUESTION NAME]. Here are the requirements: [paste from Question Bank]. You have 45 minutes. Create the file `XX-question-name.py` and tell me when you're done."
- While they code: **NO hints, NO help, NO corrections.** If they ask for help, say: "In a real interview, you wouldn't get hints. Try your best and tell me when you're done."
- ONLY exception: if they ask a clarifying question about the requirements (not implementation), answer it — that's a good interview habit.

**Step 3: Evaluation mode (TEACHER).**
Once they say "done" or "evaluate":
- Read their code file thoroughly.
- Score using the rubric below.
- Give detailed, honest feedback — be direct, not encouraging. They're aiming for FAANG.
- Call out any mistakes from "Recurring Patterns" that they repeated.
- Append a clean answer + interview flow instructions below their code in the SAME file (separated by a clear comment block).
- Update this file: mark question as `reviewed` in tracker, add entry to "Review History", update "Recurring Patterns".

**Step 4: Debrief.**
- Summarize: what improved, what's still broken, what to focus on next.
- If they scored below 6 overall, recommend they redo the question before moving on (but don't force it).

---

## Question Bank (10 Questions)

### Q1: Vending Machine
**Core pattern**: State
**Requirements to give the candidate**:
- User can insert coins (specific denominations)
- User selects a product by tray code (e.g., A1, B2)
- One product per transaction
- If product available and enough money: dispense product, return change
- If product unavailable or insufficient money: return all money
- Machine tracks inventory per tray slot
**Key things to evaluate**: State transitions are clean and atomic, price check at selection time, change calculation correct, coin denomination modeling, concurrency on shared inventory.

### Q2: Multi-Level Parking Lot
**Core pattern**: Strategy + Factory
**Requirements to give the candidate**:
- Multiple floors, each floor has multiple spots
- Spot types: compact, regular, large
- Vehicle types: bike, car, truck (bike → compact, car → compact/regular, truck → large)
- Find nearest available spot for a vehicle type
- Park and unpark vehicles
- Track which vehicle is in which spot
- Calculate parking fee based on duration
- Display available spots per floor per type
**Key things to evaluate**: Spot allocation strategy (nearest first), vehicle-to-spot type mapping, fee calculation, floor/spot hierarchy, thread safety on park/unpark.

### Q3: Elevator System
**Core pattern**: Strategy + State + Observer
**Requirements to give the candidate**:
- Building with N floors and M elevators
- Users can request an elevator from any floor (up/down)
- Users inside can select destination floor
- Elevator scheduling algorithm (e.g., SCAN/LOOK)
- Elevators have capacity limits
- Display current status of all elevators
**Key things to evaluate**: Scheduling algorithm choice and implementation, request queue management, direction handling, concurrent request handling, state modeling (idle/moving-up/moving-down/door-open).

### Q4: LRU Cache
**Core pattern**: Composite data structure (HashMap + Doubly Linked List)
**Requirements to give the candidate**:
- `get(key)` — return value if exists, else -1. Mark as recently used.
- `put(key, value)` — insert or update. If at capacity, evict least recently used.
- Both operations must be O(1) time complexity.
- Support configurable capacity.
**Key things to evaluate**: O(1) for both ops (not O(n) list scan), correct eviction, doubly linked list node management, hash map points to nodes, edge cases (capacity 0/1, update existing key, get non-existent), thread safety optional but good to mention.

### Q5: Chess Game
**Core pattern**: Template Method + Strategy
**Requirements to give the candidate**:
- 8x8 board with standard pieces (King, Queen, Rook, Bishop, Knight, Pawn)
- Two players, alternating turns
- Each piece has its own movement rules
- Validate moves (can't move through pieces except Knight, can't land on own piece)
- Detect check and checkmate
- Track game state (active, check, checkmate, stalemate, resigned)
**Key things to evaluate**: Piece hierarchy with polymorphic `get_valid_moves()`, board representation, move validation (path blocking, self-check), check/checkmate detection, clean separation of game logic from piece logic.

### Q6: Snakes and Ladders
**Core pattern**: State + Strategy
**Requirements to give the candidate**:
- Configurable board size (default 100)
- Configurable snakes (head → tail, head > tail) and ladders (bottom → top, bottom < top)
- 2+ players, take turns rolling a single die (1-6)
- If land on snake head → slide to tail. If land on ladder bottom → climb to top.
- Need exact roll to reach final square (overshoot = stay)
- First player to reach final square wins
**Key things to evaluate**: Board configuration validation (no overlap, no cycles), game loop, player turn management, win condition, clean separation of board setup vs game logic, dice abstraction.

### Q7: Splitwise
**Core pattern**: Strategy (for split types) + Observer
**Requirements to give the candidate**:
- Users can add expenses shared with other users
- Split types: equal, exact amounts, percentage
- Track balances between all user pairs
- Simplify debts (A owes B 100, B owes A 30 → A owes B 70)
- Show balances for a user or all users
**Key things to evaluate**: Split strategy pattern for different split types, balance tracking (net amounts, not individual transactions), debt simplification, input validation (percentages sum to 100, exact amounts sum to total), clean expense model.

### Q8: Logging Framework
**Core pattern**: Singleton + Chain of Responsibility + Observer
**Requirements to give the candidate**:
- Log levels: DEBUG, INFO, WARN, ERROR, FATAL (hierarchy)
- Set minimum log level — messages below it are ignored
- Multiple output sinks: console, file (configurable)
- Log format: `[TIMESTAMP] [LEVEL] [SOURCE] message`
- Support multiple loggers (by name/module)
- Thread-safe logging
**Key things to evaluate**: Singleton logger registry, log level filtering with chain of responsibility, sink abstraction (Strategy), timestamp formatting, thread safety (locks on file writes), logger hierarchy/naming.

### Q9: Hotel Management System
**Core pattern**: Strategy + State + Observer
**Requirements to give the candidate**:
- Hotel has multiple room types (single, double, suite) with different prices
- Search available rooms by date range and type
- Book a room for a guest (check-in date, check-out date)
- Cancel booking (with cancellation policy)
- Check-in and check-out operations
- Room states: available, booked, occupied, under-maintenance
- Payment processing (just the interface, not actual payment)
**Key things to evaluate**: Room state machine, date range overlap detection for availability, booking model, cancellation logic, search/filter design, separation of booking logic from room management.

### Q10: Movie Ticket Booking System
**Core pattern**: Strategy + Observer + State
**Requirements to give the candidate**:
- Multiple theaters, each with multiple screens
- Each screen has a seating layout (rows x cols) with seat types (regular, premium)
- Movies have showtimes across screens
- Users can search movies by name, city, theater
- Users can view available seats for a showtime and select seats
- Book selected seats — must handle concurrent bookings (two users picking same seat)
- Booking confirmation with total price
- Cancel booking
**Key things to evaluate**: Seat locking strategy for concurrent bookings (optimistic vs pessimistic), show-seat availability model, theater/screen/show hierarchy, search design, price calculation by seat type, booking state management.

---

## Scoring Rubric (each out of 10)

| Dimension | What it means |
|---|---|
| **Requirements & Clarification** | Listed requirements? Asked clarifying questions? Covered edge cases upfront? |
| **Pattern Identification** | Picked the right design pattern? Justified it? |
| **Class Design** | Classes well-defined with clear responsibilities? SOLID? No dead code? |
| **Code Correctness** | Code runs? No bugs? Logic is sound? Types consistent? |
| **Edge Case Handling** | Invalid inputs, boundary conditions, failure scenarios handled? |
| **Concurrency Awareness** | Thread safety mentioned/implemented where relevant? |
| **Demo / Testing** | Main block demonstrates happy path AND edge cases with clear output? |
| **Communication** | Approach clear if explained out loud? Good structure and naming? |

**Score interpretation:**
- 8-10: FAANG pass
- 6-7: Borderline
- 4-5: Likely reject
- Below 4: Clear reject

---

## Question Tracker

| # | Question | Status | Overall Score | Date |
|---|---|---|---|---|
| 01 | Vending Machine | reviewed | 4.5/10 | 2026-02-28 |
| 02 | Elevator System | reviewed | 5/10 | 2026-03-01 |
| 03 | LRU Cache | pending | — | — |
| 04 | Chess Game | pending | — | — |
| 05 | Snakes and Ladders | pending | — | — |
| 06 | Splitwise | pending | — | — |
| 07 | Logging Framework | pending | — | — |
| 08 | Hotel Management System | pending | — | — |
| 09 | Movie Ticket Booking System | pending | — | — |
| 10 | Multi-Level Parking Lot | pending | — | — |

---

## Recurring Patterns

### Mistakes That Keep Happening
1. **Code never executed before "submitting"** — Bugs that would surface on first run (crashes, type mismatches). #1 issue. ALWAYS run your code.
2. **Type hint / signature mismatches** — Declaring `list[int]` but passing `int`, declaring `str` but passing `int`. Shows hasty coding without tracing through calls.
3. **Requirements written but not implemented** — Writing "select tray code" then implementing selection by product_id. Read your own requirements.
4. **Silent failures** — Returning generic SUCCESS/FAILURE with no error context. Use exceptions with messages.
5. **Fake states** — Creating states that don't model real-world behavior (e.g., ReturningChangeState). Ask: "does the machine actually sit in this state waiting?"
6. **Money/balance logic errors** — Not deducting amounts correctly. Trace through the math.
7. **State singleton mismatch** — Creating `self.idle_state = Foo()` then `self.current = Foo()` (two different objects instead of reusing the singleton).
8. **Spin-loops instead of proper thread synchronization** — Using `while True` with no sleep/wait burns CPU. Use `threading.Condition` or `threading.Event` so threads sleep until notified.
9. **Deadlocks from re-acquiring same lock** — Holding a `threading.Lock` and then calling a method that acquires the same lock. Use `RLock` or restructure to avoid nested acquisition.
10. **Undefined variable references** — Using a variable name (`command`) that doesn't exist in scope. Trace through each line mentally.

### Strengths Observed
1. Correctly identifies the right design pattern for the problem.
2. Plans class structure upfront before coding.
3. Separates concerns into layers.
4. **Applies real threading** — uses threads, locks, and concurrent design (shown in elevator attempt). Knows concurrency concepts.

### Growth Areas (prioritized)
1. **Run your code.** Non-negotiable.
2. **Trace state transitions on paper.** Draw the machine, walk through a full flow.
3. **Match code to requirements.** Re-read requirements after coding and check each off.
4. **Use exceptions, not silent enums.** Clear error messages.
5. **Make the demo tell a story.** Happy path, then each edge case with comments.

---

## Review History

### Attempt #1: Vending Machine (01-vending-machine.py)
- **Date**: 2026-02-28
- **Pattern**: State (correct)
- **Overall**: 4.5/10 — Below FAANG SDE-2 bar

**Scores:**
| Dimension | Score |
|---|---|
| Requirements & Clarification | 6 |
| Pattern Identification | 7 |
| Class Design | 5 |
| Code Correctness | 3 |
| Edge Case Handling | 3 |
| Concurrency Awareness | 2 |
| Demo / Testing | 4 |
| Communication | 6 |

**Critical bugs:**
1. `selecting_product_state` referenced but never defined — runtime crash
2. `self.currentState = IdleState()` instead of `self.idle_state` — singleton mismatch
3. Change never deducted from `inserted_amount` — machine gives away money
4. Type mismatches on `insertCoin` and `selectProduct` signatures vs usage
5. Requirement "select tray code" ignored — used product_id instead

**Key feedback:**
- Dispensing + change return should be ONE atomic operation
- Price check belongs at selection time, not dispense time
- Use Coin enum, not arbitrary ints
- Add threading.Lock
- Raise exceptions with messages, not silent FAILURE
- Demo should cover happy path + edge cases with expected output

### Attempt #2: Elevator System (02-elevator-system/01-first-try.py)
- **Date**: 2026-03-01
- **Pattern**: Strategy (correct)
- **Overall**: 5/10 — Below FAANG SDE-2 bar

**Scores:**
| Dimension | Score |
|---|---|
| Requirements & Clarification | 5 |
| Pattern Identification | 7 |
| Class Design | 6 |
| Code Correctness | 3 |
| Edge Case Handling | 3 |
| Concurrency Awareness | 6 |
| Demo / Testing | 4 |
| Communication | 6 |

**Critical bugs:**
1. Spin-lock in `elevator.run()` — no sleep when idle, 23M lines of "has no commands" in 12 seconds, starved all other threads
2. `NameError` on line 165 — `command` variable doesn't exist, should be `request`
3. Deadlock — `schedule_request` holds `commands_list_lock` then calls `add_command` which tries to acquire the same lock
4. Direction completely ignored in scheduling and movement
5. Capacity fields exist but never checked
6. No destination floor model — Request only has pickup, no "take me to floor X"
7. No display status method
8. No clean shutdown — threads run forever

**What improved from Q1:**
- Actually used real threading (threads, locks) — big step up from vending machine
- Strategy pattern for scheduling — clean abstraction
- Class planning upfront was thorough

**What repeated from Q1:**
- Code never executed before submitting (would have caught spin-lock and NameError immediately)
- Requirements listed but not fully implemented (capacity, display status)

**Key feedback:**
- Use `threading.Condition` for "wait until work arrives" instead of spin-loops
- Model full journey: Request needs both source_floor and dest_floor
- LOOK algorithm: separate up_stops and down_stops, process in order
- Direction-aware scheduling: prefer elevators already heading toward request
- Always run your code — this is now pattern #1 across both attempts
