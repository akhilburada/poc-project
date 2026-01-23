# System Design Interview Examples for 3 YOE (SDE-2 / Mid-Level)

> Real interview questions with detailed walkthroughs, diagrams, and explanations

---

## What's Different at 3 YOE?

| 2 YOE (Junior) | 3 YOE (Mid-Level) |
|----------------|-------------------|
| Basic components | Deeper understanding |
| Simple scale | Handle millions of users |
| Know what to use | Know WHY to use |
| Basic trade-offs | Detailed trade-off analysis |
| Single region | Multi-region awareness |
| Basic caching | Cache invalidation strategies |
| Simple DB | Sharding, replication |

### What Interviewers Expect at 3 YOE:

1. **Lead the discussion** - Don't wait for hints
2. **Consider edge cases** - What if X fails?
3. **Discuss alternatives** - "We could also do Y, but..."
4. **Quantify decisions** - Back-of-envelope calculations
5. **Think about operations** - Monitoring, deployment, debugging

---

## Example 1: Design Twitter/X Feed

### The Question

> "Design the home feed for Twitter where users see tweets from people they follow. Focus on how the feed is generated and displayed."

---

### Step 1: Clarify Requirements (5 minutes)

**You should ask:**

```
ME: "Before I start, let me understand the requirements."

1. "How many users? Daily active users?"
   INTERVIEWER: "300 million monthly active users, 150 million daily"

2. "How many tweets per day?"
   INTERVIEWER: "500 million tweets per day"

3. "Average followers per user?"
   INTERVIEWER: "Average 200, but celebrities have millions"

4. "How fresh should the feed be?"
   INTERVIEWER: "Near real-time, few seconds delay is okay"

5. "Should we handle media (images/videos)?"
   INTERVIEWER: "Focus on text tweets, mention media handling briefly"
```

**Write down:**
```
Requirements:
- 150M DAU
- 500M tweets/day
- Avg 200 followers, max millions (celebrities)
- Near real-time feed
- Read-heavy system (users read more than write)
```

---

### Step 2: API Design (3 minutes)

```
POST /api/v1/tweets
Request:
{
  "content": "Hello World!",
  "media_ids": ["id1", "id2"]  // optional
}
Response:
{
  "tweet_id": "123456",
  "created_at": "2024-01-15T10:30:00Z"
}

GET /api/v1/feed?page_token=xxx&limit=20
Response:
{
  "tweets": [
    {
      "tweet_id": "123",
      "user_id": "456",
      "user_name": "john",
      "content": "Hello!",
      "created_at": "...",
      "likes": 100,
      "retweets": 20
    }
  ],
  "next_page_token": "yyy"
}

POST /api/v1/users/{id}/follow
DELETE /api/v1/users/{id}/follow
```

---

### Step 3: High-Level Design (10 minutes)

**The Core Problem:**

When User A opens their feed, how do we quickly show tweets from all people they follow?

**Two Approaches:**

#### Approach 1: Pull Model (Fan-out on Read)

```
When User A opens feed:
1. Get list of people A follows (say 200 people)
2. Fetch recent tweets from each of those 200 people
3. Merge and sort by time
4. Return top 20

┌─────────────┐
│   User A    │
│ Opens Feed  │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│                  FEED SERVICE                     │
│                                                   │
│  1. Get followings: [User1, User2, ... User200]  │
│  2. Query tweets from each user                   │
│  3. Merge & Sort                                  │
│  4. Return top 20                                 │
└──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│  Database   │
│  (Tweets)   │
└─────────────┘
```

**Pros:**
- Simple to implement
- No extra storage
- Tweets appear instantly

**Cons:**
- SLOW for users following many people
- High read load on database
- Latency issues at scale

---

#### Approach 2: Push Model (Fan-out on Write)

```
When User B posts a tweet:
1. Get list of B's followers (say 1000 people)
2. Push tweet to each follower's pre-computed feed cache
3. When User A opens feed, just read from cache

┌─────────────┐
│   User B    │
│ Posts Tweet │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│                  TWEET SERVICE                    │
│  1. Save tweet to DB                              │
│  2. Get B's followers: [A, C, D, ... 1000 users] │
│  3. Push to message queue                         │
└──────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│              FAN-OUT SERVICE                      │
│  For each follower:                               │
│    - Add tweet_id to their feed cache             │
└──────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ User A Feed │     │ User C Feed │     │ User D Feed │
│   Cache     │     │   Cache     │     │   Cache     │
└─────────────┘     └─────────────┘     └─────────────┘

Later, when User A opens feed:
Just read from User A's feed cache - FAST!
```

