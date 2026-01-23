# System Design Interview Examples (2.5 - 3 YOE)

> Real interview questions explained step-by-step with simple language

---

## Table of Contents

1. [What Interviewers Expect](#what-interviewers-expect-at-25-3-yoe)
2. [How to Approach Any Question](#how-to-approach-any-system-design-question)
3. [Example 1: Design URL Shortener (like bit.ly)](#example-1-design-url-shortener-like-bitly)
4. [Example 2: Design Twitter Feed](#example-2-design-twitter-feed)
5. [Example 3: Design WhatsApp Messaging](#example-3-design-whatsapp-messaging)
6. [Example 4: Design Rate Limiter](#example-4-design-rate-limiter)
7. [Practice Tips](#practice-tips)

---

## What Interviewers Expect at 2.5-3 YOE

```
AT YOUR LEVEL, INTERVIEWERS WANT TO SEE:

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  ✓ You can break down a problem logically                     │
│  ✓ You ask good questions before designing                    │
│  ✓ You know basic building blocks (DB, Cache, Load Balancer)  │
│  ✓ You can draw a simple architecture                         │
│  ✓ You understand trade-offs (not just one solution)          │
│  ✓ You communicate your thinking clearly                      │
│                                                                │
│  THEY DON'T EXPECT:                                           │
│  ✗ Perfect solution                                           │
│  ✗ Deep distributed systems knowledge                         │
│  ✗ Knowing every database or tool                             │
│  ✗ Handling billions of users                                 │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Comparison: What's Expected at Different Levels

```
┌─────────────────┬────────────────────────┬────────────────────────┐
│    Aspect       │   Junior (1-2 YOE)     │   Mid (2.5-3 YOE)      │
├─────────────────┼────────────────────────┼────────────────────────┤
│ Questions       │ May need hints         │ Ask own questions      │
├─────────────────┼────────────────────────┼────────────────────────┤
│ Design          │ Basic components       │ Explain why each       │
│                 │                        │ component is needed    │
├─────────────────┼────────────────────────┼────────────────────────┤
│ Scale           │ Thousands of users     │ Millions of users      │
├─────────────────┼────────────────────────┼────────────────────────┤
│ Trade-offs      │ Mention them           │ Explain pros/cons      │
├─────────────────┼────────────────────────┼────────────────────────┤
│ Calculations    │ Basic estimates        │ Back-of-envelope math  │
├─────────────────┼────────────────────────┼────────────────────────┤
│ Communication   │ Needs guidance         │ Leads discussion       │
└─────────────────┴────────────────────────┴────────────────────────┘
```

---

## How to Approach Any System Design Question

### The 5-Step Framework

```
Every system design question can be solved with these 5 steps:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   STEP 1: UNDERSTAND (5 minutes)                               │
│   ─────────────────────────────                                │
│   Ask questions! Don't assume anything.                        │
│                                                                 │
│   STEP 2: DEFINE APIs (5 minutes)                              │
│   ───────────────────────────────                              │
│   What actions can users do? Write the endpoints.              │
│                                                                 │
│   STEP 3: DESIGN DATABASE (5 minutes)                          │
│   ────────────────────────────────────                         │
│   What data do we store? Design tables.                        │
│                                                                 │
│   STEP 4: DRAW ARCHITECTURE (15 minutes)                       │
│   ──────────────────────────────────────                       │
│   Draw boxes and arrows. Show how data flows.                  │
│                                                                 │
│   STEP 5: DISCUSS & IMPROVE (10 minutes)                       │
│   ──────────────────────────────────────                       │
│   Talk about scaling, failures, trade-offs.                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Questions You Should ALWAYS Ask

```
Before designing anything, ask:

FUNCTIONAL (What does it do?)
─────────────────────────────
• What are the main features?
• Who are the users?
• What can users do?

NON-FUNCTIONAL (How well does it do it?)
────────────────────────────────────────
• How many users? (Scale)
• How fast should it respond? (Latency)
• Can it be down sometimes? (Availability)
• Is read or write more frequent?

Example:
─────────
Interviewer: "Design a URL shortener"

You: "Before I start, can I ask a few questions?"
     "How many URLs will be shortened per day?"
     "How many times will short URLs be accessed?"
     "Should URLs expire?"
     "Do we need analytics (click counts)?"
```

---

## Example 1: Design URL Shortener (like bit.ly)

### What is a URL Shortener?

```
REAL-WORLD EXAMPLE:
──────────────────

Long URL (hard to share):
https://www.amazon.in/products/electronics/mobiles/samsung-galaxy-s24-ultra-256gb?ref=123&campaign=sale

Short URL (easy to share):
https://bit.ly/abc123

When someone clicks short URL → They reach the long URL

IT'S LIKE:
──────────
A nickname for a long name.
"Rajesh Kumar Sharma" → "Raj"
When someone calls "Raj", they mean "Rajesh Kumar Sharma"
```

### Step 1: Understand Requirements (5 min)

```
ASK THESE QUESTIONS:
────────────────────

You: "How many URLs shortened per day?"
Interviewer: "10 million per day"

You: "How many times are short URLs clicked per day?"
Interviewer: "100 million clicks per day"
(This tells us: Read-heavy system! 10x more reads than writes)

You: "Should URLs expire?"
Interviewer: "Yes, default 1 year, customizable"

You: "Do users need to see click statistics?"
Interviewer: "Yes, basic analytics"

You: "Can users choose custom short codes?"
Interviewer: "Yes, optionally"


WRITE DOWN REQUIREMENTS:
────────────────────────
┌─────────────────────────────────────────────────────────┐
│  Functional:                                            │
│  • Shorten a long URL → get short URL                  │
│  • Clicking short URL → redirect to long URL           │
│  • Custom short codes (optional)                        │
│  • URL expiration                                       │
│  • Click analytics                                      │
│                                                         │
│  Non-Functional:                                        │
│  • 10M URLs created/day                                │
│  • 100M redirects/day                                  │
│  • Low latency (redirect should be fast)               │
│  • High availability (should always work)              │
└─────────────────────────────────────────────────────────┘
```

### Step 2: Design APIs (5 min)

```
WHAT CAN USERS DO?
──────────────────
1. Create a short URL
2. Use short URL to reach original
3. View analytics

API DESIGN:
───────────

1. CREATE SHORT URL
────────────────────
POST /api/v1/shorten

Request (what user sends):
{
  "long_url": "https://amazon.in/very/long/url...",
  "custom_code": "my-link",     ← Optional
  "expires_in_days": 30         ← Optional
}

Response (what we send back):
{
  "short_url": "https://short.ly/abc123",
  "expires_at": "2025-02-15"
}


2. REDIRECT (when someone clicks short URL)
───────────────────────────────────────────
GET /abc123

Response: 
  HTTP 301 Redirect to https://amazon.in/very/long/url...
  
  (Browser automatically goes to original URL)


3. GET ANALYTICS
────────────────
GET /api/v1/analytics/abc123

Response:
{
  "short_code": "abc123",
  "long_url": "https://amazon.in/...",
  "total_clicks": 5432,
  "created_at": "2024-01-15",
  "expires_at": "2025-01-15"
}
```

### Step 3: Design Database (5 min)

```
WHAT DATA DO WE NEED TO STORE?
──────────────────────────────

For each shortened URL, we need:
• The short code (abc123)
• The original long URL
• When it was created
• When it expires
• Click count
• Who created it (optional)


DATABASE TABLE:
───────────────

┌─────────────────────────────────────────────────────────────────┐
│                         urls TABLE                               │
├───────────────┬──────────────┬──────────────────────────────────┤
│    Column     │    Type      │         Description              │
├───────────────┼──────────────┼──────────────────────────────────┤
│ id            │ BIGINT       │ Auto-increment ID                │
│ short_code    │ VARCHAR(10)  │ "abc123" (UNIQUE, INDEXED)       │
│ long_url      │ TEXT         │ Original URL                     │
│ user_id       │ BIGINT       │ Who created it (nullable)        │
│ click_count   │ BIGINT       │ Number of times clicked          │
│ created_at    │ TIMESTAMP    │ When created                     │
│ expires_at    │ TIMESTAMP    │ When it expires                  │
└───────────────┴──────────────┴──────────────────────────────────┘

WHY THESE CHOICES?
──────────────────
• short_code is INDEXED → Fast lookup when redirecting
• short_code is UNIQUE → No two URLs have same code
• Using SQL (MySQL/PostgreSQL) → Need reliability, simple queries


SQL:
────
CREATE TABLE urls (
    id           BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code   VARCHAR(10) UNIQUE NOT NULL,
    long_url     TEXT NOT NULL,
    user_id      BIGINT,
    click_count  BIGINT DEFAULT 0,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at   TIMESTAMP,
    INDEX idx_short_code (short_code)
);
```

### Step 4: Draw Architecture (15 min)

```
BASIC FLOW:
───────────

Creating Short URL:
┌────────┐    POST /shorten    ┌────────────┐    Save    ┌──────────┐
│ User   │ ─────────────────► │   Server   │ ─────────► │ Database │
│        │ ◄───────────────── │            │            │          │
└────────┘   short_url        └────────────┘            └──────────┘


Using Short URL (Redirect):
┌────────┐   GET /abc123   ┌────────────┐   Lookup   ┌──────────┐
│ User   │ ───────────────►│   Server   │ ─────────► │ Database │
│        │                 │            │ ◄───────── │          │
│        │ ◄─────────────  │            │  long_url  └──────────┘
└────────┘  301 Redirect   └────────────┘


PROBLEM: This is slow for 100 million redirects/day!
─────────────────────────────────────────────────────

Every redirect hits database. Database will crash!

SOLUTION: Add Cache
───────────────────

Cache stores frequently accessed URLs in memory.
Memory is 100x faster than database!


IMPROVED FLOW WITH CACHE:
─────────────────────────

┌────────┐                ┌────────────┐
│ User   │───────────────►│   Server   │
│        │   GET /abc123  │            │
└────────┘                └─────┬──────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       │
              ┌──────────┐                  │
              │  Cache   │                  │
              │ (Redis)  │                  │
              └────┬─────┘                  │
                   │                        │
         ┌─────────┴─────────┐              │
         │                   │              │
    Found (Hit)         Not Found           │
         │              (Miss)              │
         │                   │              │
         │                   ▼              │
         │            ┌──────────┐          │
         │            │ Database │          │
         │            └────┬─────┘          │
         │                 │                │
         │                 ▼                │
         │         Store in cache           │
         │          for next time           │
         │                 │                │
         ▼                 ▼                │
    Return URL        Return URL            │
                                            │
                                            
Step-by-step:
1. User clicks short.ly/abc123
2. Server checks Redis cache: "Is abc123 here?"
3. If YES (cache hit) → Return immediately (super fast!)
4. If NO (cache miss) → Check database → Store in cache → Return
5. Next time someone clicks abc123 → Found in cache (fast!)
```

### Full Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        URL SHORTENER ARCHITECTURE                        │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │    Users     │
                              │  (Browsers,  │
                              │    Apps)     │
                              └──────┬───────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │    Load      │
                              │   Balancer   │
                              │              │
                              │ Distributes  │
                              │ traffic to   │
                              │ servers      │
                              └──────┬───────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
              ┌──────────┐    ┌──────────┐    ┌──────────┐
              │ Server 1 │    │ Server 2 │    │ Server 3 │
              │          │    │          │    │          │
              │ Handles  │    │ Handles  │    │ Handles  │
              │ requests │    │ requests │    │ requests │
              └────┬─────┘    └────┬─────┘    └────┬─────┘
                   │               │               │
                   └───────────────┼───────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
              ┌──────────┐                 ┌──────────┐
              │  Cache   │                 │ Database │
              │ (Redis)  │                 │ (MySQL)  │
              │          │                 │          │
              │ Fast     │                 │ Permanent│
              │ storage  │                 │ storage  │
              │ (temp)   │                 │          │
              └──────────┘                 └──────────┘


WHY EACH COMPONENT?
───────────────────

Load Balancer:
  → 100M requests/day is too much for 1 server
  → Distributes requests across multiple servers
  → If one server dies, others still work

Multiple Servers:
  → Handle more traffic
  → No single point of failure

Cache (Redis):
  → Popular URLs accessed frequently
  → Database can't handle 100M requests
  → Redis handles millions of reads/second
  → Store URL mappings for quick access

Database (MySQL):
  → Permanent storage
  → Survives restarts
  → Source of truth for all data
```

### How to Generate Short Codes?

```
We need unique short codes like "abc123". How to generate them?

OPTION 1: Hash the URL
──────────────────────
Take long URL → Apply hash function → Get short code

long_url = "https://amazon.in/very/long/url"
hash(long_url) = "a1b2c3d4e5f6..."
short_code = first 7 characters = "a1b2c3d"

Problem: Different URLs might give same hash (collision)
Solution: If collision, add random character and retry


OPTION 2: Counter + Base62
──────────────────────────
Use auto-increment ID and convert to Base62

ID = 12345
Base62 = "dnh"  (using a-z, A-Z, 0-9)

Characters available: a-z (26) + A-Z (26) + 0-9 (10) = 62 characters

With 7 characters: 62^7 = 3.5 trillion unique codes!

Example:
  ID 1     → "0000001" → "b"
  ID 100   → "0000100" → "Bm"
  ID 12345 → "0012345" → "dnh"

Pros: Simple, no collisions
Cons: Predictable (can guess next code)


OPTION 3: Random String
───────────────────────
Generate random 7-character string

short_code = random(7) = "xK9mP2q"

Pros: Not predictable
Cons: Must check if already exists (unlikely but possible)


RECOMMENDED FOR INTERVIEW: Option 2 (Counter + Base62)
Why? Simple to explain, guaranteed unique, efficient
```

### Step 5: Discuss Improvements (10 min)

```
SCALING:
────────
Q: "What if we have 1 billion URLs?"
A: "We'd shard the database by short_code.
    URLs starting with a-m → Shard 1
    URLs starting with n-z → Shard 2"


CACHING:
────────
Q: "What's our caching strategy?"
A: "Cache-aside pattern:
    - Check cache first
    - If miss, get from DB and store in cache
    - Set TTL (time-to-live) of 24 hours
    - Popular URLs stay in cache, unpopular ones expire"


ANALYTICS:
──────────
Q: "How to track clicks without slowing down redirects?"
A: "Don't update database on every click.
    Instead:
    1. Log click to message queue
    2. Return redirect immediately (fast!)
    3. Background worker processes queue
    4. Updates click count in batches"

    ┌────────┐  click   ┌────────┐  log   ┌─────────┐  batch  ┌────────┐
    │  User  │─────────►│ Server │───────►│  Queue  │────────►│   DB   │
    │        │◄─────────│        │        │         │ update  │        │
    └────────┘ redirect └────────┘        └─────────┘         └────────┘
                (fast!)              (processed later)


EXPIRATION:
───────────
Q: "How to handle expired URLs?"
A: "Two approaches:
    1. Lazy: Check expiry when URL is accessed
    2. Scheduled: Background job deletes expired URLs daily"


FAILURES:
─────────
Q: "What if database goes down?"
A: "We have:
    - Read replicas for backup
    - Cache still serves popular URLs
    - Users may see errors for new URLs temporarily"
```

### Summary - URL Shortener

```
┌─────────────────────────────────────────────────────────────────┐
│                    URL SHORTENER SUMMARY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CORE COMPONENTS:                                               │
│  • Load Balancer → Distribute traffic                           │
│  • Multiple Servers → Handle load                               │
│  • Redis Cache → Fast URL lookups                               │
│  • MySQL Database → Store URL mappings                          │
│                                                                  │
│  KEY DECISIONS:                                                 │
│  • Short code: Base62 encoding of ID                            │
│  • Cache strategy: Cache-aside with TTL                         │
│  • Analytics: Async via message queue                           │
│                                                                  │
│  NUMBERS:                                                        │
│  • 10M writes/day = ~115 writes/second                         │
│  • 100M reads/day = ~1150 reads/second                         │
│  • 95%+ served from cache                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 2: Design Twitter Feed

### What is Twitter Feed?

```
REAL-WORLD EXAMPLE:
──────────────────

When you open Twitter/X:
• You see tweets from people you follow
• Tweets are sorted (newest first or by algorithm)
• New tweets appear as people post them

IT'S LIKE:
──────────
A newspaper that's personalized for YOU.
It only shows articles from writers YOU follow.
And it updates in real-time!
```

### Step 1: Understand Requirements (5 min)

```
ASK THESE QUESTIONS:
────────────────────

You: "How many users?"
Interviewer: "100 million daily active users"

You: "How many tweets per day?"
Interviewer: "500 million tweets per day"

You: "Average followers per user?"
Interviewer: "Average 200, but celebrities have millions"

You: "How should feed be sorted?"
Interviewer: "By time, newest first (for simplicity)"

You: "How fresh should the feed be?"
Interviewer: "Near real-time, few seconds delay is OK"


WRITE DOWN:
───────────
┌─────────────────────────────────────────────────────────┐
│  Functional:                                            │
│  • Users can post tweets                               │
│  • Users can follow other users                        │
│  • Users see feed of tweets from people they follow    │
│                                                         │
│  Non-Functional:                                        │
│  • 100M daily active users                             │
│  • 500M tweets/day                                     │
│  • Near real-time feed                                 │
│  • Read-heavy (people read more than post)             │
└─────────────────────────────────────────────────────────┘
```

### Step 2: Design APIs (5 min)

```
WHAT CAN USERS DO?
──────────────────
1. Post a tweet
2. View their feed
3. Follow someone

API DESIGN:
───────────

1. POST A TWEET
───────────────
POST /api/v1/tweets

Request:
{
  "content": "Hello World!",
  "media_ids": ["img123"]    ← Optional
}

Response:
{
  "tweet_id": "123456",
  "created_at": "2024-01-15T10:30:00Z"
}


2. GET FEED
───────────
GET /api/v1/feed?page=1&limit=20

Response:
{
  "tweets": [
    {
      "tweet_id": "123",
      "user_id": "456",
      "user_name": "rahul",
      "content": "Good morning!",
      "likes": 50,
      "created_at": "2024-01-15T10:30:00Z"
    },
    ...
  ],
  "next_page": 2
}


3. FOLLOW USER
──────────────
POST /api/v1/users/{user_id}/follow

Response:
{
  "success": true,
  "following_count": 201
}
```

### Step 3: Design Database (5 min)

```
WHAT DATA DO WE NEED?
─────────────────────

1. Users (who is on the platform)
2. Tweets (what they posted)
3. Follows (who follows whom)


DATABASE TABLES:
────────────────

┌─────────────────────────────────────────────────────────────────┐
│                         users TABLE                              │
├───────────────┬──────────────┬──────────────────────────────────┤
│ id            │ BIGINT       │ User ID                          │
│ username      │ VARCHAR(50)  │ @username                        │
│ name          │ VARCHAR(100) │ Display name                     │
│ followers_cnt │ INT          │ Number of followers              │
│ created_at    │ TIMESTAMP    │ When joined                      │
└───────────────┴──────────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        tweets TABLE                              │
├───────────────┬──────────────┬──────────────────────────────────┤
│ id            │ BIGINT       │ Tweet ID                         │
│ user_id       │ BIGINT       │ Who posted (INDEXED)             │
│ content       │ VARCHAR(280) │ Tweet text                       │
│ likes_count   │ INT          │ Number of likes                  │
│ created_at    │ TIMESTAMP    │ When posted (INDEXED)            │
└───────────────┴──────────────┴──────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        follows TABLE                             │
├───────────────┬──────────────┬──────────────────────────────────┤
│ follower_id   │ BIGINT       │ Who is following                 │
│ followee_id   │ BIGINT       │ Who is being followed            │
│ created_at    │ TIMESTAMP    │ When followed                    │
└───────────────┴──────────────┴──────────────────────────────────┘

Index on (follower_id) → Find who I follow
Index on (followee_id) → Find my followers
```

### Step 4: The BIG Question - How to Generate Feed?

```
THE CORE PROBLEM:
─────────────────

When Rahul opens his feed:
• Rahul follows 200 people
• We need to show him tweets from those 200 people
• Sorted by time
• And do this FAST!

TWO APPROACHES:
───────────────
1. PULL (Get tweets when user asks)
2. PUSH (Pre-compute feed in advance)

Let's understand both:
```

#### Approach 1: PULL (Fan-out on Read)

```
WHAT IS IT?
───────────
When user opens feed, we PULL tweets from everyone they follow.

HOW IT WORKS:
─────────────

Rahul opens his feed:

Step 1: Get list of people Rahul follows
        → [User1, User2, User3, ... User200]

Step 2: For each person, get their recent tweets
        → User1's tweets: [T1, T2, T3]
        → User2's tweets: [T4, T5]
        → User3's tweets: [T6, T7, T8]
        → ...

Step 3: Merge all tweets and sort by time

Step 4: Return top 20


DIAGRAM:
────────

┌─────────┐
│  Rahul  │ Opens feed
└────┬────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│                      FEED SERVICE                            │
│                                                              │
│  Step 1: Who does Rahul follow?                             │
│          → Query follows table                               │
│          → Get [User1, User2, ... User200]                  │
│                                                              │
│  Step 2: Get tweets from each user                          │
│          → 200 queries to tweets table!                     │
│                                                              │
│  Step 3: Merge all tweets                                   │
│          → Sort by created_at                               │
│                                                              │
│  Step 4: Return top 20                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘


PROS:
  ✓ Simple to build
  ✓ No extra storage needed
  ✓ Tweets appear instantly after posting

CONS:
  ✗ SLOW! 200 database queries every time feed loads
  ✗ More following = slower feed
  ✗ Can't handle millions of users


REAL-WORLD ANALOGY:
───────────────────
Like asking each newspaper vendor individually what's new.
If you read 200 newspapers, you ask 200 vendors every morning!
VERY SLOW!
```

#### Approach 2: PUSH (Fan-out on Write)

```
WHAT IS IT?
───────────
When someone posts a tweet, we PUSH it to all their followers' feeds.
Feeds are pre-computed and ready to read!

HOW IT WORKS:
─────────────

Virat Kohli posts a tweet:

Step 1: Save tweet to database

Step 2: Get Virat's followers
        → [Rahul, Priya, ... 50 million people]

Step 3: Add tweet ID to each follower's feed cache
        → Rahul's feed cache: Add Virat's tweet
        → Priya's feed cache: Add Virat's tweet
        → ... 50 million caches updated!

Later, when Rahul opens feed:
        → Just read from Rahul's pre-computed feed cache
        → Already sorted, already ready!
        → Super fast!


DIAGRAM:
────────

Virat posts tweet:

┌───────────┐
│  Virat    │ Posts tweet
└─────┬─────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                      TWEET SERVICE                           │
│                                                              │
│  Step 1: Save tweet to DB                                   │
│                                                              │
│  Step 2: Get Virat's 50M followers                          │
│                                                              │
│  Step 3: Push to message queue                              │
│          (to process asynchronously)                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌──────────────┐
│   Message    │
│    Queue     │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FAN-OUT WORKERS                           │
│                                                              │
│  For each follower:                                         │
│    Add tweet_id to their feed cache                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       ▼                  ▼                  ▼
┌────────────┐     ┌────────────┐     ┌────────────┐
│  Rahul's   │     │  Priya's   │     │  50M more  │
│   Feed     │     │   Feed     │     │   feeds    │
│   Cache    │     │   Cache    │     │            │
└────────────┘     └────────────┘     └────────────┘


Later, Rahul opens feed:

┌─────────┐                    ┌────────────┐
│  Rahul  │ ──── Get feed ───► │  Rahul's   │
│         │ ◄──── tweets ───── │   Feed     │
└─────────┘    (instant!)      │   Cache    │
                               └────────────┘


PROS:
  ✓ Reading feed is SUPER FAST
  ✓ Feed is pre-computed
  ✓ Just one cache read

CONS:
  ✗ Celebrities are a HUGE problem!
    Virat has 50 million followers
    50 million cache writes for ONE tweet!
    Takes minutes to propagate!
  
  ✗ Wasted work for inactive users
    Someone hasn't logged in for 6 months
    Still updating their feed cache!

  ✗ High storage cost
    Storing feed for every user


REAL-WORLD ANALOGY:
───────────────────
Like newspaper delivered to your door.
Delivery person goes to EVERY subscriber's house every morning.
If newspaper has 50 million subscribers, that's a LOT of delivery!
```

#### Approach 3: HYBRID (Best Approach) ⭐

```
WHAT IS IT?
───────────
Combine PULL and PUSH based on who is posting.

THE IDEA:
─────────
• Regular users (< 10K followers): Use PUSH
  → Their tweets go to followers' feed caches
  
• Celebrities (> 10K followers): Use PULL
  → Don't push to millions of caches
  → Fetch their tweets when user opens feed


HOW IT WORKS:
─────────────

When regular user posts:
  → Push to all followers' caches (only thousands, manageable)

When celebrity posts:
  → Just save to database
  → Don't fan out to millions of caches

When Rahul opens feed:
  1. Get pre-computed feed from cache (tweets from regular followings)
  2. Fetch latest tweets from celebrities Rahul follows
  3. Merge both lists
  4. Return sorted feed


DIAGRAM:
────────

┌─────────────────────────────────────────────────────────────────────┐
│                         HYBRID APPROACH                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   WHEN POSTING:                                                     │
│   ─────────────                                                     │
│                                                                      │
│   Regular User (< 10K followers)                                    │
│   ┌──────────┐                                                      │
│   │  Posts   │───► Fan-out to all followers' caches (PUSH)         │
│   └──────────┘                                                      │
│                                                                      │
│   Celebrity (> 10K followers)                                       │
│   ┌──────────┐                                                      │
│   │  Posts   │───► Just save to database (NO fan-out)              │
│   └──────────┘                                                      │
│                                                                      │
│                                                                      │
│   WHEN READING FEED:                                                │
│   ──────────────────                                                │
│                                                                      │
│   ┌──────────────────────────────────────────────────────────────┐ │
│   │                                                              │ │
│   │  Step 1: Get pre-computed feed from cache                   │ │
│   │          (tweets from regular users I follow)               │ │
│   │                     ↓                                        │ │
│   │  Step 2: Get list of celebrities I follow                   │ │
│   │          (Virat, Sachin, PM Modi...)                        │ │
│   │                     ↓                                        │ │
│   │  Step 3: Fetch recent tweets from each celebrity            │ │
│   │          (only 5-10 celebrities, so 5-10 queries)           │ │
│   │                     ↓                                        │ │
│   │  Step 4: Merge both lists, sort by time                     │ │
│   │                     ↓                                        │ │
│   │  Step 5: Return top 20 tweets                               │ │
│   │                                                              │ │
│   └──────────────────────────────────────────────────────────────┘ │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘


WHY THIS WORKS:
───────────────

• Most users follow few celebrities (5-10)
  → Only 5-10 extra queries, fast enough!

• Celebrities don't slow down the system
  → No fan-out to millions of caches

• Regular users' tweets appear instantly
  → Pre-computed in followers' caches


THIS IS HOW TWITTER ACTUALLY WORKS! ⭐
```

### Full Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      TWITTER FEED ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────┘

                                 ┌──────────────┐
                                 │    Users     │
                                 └──────┬───────┘
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │    Load      │
                                 │   Balancer   │
                                 └──────┬───────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                         ▼                             ▼
                  ┌─────────────┐              ┌─────────────┐
                  │   Tweet     │              │    Feed     │
                  │   Service   │              │   Service   │
                  │             │              │             │
                  │ • Post tweet│              │ • Get feed  │
                  │ • Store     │              │ • Merge     │
                  └──────┬──────┘              └──────┬──────┘
                         │                            │
                         │                    ┌───────┴───────┐
                         │                    │               │
                         │                    ▼               ▼
                         │             ┌──────────┐    ┌──────────┐
                         │             │  Feed    │    │Celebrity │
                         │             │  Cache   │    │ Tweets   │
                         │             │ (Redis)  │    │ (Direct) │
                         │             └──────────┘    └──────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │   Message   │
                  │    Queue    │
                  │   (Kafka)   │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  Fan-out    │
                  │  Workers    │
                  │             │
                  │ Push tweets │
                  │ to caches   │
                  └──────┬──────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                  │
│                                                                       │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                │
│  │   Users     │   │   Tweets    │   │   Follows   │                │
│  │    DB       │   │     DB      │   │    Graph    │                │
│  └─────────────┘   └─────────────┘   └─────────────┘                │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Summary - Twitter Feed

```
┌─────────────────────────────────────────────────────────────────┐
│                     TWITTER FEED SUMMARY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  THE PROBLEM:                                                   │
│  Show personalized feed from hundreds of people you follow      │
│                                                                  │
│  THE SOLUTION:                                                  │
│  Hybrid approach - Push for regular users, Pull for celebrities │
│                                                                  │
│  KEY COMPONENTS:                                                │
│  • Feed Cache (Redis) → Pre-computed feeds                      │
│  • Message Queue → Async fan-out                                │
│  • Tweet DB → Store all tweets                                  │
│  • Follows Graph → Who follows whom                             │
│                                                                  │
│  KEY DECISIONS:                                                 │
│  • Celebrity threshold: 10K followers                           │
│  • Feed cache: Last 1000 tweets per user                        │
│  • Queue: Kafka for reliability                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 3: Design WhatsApp Messaging

### What is WhatsApp Messaging?

```
REAL-WORLD EXAMPLE:
──────────────────

WhatsApp lets you:
• Send messages to friends (1-on-1 chat)
• Create groups and chat with multiple people
• See if someone is online
• See if your message was delivered and read (✓ ✓)

IT'S LIKE:
──────────
A post office that:
• Delivers letters instantly
• Tells you when letter was delivered
• Tells you when letter was read
• Works for individuals and groups
```

### Step 1: Understand Requirements (5 min)

```
ASK THESE QUESTIONS:
────────────────────

You: "How many users?"
Interviewer: "500 million daily active users"

You: "Messages per day?"
Interviewer: "50 billion messages per day"

You: "Group chat size?"
Interviewer: "Max 256 members per group"

You: "Message types?"
Interviewer: "Text, images, videos, documents"

You: "Need online status?"
Interviewer: "Yes, show online/offline and last seen"

You: "Need read receipts?"
Interviewer: "Yes, sent/delivered/read (✓ ✓)"


WRITE DOWN:
───────────
┌─────────────────────────────────────────────────────────┐
│  Functional:                                            │
│  • 1-on-1 messaging                                    │
│  • Group messaging (up to 256)                         │
│  • Media sharing (images, videos)                      │
│  • Online status (online / last seen)                  │
│  • Read receipts (sent ✓, delivered ✓✓, read ✓✓)      │
│  • Message history                                      │
│                                                         │
│  Non-Functional:                                        │
│  • 500M daily users                                    │
│  • 50B messages/day                                    │
│  • Real-time delivery                                  │
│  • Messages should never be lost                       │
└─────────────────────────────────────────────────────────┘
```

### Step 2: Understanding Real-Time Messaging

```
HOW DO MESSAGES APPEAR INSTANTLY?
─────────────────────────────────

Normal HTTP (Request-Response):
  Client asks → Server responds → Connection closed
  
  Problem: Server can't send message unless client asks!
           Client would have to keep asking "Any new messages?"
           every second. Very inefficient!


WebSocket (Persistent Connection):
  Client connects → Connection stays open → Both can send anytime
  
  Like a phone call:
  • You dial once (connect)
  • Line stays open
  • Both can talk anytime
  • Until one hangs up (disconnect)


DIAGRAM:
────────

HTTP (Normal):
┌────────┐                        ┌────────┐
│ Client │──── "Any messages?" ──►│ Server │
│        │◄─── "No" ──────────────│        │
│        │                        │        │
│        │──── "Any messages?" ──►│        │  Client keeps
│        │◄─── "No" ──────────────│        │  asking!
│        │                        │        │  Inefficient!
│        │──── "Any messages?" ──►│        │
│        │◄─── "Yes, here's one" ─│        │
└────────┘                        └────────┘


WebSocket (Real-time):
┌────────┐                        ┌────────┐
│ Client │════ Connect ══════════►│ Server │
│        │                        │        │
│        │     (Connection stays open)     │
│        │                        │        │
│        │◄─── "New message!" ────│        │  Server pushes
│        │                        │        │  instantly!
│        │◄─── "Another one!" ────│        │
│        │                        │        │
│        │──── "I'm typing..." ──►│        │
│        │                        │        │
└────────┘                        └────────┘


WhatsApp uses WebSocket for instant messaging!
```

### Step 3: Design APIs (5 min)

```
TWO TYPES OF COMMUNICATION:
───────────────────────────

1. WebSocket (Real-time)
   → Sending/receiving messages
   → Typing indicators
   → Online status

2. REST API (Normal)
   → Login/Register
   → Get message history
   → Upload media
   → Create group


WEBSOCKET MESSAGES:
───────────────────

Sending a message:
{
  "type": "message",
  "to": "user456",           // or "group123"
  "content": "Hello!",
  "message_id": "unique-id"
}

Receiving a message:
{
  "type": "message",
  "from": "user123",
  "content": "Hello!",
  "message_id": "unique-id",
  "timestamp": "2024-01-15T10:30:00Z"
}

Delivery receipt:
{
  "type": "receipt",
  "message_id": "unique-id",
  "status": "delivered"      // or "read"
}

Typing indicator:
{
  "type": "typing",
  "chat_id": "user456",
  "is_typing": true
}


REST APIs:
──────────

GET /api/v1/messages/{chat_id}?before=timestamp&limit=50
→ Get message history (for loading old messages)

POST /api/v1/media/upload
→ Upload image/video, get media_url

POST /api/v1/groups
→ Create new group

GET /api/v1/groups/{group_id}/members
→ Get group members
```

### Step 4: Message Flow - Step by Step

```
Let's trace what happens when Rahul sends "Hello" to Priya:

┌─────────────────────────────────────────────────────────────────────────┐
│                    MESSAGE FLOW: RAHUL → PRIYA                           │
└─────────────────────────────────────────────────────────────────────────┘

STEP 1: Rahul types and sends
────────────────────────────

┌──────────┐
│  Rahul   │  Types "Hello", hits send
│  (App)   │
└────┬─────┘
     │
     │  WebSocket message:
     │  {
     │    "type": "message",
     │    "to": "priya123",
     │    "content": "Hello",
     │    "message_id": "msg-001"
     │  }
     │
     ▼


STEP 2: Server receives and saves
─────────────────────────────────

┌────────────────┐
│    Gateway     │  (WebSocket Server)
│    Server      │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│    Message     │
│    Service     │
│                │
│  1. Validate   │
│  2. Save to DB │
│  3. Mark as    │
│     "sent"     │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Database     │  Message saved!
│   (Messages)   │  Status: SENT ✓
└────────────────┘


STEP 3: Server tells Rahul "sent"
─────────────────────────────────

┌────────────────┐
│    Server      │
└───────┬────────┘
        │
        │  {
        │    "type": "receipt",
        │    "message_id": "msg-001",
        │    "status": "sent"
        │  }
        │
        ▼
┌──────────┐
│  Rahul   │  Shows ✓ (one tick)
│  (App)   │
└──────────┘


STEP 4: Server checks if Priya is online
────────────────────────────────────────

┌────────────────┐
│    Server      │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│     Redis      │  Query: Is Priya online?
│   (Sessions)   │  → YES! Connected to Server-3
└────────────────┘


STEP 5: Deliver to Priya
────────────────────────

┌────────────────┐
│   Server-3     │  (where Priya is connected)
└───────┬────────┘
        │
        │  {
        │    "type": "message",
        │    "from": "rahul456",
        │    "content": "Hello",
        │    "message_id": "msg-001",
        │    "timestamp": "..."
        │  }
        │
        ▼
┌──────────┐
│  Priya   │  Message appears!
│  (App)   │
└──────────┘


STEP 6: Priya's app sends "delivered" receipt
─────────────────────────────────────────────

┌──────────┐
│  Priya   │
│  (App)   │
└────┬─────┘
     │
     │  {
     │    "type": "receipt",
     │    "message_id": "msg-001",
     │    "status": "delivered"
     │  }
     │
     ▼
┌────────────────┐
│    Server      │  Updates DB: Status = DELIVERED
└───────┬────────┘
        │
        ▼
┌──────────┐
│  Rahul   │  Shows ✓✓ (two grey ticks)
│  (App)   │
└──────────┘


STEP 7: Priya opens and reads the message
─────────────────────────────────────────

┌──────────┐
│  Priya   │  Opens chat with Rahul
│  (App)   │
└────┬─────┘
     │
     │  {
     │    "type": "receipt",
     │    "message_id": "msg-001",
     │    "status": "read"
     │  }
     │
     ▼
┌────────────────┐
│    Server      │  Updates DB: Status = READ
└───────┬────────┘
        │
        ▼
┌──────────┐
│  Rahul   │  Shows ✓✓ (two BLUE ticks)
│  (App)   │
└──────────┘


COMPLETE! 🎉
```

### What if Priya is Offline?

```
STEP 4 (Different): Priya is NOT online
───────────────────────────────────────

┌────────────────┐
│    Server      │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│     Redis      │  Query: Is Priya online?
│   (Sessions)   │  → NO! Not connected
└────────────────┘
        │
        ▼
┌────────────────┐
│  Offline       │  Store message_id for Priya
│    Queue       │  LPUSH offline:priya123 msg-001
└────────────────┘


LATER: When Priya comes online
──────────────────────────────

┌──────────┐
│  Priya   │  Opens app, connects to server
│  (App)   │
└────┬─────┘
     │
     ▼
┌────────────────┐
│    Server      │
│                │
│  1. Priya connected!
│  2. Check offline queue
│  3. Found msg-001
│  4. Fetch from DB
│  5. Deliver to Priya
└───────┬────────┘
        │
        ▼
┌──────────┐
│  Priya   │  Gets all pending messages!
│  (App)   │
└──────────┘


MESSAGES ARE NEVER LOST!
Even if recipient is offline for days.
```

### Online Status (Presence)

```
HOW DO WE KNOW IF SOMEONE IS ONLINE?
────────────────────────────────────

Using Redis with expiring keys:

When Priya connects:
  SET online:priya123 "server-3" EX 30
  (Key expires in 30 seconds)

Priya's app sends heartbeat every 20 seconds:
  EXPIRE online:priya123 30
  (Reset expiry to 30 seconds)

When Priya disconnects (or heartbeat stops):
  Key automatically expires after 30 seconds
  SET last_seen:priya123 "2024-01-15T10:30:00Z"

To check if someone is online:
  EXISTS online:priya123
  → 1 (online)
  → 0 (offline, check last_seen)


DIAGRAM:
────────

Priya opens app:
┌──────────┐                     ┌──────────┐
│  Priya   │─── Connect ────────►│  Server  │
│          │                     │          │
└──────────┘                     └────┬─────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  Redis   │
                                │          │
                                │ SET online:priya123
                                │     "server-3"
                                │     EX 30
                                └──────────┘

Every 20 seconds:
┌──────────┐                     ┌──────────┐
│  Priya   │─── Heartbeat ──────►│  Server  │
│          │                     │          │
└──────────┘                     └────┬─────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  Redis   │
                                │          │
                                │ EXPIRE online:priya123 30
                                │ (reset timer)
                                └──────────┘

Priya closes app (no more heartbeats):
  After 30 seconds → Key expires
  Redis automatically removes online:priya123
  Priya appears "offline"
```

### Group Messaging

```
GROUP MESSAGE FLOW:
───────────────────

Rahul sends "Hi everyone" to a group of 50 people:

┌──────────┐
│  Rahul   │  Sends to group-123
└────┬─────┘
     │
     ▼
┌────────────────┐
│    Server      │
│                │
│  1. Save message once (with group_id)
│  2. Get group members (50 people)
│  3. For each member:
│     - If online → Deliver via WebSocket
│     - If offline → Add to their offline queue
└───────┬────────┘
        │
        ├──────────────────┬──────────────────┐
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐       ┌─────────────┐
   │ Online  │        │ Online  │       │   Offline   │
   │ Member1 │        │ Member2 │       │   Members   │
   │         │        │         │       │   (Queue)   │
   └─────────┘        └─────────┘       └─────────────┘
   Gets message       Gets message      Get when
   instantly!         instantly!        they connect


KEY POINT:
Message is stored ONCE in database (not 50 times).
Only reference (message_id) is sent to members.
Efficient storage!
```

### Full Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     WHATSAPP ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────┐
                              │    Users      │
                              │  (Mobile Apps)│
                              └───────┬───────┘
                                      │
                              WebSocket Connection
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         GATEWAY LAYER                                    │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  WebSocket  │  │  WebSocket  │  │  WebSocket  │  │  WebSocket  │   │
│  │  Server 1   │  │  Server 2   │  │  Server 3   │  │  Server 4   │   │
│  │  (10K conn) │  │  (10K conn) │  │  (10K conn) │  │  (10K conn) │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │                │           │
│         └────────────────┴────────────────┴────────────────┘           │
│                                   │                                     │
└───────────────────────────────────┼─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         SERVICE LAYER                                    │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Message   │  │   Group     │  │  Presence   │  │   Media     │   │
│  │   Service   │  │   Service   │  │   Service   │  │   Service   │   │
│  │             │  │             │  │             │  │             │   │
│  │ Send/receive│  │ Manage      │  │ Online/     │  │ Upload/     │   │
│  │ messages    │  │ groups      │  │ offline     │  │ download    │   │
│  └──────┬──────┘  └─────────────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                                  │                │          │
└─────────┼──────────────────────────────────┼────────────────┼──────────┘
          │                                  │                │
          ▼                                  ▼                ▼
┌─────────────────┐                  ┌─────────────┐   ┌─────────────┐
│  Message Queue  │                  │    Redis    │   │     S3      │
│    (Kafka)      │                  │  (Sessions, │   │   (Media    │
│                 │                  │   Presence) │   │   Storage)  │
│ For reliability │                  └─────────────┘   └─────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                     │
│                                                                          │
│  ┌─────────────────────┐         ┌─────────────────────┐               │
│  │      Messages       │         │    Users & Groups   │               │
│  │    (Cassandra)      │         │      (MySQL)        │               │
│  │                     │         │                     │               │
│  │  • High write volume│         │  • User accounts    │               │
│  │  • Fast by chat_id  │         │  • Group info       │               │
│  └─────────────────────┘         └─────────────────────┘               │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘


WHY EACH COMPONENT:
───────────────────

WebSocket Servers:
  → Handle persistent connections
  → Each server handles ~10,000 connections
  → Need many servers for 500M users

Redis:
  → Store who is online
  → Store which server each user is connected to
  → Super fast lookups

Cassandra (for messages):
  → Handles billions of writes per day
  → Fast lookups by conversation
  → Distributed, highly available

MySQL (for users/groups):
  → Reliable for user data
  → Relationships (user belongs to groups)
  → Not high volume like messages

S3:
  → Store images, videos, documents
  → Cheap, reliable, scales automatically

Kafka:
  → Message queue for reliability
  → If server crashes, message isn't lost
```

### Summary - WhatsApp

```
┌─────────────────────────────────────────────────────────────────┐
│                      WHATSAPP SUMMARY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  KEY CONCEPTS:                                                  │
│  • WebSocket for real-time messaging                            │
│  • Redis for online status (with TTL)                           │
│  • Message receipts: sent → delivered → read                    │
│  • Offline queue for offline users                              │
│                                                                  │
│  KEY COMPONENTS:                                                │
│  • WebSocket Gateway → Handle connections                       │
│  • Message Service → Process messages                           │
│  • Cassandra → Store messages (high write)                      │
│  • Redis → Sessions & presence                                  │
│  • S3 → Media storage                                           │
│                                                                  │
│  KEY FLOWS:                                                     │
│  • Send message → Save → Check online → Deliver/Queue          │
│  • Come online → Check offline queue → Deliver pending          │
│  • Heartbeat every 20s → Keep presence alive                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Example 4: Design Rate Limiter

### What is a Rate Limiter?

```
REAL-WORLD EXAMPLE:
──────────────────

At a buffet restaurant:
• Rule: Each person can take max 3 plates
• Why? So food doesn't run out, everyone gets some

If someone tries to take 4th plate:
• They're stopped: "Sorry, limit reached!"

RATE LIMITER = Digital version of this rule

IT'S LIKE:
──────────
A security guard that counts:
"This user made 100 API calls this minute. No more allowed!"

WHY DO WE NEED IT?
──────────────────
• Prevent abuse (someone making millions of requests)
• Protect servers from crashing
• Ensure fair usage for everyone
• Block attackers trying to overload system
```

### Step 1: Understand Requirements (5 min)

```
ASK THESE QUESTIONS:
────────────────────

You: "What are we limiting? Requests per user? Per IP?"
Interviewer: "Per user, for API endpoints"

You: "What's the limit?"
Interviewer: "100 requests per minute for most APIs"

You: "Different limits for different APIs?"
Interviewer: "Yes, login should be stricter (5 per minute)"

You: "What happens when limit exceeded?"
Interviewer: "Return HTTP 429 Too Many Requests"

You: "Distributed system with multiple servers?"
Interviewer: "Yes, must work across all servers"


WRITE DOWN:
───────────
┌─────────────────────────────────────────────────────────┐
│  Functional:                                            │
│  • Limit API requests per user                         │
│  • Different limits for different endpoints            │
│  • Return 429 when limit exceeded                      │
│  • Show remaining quota in response                    │
│                                                         │
│  Non-Functional:                                        │
│  • Work across multiple servers (distributed)          │
│  • Low latency (don't slow down requests)              │
│  • Accurate counting                                    │
└─────────────────────────────────────────────────────────┘
```

### Step 2: Where Does Rate Limiter Sit?

```
RATE LIMITER SITS BETWEEN USER AND YOUR SERVICE:
────────────────────────────────────────────────

┌────────┐         ┌──────────────┐         ┌─────────────┐
│  User  │────────►│ Rate Limiter │────────►│ API Server  │
│        │◄────────│              │◄────────│             │
└────────┘         └──────────────┘         └─────────────┘
                          │
                          │ Checks: "Has this user
                          │ exceeded their limit?"
                          │
                    ┌─────▼─────┐
                    │  Counter  │
                    │  Storage  │
                    │  (Redis)  │
                    └───────────┘

FLOW:
─────
1. User sends request
2. Rate limiter checks: "How many requests has this user made?"
3. If under limit → Allow request → Forward to API server
4. If over limit → Block request → Return 429 error
```

### Step 3: Algorithm - Token Bucket (Most Popular)

```
WHAT IS TOKEN BUCKET?
─────────────────────

Imagine a bucket that holds tokens:

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    THE TOKEN BUCKET                             │
│                                                                 │
│     ┌─────────────────────┐                                    │
│     │  ● ● ● ● ● ● ● ● ● │ ← Bucket (max 10 tokens)           │
│     │  ●                  │                                    │
│     └─────────────────────┘                                    │
│              ↑                                                  │
│              │                                                  │
│     Tokens added at fixed rate                                  │
│     (e.g., 10 tokens per minute)                               │
│                                                                 │
│                                                                 │
│     RULES:                                                      │
│     ───────                                                     │
│     • Each request takes 1 token from bucket                   │
│     • If bucket is empty → Request denied!                     │
│     • Tokens refill at constant rate                           │
│     • Bucket has max capacity (can't overflow)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


EXAMPLE WITH NUMBERS:
─────────────────────

Settings: 10 tokens/minute, bucket size 10

Time 0:00
  Bucket: [●●●●●●●●●●] (10 tokens - full)

Time 0:10 - User makes 3 requests
  Bucket: [●●●●●●●○○○] (7 tokens left)
  All 3 allowed ✓

Time 0:20 - User makes 8 requests
  Bucket: [○○○○○○○○○○] (0 tokens after 7 requests)
  7 allowed ✓, 1 blocked ✗ (not enough tokens!)

Time 0:30 - 5 tokens refilled (30 seconds = 5 tokens at 10/min rate)
  Bucket: [●●●●●○○○○○] (5 tokens)

Time 0:35 - User makes 2 requests
  Bucket: [●●●○○○○○○○] (3 tokens left)
  Both allowed ✓


WHY TOKEN BUCKET IS GOOD:
─────────────────────────
• Allows burst traffic (up to bucket size)
• Smooth rate limiting over time
• Simple to understand and implement
```

### Step 4: Token Bucket Implementation

```
HOW TO IMPLEMENT WITH REDIS:
────────────────────────────

For each user, store:
• Current token count
• Last refill timestamp

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   REDIS STORAGE:                                               │
│                                                                 │
│   Key: rate_limit:user123                                      │
│   Value: {                                                     │
│     "tokens": 7,                                               │
│     "last_refill": 1705312200                                  │
│   }                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


WHEN A REQUEST COMES:
─────────────────────

Step 1: Get current state from Redis
        tokens = 7
        last_refill = 60 seconds ago

Step 2: Calculate tokens to add
        time_passed = 60 seconds
        refill_rate = 10 tokens/minute
        tokens_to_add = 60/60 × 10 = 10 tokens

Step 3: Calculate new token count (cap at max)
        new_tokens = min(7 + 10, 10) = 10  (max is 10)

Step 4: Check if we have tokens
        if new_tokens >= 1:
            Allow request ✓
            new_tokens = new_tokens - 1 = 9
            Update Redis
        else:
            Deny request ✗
            Return 429


PYTHON-LIKE CODE:
─────────────────

def is_allowed(user_id):
    key = f"rate_limit:{user_id}"
    now = current_time()
    
    # Get current state
    data = redis.get(key)
    
    if data is None:
        # First request - give full bucket
        redis.set(key, {
            "tokens": MAX_TOKENS - 1,  # minus 1 for this request
            "last_refill": now
        })
        return True  # Allowed!
    
    # Calculate tokens to add based on time passed
    time_passed = now - data["last_refill"]
    tokens_to_add = time_passed * REFILL_RATE
    
    # New token count (capped at max)
    tokens = min(data["tokens"] + tokens_to_add, MAX_TOKENS)
    
    if tokens >= 1:
        # Allow request, consume 1 token
        redis.set(key, {
            "tokens": tokens - 1,
            "last_refill": now
        })
        return True  # Allowed!
    else:
        return False  # Denied! 429 error
```

### Alternative Algorithm: Sliding Window

```
WHAT IS SLIDING WINDOW?
───────────────────────

Instead of tokens, we track timestamps of each request.

Count requests in the last N seconds.
If count < limit → Allow
If count >= limit → Deny


EXAMPLE:
────────

Limit: 5 requests per minute

Requests made at:
  10:00:10 ✓
  10:00:20 ✓
  10:00:35 ✓
  10:00:45 ✓
  10:00:55 ✓

Now it's 10:01:00, new request comes:
  Window: 10:00:00 to 10:01:00
  Count requests in window: 5
  Limit: 5
  DENIED! (5 >= 5)

At 10:01:15, new request comes:
  Window: 10:00:15 to 10:01:15
  Count: 4 (10:00:10 is outside window now)
  ALLOWED! (4 < 5)


VISUAL:
───────

Timeline:
────────────────────────────────────────────────────────────►
10:00:00   10:00:10  10:00:20  10:00:35  10:00:45  10:00:55  10:01:00
              ✓         ✓         ✓         ✓         ✓         ?
              
At 10:01:00:
|←────────────── 1 minute window ──────────────→|
              ✓         ✓         ✓         ✓         ✓
              1         2         3         4         5     = 5 (DENY!)

At 10:01:15:
              |←────────────── 1 minute window ──────────────→|
                        ✓         ✓         ✓         ✓
                        1         2         3         4     = 4 (ALLOW!)


REDIS IMPLEMENTATION:
─────────────────────

# Use Sorted Set - score is timestamp

# Add request timestamp
ZADD rate_limit:user123 1705312200 "req1"
ZADD rate_limit:user123 1705312210 "req2"

# Remove old entries (outside window)
ZREMRANGEBYSCORE rate_limit:user123 0 <window_start>

# Count current entries
ZCARD rate_limit:user123

# If count < limit, allow and add new entry
```

### Step 5: Full Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     RATE LIMITER ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌───────────────┐
                              │    Users      │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │     Load      │
                              │   Balancer    │
                              └───────┬───────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
             ┌────────────┐   ┌────────────┐   ┌────────────┐
             │ API Server │   │ API Server │   │ API Server │
             │     1      │   │     2      │   │     3      │
             │            │   │            │   │            │
             │ ┌────────┐ │   │ ┌────────┐ │   │ ┌────────┐ │
             │ │  Rate  │ │   │ │  Rate  │ │   │ │  Rate  │ │
             │ │Limiter │ │   │ │Limiter │ │   │ │Limiter │ │
             │ │Middleware│   │ │Middleware│   │ │Middleware│
             │ └───┬────┘ │   │ └───┬────┘ │   │ └───┬────┘ │
             └─────┼──────┘   └─────┼──────┘   └─────┼──────┘
                   │               │               │
                   └───────────────┼───────────────┘
                                   │
                                   ▼
                           ┌───────────────┐
                           │     Redis     │
                           │   (Shared)    │
                           │               │
                           │ Stores counts │
                           │ for all users │
                           └───────────────┘


WHY SHARED REDIS?
─────────────────

Without shared storage:
  User makes request → Goes to Server 1 → Count: 1
  User makes request → Goes to Server 2 → Count: 1
  User makes request → Goes to Server 3 → Count: 1
  
  User made 3 requests but each server thinks only 1!
  Rate limiting is broken! ✗

With shared Redis:
  User makes request → Server 1 → Redis count: 1
  User makes request → Server 2 → Redis count: 2
  User makes request → Server 3 → Redis count: 3
  
  All servers see the same count! ✓
```

### Response Headers

```
GOOD PRACTICE: Tell users their quota
─────────────────────────────────────

SUCCESSFUL REQUEST (200 OK):
────────────────────────────
HTTP/1.1 200 OK
X-RateLimit-Limit: 100          ← Max requests allowed
X-RateLimit-Remaining: 45       ← Requests left
X-RateLimit-Reset: 1705312260   ← When limit resets (Unix timestamp)

{"data": "your response here"}


RATE LIMITED REQUEST (429):
───────────────────────────
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705312260
Retry-After: 30                 ← Try again after 30 seconds

{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again in 30 seconds."
}


WHY THESE HEADERS?
──────────────────
• User's app can show "45 requests remaining"
• User's app knows when to retry
• Better user experience
• Helps developers debug
```

### Different Limits for Different APIs

```
NOT ALL APIS ARE EQUAL:
───────────────────────

┌─────────────────────────────────────────────────────────────────┐
│                      RATE LIMIT RULES                            │
├───────────────────┬───────────────┬─────────────────────────────┤
│     Endpoint      │    Limit      │         Why?                │
├───────────────────┼───────────────┼─────────────────────────────┤
│  POST /login      │  5/minute     │ Prevent brute force attacks │
├───────────────────┼───────────────┼─────────────────────────────┤
│  POST /signup     │  3/hour       │ Prevent spam accounts       │
├───────────────────┼───────────────┼─────────────────────────────┤
│  GET /api/*       │  100/minute   │ Normal usage                │
├───────────────────┼───────────────┼─────────────────────────────┤
│  POST /upload     │  10/hour      │ Expensive operation         │
├───────────────────┼───────────────┼─────────────────────────────┤
│  POST /payment    │  20/minute    │ Fraud prevention            │
└───────────────────┴───────────────┴─────────────────────────────┘


IMPLEMENTATION:
───────────────

# Redis key includes endpoint
rate_limit:{user_id}:{endpoint}

Examples:
rate_limit:user123:POST:/login    → 5/minute
rate_limit:user123:GET:/api       → 100/minute
rate_limit:user123:POST:/upload   → 10/hour
```

### Summary - Rate Limiter

```
┌─────────────────────────────────────────────────────────────────┐
│                    RATE LIMITER SUMMARY                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WHAT IT DOES:                                                  │
│  Limits how many requests a user can make in a time window      │
│                                                                  │
│  ALGORITHMS:                                                    │
│  • Token Bucket (recommended) - Allows burst, smooth limiting   │
│  • Sliding Window - Precise counting, more memory               │
│  • Fixed Window - Simple but has edge case issues               │
│                                                                  │
│  KEY COMPONENTS:                                                │
│  • Rate Limiter Middleware - Checks every request               │
│  • Redis - Shared counter storage                               │
│  • Configuration - Rules for different endpoints                │
│                                                                  │
│  KEY DECISIONS:                                                 │
│  • Use Redis for distributed counting                           │
│  • Token Bucket for most cases                                  │
│  • Different limits per endpoint                                │
│  • Return helpful headers (remaining, reset time)               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Practice Tips

### How to Practice

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRACTICE TIPS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. TIME YOURSELF                                               │
│     • 45 minutes per problem                                    │
│     • 5 min requirements, 5 min API, 5 min DB,                  │
│       15 min architecture, 10 min discussion                    │
│                                                                  │
│  2. DRAW DIAGRAMS                                               │
│     • Use paper/whiteboard even when practicing alone           │
│     • Boxes for components, arrows for data flow                │
│     • Label everything                                          │
│                                                                  │
│  3. TALK OUT LOUD                                               │
│     • Explain your thinking as you design                       │
│     • "I'm choosing Redis here because..."                      │
│     • Practice articulating trade-offs                          │
│                                                                  │
│  4. START WITH REQUIREMENTS                                     │
│     • NEVER jump to solution                                    │
│     • Ask at least 5 clarifying questions                       │
│                                                                  │
│  5. KNOW THE NUMBERS                                            │
│     • 1M requests/day ≈ 12/second                              │
│     • 1 day ≈ 100,000 seconds                                  │
│     • Practice quick calculations                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Common Questions to Practice

```
FOR 2.5-3 YOE, PRACTICE THESE:
──────────────────────────────

TIER 1 (Most likely):
1. URL Shortener ✓ (covered above)
2. Rate Limiter ✓ (covered above)
3. Twitter Feed ✓ (covered above)
4. Chat/Messaging ✓ (covered above)

TIER 2 (Sometimes asked):
5. Notification System
6. Pastebin (text sharing)
7. File Storage (like Dropbox)
8. News Feed
9. Parking Lot System
10. Booking System (movie tickets)
```

### Interview Day Checklist

```
BEFORE THE INTERVIEW:
─────────────────────
[ ] Review the 5-step framework
[ ] Practice drawing on whiteboard/paper
[ ] Know basic numbers (requests/sec, storage)
[ ] Review trade-offs for common decisions
[ ] Get good sleep!

DURING THE INTERVIEW:
─────────────────────
[ ] Ask clarifying questions (don't assume!)
[ ] Draw as you explain
[ ] Explain your reasoning ("I chose X because...")
[ ] Discuss trade-offs
[ ] It's okay to say "I don't know, but I would..."

REMEMBER:
─────────
• There's no perfect answer
• Process matters more than result
• Communication is key
• Ask if you're on the right track
```

---

*Good luck with your interviews! Remember: At 2.5-3 YOE, they want to see you can think through problems systematically, not that you know everything.*
