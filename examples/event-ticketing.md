# Flow: Event RSVP & Ticketing

## Flow Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Event     │     │   Ticket     │     │  Attendee    │
│   Landing    ├────▶│  Selection   ├────▶│  Info        │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │        
                                                 ▼        
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │
│ Notification │◀────┤  E-Ticket    │◀────┤  Payment     │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

Screens to wireframe:

1. Event Landing — User views event details and decides to get tickets
2. Ticket Selection — User picks ticket tier and quantity
3. Attendee Info — User enters name and email per ticket
4. Payment — User enters card details and reviews order
5. E-Ticket — User receives digital ticket with QR code
6. Notification — User gets event reminder with countdown

## Screens

### Step 1: Event Landing

```
┌────────────────────────────────────────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │
├────────────────────────────────────────────────────┤
│                                                    │
│  ██████████████████████████████████                │
│                                                    │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                              │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                          │
│                                                    │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     │
│                                                    │
│              [ Get Tickets ]                       │
│                                                    │
└────────────────────────────────────────────────────┘
```

User sees a hero image, event title, date/time, venue details, and a description. The primary action is Get Tickets.

---

### Step 2: Ticket Selection

```
┌────────────────────────────────────────────────────┐
│  Select Tickets                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  ██████████████████████████                        │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                              │
│                                                    │
├──────────────────────┬───────────┬─────────────────┤
│  TIER                │  PRICE    │  QTY            │
├──────────────────────┼───────────┼─────────────────┤
│  General Admission   │           │                 │
│  ░░░░░░░░░░░░░░░░░░  │  ▒▒▒▒▒▒   │  [1 v]          │
├──────────────────────┼───────────┼─────────────────┤
│  VIP                 │           │                 │
│  ░░░░░░░░░░░░░░░░░░  │  ▒▒▒▒▒▒   │  [0 v]          │
├──────────────────────┼───────────┼─────────────────┤
│  Early Bird          │           │                 │
│  ░░░░░░░░░░░░░░░░░░  │  ▒▒▒▒▒▒   │  [0 v]          │
├──────────────────────┴───────────┴─────────────────┤
│                                                    │
│  Promo Code                                        │
│  [_________________________]  (Apply)              │
│                                                    │
│                     Subtotal:          ▒▒▒▒▒▒▒     │
│                                                    │
│                          [ Continue ]              │
└────────────────────────────────────────────────────┘
```

User selects from ticket tiers (GA, VIP, Early Bird) in a pricing table, adjusts quantities, optionally enters a promo code, and sees the subtotal.

---

### Step 3: Attendee Info

```
┌────────────────────────────────────────────────────┐
│  Attendee Information              Step 2 of 3     │
├────────────────────────────────────────────────────┤
│                                                    │
│  TICKET 1 — General Admission                      │
│                                                    │
│  Full Name                                         │
│  [____________________________________________]    │
│                                                    │
│  Email                                             │
│  [____________________________________________]    │
│                                                    │
│  ──────────────────────────────────────────────    │
│                                                    │
│  TICKET 2 — General Admission                      │
│                                                    │
│  Full Name                                         │
│  [____________________________________________]    │
│                                                    │
│  Email                                             │
│  [____________________________________________]    │
│                                                    │
│               < Back         [ Continue ]          │
└────────────────────────────────────────────────────┘
```

User enters full name and email address for each ticket purchased. Each ticket section is clearly labeled with its tier.

---

### Step 4: Payment

```
┌────────────────────────────────────────────────────┐
│  Payment                           Step 3 of 3     │
├───────────────────────────┬────────────────────────┤
│                           │  ORDER SUMMARY         │
│  CARD DETAILS             │                        │
│                           │  ░░░░░░░░░░░░░░░░░░    │
│  Cardholder Name          │  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒    │
│  [_______________________]│                        │
│                           │  ▒▒ x General    ▒▒▒▒  │
│  Card Number              │                        │
│  [_______________________]│  Subtotal      ▒▒▒▒▒   │
│                           │  Fees          ▒▒▒▒▒   │
│  Exp Date       CVC       │  ────────────────────  │
│  [___________]  [_____]   │  Total         ▒▒▒▒▒   │
│                           │                        │
│                           │                        │
│      < Back               │                        │
│      [ Pay Now ]          │                        │
└───────────────────────────┴────────────────────────┘
```

User enters payment card details alongside the order summary showing ticket breakdown, fees, and total.

---

### Step 5: E-Ticket

```
┌────────────────────────────────────────────────────┐
│                                                    │
│            You're Going!                           │
│                                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  ██████████████████████████████████                │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                              │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                          │
│                                                    │
│           ┌──────────────────┐                     │
│           │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │                      │
│           │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │                      │
│           │ ▓▓▓  QR CODE ▓▓▓ │                     │
│           │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │                      │
│           │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │                      │
│           └──────────────────┘                     │
│                                                    │
│  Ticket:   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                      │
│  Attendee: ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                      │
│                                                    │
│         [ Add to Wallet ]                          │
│                                                    │
└────────────────────────────────────────────────────┘
```

User receives their digital ticket with event name, date/venue, a QR code for entry, ticket type, and an option to add to their phone wallet.

---

### Step 6: Notification

```
┌────────────────────────────────────────────────────┐
│  Event Reminder                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  ██████████████████████████████████                │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                              │
│                                                    │
│  ┌────────────────────────────────────────────┐    │
│  │                                            │    │
│  │       ██████████████████                   │    │
│  │                                            │    │
│  │  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒      │       │
│  │                                            │    │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │       │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │       │
│  │  ▓▓▓▓▓▓▓▓▓▓ VENUE MAP ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │      │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │       │
│  │                                            │    │
│  │    [ View Ticket ]   (Get Directions)      │    │
│  │                                            │    │
│  └────────────────────────────────────────────┘    │
│                                                    │
└────────────────────────────────────────────────────┘
```

User receives an event reminder showing a countdown, venue map preview, and quick actions to view their ticket or get directions.