**Pros:**
- Very fast reads (pre-computed)
- Low latency for users

**Cons:**
- Celebrity problem (millions of followers = slow writes)
- Wasted computation for inactive users
- Higher storage cost

---

#### Approach 3: Hybrid Model (Best for Twitter) ⭐

```
Regular users (< 10K followers): Push model
Celebrities (> 10K followers): Pull model at read time

┌────────────────────────────────────────────────────────────────┐
│                    HYBRID FEED GENERATION                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  When regular user posts tweet:                                 │
│    → Fan-out to all followers' caches (Push)                   │
│                                                                 │
│  When celebrity posts tweet:                                    │
│    → Just save to DB (no fan-out)                              │
│                                                                 │
│  When User A opens feed:                                        │
│    1. Get pre-computed feed from cache (regular followings)    │
│    2. Fetch latest from celebrities A follows (Pull)           │
│    3. Merge both lists                                          │
│    4. Return sorted feed                                        │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### Step 4: Detailed Architecture (10 minutes)

```
                                    ┌─────────────────┐
                                    │      CDN        │
                                    │ (Static Assets) │
                                    └────────┬────────┘
                                             │
┌──────────┐                        ┌────────▼────────┐
│  Mobile  │◄──────────────────────►│  Load Balancer  │
│   App    │                        └────────┬────────┘
└──────────┘                                 │
                          ┌──────────────────┼──────────────────┐
                          │                  │                  │
                   ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐
                   │ API Gateway │    │ API Gateway │    │ API Gateway │
                   └──────┬──────┘    └─────────────┘    └─────────────┘
                          │
        ┌─────────────────┼─────────────────┬─────────────────┐
        │                 │                 │                 │
 ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
 │   Tweet     │   │    Feed     │   │    User     │   │  Follow     │
 │   Service   │   │   Service   │   │   Service   │   │  Service    │
 └──────┬──────┘   └──────┬──────┘   └─────────────┘   └─────────────┘
        │                 │
        │          ┌──────▼──────┐
        │          │ Feed Cache  │
        │          │   (Redis)   │
        │          └─────────────┘
        │
 ┌──────▼──────┐
 │   Message   │
 │    Queue    │
 │   (Kafka)   │
 └──────┬──────┘
        │
 ┌──────▼──────┐
 │  Fan-out    │
 │  Workers    │
 └──────┬──────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Tweets    │  │   Users     │  │  Follows    │          │
│  │    (DB)     │  │    (DB)     │  │   Graph     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

### Step 5: Database Design (5 minutes)

```sql
-- Users Table (MySQL)
CREATE TABLE users (
    user_id      BIGINT PRIMARY KEY,
    username     VARCHAR(50) UNIQUE,
    email        VARCHAR(255),
    is_celebrity BOOLEAN DEFAULT FALSE,  -- > 10K followers
    created_at   TIMESTAMP
);

-- Tweets Table (MySQL + Sharding by user_id)
CREATE TABLE tweets (
    tweet_id    BIGINT PRIMARY KEY,
    user_id     BIGINT NOT NULL,
    content     VARCHAR(280),
    media_urls  JSON,
    created_at  TIMESTAMP,
    INDEX idx_user_time (user_id, created_at DESC)
);

-- Follows Table (Graph DB or MySQL)
CREATE TABLE follows (
    follower_id  BIGINT,
    followee_id  BIGINT,
    created_at   TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id),
    INDEX idx_followee (followee_id)  -- Who follows this user?
);
```

**Feed Cache Structure (Redis):**

```
Key: feed:{user_id}
Value: Sorted Set of tweet_ids, scored by timestamp

ZADD feed:user123 1705312200 tweet456
ZADD feed:user123 1705312300 tweet457

# Get latest 20 tweets
ZREVRANGE feed:user123 0 19
```

---

### Step 6: Calculations (3 minutes)

