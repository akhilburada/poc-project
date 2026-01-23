# System Design Notes - Beginner Friendly

> Every concept explained simply with real-world examples

---

## Table of Contents

1. [Key Terms Glossary](#1-key-terms-glossary---must-know)
2. [Client-Server Architecture](#2-client-server-architecture)
3. [API Basics](#3-api-basics)
4. [Database Concepts](#4-database-concepts)
5. [Caching](#5-caching)
6. [Load Balancer](#6-load-balancer)
7. [Scaling](#7-scaling)
8. [Monolith vs Microservices](#8-monolith-vs-microservices)
9. [Message Queues](#9-message-queues)
10. [CDN](#10-cdn-content-delivery-network)
11. [Proxy & Reverse Proxy](#11-proxy--reverse-proxy)
12. [Database Scaling](#12-database-scaling)
13. [CAP Theorem](#13-cap-theorem)
14. [Important Numbers](#14-important-numbers)
15. [Interview Framework](#15-interview-framework)

---

## 1. Key Terms Glossary - MUST KNOW

### Server

```
WHAT IS IT?
A server is just a computer that provides services to other computers.

REAL-WORLD EXAMPLE:
Think of a restaurant kitchen. You (client) order food, the kitchen (server) 
prepares and gives you the food.

YOUR LAPTOP vs SERVER:
┌─────────────────┐          ┌─────────────────┐
│   Your Laptop   │          │     Server      │
├─────────────────┤          ├─────────────────┤
│ - For one user  │          │ - For many users│
│ - Limited power │          │ - High power    │
│ - Shuts down    │          │ - Runs 24/7     │
│   when closed   │          │ - In data center│
└─────────────────┘          └─────────────────┘
```

---

### Client

```
WHAT IS IT?
Anything that requests data from a server.

EXAMPLES:
- Your browser (Chrome, Firefox)
- Mobile app (Instagram app)
- Another server

SIMPLE FLOW:
┌────────┐   Request    ┌────────┐
│ Client │ ───────────► │ Server │
│(Browser)│ ◄─────────── │        │
└────────┘   Response   └────────┘
```

---

### Database

```
WHAT IS IT?
A database is organized storage for data. Like a digital filing cabinet.

REAL-WORLD EXAMPLE:
- Excel spreadsheet = Simple database
- Library catalog = Database of books

WHY NOT JUST USE FILES?
- Files: Hard to search, no structure, slow for large data
- Database: Fast search, organized, handles millions of records

EXAMPLE:
┌──────────────────────────────────────┐
│           USERS TABLE                │
├────────┬──────────┬─────────────────┤
│   ID   │   Name   │      Email      │
├────────┼──────────┼─────────────────┤
│   1    │  Rahul   │ rahul@email.com │
│   2    │  Priya   │ priya@email.com │
│   3    │  Amit    │ amit@email.com  │
└────────┴──────────┴─────────────────┘
```

---

### API (Application Programming Interface)

```
WHAT IS IT?
API is a way for two software programs to talk to each other.
It's like a waiter in a restaurant.

REAL-WORLD EXAMPLE:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│     You     │     │   Waiter    │     │   Kitchen   │
│  (Client)   │     │   (API)     │     │  (Server)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ "I want pizza"    │                   │
       │──────────────────►│                   │
       │                   │ "Order: Pizza"    │
       │                   │──────────────────►│
       │                   │                   │
       │                   │  "Here's pizza"   │
       │                   │◄──────────────────│
       │  "Your pizza"     │                   │
       │◄──────────────────│                   │

You don't go to kitchen directly. Waiter (API) handles it.
Similarly, your app doesn't access database directly. API handles it.
```

---

### Latency

```
WHAT IS IT?
Time taken for a request to go and response to come back.
Simply: How long you wait.

REAL-WORLD EXAMPLE:
- Ordering from nearby restaurant: 20 min (Low latency)
- Ordering from far away: 1 hour (High latency)

IN TECH:
- Good latency: < 100 milliseconds (you don't notice)
- Bad latency: > 1 second (feels slow)

LOW LATENCY = FAST = GOOD
HIGH LATENCY = SLOW = BAD
```

---

### Throughput

```
WHAT IS IT?
How much work can be done in a given time.

REAL-WORLD EXAMPLE:
- 1-lane road: 100 cars/hour (low throughput)
- 4-lane highway: 1000 cars/hour (high throughput)

IN TECH:
- Server handling 100 requests/second = throughput
- Database processing 1000 queries/second = throughput

MORE THROUGHPUT = HANDLE MORE USERS = GOOD
```

---

### Availability

```
WHAT IS IT?
How often your system is working and accessible.
Measured in percentage.

EXAMPLES:
- 99% available = Down 3.65 days/year
- 99.9% available = Down 8.76 hours/year
- 99.99% available = Down 52 minutes/year

REAL-WORLD:
- A shop open 24/7 = High availability
- A shop that closes randomly = Low availability

Your goal: Keep systems available as much as possible
```

---

### Redundancy

```
WHAT IS IT?
Having backup/duplicate of something in case the original fails.

REAL-WORLD EXAMPLE:
- Spare tire in car = Redundancy
- Two keys to your house = Redundancy
- Backup generator = Redundancy

IN TECH:
┌──────────┐     ┌──────────┐
│ Server 1 │     │ Server 2 │  ← If Server 1 dies,
│ (Main)   │     │ (Backup) │    Server 2 takes over
└──────────┘     └──────────┘

No redundancy = One failure = Everything down
With redundancy = One failure = Still working
```

---

### Fault Tolerance

```
WHAT IS IT?
System's ability to keep working even when something fails.

REAL-WORLD EXAMPLE:
- Airplane has 2 engines. If 1 fails, it can still fly.
- Car has 4 tires. If 1 goes flat... well, you stop. (Not fault tolerant!)

IN TECH:
┌────────────────────────────────────────────┐
│           FAULT TOLERANT SYSTEM            │
│                                            │
│  ┌────────┐  ┌────────┐  ┌────────┐       │
│  │Server 1│  │Server 2│  │Server 3│       │
│  │   ✓    │  │   ✗    │  │   ✓    │       │
│  └────────┘  └────────┘  └────────┘       │
│                                            │
│  Server 2 failed, but system still works!  │
└────────────────────────────────────────────┘
```

---

### Scalability

```
WHAT IS IT?
Ability to handle more load by adding resources.

REAL-WORLD EXAMPLE:
Small chai shop → More customers → Open more shops
One cook → More orders → Hire more cooks

IN TECH:
More users coming?
→ Add more servers
→ Add more database capacity
→ Add more storage

SCALABLE SYSTEM = Can grow when needed
```

---

## 2. Client-Server Architecture

```
WHAT IS IT?
A model where clients (your browser/app) request services from servers.

THE SIMPLEST ARCHITECTURE:

     ┌──────────────────────────────────────────────────┐
     │                    INTERNET                       │
     └──────────────────────────────────────────────────┘
              │                              │
              ▼                              ▼
       ┌────────────┐                 ┌────────────┐
       │  Client 1  │                 │  Client 2  │
       │ (Browser)  │                 │ (Mobile)   │
       └─────┬──────┘                 └─────┬──────┘
             │                              │
             │      ┌────────────────┐      │
             │      │                │      │
             └─────►│    SERVER      │◄─────┘
                    │                │
                    │  - Processes   │
                    │    requests    │
                    │  - Has data    │
                    │  - Runs 24/7   │
                    │                │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │   DATABASE     │
                    │  (Stores data) │
                    └────────────────┘

FLOW:
1. You open Instagram (Client)
2. App sends request to Instagram's server
3. Server fetches your feed from database
4. Server sends feed back to your app
5. App displays the feed
```

---

## 3. API Basics

### What is REST API?

```
REST API = A standard way to build APIs using HTTP.

Think of it like a menu at restaurant:
- Menu tells you what dishes are available
- API tells you what operations are available

HTTP METHODS (Actions you can do):

┌──────────┬─────────────────┬─────────────────────────────┐
│  Method  │     Meaning     │          Example            │
├──────────┼─────────────────┼─────────────────────────────┤
│   GET    │  Read/Fetch     │  Get list of all users      │
│   POST   │  Create new     │  Create a new user          │
│   PUT    │  Update entire  │  Update all user details    │
│   PATCH  │  Update partial │  Update only user's name    │
│   DELETE │  Remove         │  Delete a user              │
└──────────┴─────────────────┴─────────────────────────────┘

REAL EXAMPLE - User API:

GET    /users         →  Give me all users
GET    /users/123     →  Give me user with ID 123
POST   /users         →  Create a new user
PUT    /users/123     →  Update user 123
DELETE /users/123     →  Delete user 123
```

### HTTP Status Codes

```
When server responds, it sends a number (status code) to tell what happened.

EASY TO REMEMBER:

2xx = SUCCESS (All good!)
  200 = OK, here's your data
  201 = Created successfully

4xx = CLIENT ERROR (You did something wrong)
  400 = Bad request (wrong format)
  401 = Not logged in
  403 = Logged in but not allowed
  404 = Not found (wrong URL)

5xx = SERVER ERROR (Server has problem)
  500 = Server crashed
  503 = Server too busy

ANALOGY:
200 = "Here's your pizza"
404 = "We don't have that dish"
500 = "Kitchen is on fire"
```

---

## 4. Database Concepts

### SQL vs NoSQL - Simple Explanation

```
SQL DATABASE (Relational):
──────────────────────────
Like an Excel spreadsheet with strict rules.
- Data in tables with rows and columns
- Must define structure before adding data
- Good for complex relationships

Examples: MySQL, PostgreSQL, Oracle

WHEN TO USE:
✓ Banking transactions
✓ E-commerce orders
✓ User accounts
✓ Any data that needs accuracy

┌─────────────────────────────────────────┐
│              SQL DATABASE               │
│                                         │
│  Users Table:                           │
│  ┌────┬────────┬───────────────┐       │
│  │ ID │  Name  │     Email     │       │
│  ├────┼────────┼───────────────┤       │
│  │ 1  │ Rahul  │ rahul@x.com   │       │
│  │ 2  │ Priya  │ priya@x.com   │       │
│  └────┴────────┴───────────────┘       │
│                                         │
│  Orders Table:                          │
│  ┌────┬─────────┬────────┐             │
│  │ ID │ User_ID │ Amount │             │
│  ├────┼─────────┼────────┤             │
│  │ 1  │    1    │  500   │  ← Links to │
│  │ 2  │    2    │  300   │    Users    │
│  └────┴─────────┴────────┘             │
└─────────────────────────────────────────┘


NoSQL DATABASE (Non-Relational):
────────────────────────────────
Like storing documents or JSON objects.
- Flexible structure
- Can add any field anytime
- Good for unstructured data

Examples: MongoDB, Cassandra, Redis

WHEN TO USE:
✓ Chat messages
✓ User activity logs
✓ Session data
✓ Real-time analytics

┌─────────────────────────────────────────┐
│             NoSQL DATABASE              │
│                                         │
│  User Document:                         │
│  {                                      │
│    "id": 1,                             │
│    "name": "Rahul",                     │
│    "email": "rahul@x.com",              │
│    "hobbies": ["cricket", "music"],     │
│    "address": {                         │
│      "city": "Mumbai",                  │
│      "pin": "400001"                    │
│    }                                    │
│  }                                      │
│                                         │
│  Note: Structure can be different for   │
│  each document!                         │
└─────────────────────────────────────────┘
```

### ACID Properties - Simple Explanation

```
ACID = Rules that make database transactions reliable

A - ATOMICITY (All or Nothing)
──────────────────────────────
Like transferring money:
- Either BOTH debit AND credit happen
- Or NEITHER happens
- No partial transfers!

Example:
  Transfer ₹100 from A to B
  Step 1: Deduct ₹100 from A  ✓
  Step 2: Add ₹100 to B       ✗ (failed!)
  
  With Atomicity: Step 1 is also reversed. A gets money back.
  Without: A loses money, B doesn't get it. Money vanishes!


C - CONSISTENCY (Data stays valid)
──────────────────────────────────
Database rules are always followed.

Example:
  Rule: Account balance cannot be negative
  
  If transaction would make balance -50,
  transaction is rejected.


I - ISOLATION (Transactions don't interfere)
────────────────────────────────────────────
Two transactions happening at same time don't affect each other.

Example:
  Person A and Person B both check seat availability: 1 seat left
  Person A books it
  Person B also tries to book same seat
  
  With Isolation: Only one succeeds, other gets error
  Without: Both might book same seat! Chaos!


D - DURABILITY (Data survives crashes)
──────────────────────────────────────
Once saved, data is permanent even if power goes off.

Example:
  You book a ticket, get confirmation
  Server crashes 1 second later
  
  With Durability: Your booking is still there when server restarts
  Without: Booking might be lost
```

### What is an Index?

```
INDEX = A shortcut to find data faster

REAL-WORLD EXAMPLE:
──────────────────
Book without index:
  Find topic "Arrays"? 
  → Read every page until you find it (SLOW)

Book with index:
  Look at index → "Arrays: Page 45"
  → Go directly to page 45 (FAST)

IN DATABASE:
────────────
Table with 1 million users, find "rahul@email.com"

Without Index:
  Check row 1... not found
  Check row 2... not found
  Check row 3... not found
  ... check all 1 million rows
  TIME: Very slow!

With Index on email:
  Index says "rahul@email.com" is at row 5432
  Go directly to row 5432
  TIME: Instant!

WHEN TO CREATE INDEX:
✓ Columns you search often (WHERE email = ?)
✓ Columns you sort by (ORDER BY created_at)
✓ Columns you join on

WHEN NOT TO:
✗ Tables with few rows (not needed)
✗ Columns that change very often (slows down updates)
```

---

## 5. Caching

### What is Cache?

```
CACHE = Temporary storage for frequently used data

REAL-WORLD EXAMPLE:
──────────────────
Your phone's recent apps:
- Opening Instagram first time: Loads everything (slow)
- Opening Instagram again: Already in memory (fast!)

The "memory" is cache.

WHY USE CACHE?
─────────────
┌────────────────────────────────────────────────────────┐
│                                                        │
│  WITHOUT CACHE:                                        │
│                                                        │
│  User → Server → Database → Server → User              │
│                    ↑                                   │
│              Takes 100ms                               │
│                                                        │
│  WITH CACHE:                                           │
│                                                        │
│  User → Server → Cache → Server → User                 │
│                    ↑                                   │
│              Takes 5ms (20x faster!)                   │
│                                                        │
│  If not in cache, then go to database.                 │
│                                                        │
└────────────────────────────────────────────────────────┘

POPULAR CACHE: Redis, Memcached
```

### Cache Flow - Step by Step

```
CACHE-ASIDE PATTERN (Most Common):

Step 1: User requests "Show user profile"

Step 2: Server checks cache
        "Is user profile in cache?"
        
        ┌─────────────────────────────────────────┐
        │                                         │
        │  IF IN CACHE (Cache Hit):               │
        │    → Return from cache                  │
        │    → Done! (Super fast)                 │
        │                                         │
        │  IF NOT IN CACHE (Cache Miss):          │
        │    → Query database                     │
        │    → Store result in cache              │
        │    → Return to user                     │
        │                                         │
        └─────────────────────────────────────────┘

DIAGRAM:

        ┌─────────┐
        │  User   │
        └────┬────┘
             │ 1. Request
             ▼
        ┌─────────┐
        │ Server  │
        └────┬────┘
             │ 2. Check cache
             ▼
        ┌─────────┐
        │  Cache  │──── Hit? ──── Yes ──► Return data
        └────┬────┘
             │ No (Miss)
             ▼
        ┌─────────┐
        │Database │
        └────┬────┘
             │ 3. Get data
             ▼
        Store in cache
             │
             ▼
        Return to user
```

### What to Cache?

```
CACHE THIS ✓                      DON'T CACHE ✗
─────────────                     ──────────────
- User profile                    - Passwords
- Product details                 - Payment info
- Homepage content                - Data that changes every second
- API responses                   - Very large files
- Session data                    - One-time data

CACHE EXPIRY (TTL - Time To Live):
──────────────────────────────────
Cache doesn't store forever. It expires.

Example:
  Store user profile in cache for 5 minutes
  After 5 minutes, cache deletes it
  Next request fetches fresh data from database

Why? Data might have changed. Don't show stale data forever.
```

---

## 6. Load Balancer

### What is Load Balancer?

```
LOAD BALANCER = Distributes incoming traffic across multiple servers

REAL-WORLD EXAMPLE:
──────────────────
Imagine a bank with 1 counter:
  - 100 customers waiting
  - Long queue, slow service

Bank with 5 counters + Queue manager:
  - Queue manager sends customers to available counters
  - Faster service, shorter wait

Queue Manager = Load Balancer
Counters = Servers


WHY NEED LOAD BALANCER?
───────────────────────

WITHOUT Load Balancer:
┌─────────────────────────────────────────────────────┐
│                                                     │
│    1000 users                                       │
│        │                                            │
│        ▼                                            │
│  ┌──────────┐                                       │
│  │  Single  │  ← Gets overwhelmed!                  │
│  │  Server  │  ← Crashes!                           │
│  └──────────┘  ← Everyone affected!                 │
│                                                     │
└─────────────────────────────────────────────────────┘

WITH Load Balancer:
┌─────────────────────────────────────────────────────┐
│                                                     │
│    1000 users                                       │
│        │                                            │
│        ▼                                            │
│  ┌──────────────┐                                   │
│  │Load Balancer │                                   │
│  └──────┬───────┘                                   │
│         │                                           │
│    ┌────┼────┬────┐                                 │
│    ▼    ▼    ▼    ▼                                 │
│  ┌───┐┌───┐┌───┐┌───┐                              │
│  │S1 ││S2 ││S3 ││S4 │  ← 250 users each            │
│  └───┘└───┘└───┘└───┘  ← No single server          │
│                           overwhelmed!              │
│                                                     │
│  If S2 dies, LB stops sending to S2.               │
│  Other servers handle traffic. No downtime!         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Load Balancing Algorithms

```
How does Load Balancer decide which server to send request to?

1. ROUND ROBIN (Most Simple)
─────────────────────────────
Send to servers one by one, in rotation.

Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1  (back to start)
Request 5 → Server 2
...

Like dealing cards to players.


2. LEAST CONNECTIONS
────────────────────
Send to server that has fewest active users.

Server 1: 50 connections
Server 2: 20 connections  ← Send here (least busy)
Server 3: 45 connections


3. IP HASH
──────────
Same user always goes to same server.

User from IP 1.2.3.4 → Always Server 2
User from IP 5.6.7.8 → Always Server 1

Useful when server stores user's session.


4. WEIGHTED
───────────
Powerful servers get more requests.

Server 1 (powerful): 60% traffic
Server 2 (weak):     40% traffic
```

---

## 7. Scaling

### Vertical vs Horizontal Scaling

```
When your system needs to handle more users, you have 2 options:

VERTICAL SCALING (Scale Up)
───────────────────────────
Make your server BIGGER and more powerful.

Before:          After:
┌──────────┐     ┌──────────────┐
│ 4GB RAM  │     │  64GB RAM    │
│ 2 CPU    │ →   │  32 CPU      │
│ 100GB    │     │  2TB SSD     │
└──────────┘     └──────────────┘

Like: Replacing your Maruti with a BMW

PROS:
  ✓ Simple - just upgrade hardware
  ✓ No code changes needed
  
CONS:
  ✗ Has limit (can't add infinite RAM)
  ✗ Expensive
  ✗ Single point of failure (if it dies, everything dies)


HORIZONTAL SCALING (Scale Out)
──────────────────────────────
Add MORE servers instead of bigger server.

Before:          After:
┌──────────┐     ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Server 1 │     │ Server 1 │ │ Server 2 │ │ Server 3 │
└──────────┘     └──────────┘ └──────────┘ └──────────┘

Like: Instead of 1 big truck, use 3 small trucks

PROS:
  ✓ No limit (add as many as needed)
  ✓ If one dies, others still work
  ✓ Cost-effective
  
CONS:
  ✗ More complex
  ✗ Need load balancer
  ✗ Need to handle distributed data


WHEN TO USE WHAT:
─────────────────
Small app, starting out → Vertical (simpler)
Growing app, many users → Horizontal (scalable)
Big companies (Google, Amazon) → Horizontal (only option at scale)
```

### Stateless vs Stateful

```
STATEFUL SERVER:
────────────────
Server remembers information about the user.

Problem:
┌──────────────────────────────────────────────────────┐
│                                                      │
│  User logs in → Request goes to Server 1             │
│  Server 1 stores: "User ABC is logged in"            │
│                                                      │
│  Next request → Load balancer sends to Server 2      │
│  Server 2 doesn't know User ABC!                     │
│  User appears logged out! 😱                         │
│                                                      │
└──────────────────────────────────────────────────────┘


STATELESS SERVER:
─────────────────
Server doesn't store any user information.
All user info stored in shared place (like Redis).

Solution:
┌──────────────────────────────────────────────────────┐
│                                                      │
│  User logs in → Server 1 stores session in Redis     │
│                                                      │
│  Next request → Goes to Server 2                     │
│  Server 2 checks Redis → Finds user session          │
│  User is still logged in! ✓                          │
│                                                      │
│        ┌──────────┐                                  │
│        │  Redis   │  ← Shared session storage        │
│        │(Sessions)│                                  │
│        └────┬─────┘                                  │
│             │                                        │
│      ┌──────┴──────┐                                │
│      ▼             ▼                                │
│  ┌────────┐   ┌────────┐                            │
│  │Server 1│   │Server 2│   Both read from Redis     │
│  └────────┘   └────────┘                            │
│                                                      │
└──────────────────────────────────────────────────────┘

RULE: Always make servers STATELESS for horizontal scaling!
```

---

## 8. Monolith vs Microservices

### What is Monolith?

```
MONOLITH = One big application that does everything

REAL-WORLD EXAMPLE:
──────────────────
A single restaurant where:
- Same kitchen makes all cuisines (Indian, Chinese, Italian)
- Same staff handles everything
- One building, one menu, one management

IN CODE:
────────
┌────────────────────────────────────────────────────────┐
│                   MONOLITH APPLICATION                  │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │                                                 │  │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐       │  │
│  │   │  User   │  │  Order  │  │ Payment │       │  │
│  │   │ Module  │  │ Module  │  │ Module  │       │  │
│  │   └─────────┘  └─────────┘  └─────────┘       │  │
│  │                                                 │  │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐       │  │
│  │   │  Cart   │  │ Product │  │ Review  │       │  │
│  │   │ Module  │  │ Module  │  │ Module  │       │  │
│  │   └─────────┘  └─────────┘  └─────────┘       │  │
│  │                                                 │  │
│  │        ALL IN ONE APPLICATION                   │  │
│  │        ONE CODEBASE                            │  │
│  │        ONE DATABASE                            │  │
│  │        ONE DEPLOYMENT                          │  │
│  │                                                 │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
└────────────────────────────────────────────────────────┘

WHEN TO USE MONOLITH:
  ✓ Small team (< 10 developers)
  ✓ New product/startup
  ✓ Simple application
  ✓ Quick development needed

PROBLEMS WITH MONOLITH:
  ✗ One bug can crash entire application
  ✗ Small change needs full deployment
  ✗ Hard to scale specific parts
  ✗ Tech stack locked (can't use different languages)
  ✗ Large codebase becomes hard to manage
```

### What is Microservices?

```
MICROSERVICES = Application split into small, independent services

REAL-WORLD EXAMPLE:
──────────────────
Food court in a mall:
- Pizza shop (only makes pizza)
- Chinese counter (only Chinese)
- Indian food stall (only Indian)
- Each has own kitchen, staff, menu
- If pizza shop closes, others still work!

IN CODE:
────────
┌─────────────────────────────────────────────────────────────────┐
│                    MICROSERVICES ARCHITECTURE                    │
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │   User      │   │   Order     │   │  Payment    │           │
│  │  Service    │   │  Service    │   │  Service    │           │
│  │             │   │             │   │             │           │
│  │ Own code    │   │ Own code    │   │ Own code    │           │
│  │ Own DB      │   │ Own DB      │   │ Own DB      │           │
│  │ Own team    │   │ Own team    │   │ Own team    │           │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│         │                 │                 │                   │
│         └────────────┬────┴─────────────────┘                   │
│                      │                                          │
│                      ▼                                          │
│              ┌───────────────┐                                  │
│              │  API Gateway  │  ← Entry point for all           │
│              └───────────────┘                                  │
│                      │                                          │
│                      ▼                                          │
│                   Client                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Each service:
- Runs independently
- Has own database
- Can use different programming language
- Can be deployed separately
- Can be scaled separately
```

### Monolith vs Microservices Comparison

```
┌────────────────────┬────────────────────┬────────────────────┐
│      Aspect        │     Monolith       │   Microservices    │
├────────────────────┼────────────────────┼────────────────────┤
│ Structure          │ Single unit        │ Multiple services  │
├────────────────────┼────────────────────┼────────────────────┤
│ Deployment         │ Deploy entire app  │ Deploy each        │
│                    │                    │ service separately │
├────────────────────┼────────────────────┼────────────────────┤
│ Scaling            │ Scale entire app   │ Scale specific     │
│                    │                    │ service only       │
├────────────────────┼────────────────────┼────────────────────┤
│ Technology         │ One language/      │ Different tech     │
│                    │ framework          │ per service        │
├────────────────────┼────────────────────┼────────────────────┤
│ Failure Impact     │ One bug can        │ Failure isolated   │
│                    │ crash everything   │ to one service     │
├────────────────────┼────────────────────┼────────────────────┤
│ Development Speed  │ Faster initially   │ Slower initially   │
│                    │                    │ but faster later   │
├────────────────────┼────────────────────┼────────────────────┤
│ Team Size          │ Small teams        │ Large teams        │
├────────────────────┼────────────────────┼────────────────────┤
│ Complexity         │ Simple             │ Complex            │
├────────────────────┼────────────────────┼────────────────────┤
│ Examples           │ Small startups     │ Netflix, Amazon,   │
│                    │                    │ Uber               │
└────────────────────┴────────────────────┴────────────────────┘

SIMPLE RULE:
─────────────
Starting new project? → Start with Monolith
Growing big? Many teams? → Consider Microservices
```

### API Gateway

```
WHAT IS IT?
API Gateway = Front door for all microservices

PROBLEM WITHOUT API GATEWAY:
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   Client needs to know address of EVERY service:            │
│                                                              │
│   Client → http://user-service:8001/users                   │
│   Client → http://order-service:8002/orders                 │
│   Client → http://payment-service:8003/pay                  │
│                                                              │
│   Problems:                                                  │
│   - Client is complex                                        │
│   - Service addresses can change                             │
│   - No central security                                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘

WITH API GATEWAY:
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   Client only knows ONE address:                             │
│                                                              │
│   Client → http://api.myapp.com/users     → User Service    │
│   Client → http://api.myapp.com/orders    → Order Service   │
│   Client → http://api.myapp.com/pay       → Payment Service │
│                                                              │
│                    ┌─────────────┐                          │
│                    │ API Gateway │                          │
│                    │             │                          │
│                    │ - Routing   │                          │
│                    │ - Auth      │                          │
│                    │ - Rate limit│                          │
│                    └──────┬──────┘                          │
│                           │                                  │
│              ┌────────────┼────────────┐                    │
│              ▼            ▼            ▼                    │
│         ┌────────┐  ┌────────┐  ┌────────┐                 │
│         │  User  │  │ Order  │  │Payment │                 │
│         │Service │  │Service │  │Service │                 │
│         └────────┘  └────────┘  └────────┘                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘

API GATEWAY DOES:
  ✓ Routing (send request to right service)
  ✓ Authentication (check if user is logged in)
  ✓ Rate Limiting (prevent too many requests)
  ✓ Load Balancing
  ✓ Caching
  ✓ Logging

Popular: AWS API Gateway, Kong, Nginx
```

---

## 9. Message Queues

### What is a Message Queue?

```
MESSAGE QUEUE = A waiting line for messages between services

REAL-WORLD EXAMPLE:
──────────────────
Restaurant order system:
1. Waiter takes order, puts slip on queue
2. Kitchen picks up orders from queue one by one
3. Waiter doesn't wait for kitchen to finish

Benefits:
- Waiter serves more tables (not blocked)
- Kitchen works at own pace
- Orders don't get lost

IN TECH:
────────
Without Queue (Synchronous):
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  User places order → Server → Sends email → Response       │
│                              (takes 5 seconds)             │
│                                                            │
│  User waits 5 seconds! 😤                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘

With Queue (Asynchronous):
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  User places order → Server → Response immediately         │
│                         │                                  │
│                         ▼                                  │
│                   ┌──────────┐                             │
│                   │  Queue   │ "Send email to user"        │
│                   └────┬─────┘                             │
│                        │                                   │
│                        ▼ (processes in background)         │
│                   ┌──────────┐                             │
│                   │  Worker  │ Sends email                 │
│                   └──────────┘                             │
│                                                            │
│  User gets instant response! Email comes later.            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Queue Components

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PRODUCER              QUEUE              CONSUMER         │
│  (Sender)             (Storage)           (Processor)       │
│                                                             │
│  ┌─────────┐        ┌───────────┐        ┌─────────┐       │
│  │   API   │───────►│ ■ ■ ■ ■ ■ │───────►│ Worker  │       │
│  │ Server  │        │ (Messages)│        │         │       │
│  └─────────┘        └───────────┘        └─────────┘       │
│                                                             │
│  Producer: Creates and adds messages to queue               │
│  Queue: Stores messages until processed                     │
│  Consumer: Takes messages and processes them                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### When to Use Queues

```
USE QUEUES FOR ✓                    DON'T USE FOR ✗
─────────────────                   ─────────────────
Sending emails                      Login/Authentication
Sending notifications               Reading user profile
Image/Video processing              Simple database reads
Report generation                   Anything needing instant result
Order processing
Payment processing
File uploads
```

### Popular Message Queues

```
┌─────────────┬────────────────────────────────────────────────┐
│    Name     │               Best For                         │
├─────────────┼────────────────────────────────────────────────┤
│  RabbitMQ   │ General purpose, complex routing               │
│  Kafka      │ High volume, event streaming, logs             │
│  AWS SQS    │ Simple, managed by AWS, easy to use            │
│  Redis      │ Simple queues (if you already use Redis)       │
└─────────────┴────────────────────────────────────────────────┘
```

---

## 10. CDN (Content Delivery Network)

### What is CDN?

```
CDN = Network of servers around the world that store copies of your content

REAL-WORLD EXAMPLE:
──────────────────
Netflix doesn't stream movies from one server in USA to everyone.
They have copies in servers near you (India, Europe, etc.)

PROBLEM WITHOUT CDN:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  User in India wants to load image from server in USA      │
│                                                            │
│  India ─────────── 15,000 km ─────────────► USA            │
│                                                            │
│  Result: SLOW (150-300ms for each request)                 │
│                                                            │
└────────────────────────────────────────────────────────────┘

WITH CDN:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  Image is copied to CDN server in India                    │
│                                                            │
│  User in India ──── 100 km ────► CDN (India)              │
│                                                            │
│  Result: FAST (10-20ms)                                    │
│                                                            │
│          ┌─────────┐                                       │
│          │  USA    │ (Origin Server)                       │
│          │ Server  │                                       │
│          └────┬────┘                                       │
│               │ Copies content to CDN edges                │
│       ┌───────┼───────┬───────────┐                       │
│       ▼       ▼       ▼           ▼                       │
│     ┌───┐   ┌───┐   ┌───┐      ┌───┐                     │
│     │CDN│   │CDN│   │CDN│      │CDN│                     │
│     │EU │   │Asia│  │India│    │Aus│                     │
│     └───┘   └───┘   └───┘      └───┘                     │
│       ▲                 ▲                                  │
│       │                 │                                  │
│    User in           User in                               │
│    Germany           India                                 │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### What to Put on CDN

```
PUT ON CDN ✓                      DON'T PUT ON CDN ✗
─────────────                     ────────────────────
Images                            User-specific data
Videos                            Frequently changing data
CSS files                         Sensitive information
JavaScript files                  Database queries
Fonts
PDFs, Documents
Any static content
```

---

## 11. Proxy & Reverse Proxy

### What is Proxy (Forward Proxy)?

```
PROXY = An intermediary that makes requests on your behalf

REAL-WORLD EXAMPLE:
──────────────────
You want to buy a house but want to stay anonymous.
You hire an agent (proxy) to buy on your behalf.
Seller doesn't know who you are.

IN TECH:
────────
┌───────────────────────────────────────────────────────────┐
│                                                           │
│  WITHOUT PROXY:                                           │
│  User ────────────────────────────────────────► Website   │
│  Website knows your IP address                            │
│                                                           │
│  WITH PROXY:                                              │
│  User ──────► Proxy ──────────────────────────► Website   │
│               │                                           │
│               └─ Makes request on your behalf             │
│                  Website sees proxy's IP, not yours       │
│                                                           │
└───────────────────────────────────────────────────────────┘

USE CASES:
- Hide identity
- Access blocked websites
- Company monitoring employee internet use
```

### What is Reverse Proxy?

```
REVERSE PROXY = Sits in front of servers, handles incoming requests

REAL-WORLD EXAMPLE:
──────────────────
Reception desk at a company:
- Visitors don't go directly to employees
- They go to reception first
- Reception directs them to right person

IN TECH:
────────
┌───────────────────────────────────────────────────────────┐
│                                                           │
│  WITHOUT REVERSE PROXY:                                   │
│  Users know exact server addresses                        │
│  Each server handles its own security, SSL, etc.          │
│                                                           │
│  WITH REVERSE PROXY:                                      │
│                                                           │
│     Users                                                 │
│       │                                                   │
│       ▼                                                   │
│  ┌─────────────┐                                         │
│  │   Reverse   │                                         │
│  │    Proxy    │                                         │
│  │  (Nginx)    │                                         │
│  └──────┬──────┘                                         │
│         │                                                 │
│    ┌────┴────┐                                           │
│    ▼         ▼                                           │
│ ┌──────┐ ┌──────┐                                        │
│ │Server│ │Server│  Users don't know these servers exist  │
│ │  1   │ │  2   │                                        │
│ └──────┘ └──────┘                                        │
│                                                           │
└───────────────────────────────────────────────────────────┘

REVERSE PROXY DOES:
  ✓ Load balancing
  ✓ SSL termination (HTTPS)
  ✓ Caching
  ✓ Security (hide server details)
  ✓ Compression

Popular: Nginx, HAProxy, AWS ALB
```

### Proxy vs Reverse Proxy

```
┌─────────────────┬─────────────────────┬─────────────────────┐
│                 │    Forward Proxy    │   Reverse Proxy     │
├─────────────────┼─────────────────────┼─────────────────────┤
│ Sits in front of│      Clients        │      Servers        │
├─────────────────┼─────────────────────┼─────────────────────┤
│ Hides           │   Client identity   │   Server identity   │
├─────────────────┼─────────────────────┼─────────────────────┤
│ Used by         │      Users          │   Server admins     │
├─────────────────┼─────────────────────┼─────────────────────┤
│ Purpose         │ Privacy, bypass     │ Load balance,       │
│                 │ restrictions        │ security            │
└─────────────────┴─────────────────────┴─────────────────────┘
```

---

## 12. Database Scaling

### Read Replicas

```
WHAT IS IT?
Copies of main database that handle read queries.

WHY?
Most apps read more than write (90% reads, 10% writes)
One database can get overwhelmed with all requests.

HOW IT WORKS:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                    ┌──────────────┐                        │
│   All WRITES ────► │   PRIMARY    │                        │
│                    │   (Master)   │                        │
│                    └──────┬───────┘                        │
│                           │                                │
│                           │ Copies data                    │
│                           │ (Replication)                  │
│                           │                                │
│              ┌────────────┼────────────┐                   │
│              ▼            ▼            ▼                   │
│         ┌────────┐   ┌────────┐   ┌────────┐              │
│         │Replica │   │Replica │   │Replica │              │
│         │   1    │   │   2    │   │   3    │              │
│         └────┬───┘   └────┬───┘   └────┬───┘              │
│              │            │            │                   │
│              └────────────┼────────────┘                   │
│                           │                                │
│                      All READS                             │
│                                                            │
└────────────────────────────────────────────────────────────┘

Benefits:
  ✓ Read operations are faster (distributed)
  ✓ If replica dies, others still work
  ✓ Primary only handles writes (less load)
```

### Database Sharding

```
WHAT IS IT?
Splitting data across multiple databases.

WHY?
When single database can't hold all data or handle all traffic.

EXAMPLE:
100 million users - too much for one database!

Split by User ID:
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   Users 1 - 33M      Users 33M - 66M    Users 66M - 100M  │
│        │                   │                   │           │
│        ▼                   ▼                   ▼           │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐     │
│   │ Shard 1 │         │ Shard 2 │         │ Shard 3 │     │
│   │  (DB)   │         │  (DB)   │         │  (DB)   │     │
│   └─────────┘         └─────────┘         └─────────┘     │
│                                                            │
│   Query for user ID 5000000?                              │
│   → Goes to Shard 1                                        │
│                                                            │
│   Query for user ID 50000000?                             │
│   → Goes to Shard 2                                        │
│                                                            │
└────────────────────────────────────────────────────────────┘

SHARDING STRATEGIES:

1. Range Based: Users 1-1M → Shard 1, 1M-2M → Shard 2
2. Hash Based: user_id % 3 → Determines shard (0, 1, or 2)
3. Geographic: India users → Shard India, US users → Shard US

CHALLENGES:
  ✗ Joins across shards are hard
  ✗ Rebalancing data is complex
  ✗ Some queries need to hit all shards
```

---

## 13. CAP Theorem

```
CAP THEOREM = In a distributed system, you can only guarantee 2 of 3:

C - CONSISTENCY
─────────────────
All users see the same data at the same time.

Example: Bank balance shows ₹1000 on all devices, always.


A - AVAILABILITY
────────────────
System always responds, even if some servers are down.

Example: Website always loads, never shows error.


P - PARTITION TOLERANCE
───────────────────────
System works even if network between servers breaks.

Example: Server in Mumbai can't talk to server in Delhi,
but both still work.

┌────────────────────────────────────────────────────────────┐
│                                                            │
│                        CAP                                 │
│                                                            │
│                    Consistency                             │
│                        /\                                  │
│                       /  \                                 │
│                      /    \                                │
│                     /      \                               │
│                    /   CP   \                              │
│                   /    or    \                             │
│                  /     AP     \                            │
│                 /              \                           │
│                /________________\                          │
│          Availability      Partition                       │
│                            Tolerance                       │
│                                                            │
│   YOU CAN ONLY PICK 2!                                    │
│                                                            │
│   CP (Consistency + Partition):                           │
│      → Banking system                                      │
│      → May be unavailable during network issues            │
│      → But data is always correct                          │
│                                                            │
│   AP (Availability + Partition):                          │
│      → Social media likes                                  │
│      → Always available                                    │
│      → But counts might be slightly off temporarily        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 14. Important Numbers

### Latency Numbers

```
┌────────────────────────────────────────────────────────────┐
│                    LATENCY REFERENCE                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Action                           Time                     │
│  ─────────────────────────────────────────                 │
│  L1 cache read                    1 nanosecond             │
│  RAM read                         100 nanoseconds          │
│  SSD read                         100 microseconds         │
│  Network (same city)              500 microseconds         │
│  HDD read                         10 milliseconds          │
│  Network (cross country)          100 milliseconds         │
│  Network (cross continent)        200 milliseconds         │
│                                                            │
│  RULE OF THUMB:                                            │
│  ─────────────                                             │
│  Cache     = Instant (nanoseconds)                         │
│  RAM       = Very fast (nanoseconds)                       │
│  SSD       = Fast (microseconds)                           │
│  Network   = Slow (milliseconds)                           │
│  HDD       = Slowest (milliseconds)                        │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Capacity Estimation

```
┌────────────────────────────────────────────────────────────┐
│                    QUICK MATH                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  TIME:                                                     │
│  1 day    = 86,400 seconds ≈ 100,000 seconds              │
│  1 month  = 2.5 million seconds                            │
│  1 year   = 30 million seconds                             │
│                                                            │
│  STORAGE:                                                  │
│  1 KB     = 1,000 bytes                                   │
│  1 MB     = 1,000 KB                                      │
│  1 GB     = 1,000 MB                                      │
│  1 TB     = 1,000 GB                                      │
│                                                            │
│  TRAFFIC:                                                  │
│  1 million requests/day ≈ 12 requests/second              │
│  10 million requests/day ≈ 120 requests/second            │
│  100 million requests/day ≈ 1,200 requests/second         │
│                                                            │
│  FORMULA:                                                  │
│  requests/second = requests/day ÷ 86,400                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 15. Interview Framework

### RADIO Method

```
R - REQUIREMENTS (5 minutes)
────────────────────────────
Ask questions before designing!

Questions to ask:
• What are the main features?
• How many users?
• Read-heavy or write-heavy?
• What's acceptable latency?
• Any special requirements?


A - API DESIGN (5 minutes)
──────────────────────────
Define the main API endpoints.

Example:
POST   /api/v1/users       - Create user
GET    /api/v1/users/:id   - Get user
PUT    /api/v1/users/:id   - Update user
DELETE /api/v1/users/:id   - Delete user


D - DATA MODEL (5 minutes)
──────────────────────────
Design your database tables.

• What tables do you need?
• What columns in each table?
• SQL or NoSQL?
• What to index?


I - HIGH-LEVEL DESIGN (15 minutes)
──────────────────────────────────
Draw the architecture!

Client → Load Balancer → Servers → Cache → Database
                                 ↓
                              Queue → Workers


O - OPTIMIZATIONS (10 minutes)
──────────────────────────────
Discuss improvements and trade-offs.

• How to cache?
• How to scale?
• What if something fails?
• Any bottlenecks?
```

### Interview Checklist

```
Before interview, make sure you can:

[ ] Explain client-server architecture
[ ] Design REST APIs
[ ] Choose SQL vs NoSQL
[ ] Explain caching and strategies
[ ] Draw load-balanced architecture
[ ] Explain horizontal vs vertical scaling
[ ] Explain monolith vs microservices
[ ] Explain message queues
[ ] Do basic capacity calculations
[ ] Draw system design diagrams

Common questions for 3 YOE:
1. URL Shortener
2. Rate Limiter  
3. Notification System
4. Chat Application
5. News Feed
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────┐
│                 SYSTEM DESIGN CHEAT SHEET                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  SCALING:                                                │
│    More users? → Add servers (horizontal)                │
│    Slow reads? → Add cache (Redis)                       │
│    Slow DB?    → Add read replicas                       │
│    Too much data? → Shard database                       │
│                                                          │
│  DATABASE CHOICE:                                        │
│    Need transactions? → SQL                              │
│    Flexible schema?   → NoSQL                            │
│    Fast key-value?    → Redis                            │
│                                                          │
│  ASYNC TASKS:                                            │
│    Email, SMS, notifications → Message Queue             │
│    Heavy processing → Message Queue                      │
│                                                          │
│  ARCHITECTURE:                                           │
│    Small team/app → Monolith                             │
│    Big team/app   → Microservices                        │
│                                                          │
│  ALWAYS INCLUDE:                                         │
│    → Load Balancer (for multiple servers)                │
│    → Cache (for speed)                                   │
│    → Database with replicas (for reliability)            │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

*Remember: System design is about trade-offs. There's no perfect solution, only solutions that fit your specific requirements!*