```
Tweets per second:
- 500M tweets/day
- 500M / 86400 ≈ 6000 tweets/second

Feed reads per second:
- 150M DAU, assume each opens feed 10 times/day
- 150M × 10 / 86400 ≈ 17,000 reads/second

Fan-out calculation:
- Average 200 followers
- 6000 tweets/sec × 200 = 1.2M cache writes/second
- Need distributed cache cluster

Feed storage:
- Store 1000 tweet_ids per user (last few days)
- 150M users × 1000 × 8 bytes = 1.2 TB
- Fits in Redis cluster
```

---

### Step 7: Key Discussion Points

**Q: How to handle celebrity tweets?**
```
Don't fan-out for celebrities (> 10K followers)
Pull their tweets at read time and merge with cached feed
Celebrities' recent tweets can be cached separately
```

**Q: How to handle new followers?**
```
When A follows B:
1. If B is not celebrity: Backfill A's cache with B's recent tweets
2. If B is celebrity: No action, will be pulled at read time
```

**Q: How to rank/sort the feed?**
```
Simple: Chronological (by timestamp)
Advanced: ML-based ranking considering:
- Engagement (likes, retweets)
- User's past interactions
- Recency
- Content type
```

---

## Example 2: Design WhatsApp / Messaging System

### The Question

> "Design a messaging system like WhatsApp that supports 1-on-1 chats, group chats, and shows online status and read receipts."

---

### Step 1: Clarify Requirements (5 minutes)

```
ME: "Let me understand the scope."

1. "How many users?"
   INTERVIEWER: "500 million daily active users"

2. "Messages per day?"
   INTERVIEWER: "50 billion messages per day"

3. "Group size limit?"
   INTERVIEWER: "Max 256 members per group"

4. "Media support?"
   INTERVIEWER: "Yes, images, videos, documents"

5. "Message retention?"
   INTERVIEWER: "Store forever, but only recent on device"

6. "End-to-end encryption?"
   INTERVIEWER: "Mention it, but focus on architecture"
```

**Write down:**
```
Requirements:
- 500M DAU
- 50B messages/day ≈ 580K messages/second
- 1-on-1 and group chat (max 256)
- Media support
- Online status
- Read receipts (sent, delivered, read)
- Message history
```

---

### Step 2: API Design (3 minutes)

```
WebSocket Connection:
ws://chat.app/ws?token=xxx

Message Format (WebSocket):

# Send message
{
  "type": "message",
  "message_id": "uuid",
  "chat_id": "chat123",
  "content": "Hello!",
  "media_url": null
}

# Receive message
{
  "type": "message",
  "message_id": "uuid",
  "chat_id": "chat123",
  "sender_id": "user456",
  "content": "Hi there!",
  "timestamp": "2024-01-15T10:30:00Z"
}

# Delivery receipt
{
  "type": "receipt",
  "message_id": "uuid",
  "status": "delivered"  // or "read"
}

# Typing indicator
{
  "type": "typing",
  "chat_id": "chat123",
  "user_id": "user456"
}

# Online status
{
  "type": "presence",
  "user_id": "user456",
  "status": "online"  // or "offline", "last_seen: timestamp"
}

REST APIs:
GET  /api/v1/chats                    - List all chats
GET  /api/v1/chats/{id}/messages      - Get message history
POST /api/v1/chats/{id}/media         - Upload media
POST /api/v1/groups                   - Create group
```

---

### Step 3: High-Level Architecture (10 minutes)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT APPS                                    │
│    ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     │
│    │ Mobile A │     │ Mobile B │     │ Mobile C │     │   Web    │     │
│    └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     │
└─────────┼────────────────┼────────────────┼────────────────┼────────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                   │
                          WebSocket Connection
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         GATEWAY LAYER                                    │
│                                                                          │
│    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐       │
│    │  WebSocket     │    │  WebSocket     │    │  WebSocket     │       │
│    │  Server 1      │    │  Server 2      │    │  Server 3      │       │
│    │  (10K conn)    │    │  (10K conn)    │    │  (10K conn)    │       │
│    └───────┬────────┘    └───────┬────────┘    └───────┬────────┘       │
│            │                     │                     │                 │
│            └─────────────────────┴─────────────────────┘                 │
│                                  │                                       │
└──────────────────────────────────┼───────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        SERVICE LAYER                                     │
│                                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Message   │  │   Group     │  │  Presence   │  │   Media     │    │
│  │   Service   │  │   Service   │  │   Service   │  │   Service   │    │
│  └──────┬──────┘  └─────────────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                                  │                │           │
└─────────┼──────────────────────────────────┼────────────────┼───────────┘
          │                                  │                │
          ▼                                  ▼                ▼
┌─────────────────────┐            ┌─────────────┐    ┌─────────────┐
│    Message Queue    │            │   Redis     │    │     S3      │
│      (Kafka)        │            │  (Status)   │    │   (Media)   │
└─────────┬───────────┘            └─────────────┘    └─────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                       │
│                                                                          │
│    ┌─────────────────┐         ┌─────────────────┐                      │
│    │    Messages     │         │   Users/Groups  │                      │
│    │   (Cassandra)   │         │    (MySQL)      │                      │
│    └─────────────────┘         └─────────────────┘                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Step 4: Message Flow - Detailed (10 minutes)

#### Flow 1: User A sends message to User B (1-on-1)

```
┌────────────────────────────────────────────────────────────────────────┐
│                    1-ON-1 MESSAGE FLOW                                  │
└────────────────────────────────────────────────────────────────────────┘

Step 1: User A sends message
┌─────────┐         ┌──────────────┐
│ User A  │────────►│ WebSocket    │
│         │         │ Server 1     │
└─────────┘         └──────┬───────┘
                           │
Step 2: Server processes   │
                           ▼
                    ┌──────────────┐
                    │   Message    │
                    │   Service    │
                    └──────┬───────┘
                           │
Step 3: Save to DB         │
                           ▼
                    ┌──────────────┐
                    │  Cassandra   │
                    │  (Messages)  │
                    └──────────────┘
                           │
Step 4: Check if B online  │
                           ▼
                    ┌──────────────┐
                    │    Redis     │  ──► B is online on Server 2
                    │  (Sessions)  │
                    └──────────────┘
                           │
Step 5: Route to B         │
                           ▼
                    ┌──────────────┐
                    │  Message     │
                    │   Queue      │
                    └──────┬───────┘
                           │
Step 6: Deliver            │
                           ▼
                    ┌──────────────┐         ┌─────────┐
                    │ WebSocket    │────────►│ User B  │
                    │ Server 2     │         │         │
                    └──────────────┘         └─────────┘

Step 7: B's device sends "delivered" receipt back
Step 8: When B reads, sends "read" receipt
Step 9: Update message status, notify A
```

#### Flow 2: Group Message (A sends to group of 100)

```
┌────────────────────────────────────────────────────────────────────────┐
│                    GROUP MESSAGE FLOW                                   │
└────────────────────────────────────────────────────────────────────────┘

┌─────────┐
│ User A  │──────► Sends message to Group (100 members)
└─────────┘
      │
      ▼
┌──────────────┐
│   Message    │
│   Service    │
└──────┬───────┘
       │
       ├──────► Save to DB (once, with group_id)
       │
       ▼
┌──────────────┐
│    Group     │──────► Get 100 member IDs
│   Service    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Message    │──────► 99 messages (excluding sender)
│    Queue     │
└──────┬───────┘
       │
       ├─────────────────────────────────┐
       │                                 │
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│   Online     │                  │   Offline    │
│   Members    │                  │   Members    │
│  (Deliver    │                  │  (Store for  │
│   via WS)    │                  │   later)     │
└──────────────┘                  └──────────────┘
```

---

### Step 5: Database Design (5 minutes)

```sql
-- Users Table (MySQL)
CREATE TABLE users (
    user_id     BIGINT PRIMARY KEY,
    phone       VARCHAR(20) UNIQUE,
    name        VARCHAR(100),
    avatar_url  VARCHAR(500),
    created_at  TIMESTAMP
);

-- Groups Table (MySQL)
CREATE TABLE groups (
    group_id    BIGINT PRIMARY KEY,
    name        VARCHAR(100),
    avatar_url  VARCHAR(500),
    created_by  BIGINT,
    created_at  TIMESTAMP
);

-- Group Members (MySQL)
CREATE TABLE group_members (
    group_id    BIGINT,
    user_id     BIGINT,
    role        ENUM('admin', 'member'),
    joined_at   TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);
```

**Messages Table (Cassandra - for scale):**

```sql
-- Partitioned by chat_id for fast retrieval
CREATE TABLE messages (
    chat_id     TEXT,           -- "user1_user2" or "group_123"
    message_id  TIMEUUID,       -- Time-based UUID
    sender_id   BIGINT,
    content     TEXT,
    media_url   TEXT,
    status      TEXT,           -- sent, delivered, read
    created_at  TIMESTAMP,
    PRIMARY KEY (chat_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

**Session Storage (Redis):**

```
# Which server is user connected to?
SET user_session:user123 "ws-server-2" EX 300

# Online status
SET online:user123 "1" EX 30  # Refresh with heartbeat

# Last seen
SET last_seen:user123 "1705312200"
```

---

### Step 6: Key Components Explained

#### Online Status (Presence)

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENCE SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  User connects:                                              │
│    SET online:user123 "1" EX 30                             │
│    PUBLISH presence_channel "user123:online"                │
│                                                              │
│  Heartbeat every 20 seconds:                                │
│    EXPIRE online:user123 30                                  │
│                                                              │
│  User disconnects (or timeout):                             │
│    Key expires automatically                                 │
│    SET last_seen:user123 {timestamp}                        │
│    PUBLISH presence_channel "user123:offline"               │
│                                                              │
│  Check if user online:                                       │
│    EXISTS online:user123                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Message Status (Receipts)

```
Message Lifecycle:

┌────────┐     ┌───────────┐     ┌───────────┐     ┌────────┐
│  SENT  │────►│ DELIVERED │────►│   READ    │     │        │
│   ✓    │     │    ✓✓     │     │   ✓✓      │     │        │
│ (gray) │     │  (gray)   │     │  (blue)   │     │        │
└────────┘     └───────────┘     └───────────┘     └────────┘
    │               │                  │
    │               │                  │
    ▼               ▼                  ▼
 Saved to      Received by        User opened
   DB          recipient's        the chat
               device
```

---

### Step 7: Handling Offline Users

```
┌─────────────────────────────────────────────────────────────┐
│                 OFFLINE MESSAGE HANDLING                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  When sending to offline user:                               │
│                                                              │
│  1. Save message to DB (status: "sent")                     │
│                                                              │
│  2. Add to offline queue:                                    │
│     LPUSH offline:user456 message_id                        │
│                                                              │
│  3. Send push notification (optional)                        │
│                                                              │
│  When user comes online:                                     │
│                                                              │
│  1. Check offline queue:                                     │
│     LRANGE offline:user456 0 -1                             │
│                                                              │
│  2. Fetch messages from DB                                   │
│                                                              │
│  3. Deliver via WebSocket                                    │
│                                                              │
│  4. Clear queue:                                             │
│     DEL offline:user456                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Example 3: Design Rate Limiter

### The Question

> "Design a rate limiting system that can limit API requests. It should work across multiple servers and support different limits for different APIs."

---

### Step 1: Clarify Requirements (3 minutes)

```
ME: "Let me understand what we're building."

1. "What kind of limits? Per user? Per IP? Per API?"
   INTERVIEWER: "Per user per API endpoint"

2. "What's the limit?"
   INTERVIEWER: "100 requests per minute for most APIs"

3. "Distributed system?"
   INTERVIEWER: "Yes, multiple API servers"

4. "What happens when limit exceeded?"
   INTERVIEWER: "Return 429 Too Many Requests"

5. "Hard limit or soft limit?"
   INTERVIEWER: "Hard limit, must not exceed"
```

---

### Step 2: Algorithms Explained (10 minutes)

#### Algorithm 1: Token Bucket ⭐ (Most Popular)

```
┌─────────────────────────────────────────────────────────────┐
│                     TOKEN BUCKET                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Imagine a bucket that holds tokens:                         │
│                                                              │
│  ┌─────────────────┐                                        │
│  │  ○ ○ ○ ○ ○ ○ ○  │  ← Bucket (capacity: 10 tokens)       │
│  │  ○ ○ ○          │                                        │
│  └─────────────────┘                                        │
│          ↑                                                   │
│    Tokens added at                                           │
│    fixed rate (10/min)                                       │
│                                                              │
│  Rules:                                                      │
│  - Each request takes 1 token                                │
│  - If no tokens, request rejected                            │
│  - Tokens refill at constant rate                            │
│  - Bucket has max capacity (can't overflow)                  │
│                                                              │
│  Example: 10 tokens/minute, bucket size 10                   │
│                                                              │
│  Time 0:00 - Bucket full (10 tokens)                        │
│  Time 0:01 - 5 requests come → 5 tokens left                │
│  Time 0:02 - 6 requests come → 1 rejected (only 5 tokens)   │
│  Time 0:30 - 5 tokens refilled → 10 tokens                  │
│                                                              │
│  ALLOWS: Burst traffic up to bucket size                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
def is_allowed_token_bucket(user_id, capacity=10, refill_rate=10):
    """
    capacity: max tokens (bucket size)
    refill_rate: tokens added per minute
    """
    key = f"ratelimit:{user_id}"
    now = time.time()
    
    # Get current state
    data = redis.hgetall(key)
    
    if not data:
        # First request - full bucket
        redis.hset(key, {
            'tokens': capacity - 1,
            'last_refill': now
        })
        redis.expire(key, 60)
        return True
    
    # Calculate tokens to add based on time passed
    tokens = float(data['tokens'])
    last_refill = float(data['last_refill'])
    time_passed = now - last_refill
    
    # Add tokens (but not more than capacity)
    tokens_to_add = time_passed * (refill_rate / 60)
    tokens = min(capacity, tokens + tokens_to_add)
    
    if tokens >= 1:
        # Allow request, consume token
        redis.hset(key, {
            'tokens': tokens - 1,
            'last_refill': now
        })
        return True
    else:
        # Reject request
        return False
```

---

#### Algorithm 2: Sliding Window Log

```
┌─────────────────────────────────────────────────────────────┐
│                   SLIDING WINDOW LOG                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Store timestamp of each request:                            │
│                                                              │
│  User: user123                                               │
│  Limit: 5 requests per minute                                │
│                                                              │
│  Timeline:                                                   │
│  ─────────────────────────────────────────────────────────  │
│  10:00:10  10:00:20  10:00:35  10:00:45  10:00:55           │
│     ✓         ✓         ✓         ✓         ✓              │
│                                                              │
│  At 10:01:05, new request comes:                            │
│  - Window: 10:00:05 to 10:01:05                             │
│  - Remove old: 10:00:10 is outside (barely)                 │
│  - Wait, 10:00:10 is INSIDE the window                      │
│  - Count: 5 requests in window                               │
│  - REJECT (limit is 5)                                       │
│                                                              │
│  At 10:01:15, new request comes:                            │
│  - Window: 10:00:15 to 10:01:15                             │
│  - 10:00:10 is outside, remove it                           │
│  - Count: 4 requests in window                               │
│  - ALLOW ✓                                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
def is_allowed_sliding_window(user_id, limit=100, window_seconds=60):
    key = f"ratelimit:{user_id}"
    now = time.time()
    window_start = now - window_seconds
    
    # Use Redis sorted set
    pipe = redis.pipeline()
    
    # Remove old entries outside window
    pipe.zremrangebyscore(key, 0, window_start)
    
    # Count entries in current window
    pipe.zcard(key)
    
    # Add current request (optimistically)
    pipe.zadd(key, {str(now): now})
    
    # Set expiry
    pipe.expire(key, window_seconds)
    
    results = pipe.execute()
    request_count = results[1]
    
    if request_count < limit:
        return True
    else:
        # Remove the optimistically added request
        redis.zrem(key, str(now))
        return False
```

---

#### Algorithm 3: Fixed Window Counter (Simplest)

```
┌─────────────────────────────────────────────────────────────┐
│                  FIXED WINDOW COUNTER                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Divide time into fixed windows:                             │
│                                                              │
│  Window 1         Window 2         Window 3                  │
│  10:00-10:01     10:01-10:02     10:02-10:03                │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐                │
│  │ Count:5 │     │ Count:3 │     │ Count:0 │                │
│  └─────────┘     └─────────┘     └─────────┘                │
│                                                              │
│  Limit: 5 per minute                                         │
│                                                              │
│  Pros: Simple, memory efficient                              │
│  Cons: Burst at window edges                                 │
│                                                              │
│  Edge problem:                                               │
│  - 5 requests at 10:00:59                                   │
│  - 5 requests at 10:01:01                                   │
│  - 10 requests in 2 seconds! (both allowed)                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
def is_allowed_fixed_window(user_id, limit=100, window_seconds=60):
    # Key includes window timestamp
    window = int(time.time() / window_seconds)
    key = f"ratelimit:{user_id}:{window}"
    
    current = redis.incr(key)
    
    if current == 1:
        redis.expire(key, window_seconds)
    
    return current <= limit
```

---

### Step 3: Distributed Architecture (5 minutes)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DISTRIBUTED RATE LIMITER                              │
└─────────────────────────────────────────────────────────────────────────┘

           Request
              │
              ▼
     ┌────────────────┐
     │ Load Balancer  │
     └────────┬───────┘
              │
    ┌─────────┼─────────┐
    │         │         │
    ▼         ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐
│ API   │ │ API   │ │ API   │
│Server1│ │Server2│ │Server3│
└───┬───┘ └───┬───┘ └───┬───┘
    │         │         │
    └─────────┼─────────┘
              │
              ▼
     ┌────────────────┐
     │  Redis Cluster │    ← Single source of truth
     │  (Centralized) │
     └────────────────┘


Each API Server:
1. Receives request
2. Checks Redis for rate limit
3. If allowed: process request
4. If exceeded: return 429
```

---

### Step 4: Response Headers

```
HTTP Response when ALLOWED:
────────────────────────────
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705312260

HTTP Response when EXCEEDED:
────────────────────────────
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705312260
Retry-After: 30

{
  "error": "Rate limit exceeded",
  "retry_after": 30
}
```

---

### Step 5: Different Limits for Different APIs

```
┌─────────────────────────────────────────────────────────────┐
│                MULTI-TIER RATE LIMITING                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Rate Limit Rules (stored in config/DB):                     │
│                                                              │
│  ┌──────────────────┬─────────┬────────────┐                │
│  │    Endpoint      │  Limit  │   Window   │                │
│  ├──────────────────┼─────────┼────────────┤                │
│  │ POST /login      │   5     │  1 minute  │  (prevent      │
│  │ POST /signup     │   3     │  1 hour    │   brute force) │
│  │ GET /api/*       │  100    │  1 minute  │                │
│  │ POST /api/*      │   50    │  1 minute  │                │
│  │ POST /upload     │   10    │  1 hour    │  (expensive)   │
│  └──────────────────┴─────────┴────────────┘                │
│                                                              │
│  Redis Key Pattern:                                          │
│  ratelimit:{user_id}:{endpoint}:{window}                    │
│                                                              │
│  Example:                                                    │
│  ratelimit:user123:POST:/login:12345                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary: What to Remember

### For Each Design Question:

```
1. CLARIFY (5 min)
   - Users, scale, features
   - Read vs write heavy
   - Consistency requirements

2. API DESIGN (5 min)
   - REST endpoints
   - Request/Response format

3. DATA MODEL (5 min)
   - Tables, relationships
   - SQL vs NoSQL decision
   - Indexes

4. HIGH-LEVEL DESIGN (15 min)
   - Draw components
   - Show data flow
   - Explain interactions

5. DEEP DIVE (10 min)
   - Trade-offs
   - Scaling approach
   - Failure handling
```

### Key Differences for 3 YOE vs 2 YOE:

| Aspect | 2 YOE | 3 YOE |
|--------|-------|-------|
| Calculations | Basic | Detailed with numbers |
| Trade-offs | Mention | Explain in depth |
| Alternatives | Know one approach | Discuss multiple options |
| Failure handling | Brief | Detailed scenarios |
| Scale | Thousands | Millions |
| Communication | Guided | Lead the discussion |

---

## Practice Tips

1. **Time yourself** - 45 minutes per problem
2. **Draw diagrams** - Even when practicing alone
3. **Talk out loud** - Practice explaining your thoughts
4. **Start with requirements** - Never jump to solution
5. **Know the numbers** - Practice calculations
6. **Prepare questions** - Have clarifying questions ready
7. **Review and iterate** - Improve your designs after practice

Good luck with your interviews!
